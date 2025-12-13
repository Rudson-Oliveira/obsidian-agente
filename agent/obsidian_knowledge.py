#!/usr/bin/env python3
"""
Obsidian Knowledge Base
Base de conhecimento completa sobre Obsidian para o agente inteligente
"""

class ObsidianKnowledge:
    """Classe para acessar a base de conhecimento do Obsidian"""
    
    def __init__(self):
        self.features = OBSIDIAN_KNOWLEDGE
    
    def get_feature_info(self, feature_name):
        """Retorna informações sobre um recurso específico"""
        return self.features.get(feature_name, None)
    
    def get_popular_plugins(self):
        """Retorna lista de plugins populares"""
        plugins_info = self.features.get('plugins', {})
        popular = plugins_info.get('popular_community', {})
        return list(popular.keys())
    
    def search_knowledge(self, query):
        """Busca na base de conhecimento"""
        results = []
        query_lower = query.lower()
        
        for key, value in self.features.items():
            if query_lower in key.lower():
                results.append({"key": key, "data": value})
            elif isinstance(value, dict):
                desc = value.get('description', '')
                if query_lower in desc.lower():
                    results.append({"key": key, "data": value})
        
        return results

OBSIDIAN_KNOWLEDGE = {
    "vault_structure": {
        "description": "Estrutura de um vault do Obsidian",
        "details": {
            "vault_folder": "Pasta raiz contendo todas as notas e configurações",
            "obsidian_folder": ".obsidian/ - Pasta oculta com configurações do vault",
            "config_files": [
                "app.json - Configurações gerais do app",
                "appearance.json - Temas e aparência",
                "hotkeys.json - Atalhos de teclado",
                "workspace.json - Layout das janelas",
                "community-plugins.json - Lista de plugins instalados",
                "plugins/ - Pasta com plugins da comunidade"
            ],
            "note_format": "Arquivos .md (Markdown) com frontmatter YAML opcional"
        }
    },
    
    "markdown_features": {
        "description": "Recursos Markdown suportados pelo Obsidian",
        "syntax": {
            "headers": "# H1, ## H2, ### H3, etc.",
            "bold": "**texto** ou __texto__",
            "italic": "*texto* ou _texto_",
            "strikethrough": "~~texto~~",
            "highlight": "==texto==",
            "code_inline": "`código`",
            "code_block": "```linguagem\\ncódigo\\n```",
            "links_internal": "[[Nome da Nota]]",
            "links_with_alias": "[[Nome da Nota|Alias]]",
            "links_external": "[texto](url)",
            "images": "![[imagem.png]] ou ![alt](url)",
            "lists_unordered": "- item ou * item",
            "lists_ordered": "1. item",
            "tasks": "- [ ] tarefa ou - [x] tarefa completa",
            "blockquotes": "> citação",
            "horizontal_rule": "--- ou ***",
            "tables": "| Col1 | Col2 |\\n|------|------|\\n| val1 | val2 |",
            "footnotes": "[^1] e [^1]: texto da nota",
            "math": "$equação$ ou $$\\nequação\\n$$"
        }
    },
    
    "wikilinks": {
        "description": "Sistema de links internos do Obsidian",
        "types": {
            "basic": "[[Nome da Nota]]",
            "with_alias": "[[Nome da Nota|Texto Exibido]]",
            "with_header": "[[Nome da Nota#Seção]]",
            "with_block": "[[Nome da Nota#^block-id]]",
            "embed_note": "![[Nome da Nota]]",
            "embed_section": "![[Nome da Nota#Seção]]",
            "embed_block": "![[Nome da Nota#^block-id]]",
            "embed_image": "![[imagem.png]]",
            "embed_pdf": "![[documento.pdf#page=5]]"
        },
        "backlinks": "Links reversos mostram quais notas apontam para a nota atual"
    },
    
    "frontmatter": {
        "description": "Metadados YAML no início das notas",
        "format": "---\\nkey: value\\ntags: [tag1, tag2]\\n---",
        "common_fields": {
            "title": "Título da nota",
            "tags": "Lista de tags",
            "aliases": "Nomes alternativos para a nota",
            "cssclass": "Classe CSS customizada",
            "date": "Data de criação",
            "author": "Autor da nota",
            "status": "Status (draft, published, etc.)"
        }
    },
    
    "tags": {
        "description": "Sistema de tags do Obsidian",
        "syntax": {
            "inline": "#tag ou #tag/subtag",
            "frontmatter": "tags: [tag1, tag2]",
            "nested": "#projeto/trabalho/cliente"
        },
        "search": "tag:#nome para buscar por tag"
    },
    
    "plugins": {
        "core_plugins": {
            "file_explorer": "Navegação de arquivos",
            "search": "Busca global",
            "quick_switcher": "Navegação rápida (Ctrl+O)",
            "graph_view": "Visualização de grafo",
            "backlinks": "Links reversos",
            "outgoing_links": "Links de saída",
            "tag_pane": "Painel de tags",
            "page_preview": "Preview ao passar mouse",
            "starred": "Notas favoritas",
            "templates": "Sistema de templates",
            "command_palette": "Paleta de comandos (Ctrl+P)",
            "daily_notes": "Notas diárias",
            "workspaces": "Espaços de trabalho salvos"
        },
        "popular_community": {
            "dataview": "Queries SQL-like para notas",
            "templater": "Templates avançados com scripts",
            "calendar": "Visualização de calendário",
            "kanban": "Quadros kanban",
            "advanced_tables": "Editor de tabelas",
            "excalidraw": "Desenhos e diagramas",
            "obsidian_git": "Sincronização via Git"
        }
    },
    
    "dataview": {
        "description": "Plugin para queries avançadas",
        "query_types": {
            "list": "LIST FROM #tag",
            "table": "TABLE field1, field2 FROM #tag",
            "task": "TASK FROM #tag",
            "calendar": "CALENDAR FROM #tag"
        },
        "operators": {
            "from": "FROM #tag ou FROM \"pasta\"",
            "where": "WHERE field = value",
            "sort": "SORT field ASC/DESC",
            "limit": "LIMIT 10",
            "group_by": "GROUP BY field"
        },
        "functions": {
            "date": "date(field)",
            "length": "length(list)",
            "contains": "contains(list, value)",
            "filter": "filter(list, condition)"
        }
    },
    
    "templater": {
        "description": "Plugin para templates dinâmicos",
        "syntax": {
            "date": "<% tp.date.now() %>",
            "time": "<% tp.date.now('HH:mm') %>",
            "file_title": "<% tp.file.title %>",
            "file_path": "<% tp.file.path() %>",
            "prompt": "<% tp.system.prompt('Pergunta') %>",
            "suggester": "<% tp.system.suggester(['Op1', 'Op2'], ['val1', 'val2']) %>"
        }
    },
    
    "api": {
        "description": "API JavaScript do Obsidian para plugins",
        "main_classes": {
            "App": "Classe principal do aplicativo",
            "Vault": "Acesso ao vault e arquivos",
            "Workspace": "Gerenciamento de workspace",
            "MetadataCache": "Cache de metadados",
            "FileManager": "Gerenciamento de arquivos"
        },
        "vault_methods": {
            "read": "vault.read(file) - Lê conteúdo",
            "modify": "vault.modify(file, data) - Modifica arquivo",
            "create": "vault.create(path, data) - Cria arquivo",
            "delete": "vault.delete(file) - Deleta arquivo",
            "rename": "vault.rename(file, newPath) - Renomeia"
        }
    },
    
    "uri_protocol": {
        "description": "Protocolo obsidian:// para abrir notas",
        "format": "obsidian://open?vault=VaultName&file=NotePath",
        "actions": {
            "open": "obsidian://open?vault=name&file=path",
            "new": "obsidian://new?vault=name&file=path&content=text",
            "search": "obsidian://search?vault=name&query=text",
            "hook-get-address": "obsidian://hook-get-address?vault=name&file=path"
        }
    },
    
    "best_practices": {
        "organization": [
            "Use pastas para categorias amplas",
            "Use tags para tópicos transversais",
            "Use links para conectar ideias relacionadas",
            "Mantenha notas atômicas (um conceito por nota)",
            "Use MOCs (Maps of Content) para organizar tópicos"
        ],
        "naming": [
            "Use nomes descritivos e únicos",
            "Evite caracteres especiais",
            "Use Title Case ou kebab-case",
            "Inclua data para notas temporais (YYYY-MM-DD)"
        ],
        "linking": [
            "Link liberalmente",
            "Use aliases para contexto",
            "Crie índices para tópicos grandes",
            "Revise backlinks regularmente"
        ]
    },
    
    "advanced_features": {
        "graph_view": {
            "description": "Visualização de rede de notas",
            "filters": "Filtrar por tags, pastas, links",
            "groups": "Agrupar por cores",
            "forces": "Ajustar física do grafo"
        },
        "canvas": {
            "description": "Quadro infinito para organização visual",
            "elements": "Notas, textos, imagens, links"
        },
        "sync": {
            "official": "Obsidian Sync (pago)",
            "alternatives": ["Git", "Syncthing", "iCloud", "Dropbox"]
        }
    },
    
    "shortcuts": {
        "navigation": {
            "quick_switcher": "Ctrl/Cmd + O",
            "command_palette": "Ctrl/Cmd + P",
            "search": "Ctrl/Cmd + Shift + F",
            "graph_view": "Ctrl/Cmd + G"
        },
        "editing": {
            "bold": "Ctrl/Cmd + B",
            "italic": "Ctrl/Cmd + I",
            "insert_link": "Ctrl/Cmd + K",
            "toggle_checkbox": "Ctrl/Cmd + Enter"
        },
        "view": {
            "toggle_edit_preview": "Ctrl/Cmd + E",
            "toggle_left_sidebar": "Ctrl/Cmd + Shift + L",
            "toggle_right_sidebar": "Ctrl/Cmd + Shift + R"
        }
    }
}

def get_knowledge(category: str = None):
    """Retorna conhecimento sobre uma categoria específica ou tudo"""
    if category:
        return OBSIDIAN_KNOWLEDGE.get(category, {})
    return OBSIDIAN_KNOWLEDGE

def search_knowledge(query: str):
    """Busca conhecimento por termo"""
    results = []
    query_lower = query.lower()
    
    for category, content in OBSIDIAN_KNOWLEDGE.items():
        if query_lower in str(content).lower():
            results.append({
                'category': category,
                'content': content
            })
    
    return results
