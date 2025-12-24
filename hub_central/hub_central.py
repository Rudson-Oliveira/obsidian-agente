#!/usr/bin/env python3
"""
HUB CENTRAL - Sistema de Coordenação de Agentes Autônomos
Criado por Manus para Rudson Oliveira
Data: 24-12-2025
Versão: 1.0

Este módulo coordena todos os agentes e serviços do ecossistema de IA,
gerenciando eventos, gatilhos, decisões e armazenamento multi-destino.
"""

import os
import json
import logging
import threading
import time
from datetime import datetime
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum
from queue import Queue, PriorityQueue
import hashlib

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('HubCentral')


class EventType(Enum):
    """Tipos de eventos que o Hub pode processar"""
    SYSTEM = "system"           # Eventos do sistema (startup, shutdown)
    USER_REQUEST = "user"       # Requisições do usuário
    SCHEDULED = "scheduled"     # Tarefas agendadas
    WEBHOOK = "webhook"         # Eventos externos via webhook
    TRIGGER = "trigger"         # Gatilhos automáticos
    AI_RESPONSE = "ai_response" # Respostas de IAs
    FILE_CHANGE = "file_change" # Mudanças em arquivos
    NOTIFICATION = "notification" # Notificações


class Priority(Enum):
    """Níveis de prioridade para processamento"""
    CRITICAL = 1
    HIGH = 2
    NORMAL = 3
    LOW = 4
    BACKGROUND = 5


class StorageType(Enum):
    """Tipos de armazenamento disponíveis"""
    OBSIDIAN = "obsidian"
    GOOGLE_DRIVE = "google_drive"
    ONEDRIVE = "onedrive"
    MYSQL = "mysql"
    LOCAL_FILE = "local_file"
    MEMORY = "memory"


@dataclass
class Event:
    """Representa um evento no sistema"""
    id: str
    type: EventType
    source: str
    data: Dict[str, Any]
    priority: Priority = Priority.NORMAL
    timestamp: datetime = field(default_factory=datetime.now)
    processed: bool = False
    result: Optional[Dict[str, Any]] = None
    
    def __lt__(self, other):
        return self.priority.value < other.priority.value


@dataclass
class Trigger:
    """Representa um gatilho automático"""
    id: str
    name: str
    condition: Callable[[Event], bool]
    action: Callable[[Event], Any]
    enabled: bool = True
    last_triggered: Optional[datetime] = None
    trigger_count: int = 0


@dataclass
class StorageConfig:
    """Configuração de um destino de armazenamento"""
    type: StorageType
    enabled: bool = True
    config: Dict[str, Any] = field(default_factory=dict)
    priority: int = 1  # Menor = mais prioritário


class HubCentral:
    """
    Hub Central - Coordenador principal do ecossistema de IA
    
    Responsabilidades:
    - Gerenciar eventos e filas de processamento
    - Coordenar gatilhos automáticos
    - Rotear para IAs apropriadas
    - Gerenciar armazenamento multi-destino
    - Manter histórico e logs
    """
    
    def __init__(self, config_path: str = None):
        self.config_path = config_path or os.path.expanduser("~/.hub_central/config.json")
        self.config = self._load_config()
        
        # Filas de eventos
        self.event_queue = PriorityQueue()
        self.processed_events: List[Event] = []
        
        # Gatilhos registrados
        self.triggers: Dict[str, Trigger] = {}
        
        # Configurações de armazenamento
        self.storage_configs: Dict[StorageType, StorageConfig] = {}
        
        # Handlers de eventos por tipo
        self.event_handlers: Dict[EventType, List[Callable]] = {
            event_type: [] for event_type in EventType
        }
        
        # Estado do Hub
        self.running = False
        self.worker_thread: Optional[threading.Thread] = None
        
        # Estatísticas
        self.stats = {
            "events_processed": 0,
            "triggers_fired": 0,
            "errors": 0,
            "start_time": None
        }
        
        # Inicializar armazenamentos padrão
        self._init_default_storage()
        
        logger.info("[HUB_CENTRAL] Hub Central inicializado")
    
    def _load_config(self) -> Dict[str, Any]:
        """Carrega configuração do Hub"""
        default_config = {
            "version": "1.0",
            "auto_start": True,
            "max_queue_size": 1000,
            "worker_threads": 1,
            "default_storage": "obsidian",
            "ai_providers": {
                "primary": "openai",
                "fallback": ["gemini", "claude"]
            },
            "storage": {
                "obsidian": {"enabled": True, "priority": 1},
                "google_drive": {"enabled": False, "priority": 2},
                "onedrive": {"enabled": False, "priority": 3},
                "mysql": {"enabled": False, "priority": 4}
            },
            "triggers": {
                "auto_backup": {"enabled": True, "interval": 3600},
                "health_check": {"enabled": True, "interval": 300}
            }
        }
        
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    loaded = json.load(f)
                    default_config.update(loaded)
            except Exception as e:
                logger.warning(f"Erro ao carregar config: {e}")
        
        return default_config
    
    def _save_config(self):
        """Salva configuração do Hub"""
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=2, ensure_ascii=False)
    
    def _init_default_storage(self):
        """Inicializa configurações de armazenamento padrão"""
        storage_config = self.config.get("storage", {})
        
        for storage_type in StorageType:
            type_config = storage_config.get(storage_type.value, {})
            self.storage_configs[storage_type] = StorageConfig(
                type=storage_type,
                enabled=type_config.get("enabled", False),
                config=type_config.get("config", {}),
                priority=type_config.get("priority", 99)
            )
        
        # Obsidian sempre habilitado por padrão
        self.storage_configs[StorageType.OBSIDIAN].enabled = True
    
    def generate_event_id(self) -> str:
        """Gera ID único para evento"""
        timestamp = datetime.now().isoformat()
        random_part = hashlib.md5(f"{timestamp}{time.time()}".encode()).hexdigest()[:8]
        return f"evt_{random_part}"
    
    # ==================== GERENCIAMENTO DE EVENTOS ====================
    
    def create_event(
        self,
        event_type: EventType,
        source: str,
        data: Dict[str, Any],
        priority: Priority = Priority.NORMAL
    ) -> Event:
        """Cria e enfileira um novo evento"""
        event = Event(
            id=self.generate_event_id(),
            type=event_type,
            source=source,
            data=data,
            priority=priority
        )
        
        self.event_queue.put((priority.value, event))
        logger.info(f"[EVENT] Criado: {event.id} | Tipo: {event_type.value} | Fonte: {source}")
        
        # Verificar gatilhos
        self._check_triggers(event)
        
        return event
    
    def register_handler(self, event_type: EventType, handler: Callable):
        """Registra um handler para um tipo de evento"""
        self.event_handlers[event_type].append(handler)
        logger.info(f"[HANDLER] Registrado para {event_type.value}: {handler.__name__}")
    
    def process_event(self, event: Event) -> Dict[str, Any]:
        """Processa um evento"""
        logger.info(f"[PROCESS] Processando evento: {event.id}")
        
        results = []
        handlers = self.event_handlers.get(event.type, [])
        
        for handler in handlers:
            try:
                result = handler(event)
                results.append({"handler": handler.__name__, "result": result})
            except Exception as e:
                logger.error(f"[ERROR] Handler {handler.__name__}: {e}")
                results.append({"handler": handler.__name__, "error": str(e)})
                self.stats["errors"] += 1
        
        event.processed = True
        event.result = {"handlers_executed": len(results), "results": results}
        self.processed_events.append(event)
        self.stats["events_processed"] += 1
        
        return event.result
    
    # ==================== GERENCIAMENTO DE GATILHOS ====================
    
    def register_trigger(
        self,
        name: str,
        condition: Callable[[Event], bool],
        action: Callable[[Event], Any],
        enabled: bool = True
    ) -> Trigger:
        """Registra um novo gatilho"""
        trigger_id = f"trg_{hashlib.md5(name.encode()).hexdigest()[:8]}"
        
        trigger = Trigger(
            id=trigger_id,
            name=name,
            condition=condition,
            action=action,
            enabled=enabled
        )
        
        self.triggers[trigger_id] = trigger
        logger.info(f"[TRIGGER] Registrado: {name} ({trigger_id})")
        
        return trigger
    
    def _check_triggers(self, event: Event):
        """Verifica se algum gatilho deve ser acionado"""
        for trigger_id, trigger in self.triggers.items():
            if not trigger.enabled:
                continue
            
            try:
                if trigger.condition(event):
                    logger.info(f"[TRIGGER] Acionado: {trigger.name}")
                    trigger.action(event)
                    trigger.last_triggered = datetime.now()
                    trigger.trigger_count += 1
                    self.stats["triggers_fired"] += 1
            except Exception as e:
                logger.error(f"[TRIGGER_ERROR] {trigger.name}: {e}")
    
    def enable_trigger(self, trigger_id: str):
        """Habilita um gatilho"""
        if trigger_id in self.triggers:
            self.triggers[trigger_id].enabled = True
    
    def disable_trigger(self, trigger_id: str):
        """Desabilita um gatilho"""
        if trigger_id in self.triggers:
            self.triggers[trigger_id].enabled = False
    
    # ==================== ARMAZENAMENTO MULTI-DESTINO ====================
    
    def store(
        self,
        data: Dict[str, Any],
        storage_types: List[StorageType] = None,
        metadata: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Armazena dados em um ou mais destinos
        
        Args:
            data: Dados a serem armazenados
            storage_types: Lista de destinos (None = todos habilitados)
            metadata: Metadados adicionais
        
        Returns:
            Resultado do armazenamento por destino
        """
        if storage_types is None:
            # Usar todos os habilitados, ordenados por prioridade
            storage_types = [
                config.type for config in 
                sorted(self.storage_configs.values(), key=lambda x: x.priority)
                if config.enabled
            ]
        
        results = {}
        
        for storage_type in storage_types:
            try:
                result = self._store_to(storage_type, data, metadata)
                results[storage_type.value] = {"success": True, "result": result}
            except Exception as e:
                logger.error(f"[STORAGE_ERROR] {storage_type.value}: {e}")
                results[storage_type.value] = {"success": False, "error": str(e)}
        
        return results
    
    def _store_to(
        self,
        storage_type: StorageType,
        data: Dict[str, Any],
        metadata: Dict[str, Any] = None
    ) -> Any:
        """Armazena em um destino específico"""
        
        if storage_type == StorageType.OBSIDIAN:
            return self._store_obsidian(data, metadata)
        elif storage_type == StorageType.GOOGLE_DRIVE:
            return self._store_google_drive(data, metadata)
        elif storage_type == StorageType.ONEDRIVE:
            return self._store_onedrive(data, metadata)
        elif storage_type == StorageType.MYSQL:
            return self._store_mysql(data, metadata)
        elif storage_type == StorageType.LOCAL_FILE:
            return self._store_local_file(data, metadata)
        elif storage_type == StorageType.MEMORY:
            return self._store_memory(data, metadata)
        else:
            raise ValueError(f"Storage type não suportado: {storage_type}")
    
    def _store_obsidian(self, data: Dict[str, Any], metadata: Dict[str, Any] = None) -> Dict:
        """Armazena no Obsidian via API"""
        # Implementação via COMET Bridge
        import requests
        
        note_name = data.get("name", f"HubCentral_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
        content = data.get("content", json.dumps(data, indent=2, ensure_ascii=False))
        folder = data.get("folder", "Hub Central")
        
        try:
            response = requests.post(
                f"http://localhost:5000/obsidian/vault/{folder}/{note_name}.md",
                json={"content": content},
                timeout=10
            )
            return {"note": f"{folder}/{note_name}.md", "status": response.status_code}
        except Exception as e:
            logger.error(f"Erro ao salvar no Obsidian: {e}")
            raise
    
    def _store_google_drive(self, data: Dict[str, Any], metadata: Dict[str, Any] = None) -> Dict:
        """Armazena no Google Drive"""
        # Placeholder - implementar com API do Google Drive
        config = self.storage_configs[StorageType.GOOGLE_DRIVE].config
        logger.info("[GOOGLE_DRIVE] Armazenamento configurado mas não implementado")
        return {"status": "not_implemented", "config": config}
    
    def _store_onedrive(self, data: Dict[str, Any], metadata: Dict[str, Any] = None) -> Dict:
        """Armazena no OneDrive"""
        # Placeholder - implementar com API do OneDrive
        config = self.storage_configs[StorageType.ONEDRIVE].config
        logger.info("[ONEDRIVE] Armazenamento configurado mas não implementado")
        return {"status": "not_implemented", "config": config}
    
    def _store_mysql(self, data: Dict[str, Any], metadata: Dict[str, Any] = None) -> Dict:
        """Armazena no MySQL"""
        # Placeholder - implementar com mysql-connector-python
        config = self.storage_configs[StorageType.MYSQL].config
        logger.info("[MYSQL] Armazenamento configurado mas não implementado")
        return {"status": "not_implemented", "config": config}
    
    def _store_local_file(self, data: Dict[str, Any], metadata: Dict[str, Any] = None) -> Dict:
        """Armazena em arquivo local"""
        filename = data.get("filename", f"hub_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        filepath = os.path.expanduser(f"~/.hub_central/data/{filename}")
        
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False, default=str)
        
        return {"filepath": filepath}
    
    def _store_memory(self, data: Dict[str, Any], metadata: Dict[str, Any] = None) -> Dict:
        """Armazena em memória (temporário)"""
        if not hasattr(self, '_memory_store'):
            self._memory_store = {}
        
        key = data.get("key", self.generate_event_id())
        self._memory_store[key] = {
            "data": data,
            "metadata": metadata,
            "timestamp": datetime.now().isoformat()
        }
        
        return {"key": key}
    
    # ==================== CONFIGURAÇÃO DE ARMAZENAMENTO ====================
    
    def configure_storage(
        self,
        storage_type: StorageType,
        enabled: bool = True,
        config: Dict[str, Any] = None,
        priority: int = None
    ):
        """Configura um destino de armazenamento"""
        if storage_type not in self.storage_configs:
            self.storage_configs[storage_type] = StorageConfig(type=storage_type)
        
        storage = self.storage_configs[storage_type]
        storage.enabled = enabled
        
        if config:
            storage.config.update(config)
        
        if priority is not None:
            storage.priority = priority
        
        # Atualizar config
        self.config["storage"][storage_type.value] = {
            "enabled": storage.enabled,
            "config": storage.config,
            "priority": storage.priority
        }
        self._save_config()
        
        logger.info(f"[STORAGE] Configurado: {storage_type.value} | Enabled: {enabled}")
    
    # ==================== CONTROLE DO HUB ====================
    
    def start(self):
        """Inicia o Hub Central"""
        if self.running:
            logger.warning("[HUB] Já está rodando")
            return
        
        self.running = True
        self.stats["start_time"] = datetime.now()
        
        # Iniciar worker thread
        self.worker_thread = threading.Thread(target=self._worker_loop, daemon=True)
        self.worker_thread.start()
        
        logger.info("[HUB_CENTRAL] Iniciado com sucesso!")
        
        # Criar evento de startup
        self.create_event(
            EventType.SYSTEM,
            "hub_central",
            {"action": "startup", "timestamp": datetime.now().isoformat()},
            Priority.HIGH
        )
    
    def stop(self):
        """Para o Hub Central"""
        if not self.running:
            return
        
        logger.info("[HUB_CENTRAL] Parando...")
        
        # Criar evento de shutdown
        self.create_event(
            EventType.SYSTEM,
            "hub_central",
            {"action": "shutdown", "timestamp": datetime.now().isoformat()},
            Priority.CRITICAL
        )
        
        self.running = False
        
        if self.worker_thread:
            self.worker_thread.join(timeout=5)
        
        logger.info("[HUB_CENTRAL] Parado")
    
    def _worker_loop(self):
        """Loop principal do worker"""
        while self.running:
            try:
                if not self.event_queue.empty():
                    _, event = self.event_queue.get(timeout=1)
                    self.process_event(event)
                else:
                    time.sleep(0.1)
            except Exception as e:
                logger.error(f"[WORKER_ERROR] {e}")
                self.stats["errors"] += 1
    
    def get_status(self) -> Dict[str, Any]:
        """Retorna status do Hub"""
        uptime = None
        if self.stats["start_time"]:
            uptime = (datetime.now() - self.stats["start_time"]).total_seconds()
        
        return {
            "running": self.running,
            "uptime_seconds": uptime,
            "events_in_queue": self.event_queue.qsize(),
            "events_processed": self.stats["events_processed"],
            "triggers_registered": len(self.triggers),
            "triggers_fired": self.stats["triggers_fired"],
            "errors": self.stats["errors"],
            "storage_enabled": [
                st.value for st, cfg in self.storage_configs.items() if cfg.enabled
            ]
        }


# ==================== INSTÂNCIA GLOBAL ====================

hub = HubCentral()


# ==================== FUNÇÕES DE CONVENIÊNCIA ====================

def start_hub():
    """Inicia o Hub Central"""
    hub.start()

def stop_hub():
    """Para o Hub Central"""
    hub.stop()

def create_event(event_type: str, source: str, data: Dict, priority: str = "normal") -> Event:
    """Cria um evento"""
    return hub.create_event(
        EventType(event_type),
        source,
        data,
        Priority[priority.upper()]
    )

def register_trigger(name: str, condition: Callable, action: Callable) -> Trigger:
    """Registra um gatilho"""
    return hub.register_trigger(name, condition, action)

def store_data(data: Dict, storage_types: List[str] = None) -> Dict:
    """Armazena dados"""
    types = [StorageType(t) for t in storage_types] if storage_types else None
    return hub.store(data, types)

def get_hub_status() -> Dict:
    """Retorna status do Hub"""
    return hub.get_status()

def configure_mysql(host: str, port: int, database: str, user: str, password: str):
    """Configura conexão MySQL"""
    hub.configure_storage(
        StorageType.MYSQL,
        enabled=True,
        config={
            "host": host,
            "port": port,
            "database": database,
            "user": user,
            "password": password
        }
    )

def configure_google_drive(credentials_path: str, folder_id: str = None):
    """Configura Google Drive"""
    hub.configure_storage(
        StorageType.GOOGLE_DRIVE,
        enabled=True,
        config={
            "credentials_path": credentials_path,
            "folder_id": folder_id
        }
    )

def configure_onedrive(client_id: str, client_secret: str, folder_path: str = None):
    """Configura OneDrive"""
    hub.configure_storage(
        StorageType.ONEDRIVE,
        enabled=True,
        config={
            "client_id": client_id,
            "client_secret": client_secret,
            "folder_path": folder_path
        }
    )


# ==================== TESTE ====================

if __name__ == "__main__":
    print("=" * 50)
    print("  HUB CENTRAL - Sistema de Coordenação")
    print("=" * 50)
    
    # Iniciar Hub
    start_hub()
    
    # Registrar um gatilho de exemplo
    def on_user_request(event):
        return event.type == EventType.USER_REQUEST
    
    def handle_user_request(event):
        print(f"[TRIGGER] Processando requisição do usuário: {event.data}")
    
    register_trigger("user_request_handler", on_user_request, handle_user_request)
    
    # Criar evento de teste
    create_event("user", "test", {"message": "Teste do Hub Central"})
    
    # Aguardar processamento
    time.sleep(2)
    
    # Mostrar status
    status = get_hub_status()
    print(f"\nStatus do Hub:")
    print(json.dumps(status, indent=2))
    
    # Parar Hub
    stop_hub()

