#!/usr/bin/env python3
"""
GERENCIADOR DE GATILHOS AVANÇADO
Sistema completo com CRUD e configuração dinâmica
Criado por Manus para Rudson Oliveira
"""

import os
import json
import uuid
import logging
import threading
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Callable
from enum import Enum
import schedule
import time

logger = logging.getLogger('TriggersManager')


class TriggerType(Enum):
    """Tipos de gatilhos disponíveis"""
    SCHEDULED = "scheduled"      # Agendados por tempo
    EVENT = "event"              # Baseados em eventos
    WEBHOOK = "webhook"          # Recebem dados externos
    INTELLIGENT = "intelligent"  # Baseados em padrões/IA


class TriggerStatus(Enum):
    """Status do gatilho"""
    ACTIVE = "active"
    PAUSED = "paused"
    DISABLED = "disabled"
    ERROR = "error"


class Trigger:
    """Classe base para gatilhos"""
    
    def __init__(
        self,
        name: str,
        trigger_type: TriggerType,
        config: Dict[str, Any],
        action: Dict[str, Any],
        description: str = "",
        enabled: bool = True
    ):
        self.id = f"trg_{uuid.uuid4().hex[:8]}"
        self.name = name
        self.type = trigger_type
        self.config = config
        self.action = action
        self.description = description
        self.enabled = enabled
        self.status = TriggerStatus.ACTIVE if enabled else TriggerStatus.DISABLED
        self.created_at = datetime.now().isoformat()
        self.updated_at = self.created_at
        self.last_run = None
        self.run_count = 0
        self.error_count = 0
        self.last_error = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Converte para dicionário"""
        return {
            "id": self.id,
            "name": self.name,
            "type": self.type.value,
            "config": self.config,
            "action": self.action,
            "description": self.description,
            "enabled": self.enabled,
            "status": self.status.value,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "last_run": self.last_run,
            "run_count": self.run_count,
            "error_count": self.error_count,
            "last_error": self.last_error
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Trigger':
        """Cria instância a partir de dicionário"""
        trigger = cls(
            name=data["name"],
            trigger_type=TriggerType(data["type"]),
            config=data["config"],
            action=data["action"],
            description=data.get("description", ""),
            enabled=data.get("enabled", True)
        )
        trigger.id = data.get("id", trigger.id)
        trigger.created_at = data.get("created_at", trigger.created_at)
        trigger.updated_at = data.get("updated_at", trigger.updated_at)
        trigger.last_run = data.get("last_run")
        trigger.run_count = data.get("run_count", 0)
        trigger.error_count = data.get("error_count", 0)
        trigger.last_error = data.get("last_error")
        trigger.status = TriggerStatus(data.get("status", "active"))
        return trigger


class TriggersManager:
    """
    Gerenciador central de gatilhos com CRUD completo
    """
    
    def __init__(self, config_path: str = None, hub=None):
        self.hub = hub
        self.config_path = config_path or os.path.expanduser("~/.hub_central/triggers_config.json")
        self.triggers: Dict[str, Trigger] = {}
        self.scheduler_thread = None
        self.running = False
        self.action_handlers: Dict[str, Callable] = {}
        
        # Criar diretório de configuração
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
        
        # Carregar configuração
        self._load_config()
        
        # Registrar handlers de ação padrão
        self._register_default_handlers()
        
        logger.info(f"[TRIGGERS] Gerenciador inicializado com {len(self.triggers)} gatilhos")
    
    def _load_config(self):
        """Carrega configuração do arquivo"""
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for trigger_data in data.get("triggers", []):
                        trigger = Trigger.from_dict(trigger_data)
                        self.triggers[trigger.id] = trigger
                logger.info(f"[TRIGGERS] Carregados {len(self.triggers)} gatilhos do arquivo")
            except Exception as e:
                logger.error(f"[TRIGGERS] Erro ao carregar config: {e}")
    
    def _save_config(self):
        """Salva configuração no arquivo"""
        try:
            data = {
                "version": "1.0",
                "updated_at": datetime.now().isoformat(),
                "triggers": [t.to_dict() for t in self.triggers.values()]
            }
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            logger.info(f"[TRIGGERS] Configuração salva com {len(self.triggers)} gatilhos")
        except Exception as e:
            logger.error(f"[TRIGGERS] Erro ao salvar config: {e}")
    
    def _register_default_handlers(self):
        """Registra handlers de ação padrão"""
        self.action_handlers = {
            "create_note": self._action_create_note,
            "update_note": self._action_update_note,
            "send_notification": self._action_send_notification,
            "run_ai_analysis": self._action_run_ai_analysis,
            "backup_vault": self._action_backup_vault,
            "generate_summary": self._action_generate_summary,
            "apply_template": self._action_apply_template,
            "process_with_ai": self._action_process_with_ai,
            "send_webhook": self._action_send_webhook,
            "log_event": self._action_log_event,
            "custom_script": self._action_custom_script,
        }
    
    # ==================== CRUD ====================
    
    def create(
        self,
        name: str,
        trigger_type: str,
        config: Dict[str, Any],
        action: Dict[str, Any],
        description: str = "",
        enabled: bool = True
    ) -> Dict[str, Any]:
        """
        Cria um novo gatilho
        
        Args:
            name: Nome do gatilho
            trigger_type: Tipo (scheduled, event, webhook, intelligent)
            config: Configuração específica do tipo
            action: Ação a executar
            description: Descrição opcional
            enabled: Se está ativo
        
        Returns:
            Dados do gatilho criado
        """
        try:
            trigger = Trigger(
                name=name,
                trigger_type=TriggerType(trigger_type),
                config=config,
                action=action,
                description=description,
                enabled=enabled
            )
            
            self.triggers[trigger.id] = trigger
            self._save_config()
            
            # Se for agendado e estiver ativo, configurar schedule
            if trigger.type == TriggerType.SCHEDULED and enabled:
                self._setup_scheduled_trigger(trigger)
            
            logger.info(f"[TRIGGERS] Criado: {trigger.name} ({trigger.id})")
            
            return {
                "success": True,
                "trigger": trigger.to_dict(),
                "message": f"Gatilho '{name}' criado com sucesso"
            }
            
        except Exception as e:
            logger.error(f"[TRIGGERS] Erro ao criar: {e}")
            return {"success": False, "error": str(e)}
    
    def read(self, trigger_id: str = None) -> Dict[str, Any]:
        """
        Lê um ou todos os gatilhos
        
        Args:
            trigger_id: ID específico ou None para todos
        
        Returns:
            Dados do(s) gatilho(s)
        """
        if trigger_id:
            trigger = self.triggers.get(trigger_id)
            if trigger:
                return {"success": True, "trigger": trigger.to_dict()}
            return {"success": False, "error": "Gatilho não encontrado"}
        
        return {
            "success": True,
            "triggers": [t.to_dict() for t in self.triggers.values()],
            "total": len(self.triggers)
        }
    
    def update(self, trigger_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        """
        Atualiza um gatilho existente
        
        Args:
            trigger_id: ID do gatilho
            updates: Campos a atualizar
        
        Returns:
            Dados do gatilho atualizado
        """
        trigger = self.triggers.get(trigger_id)
        if not trigger:
            return {"success": False, "error": "Gatilho não encontrado"}
        
        try:
            # Atualizar campos permitidos
            if "name" in updates:
                trigger.name = updates["name"]
            if "config" in updates:
                trigger.config.update(updates["config"])
            if "action" in updates:
                trigger.action.update(updates["action"])
            if "description" in updates:
                trigger.description = updates["description"]
            if "enabled" in updates:
                trigger.enabled = updates["enabled"]
                trigger.status = TriggerStatus.ACTIVE if updates["enabled"] else TriggerStatus.DISABLED
            
            trigger.updated_at = datetime.now().isoformat()
            
            self._save_config()
            
            # Reconfigurar schedule se necessário
            if trigger.type == TriggerType.SCHEDULED:
                self._setup_scheduled_trigger(trigger)
            
            logger.info(f"[TRIGGERS] Atualizado: {trigger.name} ({trigger.id})")
            
            return {
                "success": True,
                "trigger": trigger.to_dict(),
                "message": f"Gatilho '{trigger.name}' atualizado"
            }
            
        except Exception as e:
            logger.error(f"[TRIGGERS] Erro ao atualizar: {e}")
            return {"success": False, "error": str(e)}
    
    def delete(self, trigger_id: str) -> Dict[str, Any]:
        """
        Remove um gatilho
        
        Args:
            trigger_id: ID do gatilho
        
        Returns:
            Resultado da operação
        """
        trigger = self.triggers.get(trigger_id)
        if not trigger:
            return {"success": False, "error": "Gatilho não encontrado"}
        
        try:
            name = trigger.name
            del self.triggers[trigger_id]
            self._save_config()
            
            logger.info(f"[TRIGGERS] Removido: {name} ({trigger_id})")
            
            return {
                "success": True,
                "message": f"Gatilho '{name}' removido com sucesso"
            }
            
        except Exception as e:
            logger.error(f"[TRIGGERS] Erro ao remover: {e}")
            return {"success": False, "error": str(e)}
    
    def toggle(self, trigger_id: str) -> Dict[str, Any]:
        """Alterna estado ativo/inativo do gatilho"""
        trigger = self.triggers.get(trigger_id)
        if not trigger:
            return {"success": False, "error": "Gatilho não encontrado"}
        
        trigger.enabled = not trigger.enabled
        trigger.status = TriggerStatus.ACTIVE if trigger.enabled else TriggerStatus.DISABLED
        trigger.updated_at = datetime.now().isoformat()
        
        self._save_config()
        
        status = "ativado" if trigger.enabled else "desativado"
        logger.info(f"[TRIGGERS] {trigger.name} {status}")
        
        return {
            "success": True,
            "trigger": trigger.to_dict(),
            "message": f"Gatilho '{trigger.name}' {status}"
        }
    
    # ==================== EXECUÇÃO ====================
    
    def execute(self, trigger_id: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Executa um gatilho manualmente
        
        Args:
            trigger_id: ID do gatilho
            context: Contexto adicional
        
        Returns:
            Resultado da execução
        """
        trigger = self.triggers.get(trigger_id)
        if not trigger:
            return {"success": False, "error": "Gatilho não encontrado"}
        
        return self._execute_trigger(trigger, context or {})
    
    def _execute_trigger(self, trigger: Trigger, context: Dict[str, Any]) -> Dict[str, Any]:
        """Executa a ação do gatilho"""
        try:
            action_type = trigger.action.get("type", "log_event")
            handler = self.action_handlers.get(action_type)
            
            if not handler:
                raise ValueError(f"Handler não encontrado: {action_type}")
            
            # Preparar contexto
            full_context = {
                "trigger": trigger.to_dict(),
                "timestamp": datetime.now().isoformat(),
                **context
            }
            
            # Executar ação
            result = handler(trigger.action, full_context)
            
            # Atualizar estatísticas
            trigger.last_run = datetime.now().isoformat()
            trigger.run_count += 1
            self._save_config()
            
            logger.info(f"[TRIGGERS] Executado: {trigger.name}")
            
            return {
                "success": True,
                "trigger_id": trigger.id,
                "action": action_type,
                "result": result
            }
            
        except Exception as e:
            trigger.error_count += 1
            trigger.last_error = str(e)
            trigger.status = TriggerStatus.ERROR
            self._save_config()
            
            logger.error(f"[TRIGGERS] Erro ao executar {trigger.name}: {e}")
            return {"success": False, "error": str(e)}
    
    # ==================== HANDLERS DE AÇÃO ====================
    
    def _action_create_note(self, action: Dict, context: Dict) -> Dict:
        """Cria uma nota no Obsidian"""
        if not self.hub:
            return {"error": "Hub não disponível"}
        
        path = action.get("path", "Hub Central/Notas Automáticas")
        title = action.get("title", f"Nota_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
        template = action.get("template", "")
        
        # Substituir variáveis no template
        content = template.format(
            date=datetime.now().strftime("%d/%m/%Y"),
            time=datetime.now().strftime("%H:%M"),
            datetime=datetime.now().strftime("%d/%m/%Y %H:%M"),
            trigger_name=context.get("trigger", {}).get("name", ""),
            **context
        )
        
        # Criar nota via hub
        result = self.hub.storage.save({
            "title": title,
            "content": content
        }, f"{path}/{title}.md")
        
        return {"note_created": f"{path}/{title}.md", "result": result}
    
    def _action_update_note(self, action: Dict, context: Dict) -> Dict:
        """Atualiza uma nota existente"""
        if not self.hub:
            return {"error": "Hub não disponível"}
        
        path = action.get("path")
        append = action.get("append", "")
        
        # Carregar nota existente
        existing = self.hub.storage.load(path)
        if existing.get("success"):
            new_content = existing["content"] + "\n" + append.format(**context)
            result = self.hub.storage.save({"content": new_content}, path)
            return {"note_updated": path, "result": result}
        
        return {"error": "Nota não encontrada"}
    
    def _action_send_notification(self, action: Dict, context: Dict) -> Dict:
        """Envia notificação"""
        title = action.get("title", "Notificação do Hub Central")
        message = action.get("message", "").format(**context)
        
        # Por enquanto, registra no log e cria nota
        logger.info(f"[NOTIFICATION] {title}: {message}")
        
        return {"notification_sent": True, "title": title, "message": message}
    
    def _action_run_ai_analysis(self, action: Dict, context: Dict) -> Dict:
        """Executa análise com IA"""
        if not self.hub:
            return {"error": "Hub não disponível"}
        
        prompt = action.get("prompt", "").format(**context)
        provider = action.get("provider", "auto")
        
        # Usar motor de execução do hub
        result = self.hub.execution_engine.execute({
            "prompt": prompt,
            "provider": provider
        })
        
        return {"ai_result": result}
    
    def _action_backup_vault(self, action: Dict, context: Dict) -> Dict:
        """Executa backup do vault"""
        import subprocess
        
        backup_script = action.get("script_path", r"C:\Users\rudpa\COMET\backup\Backup_Sistema_IA.ps1")
        
        try:
            result = subprocess.run(
                ["powershell", "-ExecutionPolicy", "Bypass", "-File", backup_script],
                capture_output=True,
                text=True,
                timeout=300
            )
            return {"backup_completed": True, "output": result.stdout}
        except Exception as e:
            return {"backup_completed": False, "error": str(e)}
    
    def _action_generate_summary(self, action: Dict, context: Dict) -> Dict:
        """Gera resumo de notas"""
        if not self.hub:
            return {"error": "Hub não disponível"}
        
        period = action.get("period", "day")  # day, week, month
        folder = action.get("folder", "")
        
        # Buscar notas do período
        # TODO: Implementar busca por período
        
        return {"summary_generated": True, "period": period}
    
    def _action_apply_template(self, action: Dict, context: Dict) -> Dict:
        """Aplica template a uma nota"""
        template_name = action.get("template_name", "default")
        target_path = context.get("note_path", "")
        
        # TODO: Implementar aplicação de template
        
        return {"template_applied": template_name, "target": target_path}
    
    def _action_process_with_ai(self, action: Dict, context: Dict) -> Dict:
        """Processa conteúdo com IA"""
        if not self.hub:
            return {"error": "Hub não disponível"}
        
        content = context.get("content", "")
        instruction = action.get("instruction", "Analise o seguinte conteúdo:")
        
        prompt = f"{instruction}\n\n{content}"
        
        result = self.hub.execution_engine.execute({
            "prompt": prompt,
            "provider": action.get("provider", "auto")
        })
        
        return {"processed": True, "result": result}
    
    def _action_send_webhook(self, action: Dict, context: Dict) -> Dict:
        """Envia dados para webhook externo"""
        import requests
        
        url = action.get("url", "")
        method = action.get("method", "POST")
        headers = action.get("headers", {"Content-Type": "application/json"})
        payload = action.get("payload", context)
        
        try:
            response = requests.request(method, url, json=payload, headers=headers, timeout=30)
            return {
                "webhook_sent": True,
                "status_code": response.status_code,
                "response": response.text[:500]
            }
        except Exception as e:
            return {"webhook_sent": False, "error": str(e)}
    
    def _action_log_event(self, action: Dict, context: Dict) -> Dict:
        """Registra evento no log"""
        message = action.get("message", "Evento registrado")
        level = action.get("level", "info")
        
        log_func = getattr(logger, level, logger.info)
        log_func(f"[EVENT] {message.format(**context)}")
        
        return {"logged": True, "message": message}
    
    def _action_custom_script(self, action: Dict, context: Dict) -> Dict:
        """Executa script customizado"""
        import subprocess
        
        script = action.get("script", "")
        script_type = action.get("script_type", "powershell")
        
        try:
            if script_type == "powershell":
                result = subprocess.run(
                    ["powershell", "-Command", script],
                    capture_output=True,
                    text=True,
                    timeout=60
                )
            else:
                result = subprocess.run(
                    script,
                    shell=True,
                    capture_output=True,
                    text=True,
                    timeout=60
                )
            
            return {
                "script_executed": True,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "return_code": result.returncode
            }
        except Exception as e:
            return {"script_executed": False, "error": str(e)}
    
    # ==================== SCHEDULER ====================
    
    def _setup_scheduled_trigger(self, trigger: Trigger):
        """Configura gatilho agendado no scheduler"""
        config = trigger.config
        schedule_type = config.get("schedule_type", "interval")
        
        # Criar job function
        def job():
            if trigger.enabled:
                self._execute_trigger(trigger, {})
        
        # Limpar jobs anteriores deste trigger
        schedule.clear(trigger.id)
        
        if not trigger.enabled:
            return
        
        # Configurar baseado no tipo
        if schedule_type == "interval":
            interval = config.get("interval", 60)  # minutos
            unit = config.get("unit", "minutes")
            
            if unit == "seconds":
                schedule.every(interval).seconds.do(job).tag(trigger.id)
            elif unit == "minutes":
                schedule.every(interval).minutes.do(job).tag(trigger.id)
            elif unit == "hours":
                schedule.every(interval).hours.do(job).tag(trigger.id)
            elif unit == "days":
                schedule.every(interval).days.do(job).tag(trigger.id)
        
        elif schedule_type == "daily":
            time_str = config.get("time", "09:00")
            schedule.every().day.at(time_str).do(job).tag(trigger.id)
        
        elif schedule_type == "weekly":
            day = config.get("day", "monday").lower()
            time_str = config.get("time", "09:00")
            
            day_map = {
                "monday": schedule.every().monday,
                "tuesday": schedule.every().tuesday,
                "wednesday": schedule.every().wednesday,
                "thursday": schedule.every().thursday,
                "friday": schedule.every().friday,
                "saturday": schedule.every().saturday,
                "sunday": schedule.every().sunday
            }
            
            if day in day_map:
                day_map[day].at(time_str).do(job).tag(trigger.id)
        
        elif schedule_type == "cron":
            # Para cron expressions mais complexas
            # TODO: Implementar parser de cron
            pass
        
        logger.info(f"[TRIGGERS] Agendado: {trigger.name} ({schedule_type})")
    
    def start_scheduler(self):
        """Inicia o scheduler em background"""
        if self.running:
            return
        
        self.running = True
        
        # Configurar todos os gatilhos agendados
        for trigger in self.triggers.values():
            if trigger.type == TriggerType.SCHEDULED and trigger.enabled:
                self._setup_scheduled_trigger(trigger)
        
        # Iniciar thread do scheduler
        def run_scheduler():
            while self.running:
                schedule.run_pending()
                time.sleep(1)
        
        self.scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
        self.scheduler_thread.start()
        
        logger.info("[TRIGGERS] Scheduler iniciado")
    
    def stop_scheduler(self):
        """Para o scheduler"""
        self.running = False
        schedule.clear()
        logger.info("[TRIGGERS] Scheduler parado")
    
    # ==================== EVENTOS ====================
    
    def process_event(self, event_type: str, event_data: Dict[str, Any]) -> List[Dict]:
        """
        Processa um evento e executa gatilhos correspondentes
        
        Args:
            event_type: Tipo do evento (note_created, note_modified, etc)
            event_data: Dados do evento
        
        Returns:
            Lista de resultados das execuções
        """
        results = []
        
        for trigger in self.triggers.values():
            if trigger.type != TriggerType.EVENT or not trigger.enabled:
                continue
            
            # Verificar se o evento corresponde ao gatilho
            trigger_event = trigger.config.get("event_type", "")
            if trigger_event != event_type:
                continue
            
            # Verificar condições adicionais
            if self._check_event_conditions(trigger, event_data):
                result = self._execute_trigger(trigger, event_data)
                results.append(result)
        
        return results
    
    def _check_event_conditions(self, trigger: Trigger, event_data: Dict) -> bool:
        """Verifica se as condições do gatilho são atendidas"""
        conditions = trigger.config.get("conditions", {})
        
        # Verificar pasta
        folder = conditions.get("folder")
        if folder:
            note_path = event_data.get("path", "")
            if not note_path.startswith(folder):
                return False
        
        # Verificar tag
        tag = conditions.get("tag")
        if tag:
            tags = event_data.get("tags", [])
            if tag not in tags:
                return False
        
        # Verificar padrão no conteúdo
        pattern = conditions.get("content_pattern")
        if pattern:
            import re
            content = event_data.get("content", "")
            if not re.search(pattern, content):
                return False
        
        return True
    
    # ==================== WEBHOOKS ====================
    
    def process_webhook(self, source: str, data: Dict[str, Any]) -> List[Dict]:
        """
        Processa dados recebidos via webhook
        
        Args:
            source: Fonte do webhook (n8n, whatsapp, github, etc)
            data: Dados recebidos
        
        Returns:
            Lista de resultados das execuções
        """
        results = []
        
        for trigger in self.triggers.values():
            if trigger.type != TriggerType.WEBHOOK or not trigger.enabled:
                continue
            
            # Verificar se a fonte corresponde
            trigger_source = trigger.config.get("source", "")
            if trigger_source != source and trigger_source != "*":
                continue
            
            result = self._execute_trigger(trigger, {"source": source, "data": data})
            results.append(result)
        
        return results
    
    # ==================== GATILHOS INTELIGENTES ====================
    
    def check_intelligent_triggers(self, context: Dict[str, Any] = None) -> List[Dict]:
        """
        Verifica e executa gatilhos inteligentes
        
        Args:
            context: Contexto atual do sistema
        
        Returns:
            Lista de resultados das execuções
        """
        results = []
        context = context or {}
        
        for trigger in self.triggers.values():
            if trigger.type != TriggerType.INTELLIGENT or not trigger.enabled:
                continue
            
            # Verificar condição inteligente
            if self._check_intelligent_condition(trigger, context):
                result = self._execute_trigger(trigger, context)
                results.append(result)
        
        return results
    
    def _check_intelligent_condition(self, trigger: Trigger, context: Dict) -> bool:
        """Verifica condição de gatilho inteligente"""
        condition_type = trigger.config.get("condition_type", "")
        
        if condition_type == "inactivity":
            # Verificar tempo de inatividade
            threshold_minutes = trigger.config.get("threshold_minutes", 60)
            last_activity = context.get("last_activity")
            
            if last_activity:
                inactive_time = (datetime.now() - datetime.fromisoformat(last_activity)).total_seconds() / 60
                return inactive_time >= threshold_minutes
        
        elif condition_type == "pattern":
            # Verificar padrão nos dados
            pattern = trigger.config.get("pattern", "")
            data = context.get("data", "")
            
            import re
            return bool(re.search(pattern, str(data)))
        
        elif condition_type == "threshold":
            # Verificar limiar numérico
            field = trigger.config.get("field", "")
            threshold = trigger.config.get("threshold", 0)
            operator = trigger.config.get("operator", ">=")
            
            value = context.get(field, 0)
            
            if operator == ">=":
                return value >= threshold
            elif operator == "<=":
                return value <= threshold
            elif operator == "==":
                return value == threshold
            elif operator == ">":
                return value > threshold
            elif operator == "<":
                return value < threshold
        
        return False
    
    # ==================== TEMPLATES DE GATILHOS ====================
    
    def get_templates(self) -> List[Dict[str, Any]]:
        """Retorna templates de gatilhos pré-configurados"""
        return [
            # Agendados
            {
                "name": "Resumo Semanal",
                "type": "scheduled",
                "config": {
                    "schedule_type": "weekly",
                    "day": "monday",
                    "time": "09:00"
                },
                "action": {
                    "type": "generate_summary",
                    "period": "week"
                },
                "description": "Gera resumo das atividades da semana toda segunda às 9h"
            },
            {
                "name": "Check de Emails",
                "type": "scheduled",
                "config": {
                    "schedule_type": "interval",
                    "interval": 2,
                    "unit": "hours"
                },
                "action": {
                    "type": "run_ai_analysis",
                    "prompt": "Verificar emails importantes"
                },
                "description": "Verifica emails importantes a cada 2 horas"
            },
            {
                "name": "Backup Diário",
                "type": "scheduled",
                "config": {
                    "schedule_type": "daily",
                    "time": "23:00"
                },
                "action": {
                    "type": "backup_vault"
                },
                "description": "Executa backup do vault todo dia às 23h"
            },
            # Eventos
            {
                "name": "Template de Projeto",
                "type": "event",
                "config": {
                    "event_type": "note_created",
                    "conditions": {
                        "folder": "Projetos"
                    }
                },
                "action": {
                    "type": "apply_template",
                    "template_name": "projeto"
                },
                "description": "Aplica template quando criar nota na pasta Projetos"
            },
            {
                "name": "Alerta Urgente",
                "type": "event",
                "config": {
                    "event_type": "note_modified",
                    "conditions": {
                        "tag": "#urgente"
                    }
                },
                "action": {
                    "type": "send_notification",
                    "title": "Nota Urgente",
                    "message": "A nota {note_path} foi marcada como urgente"
                },
                "description": "Envia alerta quando nota é marcada com #urgente"
            },
            # Webhooks
            {
                "name": "Processar N8N",
                "type": "webhook",
                "config": {
                    "source": "n8n"
                },
                "action": {
                    "type": "create_note",
                    "path": "N8N/Automações",
                    "template": "# Dados do N8N\n\n**Recebido em:** {datetime}\n\n```json\n{data}\n```"
                },
                "description": "Processa dados recebidos do N8N e cria nota"
            },
            {
                "name": "WhatsApp para Nota",
                "type": "webhook",
                "config": {
                    "source": "whatsapp"
                },
                "action": {
                    "type": "create_note",
                    "path": "WhatsApp/Mensagens",
                    "template": "# Mensagem WhatsApp\n\n**De:** {sender}\n**Data:** {datetime}\n\n{message}"
                },
                "description": "Cria nota quando recebe mensagem do WhatsApp"
            },
            # Inteligentes
            {
                "name": "Sugestão de Tarefas",
                "type": "intelligent",
                "config": {
                    "condition_type": "inactivity",
                    "threshold_minutes": 60
                },
                "action": {
                    "type": "run_ai_analysis",
                    "prompt": "Baseado no contexto atual, sugira as próximas tarefas prioritárias"
                },
                "description": "Sugere tarefas após 1 hora de inatividade"
            },
            {
                "name": "Insights Diários",
                "type": "scheduled",
                "config": {
                    "schedule_type": "daily",
                    "time": "20:00"
                },
                "action": {
                    "type": "run_ai_analysis",
                    "prompt": "Analise as notas criadas hoje e gere insights relevantes"
                },
                "description": "Gera insights das notas do dia às 20h"
            }
        ]
    
    def create_from_template(self, template_name: str, overrides: Dict = None) -> Dict[str, Any]:
        """Cria gatilho a partir de um template"""
        templates = {t["name"]: t for t in self.get_templates()}
        
        if template_name not in templates:
            return {"success": False, "error": f"Template '{template_name}' não encontrado"}
        
        template = templates[template_name].copy()
        
        if overrides:
            if "config" in overrides:
                template["config"].update(overrides["config"])
            if "action" in overrides:
                template["action"].update(overrides["action"])
            if "name" in overrides:
                template["name"] = overrides["name"]
            if "description" in overrides:
                template["description"] = overrides["description"]
        
        return self.create(
            name=template["name"],
            trigger_type=template["type"],
            config=template["config"],
            action=template["action"],
            description=template.get("description", "")
        )


# ==================== INSTÂNCIA GLOBAL ====================

triggers_manager = None

def get_triggers_manager(hub=None) -> TriggersManager:
    """Obtém instância do gerenciador de gatilhos"""
    global triggers_manager
    if triggers_manager is None:
        triggers_manager = TriggersManager(hub=hub)
    return triggers_manager
