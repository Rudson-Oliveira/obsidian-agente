"""
HUB CENTRAL - Sistema de Coordenação de Agentes Autônomos
Criado por Manus para Rudson Oliveira
Versão: 1.0
"""

from .hub_central import (
    hub,
    start_hub,
    stop_hub,
    create_event,
    register_trigger,
    store_data,
    get_hub_status,
    configure_mysql,
    configure_google_drive,
    configure_onedrive,
    EventType,
    Priority,
    StorageType
)

from .execution_engine import (
    engine,
    ask_ai,
    ask_multiple,
    TaskCategory,
    AIProvider
)

from .storage_connectors import (
    storage_manager,
    ObsidianConnector,
    GoogleDriveConnector,
    OneDriveConnector,
    MySQLConnector
)

from .triggers_system import (
    BuiltInTriggers,
    CustomTriggerBuilder,
    TriggerCategory
)

__version__ = "1.0.0"
__author__ = "Manus para Rudson Oliveira"

__all__ = [
    # Hub Central
    "hub",
    "start_hub",
    "stop_hub",
    "create_event",
    "register_trigger",
    "store_data",
    "get_hub_status",
    "EventType",
    "Priority",
    "StorageType",
    
    # Execution Engine
    "engine",
    "ask_ai",
    "ask_multiple",
    "TaskCategory",
    "AIProvider",
    
    # Storage
    "storage_manager",
    "configure_mysql",
    "configure_google_drive",
    "configure_onedrive",
    "ObsidianConnector",
    "GoogleDriveConnector",
    "OneDriveConnector",
    "MySQLConnector",
    
    # Triggers
    "BuiltInTriggers",
    "CustomTriggerBuilder",
    "TriggerCategory"
]

