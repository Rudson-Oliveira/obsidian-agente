#!/usr/bin/env python3
"""
Intelligent Obsidian Agent
Sistema de IA inteligente para processar comandos em linguagem natural
"""

import re
from pathlib import Path
from obsidian_knowledge import get_knowledge, search_knowledge

class IntelligentAgent:
    """Agente inteligente para processar comandos do Obsidian"""
    
    def __init__(self):
        self.knowledge = get_knowledge()
        self.command_patterns = self._build_command_patterns()
    
    def _build_command_patterns(self):
        """Constrói padrões de reconhecimento de comandos"""
        return {
            'open_obsidian': [
                r'abr(ir|a).*obsidian',
                r'open.*obsidian',
                r'iniciar.*obsidian',
                r'start.*obsidian'
            ],
            'list_notes': [
                r'list(ar|a).*nota',
                r'list.*note',
                r'mostrar.*nota',
                r'show.*note',
                r'quais.*nota',
                r'ver.*nota'
            ],
            'create_note': [
                r'cri(ar|a).*nota',
                r'create.*note',
                r'nova.*nota',
                r'new.*note',
                r'adicionar.*nota',
                r'add.*note'
            ],
            'search_notes': [
                r'busc(ar|a).*nota',
                r'search.*note',
                r'procur(ar|a).*nota',
                r'find.*note',
                r'encontrar.*nota'
            ],
            'configure_vault': [
                r'configur(ar|a).*vault',
                r'configure.*vault',
                r'definir.*vault',
                r'set.*vault',
                r'caminho.*vault',
                r'path.*vault'
            ],
            'help': [
                r'ajuda',
                r'help',
                r'comandos',
                r'commands',
                r'o que.*fazer',
                r'what.*can'
            ],
            'explain': [
                r'explicar.*obsidian',
                r'explain.*obsidian',
                r'como.*funciona',
                r'how.*work',
                r'o que.*é',
                r'what.*is'
            ]
        }
    
    def process_command(self, text: str):
        """Processa comando em linguagem natural"""
        text_lower = text.lower()
        
        # Detectar tipo de comando
        command_type = self._detect_command_type(text_lower)
        
        # Extrair parâmetros
        params = self._extract_parameters(text, command_type)
        
        return {
            'command': command_type,
            'parameters': params,
            'original_text': text
        }
    
    def _detect_command_type(self, text: str):
        """Detecta o tipo de comando baseado em padrões"""
        for command_type, patterns in self.command_patterns.items():
            for pattern in patterns:
                if re.search(pattern, text, re.IGNORECASE):
                    return command_type
        
        return 'unknown'
    
    def _extract_parameters(self, text: str, command_type: str):
        """Extrai parâmetros do comando"""
        params = {}
        
        if command_type == 'create_note':
            # Extrair título da nota
            match = re.search(r'(?:nota|note)\s+["\']?([^"\']+)["\']?', text, re.IGNORECASE)
            if match:
                params['title'] = match.group(1).strip()
            
            # Extrair conteúdo
            match = re.search(r'(?:com|with)\s+(?:conteúdo|content)\s+["\']?([^"\']+)["\']?', text, re.IGNORECASE)
            if match:
                params['content'] = match.group(1).strip()
        
        elif command_type == 'search_notes':
            # Extrair termo de busca
            match = re.search(r'(?:por|for)\s+["\']?([^"\']+)["\']?', text, re.IGNORECASE)
            if match:
                params['query'] = match.group(1).strip()
            else:
                # Tentar extrair última palavra/frase
                words = text.split()
                if len(words) > 2:
                    params['query'] = ' '.join(words[-3:])
        
        elif command_type == 'configure_vault':
            # Extrair caminho do vault
            match = re.search(r'(?:em|in|para|to)\s+["\']?([^"\']+)["\']?', text, re.IGNORECASE)
            if match:
                params['vault_path'] = match.group(1).strip()
        
        elif command_type == 'explain':
            # Extrair tópico para explicar
            topics = ['wikilinks', 'tags', 'frontmatter', 'dataview', 'templater', 'plugins']
            for topic in topics:
                if topic in text.lower():
                    params['topic'] = topic
                    break
        
        return params
    
    def get_help_message(self):
        """Retorna mensagem de ajuda com comandos disponíveis"""
        return """
🤖 **Obsidian Agente Inteligente**

Sou um agente superinteligente especializado em Obsidian. Posso ajudá-lo com:

**📝 Gerenciamento de Notas:**
• "Criar nota [título]" - Cria uma nova nota
• "Listar notas" - Lista todas as notas do vault
• "Buscar por [termo]" - Busca conteúdo nas notas
• "Abrir Obsidian" - Abre a aplicação

**⚙️ Configuração:**
• "Configurar vault em [caminho]" - Define o caminho do vault
• "Status" - Verifica status do agente

**📚 Conhecimento:**
• "Explicar [tópico]" - Explica conceitos do Obsidian
  Tópicos: wikilinks, tags, frontmatter, dataview, templater, plugins

**💡 Exemplos:**
• "Criar nota Reunião com conteúdo Notas da reunião"
• "Buscar por projeto"
• "Explicar wikilinks"
• "Listar todas as notas"

Digite seu comando em linguagem natural!
"""
    
    def explain_topic(self, topic: str):
        """Explica um tópico do Obsidian"""
        knowledge = get_knowledge(topic)
        
        if not knowledge:
            return f"Desculpe, não encontrei informações sobre '{topic}'. Tópicos disponíveis: wikilinks, tags, frontmatter, dataview, templater, plugins, markdown_features"
        
        # Formatar explicação
        explanation = f"📚 **{topic.upper()}**\n\n"
        
        if 'description' in knowledge:
            explanation += f"{knowledge['description']}\n\n"
        
        # Adicionar detalhes específicos
        if topic == 'wikilinks':
            explanation += "**Tipos de Links:**\n"
            for link_type, syntax in knowledge['types'].items():
                explanation += f"• {link_type}: `{syntax}`\n"
        
        elif topic == 'tags':
            explanation += "**Sintaxe:**\n"
            for tag_type, syntax in knowledge['syntax'].items():
                explanation += f"• {tag_type}: `{syntax}`\n"
        
        elif topic == 'frontmatter':
            explanation += f"**Formato:**\n```\n{knowledge['format']}\n```\n\n"
            explanation += "**Campos Comuns:**\n"
            for field, desc in knowledge['common_fields'].items():
                explanation += f"• {field}: {desc}\n"
        
        elif topic == 'dataview':
            explanation += "**Tipos de Query:**\n"
            for query_type, syntax in knowledge['query_types'].items():
                explanation += f"• {query_type}: `{syntax}`\n"
        
        elif topic == 'templater':
            explanation += "**Sintaxe:**\n"
            for func, syntax in knowledge['syntax'].items():
                explanation += f"• {func}: `{syntax}`\n"
        
        elif topic == 'plugins':
            explanation += "**Plugins Core:**\n"
            for plugin, desc in list(knowledge['core_plugins'].items())[:5]:
                explanation += f"• {plugin}: {desc}\n"
            explanation += "\n**Plugins Populares:**\n"
            for plugin, desc in knowledge['popular_community'].items():
                explanation += f"• {plugin}: {desc}\n"
        
        return explanation
    
    def generate_response(self, command_result, api_result):
        """Gera resposta inteligente baseada no resultado"""
        command = command_result['command']
        
        if command == 'help':
            return self.get_help_message()
        
        elif command == 'explain':
            topic = command_result['parameters'].get('topic')
            if topic:
                return self.explain_topic(topic)
            else:
                return "Por favor, especifique um tópico para explicar. Exemplo: 'Explicar wikilinks'"
        
        elif command == 'open_obsidian':
            if api_result.get('success'):
                return "✅ Obsidian aberto com sucesso!"
            else:
                return f"❌ Erro ao abrir Obsidian: {api_result.get('error')}"
        
        elif command == 'list_notes':
            if api_result.get('success'):
                count = len(api_result.get('data', []))
                return f"📝 Encontrei {count} notas no seu vault."
            else:
                return f"❌ Erro ao listar notas: {api_result.get('error')}"
        
        elif command == 'create_note':
            if api_result.get('success'):
                title = command_result['parameters'].get('title', 'Nova Nota')
                return f"✅ Nota '{title}' criada com sucesso!"
            else:
                return f"❌ Erro ao criar nota: {api_result.get('error')}"
        
        elif command == 'search_notes':
            if api_result.get('success'):
                count = len(api_result.get('data', []))
                query = command_result['parameters'].get('query', '')
                return f"🔍 Encontrei {count} notas contendo '{query}'."
            else:
                return f"❌ Erro ao buscar: {api_result.get('error')}"
        
        elif command == 'configure_vault':
            if api_result.get('success'):
                return "✅ Vault configurado com sucesso!"
            else:
                return f"❌ Erro ao configurar vault: {api_result.get('error')}"
        
        else:
            return self.get_help_message()
