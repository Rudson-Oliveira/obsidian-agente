"""
Intelligent Agent v5.0 - Sistema Completo com Melhorias
- Fallback Multi-Provedor de IA (OpenAI, Claude, Perplexity, Gemini)
- Integracao com Registro de Plugins
- Execucao de comandos via API REST do Obsidian
- Abertura de notas e tarefas
- Sincronizacao automatica de plugins
- Sistema de logging de atividades
- Execucao direta de comandos de plugins
"""
import re
import json
import os
import requests
import urllib3
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any
import logging

# Desabilitar warnings de SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Configuracao de logging
LOG_DIR = Path.home() / ".obsidian-agent" / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_DIR / f"agent_{datetime.now().strftime('%Y-%m-%d')}.log", encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Arquivos de configuracao
CONTEXT_FILE = Path.home() / "COMET" / "SYSTEM_CONTEXT.json"
REGISTRY_FILE = Path.home() / "COMET" / "plugin_registry.json"
ACTIVITY_LOG_FILE = LOG_DIR / f"activity_{datetime.now().strftime('%Y-%m-%d')}.json"

try:
    from obsidian_knowledge import get_knowledge, search_knowledge
except ImportError:
    def get_knowledge(): return {}
    def search_knowledge(q): return []

# Importar módulo de lógica de decisão para consulta automática de IAs
try:
    from decision_logic import DecisionLogic, analyze as analyze_query
    DECISION_LOGIC_AVAILABLE = True
    logger.info("[DECISION] Módulo de lógica de decisão carregado!")
except ImportError:
    DECISION_LOGIC_AVAILABLE = False
    logger.warning("[DECISION] Módulo de lógica de decisão não disponível")
    def analyze_query(q): return {'category': 'conversation', 'recommended_ia': 'openai', 'should_consult_external': True, 'confidence': 0.5}


def load_system_context():
    """Carrega o contexto do sistema"""
    if CONTEXT_FILE.exists():
        with open(CONTEXT_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def load_plugin_registry():
    """Carrega o registro de plugins"""
    if REGISTRY_FILE.exists():
        with open(REGISTRY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"plugins": {}}


def log_activity(action: str, details: Dict[str, Any]):
    """Registra atividade em arquivo JSON"""
    activity = {
        "timestamp": datetime.now().isoformat(),
        "action": action,
        "details": details
    }
    
    activities = []
    if ACTIVITY_LOG_FILE.exists():
        try:
            with open(ACTIVITY_LOG_FILE, "r", encoding="utf-8") as f:
                activities = json.load(f)
        except:
            activities = []
    
    activities.append(activity)
    
    # Manter apenas ultimas 1000 atividades
    if len(activities) > 1000:
        activities = activities[-1000:]
    
    with open(ACTIVITY_LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(activities, f, indent=2, ensure_ascii=False)
    
    logger.info(f"[{action}] {json.dumps(details, ensure_ascii=False)}")


class ObsidianAPI:
    """Classe para interagir com a API REST do Obsidian"""
    
    def __init__(self, context):
        self.context = context
        services = context.get("services", {}).get("obsidian_rest_api", {})
        self.base_url = services.get("url", "https://localhost:27124")
        self.api_key = services.get("api_key", "")
        self.vault_path = context.get("paths", {}).get("vault", "")
        logger.info(f"ObsidianAPI inicializado: {self.base_url}")
    
    def _request(self, method, endpoint, **kwargs):
        """Faz uma requisicao para a API do Obsidian"""
        url = f"{self.base_url}{endpoint}"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        try:
            response = requests.request(
                method, url, headers=headers, verify=False, timeout=10, **kwargs
            )
            log_activity("API_REQUEST", {
                "method": method,
                "endpoint": endpoint,
                "status_code": response.status_code
            })
            return response
        except Exception as e:
            log_activity("API_ERROR", {"endpoint": endpoint, "error": str(e)})
            return None
    
    def execute_command(self, command_id):
        """Executa um comando do Obsidian via API"""
        response = self._request("POST", f"/commands/{command_id}")
        if response and response.status_code in [200, 204]:
            log_activity("COMMAND_EXECUTED", {"command": command_id, "success": True})
            return {"success": True, "message": f"Comando '{command_id}' executado!"}
        log_activity("COMMAND_FAILED", {"command": command_id, "success": False})
        return {"success": False, "error": f"Erro ao executar comando"}
    
    def open_note(self, note_path):
        """Abre uma nota no Obsidian"""
        if not note_path.endswith('.md'):
            note_path = f"{note_path}.md"
        
        response = self._request("POST", f"/open/{note_path}")
        if response and response.status_code in [200, 204]:
            log_activity("NOTE_OPENED", {"note": note_path})
            return {"success": True, "message": f"Nota '{note_path}' aberta!"}
        return {"success": False, "error": "Erro ao abrir nota"}
    
    def create_note(self, path: str, content: str):
        """Cria uma nova nota"""
        if not path.endswith('.md'):
            path = f"{path}.md"
        
        response = self._request(
            "PUT", 
            f"/vault/{path}",
            data=content.encode('utf-8'),
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "text/markdown"
            }
        )
        if response and response.status_code in [200, 204]:
            log_activity("NOTE_CREATED", {"path": path})
            return {"success": True, "message": f"Nota '{path}' criada!"}
        return {"success": False, "error": "Erro ao criar nota"}
    
    def list_notes(self, folder=""):
        """Lista notas no vault"""
        endpoint = f"/vault/{folder}" if folder else "/vault/"
        response = self._request("GET", endpoint)
        if response and response.status_code == 200:
            return response.json()
        return {"files": []}
    
    def search_notes(self, query):
        """Busca notas por nome"""
        all_notes = self._get_all_notes()
        results = []
        query_lower = query.lower()
        for note in all_notes:
            if query_lower in note.lower():
                results.append(note)
        return results
    
    def _get_all_notes(self, folder=""):
        """Obtem todas as notas recursivamente"""
        notes = []
        data = self.list_notes(folder)
        for item in data.get("files", []):
            if item.endswith('/'):
                subfolder = folder + item if folder else item
                notes.extend(self._get_all_notes(subfolder.rstrip('/')))
            elif item.endswith('.md'):
                full_path = f"{folder}/{item}" if folder else item
                notes.append(full_path)
        return notes
    
    def find_today_note(self):
        """Encontra a nota de hoje - busca no sistema de arquivos"""
        today = datetime.now()
        date_patterns = [
            today.strftime("%Y-%m-%d"),
            today.strftime("%d-%m-%Y"),
            today.strftime("%Y%m%d")
        ]
        
        # Primeiro tentar via API
        all_notes = self._get_all_notes()
        for note in all_notes:
            note_lower = note.lower()
            for pattern in date_patterns:
                if pattern.lower() in note_lower:
                    return note
        
        # Se nao encontrou via API, buscar no sistema de arquivos
        vault_path = Path(self.vault_path)
        if vault_path.exists():
            for pattern in date_patterns:
                # Buscar em PROJETOS primeiro
                projetos_path = vault_path / "PROJETOS"
                if projetos_path.exists():
                    for file in projetos_path.glob(f"*{pattern}*.md"):
                        return f"PROJETOS/{file.name}"
                
                # Buscar na raiz
                for file in vault_path.glob(f"*{pattern}*.md"):
                    return file.name
                
                # Buscar recursivamente
                for file in vault_path.rglob(f"*{pattern}*.md"):
                    relative = file.relative_to(vault_path)
                    return str(relative).replace("\\", "/")
        
        # Buscar nota mais recente em PROJETOS
        project_notes = [n for n in all_notes if "PROJETOS" in n]
        dated_notes = [n for n in project_notes if re.search(r'\d{4}-\d{2}-\d{2}', n)]
        if dated_notes:
            dated_notes.sort(reverse=True)
            return dated_notes[0]
        
        return None
    
    def open_daily_note(self):
        """Abre a nota diaria (via comando nativo)"""
        return self.execute_command("daily-notes")
    
    def get_vault_stats(self):
        """Retorna estatisticas do vault"""
        all_notes = self._get_all_notes()
        folders = set()
        for note in all_notes:
            if "/" in note:
                folders.add(note.rsplit("/", 1)[0])
        
        return {
            "total_notes": len(all_notes),
            "total_folders": len(folders),
            "folders": list(folders)[:10]
        }


class PluginManager:
    """Gerenciador de plugins do Obsidian"""
    
    def __init__(self, registry_data):
        self.plugins = registry_data.get("plugins", {})
        self.triggers_map = self._build_triggers_map()
        self.commands_map = self._build_commands_map()
        
        # Mapeamento de comandos diretos
        self.direct_commands = {
            # Daily Notes
            "nota de hoje": "daily-notes",
            "nota diaria": "daily-notes",
            "daily note": "daily-notes",
            "abrir hoje": "daily-notes",
            
            # Templater
            "template": "templater-obsidian:insert-templater",
            "inserir template": "templater-obsidian:insert-templater",
            "novo template": "templater-obsidian:create-new-note-from-template",
            
            # Omnisearch
            "buscar": "omnisearch:show-modal",
            "pesquisar": "omnisearch:show-modal",
            "search": "omnisearch:show-modal",
            "omnisearch": "omnisearch:show-modal",
            
            # Tasks
            "tarefa": "editor:toggle-checklist-status",
            "criar tarefa": "editor:toggle-checklist-status",
            "task": "editor:toggle-checklist-status",
            "nova tarefa": "editor:toggle-checklist-status",
            
            # Excalidraw
            "excalidraw": "obsidian-excalidraw-plugin:excalidraw-autocreate",
            "desenho": "obsidian-excalidraw-plugin:excalidraw-autocreate",
            "novo desenho": "obsidian-excalidraw-plugin:excalidraw-autocreate",
            "diagrama": "obsidian-excalidraw-plugin:excalidraw-autocreate",
            
            # Canvas
            "canvas": "canvas:new-file",
            "quadro": "canvas:new-file",
            "novo canvas": "canvas:new-file",
            
            # Dataview
            "dataview": "dataview:dataview-force-refresh-views",
            "atualizar dataview": "dataview:dataview-force-refresh-views",
            
            # Navigation
            "backlinks": "app:toggle-backlinks",
            "links": "app:toggle-backlinks",
            "comandos": "command-palette:open",
            "paleta": "command-palette:open",
            "command palette": "command-palette:open",
            
            # Graph
            "grafo": "graph:open",
            "graph": "graph:open",
            "grafo local": "graph:open-local",
            
            # Quick Switcher
            "trocar nota": "switcher:open",
            "switcher": "switcher:open",
            
            # AI Commander
            "ai commander": "ai-commander:prompt",
            "ia commander": "ai-commander:prompt",
            
            # Text Generator
            "text generator": "obsidian-textgenerator-plugin:generate-text",
            "gerar texto": "obsidian-textgenerator-plugin:generate-text"
        }
        
        logger.info(f"PluginManager inicializado: {len(self.plugins)} plugins, {len(self.direct_commands)} comandos diretos")
    
    def _build_triggers_map(self):
        """Constroi mapa de triggers para plugins"""
        triggers = {}
        for plugin_id, plugin in self.plugins.items():
            for trigger in plugin.get("triggers", []):
                triggers[trigger.lower()] = plugin_id
        return triggers
    
    def _build_commands_map(self):
        """Constroi mapa de comandos para plugins"""
        commands = {}
        for plugin_id, plugin in self.plugins.items():
            for cmd in plugin.get("commands", []):
                commands[cmd] = plugin_id
        return commands
    
    def find_plugin_by_text(self, text):
        """Encontra plugin baseado no texto"""
        text_lower = text.lower()
        for trigger, plugin_id in self.triggers_map.items():
            if trigger in text_lower:
                return self.plugins.get(plugin_id)
        return None
    
    def get_command_for_action(self, action):
        action_lower = action.lower()
        daily_keywords = ['nota de hoje', 'nota diaria', 'daily note', 'abrir hoje', 'abra a nota', 'abra hoje', 'nota do dia']
        for kw in daily_keywords:
            if kw in action_lower:
                return 'daily-notes'
        if action_lower in self.direct_commands:
            return self.direct_commands[action_lower]
        sorted_commands = sorted(self.direct_commands.items(), key=lambda x: len(x[0]), reverse=True)
        for key, cmd in sorted_commands:
            if key in action_lower:
                return cmd
        plugin = self.find_plugin_by_text(action)
        if plugin:
            commands = plugin.get('commands', [])
            if commands:
                return commands[0]
        return None
    
    def get_plugin_info(self, plugin_id):
        """Obtem informacoes de um plugin"""
        return self.plugins.get(plugin_id)
    
    def list_ai_plugins(self):
        """Lista plugins de IA"""
        return [p for p in self.plugins.values() if p.get("category") == "ai"]
    
    def get_plugins_summary(self):
        """Retorna resumo dos plugins"""
        categories = {}
        for plugin in self.plugins.values():
            cat = plugin.get("category", "other")
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(plugin.get("name", plugin.get("id")))
        
        summary = "=== PLUGINS DISPONIVEIS ===\n\n"
        cat_names = {
            "ai": "IA",
            "productivity": "Produtividade",
            "navigation": "Navegacao",
            "visual": "Visual",
            "data": "Dados",
            "search": "Busca",
            "integration": "Integracao",
            "utility": "Utilitarios",
            "editing": "Edicao"
        }
        
        for cat, plugins in categories.items():
            name = cat_names.get(cat, cat.upper())
            summary += f"{name}: {', '.join(plugins)}\n"
        
        return summary
    
    def get_available_commands(self):
        """Retorna lista de comandos disponiveis"""
        return list(self.direct_commands.keys())


class AIProvider:
    """Provedor de IA com fallback automatico"""
    
    def __init__(self, context):
        self.context = context
        self.apis = context.get("apis", {})
        self.last_provider = None
        self.last_error = None
        self.request_count = 0
        logger.info("AIProvider inicializado")
    
    def call_openai(self, prompt):
        """Chama a API da OpenAI"""
        api_key = self.apis.get("openai", {}).get("key")
        if not api_key:
            return None, "Chave OpenAI nao configurada"
        
        try:
            r = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers={"Authorization": f"Bearer {api_key}"},
                json={
                    "model": "gpt-3.5-turbo",
                    "messages": [{"role": "user", "content": prompt}],
                    "max_tokens": 1000,
                    "temperature": 0.7
                },
                timeout=30
            )
            if r.status_code == 200:
                content = r.json().get("choices", [{}])[0].get("message", {}).get("content", "")
                self.last_provider = "OpenAI"
                self.request_count += 1
                log_activity("AI_REQUEST", {"provider": "openai", "success": True})
                return content, None
            return None, f"OpenAI erro {r.status_code}"
        except Exception as e:
            return None, f"OpenAI excecao: {str(e)}"
    
    def call_claude(self, prompt):
        """Chama a API do Claude"""
        api_key = self.apis.get("claude", {}).get("key")
        if not api_key:
            return None, "Chave Claude nao configurada"
        
        try:
            r = requests.post(
                "https://api.anthropic.com/v1/messages",
                headers={
                    "x-api-key": api_key,
                    "Content-Type": "application/json",
                    "anthropic-version": "2023-06-01"
                },
                json={
                    "model": "claude-3-haiku-20240307",
                    "max_tokens": 1000,
                    "messages": [{"role": "user", "content": prompt}]
                },
                timeout=30
            )
            if r.status_code == 200:
                content = r.json().get("content", [{}])[0].get("text", "")
                self.last_provider = "Claude"
                self.request_count += 1
                log_activity("AI_REQUEST", {"provider": "claude", "success": True})
                return content, None
            return None, f"Claude erro {r.status_code}"
        except Exception as e:
            return None, f"Claude excecao: {str(e)}"
    
    def call_perplexity(self, prompt):
        """Chama a API do Perplexity"""
        api_key = self.apis.get("perplexity", {}).get("key")
        if not api_key:
            return None, "Chave Perplexity nao configurada"
        
        try:
            r = requests.post(
                "https://api.perplexity.ai/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "llama-3.1-sonar-small-128k-online",
                    "messages": [{"role": "user", "content": prompt}],
                    "max_tokens": 1000
                },
                timeout=30
            )
            if r.status_code == 200:
                content = r.json().get("choices", [{}])[0].get("message", {}).get("content", "")
                self.last_provider = "Perplexity"
                self.request_count += 1
                log_activity("AI_REQUEST", {"provider": "perplexity", "success": True})
                return content, None
            return None, f"Perplexity erro {r.status_code}"
        except Exception as e:
            return None, f"Perplexity excecao: {str(e)}"
    
    def get_response(self, prompt, provider="auto"):
        """Obtem resposta da IA com fallback"""
        errors = []
        
        providers = [
            ("openai", self.call_openai),
            ("claude", self.call_claude),
            ("perplexity", self.call_perplexity)
        ]
        
        for name, func in providers:
            result, error = func(prompt)
            if result:
                return result
            if error:
                errors.append(f"{name}: {error}")
        
        self.last_error = "; ".join(errors)
        log_activity("AI_ERROR", {"errors": errors})
        return f"Erro: Nenhum provedor de IA disponivel."
    
    def get_status(self):
        """Retorna status dos provedores"""
        return {
            "openai": bool(self.apis.get("openai", {}).get("key")),
            "claude": bool(self.apis.get("claude", {}).get("key")),
            "perplexity": bool(self.apis.get("perplexity", {}).get("key")),
            "last_provider": self.last_provider,
            "request_count": self.request_count
        }


class IntelligentAgent:
    """Agente inteligente principal v5.0"""
    
    def __init__(self):
        logger.info("Inicializando IntelligentAgent v5.0...")
        self.context = load_system_context()
        self.registry = load_plugin_registry()
        self.ai_provider = AIProvider(self.context)
        self.obsidian_api = ObsidianAPI(self.context)
        self.plugin_manager = PluginManager(self.registry)
        self.paths = self.context.get("paths", {})
        self.command_patterns = self._build_command_patterns()
        self.session_start = datetime.now()
        self.commands_processed = 0
        log_activity("AGENT_STARTED", {"version": "5.0"})
        
        # Inicializar lógica de decisão
        if DECISION_LOGIC_AVAILABLE:
            self.decision_logic = DecisionLogic(ai_integration=None)
            logger.info("[DECISION] Lógica de decisão inicializada!")
        else:
            self.decision_logic = None
    
    def _build_command_patterns(self):
        """Constroi padroes de reconhecimento"""
        return {
            "open_today": [r"nota.*hoje", r"abr.*hoje", r"daily.*note", r"nota.*diaria"],
            "open_note": [r"abr.*nota", r"open.*note"],
            "list_notes": [r"list.*nota", r"mostrar.*nota", r"listar.*nota"],
            "create_note": [r"cri.*nota", r"nova.*nota"],
            "search_notes": [r"busc.*nota", r"procur.*nota", r"pesquis"],
            "create_task": [r"cri.*tarefa", r"nova.*tarefa", r"add.*task"],
            "list_tasks": [r"list.*tarefa", r"mostrar.*tarefa", r"tarefas.*pend"],
            "use_template": [r"usar.*template", r"inserir.*template", r"templater"],
            "open_canvas": [r"abr.*canvas", r"novo.*canvas", r"criar.*canvas"],
            "open_excalidraw": [r"abr.*excalidraw", r"novo.*desenho", r"criar.*diagrama"],
            "search_omnisearch": [r"omnisearch", r"busca.*avancada"],
            "plugin_status": [r"status.*plugin", r"plugins.*instalados", r"listar.*plugins"],
            "plugin_command": [r"executar.*plugin", r"rodar.*plugin", r"plugin:"],
            "vault_stats": [r"estatisticas", r"stats", r"info.*vault"],
            "activity_log": [r"log.*atividade", r"historico", r"ultimas.*acoes"],
            "help": [r"^ajuda$", r"^help$", r"^comandos$"],
            "status": [r"^status$", r"^estado$"],
            "ai_status": [r"status.*ia", r"status.*ai"],
            "ask_ai": [r"perguntar", r"pesquisar", r"me diga", r"me fale", r"o que", r"como", r"qual", r"quem", r"quando", r"onde", r"por que"]
        }
    
    def _extract_note_name(self, text):
        """Extrai nome da nota do texto"""
        keywords = ["abrir", "nota", "open", "note", "a", "o", "de", "do", "da"]
        words = text.lower().split()
        filtered = [w for w in words if w not in keywords]
        return " ".join(filtered).strip()
    
    def process_command(self, text):
        """Processa o texto e identifica o comando"""
        text_lower = text.lower().strip()
        detected = None
        
        # Verificar se e um comando de plugin direto
        # Verificar se e uma pergunta antes de buscar comando de plugin
        question_words = ["qual", "quem", "quando", "onde", "como", "por que", "o que", "me diga", "?"]
        is_question = any(q in text_lower for q in question_words)
        plugin_cmd = None if is_question else self.plugin_manager.get_command_for_action(text_lower)
        if plugin_cmd:
            detected = "plugin_command"
        else:
            for cmd, patterns in self.command_patterns.items():
                for p in patterns:
                    if re.search(p, text_lower):
                        detected = cmd
                        break
                if detected:
                    break
        
        if not detected:
            detected = "ask_ai"
        
        self.commands_processed += 1
        log_activity("COMMAND_DETECTED", {"command": detected, "text": text[:50]})
        
        return {
            "command": detected,
            "parameters": {
                "query": text, 
                "note_name": self._extract_note_name(text),
                "plugin_command": plugin_cmd
            },
            "original_text": text
        }
    
    def get_help_message(self):
        """Retorna mensagem de ajuda"""
        return """=== AJUDA - COMANDOS DISPONIVEIS ===

NOTAS:
  - criar nota [titulo] - Cria nova nota
  - listar notas - Lista todas as notas
  - buscar [termo] - Busca nas notas
  - abrir nota [nome] - Abre nota especifica
  - abrir nota de hoje - Abre nota diaria

TAREFAS:
  - criar tarefa - Cria nova tarefa
  - listar tarefas - Lista tarefas pendentes

PLUGINS:
  - status plugins - Lista plugins instalados
  - usar template - Insere template
  - abrir canvas - Cria novo canvas
  - abrir excalidraw - Cria novo desenho
  - omnisearch - Abre busca avancada
  - dataview - Atualiza queries
  - grafo - Abre visualizacao de grafo

STATUS:
  - status - Status geral do sistema
  - status ia - Status dos provedores de IA
  - estatisticas - Info do vault
  - historico - Log de atividades

IA:
  - Qualquer pergunta sera processada pela IA
  - Fallback: OpenAI -> Claude -> Perplexity
"""
    
    def get_system_status(self):
        """Retorna status do sistema"""
        uptime = datetime.now() - self.session_start
        
        status = "=== STATUS DO SISTEMA v5.0 ===\n\n"
        
        status += f"SESSAO:\n"
        status += f"  Uptime: {uptime}\n"
        status += f"  Comandos processados: {self.commands_processed}\n\n"
        
        status += "CAMINHOS:\n"
        for name, path in self.paths.items():
            exists = Path(path).exists() if path else False
            icon = "OK" if exists else "ERRO"
            status += f"  [{icon}] {name}\n"
        
        status += "\nPROVEDORES DE IA:\n"
        ai_status = self.ai_provider.get_status()
        for provider in ["openai", "claude", "perplexity"]:
            icon = "OK" if ai_status.get(provider) else "ERRO"
            status += f"  [{icon}] {provider.upper()}\n"
        status += f"  Requisicoes: {ai_status.get('request_count', 0)}\n"
        
        status += f"\nPLUGINS: {len(self.registry.get('plugins', {}))} registrados\n"
        status += f"COMANDOS DIRETOS: {len(self.plugin_manager.direct_commands)} disponiveis\n"
        
        return status
    
    def get_vault_stats(self):
        """Retorna estatisticas do vault"""
        stats = self.obsidian_api.get_vault_stats()
        
        result = "=== ESTATISTICAS DO VAULT ===\n\n"
        result += f"Total de notas: {stats.get('total_notes', 0)}\n"
        result += f"Total de pastas: {stats.get('total_folders', 0)}\n"
        result += f"\nPastas principais:\n"
        for folder in stats.get('folders', []):
            result += f"  - {folder}\n"
        
        return result
    
    def get_activity_log(self, limit=10):
        """Retorna log de atividades recentes"""
        if not ACTIVITY_LOG_FILE.exists():
            return "Nenhuma atividade registrada."
        
        with open(ACTIVITY_LOG_FILE, "r", encoding="utf-8") as f:
            activities = json.load(f)
        
        recent = activities[-limit:]
        recent.reverse()
        
        result = f"=== ULTIMAS {len(recent)} ATIVIDADES ===\n\n"
        for act in recent:
            ts = act.get("timestamp", "")[:19]
            action = act.get("action", "")
            result += f"[{ts}] {action}\n"
        
        return result
    
    def generate_response(self, command_result, api_result):
        """Gera resposta baseada no comando"""
        cmd = command_result["command"]
        params = command_result.get("parameters", {})
        
        if cmd == "help":
            return self.get_help_message()
        
        if cmd == "status":
            return self.get_system_status()
        
        if cmd == "vault_stats":
            return self.get_vault_stats()
        
        if cmd == "activity_log":
            return self.get_activity_log()
        
        if cmd == "ai_status":
            ai_status = self.ai_provider.get_status()
            status = "=== STATUS DOS PROVEDORES DE IA ===\n\n"
            for provider in ["openai", "claude", "perplexity"]:
                icon = "OK" if ai_status.get(provider) else "ERRO"
                status += f"[{icon}] {provider.upper()}\n"
            if ai_status.get("last_provider"):
                status += f"\nUltimo usado: {ai_status['last_provider']}\n"
            status += f"Total de requisicoes: {ai_status.get('request_count', 0)}\n"
            return status
        
        if cmd == "plugin_status":
            return self.plugin_manager.get_plugins_summary()
        
        if cmd == "plugin_command":
            plugin_cmd = params.get("plugin_command")
            if plugin_cmd:
                result = self.obsidian_api.execute_command(plugin_cmd)
                if result.get("success"):
                    return f"Comando executado: {plugin_cmd}"
                return f"Erro ao executar comando: {plugin_cmd}"
            return "Comando de plugin nao identificado."
        
        if cmd == "open_today":
            # Tentar via API REST primeiro
            today_note = self.obsidian_api.find_today_note()
            if today_note:
                result = self.obsidian_api.open_note(today_note)
                if result.get("success"):
                    return f"Nota de hoje aberta: {today_note}"
            
            # Tentar via comando nativo
            result = self.obsidian_api.open_daily_note()
            if result.get("success"):
                return "Nota diaria aberta!"
            
            return "Nao encontrei nota de hoje. Deseja criar uma?"
        
        if cmd == "open_note":
            note_name = params.get("note_name", "")
            if note_name:
                matches = self.obsidian_api.search_notes(note_name)
                if matches:
                    result = self.obsidian_api.open_note(matches[0])
                    if result.get("success"):
                        return f"Nota aberta: {matches[0]}"
                    return f"Erro ao abrir nota: {result.get('error')}"
                return f"Nota '{note_name}' nao encontrada."
            return "Por favor, especifique o nome da nota."
        
        if cmd == "list_notes":
            notes = self.obsidian_api._get_all_notes()
            if notes:
                result = f"=== NOTAS ({len(notes)} total) ===\n\n"
                for note in notes[:20]:
                    result += f"  - {note}\n"
                if len(notes) > 20:
                    result += f"\n... e mais {len(notes) - 20} notas"
                return result
            return "Nenhuma nota encontrada."
        
        
        if cmd == "create_note":
            # Usar comando nativo do Obsidian para criar nova nota
            result = self.obsidian_api.execute_command("file-explorer:new-file")
            if result.get("success"):
                return "Criador de notas aberto! Digite o nome da nova nota."
            return "Erro ao abrir criador de notas."
        if cmd == "create_task":
            result = self.obsidian_api.execute_command("editor:toggle-checklist-status")
            if result.get("success"):
                return "Criador de tarefas aberto!"
            return "Erro ao abrir criador de tarefas."
        
        if cmd == "use_template":
            result = self.obsidian_api.execute_command("templater-obsidian:insert-templater")
            if result.get("success"):
                return "Seletor de templates aberto!"
            return "Erro ao abrir templates."
        
        if cmd == "open_canvas":
            result = self.obsidian_api.execute_command("canvas:new-file")
            if result.get("success"):
                return "Novo canvas criado!"
            return "Erro ao criar canvas."
        
        if cmd == "open_excalidraw":
            result = self.obsidian_api.execute_command("obsidian-excalidraw-plugin:excalidraw-autocreate")
            if result.get("success"):
                return "Novo desenho Excalidraw criado!"
            return "Erro ao criar desenho."
        
        if cmd == "search_omnisearch":
            result = self.obsidian_api.execute_command("omnisearch:show-modal")
            if result.get("success"):
                return "Omnisearch aberto!"
            return "Erro ao abrir Omnisearch."
        
        if cmd == "ask_ai":
            query = params.get("query", "")
            system_prompt = "Voce e um assistente inteligente integrado ao Obsidian. Responda em portugues brasileiro de forma clara e util. Seja conciso mas informativo."
            full_prompt = f"{system_prompt}\n\nPergunta: {query}"
            
            response = self.ai_provider.get_response(full_prompt)
            
            if self.ai_provider.last_provider:
                response += f"\n\n[Via {self.ai_provider.last_provider}]"
            
            return response
        
        if api_result.get("success"):
            return f"Comando '{cmd}' executado!"
        
        return f"Erro ao executar '{cmd}'."


# Instancia global
intelligent_agent = IntelligentAgent()


def process_text(text):
    """Funcao de conveniencia para processar texto com lógica de decisão"""
    # Analisar a query com lógica de decisão
    analysis = analyze_query(text)
    
    logger.info(f"[DECISION] Query: {text[:50]}...")
    logger.info(f"[DECISION] Categoria: {analysis.get('category')}")
    logger.info(f"[DECISION] IA Recomendada: {analysis.get('recommended_ia')}")
    logger.info(f"[DECISION] Confiança: {analysis.get('confidence', 0):.2f}")
    
    # Processar comando normalmente
    command_result = intelligent_agent.process_command(text)
    api_result = {"success": True}
    response = intelligent_agent.generate_response(command_result, api_result)
    
    # Adicionar informação da decisão se foi consulta de IA
    if command_result.get('cmd') == 'ask_ai' and DECISION_LOGIC_AVAILABLE:
        category = analysis.get('category', 'conversation')
        ia_used = analysis.get('recommended_ia', 'openai')
        confidence = analysis.get('confidence', 0)
        
        # Adicionar indicador de decisão
        decision_info = f"\n\n[Decisão: {category.upper()} | Confiança: {confidence:.0%}]"
        if decision_info not in response:
            response = response.replace('[Via ', f'{decision_info}\n[Via ')
    
    return response


def get_ai_response(prompt, provider="auto"):
    """Funcao de conveniencia para obter resposta da IA"""
    return intelligent_agent.ai_provider.get_response(prompt, provider)


def get_status():
    """Funcao de conveniencia para obter status"""
    return intelligent_agent.get_system_status()


def refresh_plugins():
    """Atualiza o registro de plugins"""
    intelligent_agent.registry = load_plugin_registry()
    intelligent_agent.plugin_manager = PluginManager(intelligent_agent.registry)
    return len(intelligent_agent.registry.get("plugins", {}))


def get_activity_log(limit=10):
    """Retorna log de atividades"""
    return intelligent_agent.get_activity_log(limit)



