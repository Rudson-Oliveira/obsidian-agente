#!/usr/bin/env python3
"""
HUB CENTRAL SERVER v1.1
Servidor Flask com API de gatilhos integrada
Criado por Manus para Rudson Oliveira
"""

import os
import sys
import json
import logging
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('HubServer')

# Adicionar diretório atual ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Importar módulos do Hub
try:
    from hub_central import HubCentral
    from storage_connectors import storage_manager
    from triggers_manager import TriggersManager, get_triggers_manager
    from triggers_api import triggers_bp, init_triggers_api
    logger.info("[IMPORT] Módulos carregados com sucesso")
except ImportError as e:
    logger.error(f"[IMPORT] Erro ao importar módulos: {e}")
    raise

# Criar aplicação Flask
app = Flask(__name__)
CORS(app)

# Instâncias globais
hub = None
triggers = None


def init_hub():
    """Inicializa o Hub Central e componentes"""
    global hub, triggers
    
    # Inicializar Hub Central
    hub = HubCentral()
    
    # Inicializar gerenciador de gatilhos
    config_path = os.path.expanduser("~/.hub_central/triggers_config.json")
    
    # Copiar config padrão se não existir
    default_config = os.path.join(os.path.dirname(__file__), "triggers_config.json")
    if not os.path.exists(config_path) and os.path.exists(default_config):
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        import shutil
        shutil.copy(default_config, config_path)
        logger.info(f"[INIT] Configuração de gatilhos copiada para {config_path}")
    
    triggers = TriggersManager(config_path=config_path, hub=hub)
    
    # Inicializar API de gatilhos
    init_triggers_api(triggers)
    
    # Registrar blueprint de gatilhos
    app.register_blueprint(triggers_bp)
    
    # Iniciar scheduler
    triggers.start_scheduler()
    
    # Conectar storage
    obsidian = storage_manager.get("obsidian")
    if obsidian:
        obsidian.connect()
    
    logger.info("[INIT] Hub Central inicializado com sucesso!")
    logger.info(f"[INIT] Gatilhos registrados: {len(triggers.triggers)}")
    logger.info(f"[INIT] Conectores disponíveis: {list(storage_manager.connectors.keys())}")
    
    return hub, triggers


# ==================== ENDPOINTS PRINCIPAIS ====================

@app.route('/health', methods=['GET'])
def health():
    """Health check do servidor"""
    return jsonify({
        "service": "Hub Central",
        "status": "online",
        "timestamp": datetime.now().isoformat(),
        "version": "1.1"
    })


@app.route('/status', methods=['GET'])
def status():
    """Status detalhado do sistema"""
    global hub, triggers
    
    return jsonify({
        "hub": {
            "status": "online" if hub else "offline",
            "events_processed": hub.stats.get("events_processed", 0) if hub else 0
        },
        "triggers": {
            "total": len(triggers.triggers) if triggers else 0,
            "active": sum(1 for t in triggers.triggers.values() if t.enabled) if triggers else 0,
            "scheduler_running": triggers.running if triggers else False
        },
        "storage": storage_manager.health_check_all() if storage_manager else {},
        "timestamp": datetime.now().isoformat()
    })


@app.route('/event', methods=['POST'])
def create_event():
    """Cria um novo evento no Hub"""
    global hub
    
    if not hub:
        return jsonify({"error": "Hub não inicializado"}), 500
    
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "Dados não fornecidos"}), 400
    
    event_type = data.get("type", "user_request")
    source = data.get("source", "api")
    event_data = data.get("data", {})
    priority = data.get("priority", "normal")
    
    # Criar evento no hub
    from hub_central import EventType
    event = hub.create_event(
        EventType(event_type) if event_type in [e.value for e in EventType] else EventType.USER_REQUEST,
        source,
        event_data
    )
    
    # Processar evento com gatilhos
    if triggers:
        trigger_results = triggers.process_event(event_type, event_data)
    else:
        trigger_results = []
    
    return jsonify({
        "success": True,
        "event_id": event.id,
        "triggers_executed": len(trigger_results)
    })


@app.route('/ai/ask', methods=['POST'])
def ai_ask():
    """Envia prompt para o motor de decisão de IA"""
    global hub
    
    if not hub:
        return jsonify({"error": "Hub não inicializado"}), 500
    
    data = request.get_json()
    
    if not data or "prompt" not in data:
        return jsonify({"error": "Prompt é obrigatório"}), 400
    
    prompt = data["prompt"]
    provider = data.get("provider", "auto")
    
    # Executar via motor de execução
    result = hub.execution_engine.execute({
        "prompt": prompt,
        "provider": provider
    })
    
    return jsonify({
        "success": True,
        "result": result
    })


# ==================== STORAGE ENDPOINTS ====================

@app.route('/storage/save', methods=['POST'])
def storage_save():
    """Salva dados em um ou mais destinos"""
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "Dados não fornecidos"}), 400
    
    content = data.get("content", {})
    path = data.get("path")
    destinations = data.get("destinations", ["obsidian"])
    
    results = {}
    
    for dest in destinations:
        connector = storage_manager.get(dest)
        if connector:
            results[dest] = connector.save(content, path)
        else:
            results[dest] = {"error": f"Conector '{dest}' não encontrado"}
    
    return jsonify({
        "success": True,
        "results": results
    })


@app.route('/storage/load', methods=['GET'])
def storage_load():
    """Carrega dados de um destino"""
    path = request.args.get("path")
    source = request.args.get("source", "obsidian")
    
    if not path:
        return jsonify({"error": "Path é obrigatório"}), 400
    
    connector = storage_manager.get(source)
    if not connector:
        return jsonify({"error": f"Conector '{source}' não encontrado"}), 404
    
    result = connector.load(path)
    
    return jsonify(result)


@app.route('/storage/health', methods=['GET'])
def storage_health():
    """Verifica saúde dos conectores de storage"""
    return jsonify({
        "success": True,
        "connectors": storage_manager.health_check_all()
    })


# ==================== WEBHOOK GENÉRICO ====================

@app.route('/webhook/<source>', methods=['POST'])
def webhook_handler(source):
    """Handler genérico de webhooks"""
    global triggers
    
    data = request.get_json() or {}
    
    # Adicionar metadados
    data["_source"] = source
    data["_received_at"] = datetime.now().isoformat()
    
    # Processar com gatilhos
    if triggers:
        results = triggers.process_webhook(source, data)
        return jsonify({
            "success": True,
            "source": source,
            "triggers_executed": len(results),
            "results": results
        })
    
    return jsonify({
        "success": True,
        "source": source,
        "message": "Webhook recebido (gatilhos não inicializados)"
    })


# ==================== INICIALIZAÇÃO ====================

if __name__ == "__main__":
    logger.info("=" * 60)
    logger.info("   HUB CENTRAL SERVER v1.1")
    logger.info("=" * 60)
    
    # Inicializar componentes
    hub, triggers = init_hub()
    
    # Iniciar servidor
    port = int(os.environ.get("HUB_PORT", 5002))
    logger.info(f"[SERVER] Iniciando em http://0.0.0.0:{port}")
    
    app.run(
        host="0.0.0.0",
        port=port,
        debug=False,
        threaded=True
    )
