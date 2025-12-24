#!/usr/bin/env python3
"""
SISTEMA DE GATILHOS E EVENTOS
Gatilhos pré-configurados para automação do ecossistema de IA
Criado por Manus para Rudson Oliveira
"""

import os
import json
import logging
import schedule
import time
from datetime import datetime, timedelta
from typing import Dict, Any, Callable, List
from enum import Enum

logger = logging.getLogger('Triggers')


class TriggerCategory(Enum):
    """Categorias de gatilhos"""
    SYSTEM = "system"           # Gatilhos do sistema
    SCHEDULE = "schedule"       # Gatilhos agendados
    CONDITION = "condition"     # Gatilhos condicionais
    WEBHOOK = "webhook"         # Gatilhos via webhook
    FILE = "file"               # Gatilhos de arquivo
    AI = "ai"                   # Gatilhos de IA


class BuiltInTriggers:
    """
    Gatilhos pré-configurados do sistema
    """
    
    def __init__(self, hub):
        self.hub = hub
        self.scheduled_jobs = []
        self._setup_builtin_triggers()
    
    def _setup_builtin_triggers(self):
        """Configura gatilhos padrão"""
        
        # 1. Health Check - Verifica saúde do sistema a cada 5 minutos
        self.hub.register_trigger(
            name="health_check",
            condition=lambda e: e.type.value == "scheduled" and e.data.get("job") == "health_check",
            action=self._action_health_check
        )
        
        # 2. Auto Backup - Backup automático a cada hora
        self.hub.register_trigger(
            name="auto_backup",
            condition=lambda e: e.type.value == "scheduled" and e.data.get("job") == "auto_backup",
            action=self._action_auto_backup
        )
        
        # 3. Daily Summary - Resumo diário às 23:00
        self.hub.register_trigger(
            name="daily_summary",
            condition=lambda e: e.type.value == "scheduled" and e.data.get("job") == "daily_summary",
            action=self._action_daily_summary
        )
        
        # 4. Error Alert - Alerta quando há muitos erros
        self.hub.register_trigger(
            name="error_alert",
            condition=lambda e: self._condition_error_threshold(e),
            action=self._action_error_alert
        )
        
        # 5. New Note Created - Quando uma nova nota é criada no Obsidian
        self.hub.register_trigger(
            name="new_note_handler",
            condition=lambda e: e.type.value == "file_change" and e.data.get("action") == "created",
            action=self._action_new_note
        )
        
        # 6. AI Response Logger - Registra todas as respostas de IA
        self.hub.register_trigger(
            name="ai_response_logger",
            condition=lambda e: e.type.value == "ai_response",
            action=self._action_log_ai_response
        )
        
        # 7. Webhook Processor - Processa webhooks recebidos
        self.hub.register_trigger(
            name="webhook_processor",
            condition=lambda e: e.type.value == "webhook",
            action=self._action_process_webhook
        )
        
        logger.info("[TRIGGERS] Gatilhos padrão configurados")
    
    # ==================== CONDIÇÕES ====================
    
    def _condition_error_threshold(self, event) -> bool:
        """Verifica se o número de erros passou do limite"""
        return self.hub.stats.get("errors", 0) > 10
    
    # ==================== AÇÕES ====================
    
    def _action_health_check(self, event):
        """Executa verificação de saúde do sistema"""
        import requests
        
        services = {
            "obsidian_api": "https://localhost:27124",
            "comet_bridge": "http://localhost:5000/health",
            "obsidian_agent": "http://localhost:5001/health"
        }
        
        results = {}
        for name, url in services.items():
            try:
                response = requests.get(url, timeout=5, verify=False)
                results[name] = {
                    "status": "online" if response.status_code == 200 else "degraded",
                    "response_time_ms": response.elapsed.total_seconds() * 1000
                }
            except Exception as e:
                results[name] = {"status": "offline", "error": str(e)}
        
        # Salvar resultado
        self.hub.store({
            "name": f"HealthCheck_{datetime.now().strftime('%Y%m%d_%H%M')}",
            "folder": "Hub Central/Health",
            "content": f"# Health Check - {datetime.now().strftime('%d/%m/%Y %H:%M')}\n\n" + 
                      "\n".join([f"- **{k}**: {v['status']}" for k, v in results.items()])
        })
        
        logger.info(f"[HEALTH_CHECK] Resultado: {results}")
        return results
    
    def _action_auto_backup(self, event):
        """Executa backup automático"""
        import subprocess
        
        try:
            # Executar script de backup via COMET
            import requests
            response = requests.post(
                "http://localhost:5000/exec",
                json={"command": "powershell -ExecutionPolicy Bypass -File C:\\Users\\rudpa\\COMET\\backup\\Backup_Sistema_IA.ps1"},
                timeout=300
            )
            
            result = response.json()
            logger.info(f"[AUTO_BACKUP] Resultado: {result}")
            return result
        except Exception as e:
            logger.error(f"[AUTO_BACKUP] Erro: {e}")
            return {"error": str(e)}
    
    def _action_daily_summary(self, event):
        """Gera resumo diário das atividades"""
        summary = {
            "date": datetime.now().strftime("%d/%m/%Y"),
            "events_processed": self.hub.stats.get("events_processed", 0),
            "triggers_fired": self.hub.stats.get("triggers_fired", 0),
            "errors": self.hub.stats.get("errors", 0),
            "uptime_hours": None
        }
        
        if self.hub.stats.get("start_time"):
            uptime = datetime.now() - self.hub.stats["start_time"]
            summary["uptime_hours"] = round(uptime.total_seconds() / 3600, 2)
        
        # Criar nota no Obsidian
        content = f"""# Resumo Diário - {summary['date']}

## Estatísticas do Hub Central

| Métrica | Valor |
|---------|-------|
| Eventos Processados | {summary['events_processed']} |
| Gatilhos Acionados | {summary['triggers_fired']} |
| Erros | {summary['errors']} |
| Uptime | {summary['uptime_hours']} horas |

---
*Gerado automaticamente pelo Hub Central*
"""
        
        self.hub.store({
            "name": f"Resumo_{summary['date'].replace('/', '-')}",
            "folder": "Hub Central/Resumos",
            "content": content
        })
        
        logger.info(f"[DAILY_SUMMARY] Resumo gerado: {summary}")
        return summary
    
    def _action_error_alert(self, event):
        """Envia alerta de erro"""
        alert = {
            "type": "error_alert",
            "message": f"Sistema com {self.hub.stats.get('errors', 0)} erros!",
            "timestamp": datetime.now().isoformat()
        }
        
        # Criar nota de alerta
        self.hub.store({
            "name": f"ALERTA_Erros_{datetime.now().strftime('%Y%m%d_%H%M')}",
            "folder": "Hub Central/Alertas",
            "content": f"# ⚠️ ALERTA DE ERROS\n\n{alert['message']}\n\nData: {alert['timestamp']}"
        })
        
        logger.warning(f"[ERROR_ALERT] {alert['message']}")
        return alert
    
    def _action_new_note(self, event):
        """Processa nova nota criada"""
        note_path = event.data.get("path", "")
        logger.info(f"[NEW_NOTE] Nova nota detectada: {note_path}")
        
        # Aqui pode adicionar lógica para:
        # - Indexar conteúdo
        # - Extrair tags
        # - Criar links automáticos
        # - etc.
        
        return {"processed": note_path}
    
    def _action_log_ai_response(self, event):
        """Registra resposta de IA para análise"""
        ai_data = event.data
        
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "provider": ai_data.get("provider", "unknown"),
            "model": ai_data.get("model", "unknown"),
            "prompt_length": len(ai_data.get("prompt", "")),
            "response_length": len(ai_data.get("response", "")),
            "latency_ms": ai_data.get("latency_ms", 0)
        }
        
        # Salvar em arquivo local para análise
        self.hub.store(log_entry, storage_types=["local_file"])
        
        logger.info(f"[AI_LOG] {log_entry['provider']}/{log_entry['model']} - {log_entry['latency_ms']}ms")
        return log_entry
    
    def _action_process_webhook(self, event):
        """Processa webhook recebido"""
        webhook_data = event.data
        source = webhook_data.get("source", "unknown")
        
        logger.info(f"[WEBHOOK] Recebido de: {source}")
        
        # Roteamento baseado na fonte
        handlers = {
            "github": self._handle_github_webhook,
            "n8n": self._handle_n8n_webhook,
            "whatsapp": self._handle_whatsapp_webhook,
            "email": self._handle_email_webhook
        }
        
        handler = handlers.get(source, self._handle_generic_webhook)
        return handler(webhook_data)
    
    def _handle_github_webhook(self, data):
        """Processa webhook do GitHub"""
        action = data.get("action", "")
        repo = data.get("repository", {}).get("name", "")
        logger.info(f"[GITHUB] {action} em {repo}")
        return {"processed": True, "type": "github"}
    
    def _handle_n8n_webhook(self, data):
        """Processa webhook do N8N"""
        workflow = data.get("workflow", "")
        logger.info(f"[N8N] Workflow: {workflow}")
        return {"processed": True, "type": "n8n"}
    
    def _handle_whatsapp_webhook(self, data):
        """Processa webhook do WhatsApp"""
        message = data.get("message", "")
        sender = data.get("sender", "")
        logger.info(f"[WHATSAPP] Mensagem de {sender}")
        return {"processed": True, "type": "whatsapp", "sender": sender}
    
    def _handle_email_webhook(self, data):
        """Processa webhook de email"""
        subject = data.get("subject", "")
        sender = data.get("from", "")
        logger.info(f"[EMAIL] '{subject}' de {sender}")
        return {"processed": True, "type": "email"}
    
    def _handle_generic_webhook(self, data):
        """Processa webhook genérico"""
        logger.info(f"[WEBHOOK] Genérico: {data}")
        return {"processed": True, "type": "generic"}
    
    # ==================== AGENDAMENTO ====================
    
    def setup_schedules(self):
        """Configura tarefas agendadas"""
        from hub_central import EventType, Priority
        
        # Health Check a cada 5 minutos
        schedule.every(5).minutes.do(
            lambda: self.hub.create_event(
                EventType.SCHEDULED,
                "scheduler",
                {"job": "health_check"},
                Priority.LOW
            )
        )
        
        # Auto Backup a cada hora
        schedule.every().hour.do(
            lambda: self.hub.create_event(
                EventType.SCHEDULED,
                "scheduler",
                {"job": "auto_backup"},
                Priority.NORMAL
            )
        )
        
        # Resumo diário às 23:00
        schedule.every().day.at("23:00").do(
            lambda: self.hub.create_event(
                EventType.SCHEDULED,
                "scheduler",
                {"job": "daily_summary"},
                Priority.NORMAL
            )
        )
        
        logger.info("[SCHEDULER] Tarefas agendadas configuradas")
    
    def run_scheduler(self):
        """Executa o scheduler em loop"""
        while True:
            schedule.run_pending()
            time.sleep(1)


class CustomTriggerBuilder:
    """
    Builder para criar gatilhos customizados
    """
    
    def __init__(self, hub):
        self.hub = hub
    
    def when_keyword_mentioned(self, keyword: str, action: Callable):
        """Gatilho quando uma palavra-chave é mencionada"""
        def condition(event):
            content = str(event.data.get("content", "")).lower()
            return keyword.lower() in content
        
        return self.hub.register_trigger(
            f"keyword_{keyword}",
            condition,
            action
        )
    
    def when_time_is(self, hour: int, minute: int, action: Callable):
        """Gatilho em horário específico"""
        schedule.every().day.at(f"{hour:02d}:{minute:02d}").do(action)
        logger.info(f"[TRIGGER] Agendado para {hour:02d}:{minute:02d}")
    
    def when_file_created(self, folder: str, action: Callable):
        """Gatilho quando arquivo é criado em pasta específica"""
        def condition(event):
            if event.type.value != "file_change":
                return False
            path = event.data.get("path", "")
            return folder in path and event.data.get("action") == "created"
        
        return self.hub.register_trigger(
            f"file_created_{folder}",
            condition,
            action
        )
    
    def when_error_occurs(self, action: Callable):
        """Gatilho quando ocorre erro"""
        def condition(event):
            return event.data.get("error") is not None
        
        return self.hub.register_trigger(
            "on_error",
            condition,
            action
        )
    
    def when_ai_responds(self, provider: str, action: Callable):
        """Gatilho quando IA específica responde"""
        def condition(event):
            if event.type.value != "ai_response":
                return False
            return event.data.get("provider") == provider
        
        return self.hub.register_trigger(
            f"ai_response_{provider}",
            condition,
            action
        )


# ==================== WEBHOOKS SERVER ====================

class WebhookServer:
    """
    Servidor de webhooks para receber eventos externos
    """
    
    def __init__(self, hub, port: int = 5002):
        self.hub = hub
        self.port = port
        self.app = None
    
    def setup(self):
        """Configura servidor Flask para webhooks"""
        from flask import Flask, request, jsonify
        
        self.app = Flask(__name__)
        
        @self.app.route('/webhook/<source>', methods=['POST'])
        def receive_webhook(source):
            from hub_central import EventType, Priority
            
            data = request.json or {}
            data["source"] = source
            data["received_at"] = datetime.now().isoformat()
            
            # Criar evento de webhook
            event = self.hub.create_event(
                EventType.WEBHOOK,
                f"webhook_{source}",
                data,
                Priority.HIGH
            )
            
            return jsonify({
                "success": True,
                "event_id": event.id,
                "message": f"Webhook de {source} recebido"
            })
        
        @self.app.route('/webhook/health', methods=['GET'])
        def webhook_health():
            return jsonify({"status": "online", "port": self.port})
        
        logger.info(f"[WEBHOOK_SERVER] Configurado na porta {self.port}")
    
    def run(self):
        """Inicia servidor de webhooks"""
        if self.app:
            self.app.run(host='0.0.0.0', port=self.port, threaded=True)


# ==================== TESTE ====================

if __name__ == "__main__":
    from hub_central import hub, start_hub, stop_hub
    
    print("=" * 50)
    print("  SISTEMA DE GATILHOS - Teste")
    print("=" * 50)
    
    # Iniciar Hub
    start_hub()
    
    # Configurar gatilhos
    triggers = BuiltInTriggers(hub)
    
    # Criar builder para gatilhos customizados
    builder = CustomTriggerBuilder(hub)
    
    # Exemplo: gatilho quando "urgente" é mencionado
    builder.when_keyword_mentioned(
        "urgente",
        lambda e: print(f"[URGENTE] Detectado: {e.data}")
    )
    
    # Aguardar
    time.sleep(3)
    
    # Mostrar status
    print(f"\nGatilhos registrados: {len(hub.triggers)}")
    for tid, trigger in hub.triggers.items():
        print(f"  - {trigger.name} ({tid})")
    
    # Parar
    stop_hub()

