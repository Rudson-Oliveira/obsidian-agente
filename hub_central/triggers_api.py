#!/usr/bin/env python3
"""
API DE GERENCIAMENTO DE GATILHOS
Endpoints REST para CRUD completo de gatilhos
Criado por Manus para Rudson Oliveira
"""

from flask import Blueprint, request, jsonify
from datetime import datetime
import logging

logger = logging.getLogger('TriggersAPI')

# Blueprint para rotas de gatilhos
triggers_bp = Blueprint('triggers', __name__, url_prefix='/triggers')

# Referência ao gerenciador (será injetada)
triggers_manager = None


def init_triggers_api(manager):
    """Inicializa a API com o gerenciador de gatilhos"""
    global triggers_manager
    triggers_manager = manager
    logger.info("[TRIGGERS_API] Inicializada")


# ==================== CRUD ENDPOINTS ====================

@triggers_bp.route('', methods=['GET'])
@triggers_bp.route('/', methods=['GET'])
def list_triggers():
    """Lista todos os gatilhos"""
    if not triggers_manager:
        return jsonify({"error": "Gerenciador não inicializado"}), 500
    
    # Filtros opcionais
    trigger_type = request.args.get('type')
    status = request.args.get('status')
    enabled = request.args.get('enabled')
    
    result = triggers_manager.read()
    
    if result["success"]:
        triggers = result["triggers"]
        
        # Aplicar filtros
        if trigger_type:
            triggers = [t for t in triggers if t["type"] == trigger_type]
        if status:
            triggers = [t for t in triggers if t["status"] == status]
        if enabled is not None:
            enabled_bool = enabled.lower() == 'true'
            triggers = [t for t in triggers if t["enabled"] == enabled_bool]
        
        return jsonify({
            "success": True,
            "triggers": triggers,
            "total": len(triggers),
            "filters_applied": {
                "type": trigger_type,
                "status": status,
                "enabled": enabled
            }
        })
    
    return jsonify(result), 500


@triggers_bp.route('/<trigger_id>', methods=['GET'])
def get_trigger(trigger_id):
    """Obtém um gatilho específico"""
    if not triggers_manager:
        return jsonify({"error": "Gerenciador não inicializado"}), 500
    
    result = triggers_manager.read(trigger_id)
    
    if result["success"]:
        return jsonify(result)
    
    return jsonify(result), 404


@triggers_bp.route('', methods=['POST'])
@triggers_bp.route('/', methods=['POST'])
def create_trigger():
    """
    Cria um novo gatilho
    
    Body JSON:
    {
        "name": "Nome do Gatilho",
        "type": "scheduled|event|webhook|intelligent",
        "config": { ... configuração específica ... },
        "action": { ... ação a executar ... },
        "description": "Descrição opcional",
        "enabled": true
    }
    """
    if not triggers_manager:
        return jsonify({"error": "Gerenciador não inicializado"}), 500
    
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "Dados não fornecidos"}), 400
    
    required = ["name", "type", "config", "action"]
    missing = [f for f in required if f not in data]
    
    if missing:
        return jsonify({"error": f"Campos obrigatórios faltando: {missing}"}), 400
    
    result = triggers_manager.create(
        name=data["name"],
        trigger_type=data["type"],
        config=data["config"],
        action=data["action"],
        description=data.get("description", ""),
        enabled=data.get("enabled", True)
    )
    
    if result["success"]:
        return jsonify(result), 201
    
    return jsonify(result), 400


@triggers_bp.route('/<trigger_id>', methods=['PUT', 'PATCH'])
def update_trigger(trigger_id):
    """
    Atualiza um gatilho existente
    
    Body JSON (campos opcionais):
    {
        "name": "Novo Nome",
        "config": { ... },
        "action": { ... },
        "description": "Nova descrição",
        "enabled": true/false
    }
    """
    if not triggers_manager:
        return jsonify({"error": "Gerenciador não inicializado"}), 500
    
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "Dados não fornecidos"}), 400
    
    result = triggers_manager.update(trigger_id, data)
    
    if result["success"]:
        return jsonify(result)
    
    return jsonify(result), 404


@triggers_bp.route('/<trigger_id>', methods=['DELETE'])
def delete_trigger(trigger_id):
    """Remove um gatilho"""
    if not triggers_manager:
        return jsonify({"error": "Gerenciador não inicializado"}), 500
    
    result = triggers_manager.delete(trigger_id)
    
    if result["success"]:
        return jsonify(result)
    
    return jsonify(result), 404


# ==================== AÇÕES ESPECIAIS ====================

@triggers_bp.route('/<trigger_id>/toggle', methods=['POST'])
def toggle_trigger(trigger_id):
    """Alterna estado ativo/inativo do gatilho"""
    if not triggers_manager:
        return jsonify({"error": "Gerenciador não inicializado"}), 500
    
    result = triggers_manager.toggle(trigger_id)
    
    if result["success"]:
        return jsonify(result)
    
    return jsonify(result), 404


@triggers_bp.route('/<trigger_id>/execute', methods=['POST'])
def execute_trigger(trigger_id):
    """
    Executa um gatilho manualmente
    
    Body JSON (opcional):
    {
        "context": { ... dados de contexto ... }
    }
    """
    if not triggers_manager:
        return jsonify({"error": "Gerenciador não inicializado"}), 500
    
    data = request.get_json() or {}
    context = data.get("context", {})
    
    result = triggers_manager.execute(trigger_id, context)
    
    if result["success"]:
        return jsonify(result)
    
    return jsonify(result), 400


@triggers_bp.route('/<trigger_id>/test', methods=['POST'])
def test_trigger(trigger_id):
    """
    Testa um gatilho sem executar a ação real
    Retorna o que seria executado
    """
    if not triggers_manager:
        return jsonify({"error": "Gerenciador não inicializado"}), 500
    
    result = triggers_manager.read(trigger_id)
    
    if not result["success"]:
        return jsonify(result), 404
    
    trigger = result["trigger"]
    
    return jsonify({
        "success": True,
        "test_mode": True,
        "trigger": trigger,
        "would_execute": {
            "action_type": trigger["action"].get("type"),
            "action_config": trigger["action"],
            "conditions_met": True,
            "simulated_at": datetime.now().isoformat()
        }
    })


# ==================== TEMPLATES ====================

@triggers_bp.route('/templates', methods=['GET'])
def list_templates():
    """Lista templates de gatilhos disponíveis"""
    if not triggers_manager:
        return jsonify({"error": "Gerenciador não inicializado"}), 500
    
    templates = triggers_manager.get_templates()
    
    return jsonify({
        "success": True,
        "templates": templates,
        "total": len(templates)
    })


@triggers_bp.route('/templates/<template_name>/create', methods=['POST'])
def create_from_template(template_name):
    """
    Cria gatilho a partir de um template
    
    Body JSON (opcional):
    {
        "overrides": {
            "name": "Nome customizado",
            "config": { ... sobrescrever config ... },
            "action": { ... sobrescrever action ... }
        }
    }
    """
    if not triggers_manager:
        return jsonify({"error": "Gerenciador não inicializado"}), 500
    
    data = request.get_json() or {}
    overrides = data.get("overrides", {})
    
    result = triggers_manager.create_from_template(template_name, overrides)
    
    if result["success"]:
        return jsonify(result), 201
    
    return jsonify(result), 400


# ==================== WEBHOOKS ====================

@triggers_bp.route('/webhook/<source>', methods=['POST'])
def receive_webhook(source):
    """
    Endpoint genérico para receber webhooks
    
    Args:
        source: Fonte do webhook (n8n, whatsapp, email, github, etc)
    """
    if not triggers_manager:
        return jsonify({"error": "Gerenciador não inicializado"}), 500
    
    data = request.get_json() or {}
    
    # Adicionar metadados
    data["_webhook_source"] = source
    data["_received_at"] = datetime.now().isoformat()
    data["_headers"] = dict(request.headers)
    
    # Processar webhook
    results = triggers_manager.process_webhook(source, data)
    
    return jsonify({
        "success": True,
        "source": source,
        "triggers_executed": len(results),
        "results": results
    })


# ==================== EVENTOS ====================

@triggers_bp.route('/event', methods=['POST'])
def process_event():
    """
    Processa um evento do sistema
    
    Body JSON:
    {
        "event_type": "note_created|note_modified|...",
        "data": { ... dados do evento ... }
    }
    """
    if not triggers_manager:
        return jsonify({"error": "Gerenciador não inicializado"}), 500
    
    data = request.get_json()
    
    if not data or "event_type" not in data:
        return jsonify({"error": "event_type é obrigatório"}), 400
    
    event_type = data["event_type"]
    event_data = data.get("data", {})
    
    results = triggers_manager.process_event(event_type, event_data)
    
    return jsonify({
        "success": True,
        "event_type": event_type,
        "triggers_executed": len(results),
        "results": results
    })


# ==================== ESTATÍSTICAS ====================

@triggers_bp.route('/stats', methods=['GET'])
def get_stats():
    """Retorna estatísticas dos gatilhos"""
    if not triggers_manager:
        return jsonify({"error": "Gerenciador não inicializado"}), 500
    
    result = triggers_manager.read()
    
    if not result["success"]:
        return jsonify(result), 500
    
    triggers = result["triggers"]
    
    # Calcular estatísticas
    stats = {
        "total": len(triggers),
        "by_type": {},
        "by_status": {},
        "enabled": 0,
        "disabled": 0,
        "total_runs": 0,
        "total_errors": 0
    }
    
    for t in triggers:
        # Por tipo
        t_type = t["type"]
        stats["by_type"][t_type] = stats["by_type"].get(t_type, 0) + 1
        
        # Por status
        t_status = t["status"]
        stats["by_status"][t_status] = stats["by_status"].get(t_status, 0) + 1
        
        # Enabled/Disabled
        if t["enabled"]:
            stats["enabled"] += 1
        else:
            stats["disabled"] += 1
        
        # Runs e Errors
        stats["total_runs"] += t.get("run_count", 0)
        stats["total_errors"] += t.get("error_count", 0)
    
    return jsonify({
        "success": True,
        "stats": stats,
        "generated_at": datetime.now().isoformat()
    })


# ==================== BULK OPERATIONS ====================

@triggers_bp.route('/bulk/enable', methods=['POST'])
def bulk_enable():
    """
    Ativa múltiplos gatilhos
    
    Body JSON:
    {
        "trigger_ids": ["id1", "id2", ...]
    }
    """
    if not triggers_manager:
        return jsonify({"error": "Gerenciador não inicializado"}), 500
    
    data = request.get_json()
    trigger_ids = data.get("trigger_ids", [])
    
    results = []
    for tid in trigger_ids:
        result = triggers_manager.update(tid, {"enabled": True})
        results.append({"id": tid, "success": result["success"]})
    
    return jsonify({
        "success": True,
        "results": results,
        "enabled_count": sum(1 for r in results if r["success"])
    })


@triggers_bp.route('/bulk/disable', methods=['POST'])
def bulk_disable():
    """
    Desativa múltiplos gatilhos
    
    Body JSON:
    {
        "trigger_ids": ["id1", "id2", ...]
    }
    """
    if not triggers_manager:
        return jsonify({"error": "Gerenciador não inicializado"}), 500
    
    data = request.get_json()
    trigger_ids = data.get("trigger_ids", [])
    
    results = []
    for tid in trigger_ids:
        result = triggers_manager.update(tid, {"enabled": False})
        results.append({"id": tid, "success": result["success"]})
    
    return jsonify({
        "success": True,
        "results": results,
        "disabled_count": sum(1 for r in results if r["success"])
    })


@triggers_bp.route('/bulk/delete', methods=['POST'])
def bulk_delete():
    """
    Remove múltiplos gatilhos
    
    Body JSON:
    {
        "trigger_ids": ["id1", "id2", ...]
    }
    """
    if not triggers_manager:
        return jsonify({"error": "Gerenciador não inicializado"}), 500
    
    data = request.get_json()
    trigger_ids = data.get("trigger_ids", [])
    
    results = []
    for tid in trigger_ids:
        result = triggers_manager.delete(tid)
        results.append({"id": tid, "success": result["success"]})
    
    return jsonify({
        "success": True,
        "results": results,
        "deleted_count": sum(1 for r in results if r["success"])
    })


# ==================== IMPORT/EXPORT ====================

@triggers_bp.route('/export', methods=['GET'])
def export_triggers():
    """Exporta todos os gatilhos em formato JSON"""
    if not triggers_manager:
        return jsonify({"error": "Gerenciador não inicializado"}), 500
    
    result = triggers_manager.read()
    
    if result["success"]:
        return jsonify({
            "version": "1.0",
            "exported_at": datetime.now().isoformat(),
            "triggers": result["triggers"]
        })
    
    return jsonify(result), 500


@triggers_bp.route('/import', methods=['POST'])
def import_triggers():
    """
    Importa gatilhos de um JSON
    
    Body JSON:
    {
        "triggers": [ ... lista de gatilhos ... ],
        "mode": "merge|replace"
    }
    """
    if not triggers_manager:
        return jsonify({"error": "Gerenciador não inicializado"}), 500
    
    data = request.get_json()
    
    if not data or "triggers" not in data:
        return jsonify({"error": "Lista de triggers é obrigatória"}), 400
    
    mode = data.get("mode", "merge")
    triggers_data = data["triggers"]
    
    results = []
    
    for t in triggers_data:
        try:
            result = triggers_manager.create(
                name=t["name"],
                trigger_type=t["type"],
                config=t["config"],
                action=t["action"],
                description=t.get("description", ""),
                enabled=t.get("enabled", True)
            )
            results.append({"name": t["name"], "success": result["success"]})
        except Exception as e:
            results.append({"name": t.get("name", "unknown"), "success": False, "error": str(e)})
    
    return jsonify({
        "success": True,
        "mode": mode,
        "imported": sum(1 for r in results if r["success"]),
        "failed": sum(1 for r in results if not r["success"]),
        "results": results
    })
