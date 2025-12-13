#!/usr/bin/env python3
"""
Obsidian Advanced Features
Funcionalidades avançadas para manipulação profunda do Obsidian
"""

import re
import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional

class ObsidianAdvanced:
    """Classe para funcionalidades avançadas do Obsidian"""
    
    def __init__(self, vault_path: str):
        self.vault_path = Path(vault_path)
        self.obsidian_folder = self.vault_path / '.obsidian'
    
    # ==================== FRONTMATTER ====================
    
    def parse_frontmatter(self, content: str) -> tuple:
        """Extrai frontmatter e conteúdo de uma nota"""
        if not content.startswith('---'):
            return {}, content
        
        parts = content.split('---', 2)
        if len(parts) < 3:
            return {}, content
        
        try:
            frontmatter = {}
            for line in parts[1].strip().split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    key = key.strip()
                    value = value.strip()
                    
                    # Parse arrays
                    if value.startswith('[') and value.endswith(']'):
                        value = [v.strip() for v in value[1:-1].split(',')]
                    
                    frontmatter[key] = value
            
            return frontmatter, parts[2].strip()
        except:
            return {}, content
    
    def create_frontmatter(self, metadata: Dict) -> str:
        """Cria frontmatter YAML a partir de metadados"""
        lines = ['---']
        for key, value in metadata.items():
            if isinstance(value, list):
                lines.append(f'{key}: [{", ".join(value)}]')
            else:
                lines.append(f'{key}: {value}')
        lines.append('---')
        return '\n'.join(lines)
    
    # ==================== WIKILINKS ====================
    
    def extract_wikilinks(self, content: str) -> List[str]:
        """Extrai todos os wikilinks de uma nota"""
        pattern = r'\[\[([^\]]+)\]\]'
        matches = re.findall(pattern, content)
        
        links = []
        for match in matches:
            # Separar alias se existir
            if '|' in match:
                link = match.split('|')[0]
            else:
                link = match
            
            # Remover seção/bloco se existir
            if '#' in link:
                link = link.split('#')[0]
            
            links.append(link.strip())
        
        return list(set(links))
    
    def get_backlinks(self, note_name: str) -> List[Dict]:
        """Encontra todas as notas que linkam para a nota especificada"""
        backlinks = []
        
        for md_file in self.vault_path.rglob('*.md'):
            if md_file.stem == note_name:
                continue
            
            try:
                with open(md_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    links = self.extract_wikilinks(content)
                    
                    if note_name in links:
                        backlinks.append({
                            'name': md_file.stem,
                            'path': str(md_file.relative_to(self.vault_path))
                        })
            except:
                continue
        
        return backlinks
    
    def create_wikilink(self, target: str, alias: Optional[str] = None, 
                       section: Optional[str] = None) -> str:
        """Cria um wikilink formatado"""
        link = f'[[{target}'
        
        if section:
            link += f'#{section}'
        
        if alias:
            link += f'|{alias}'
        
        link += ']]'
        return link
    
    # ==================== TAGS ====================
    
    def extract_tags(self, content: str, frontmatter: Dict) -> List[str]:
        """Extrai todas as tags de uma nota (inline e frontmatter)"""
        tags = set()
        
        # Tags do frontmatter
        if 'tags' in frontmatter:
            fm_tags = frontmatter['tags']
            if isinstance(fm_tags, list):
                tags.update(fm_tags)
            else:
                tags.add(fm_tags)
        
        # Tags inline
        pattern = r'#([a-zA-Z0-9_/-]+)'
        inline_tags = re.findall(pattern, content)
        tags.update(inline_tags)
        
        return sorted(list(tags))
    
    def find_notes_by_tag(self, tag: str) -> List[Dict]:
        """Encontra todas as notas com uma tag específica"""
        notes = []
        
        for md_file in self.vault_path.rglob('*.md'):
            try:
                with open(md_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    frontmatter, _ = self.parse_frontmatter(content)
                    tags = self.extract_tags(content, frontmatter)
                    
                    if tag in tags:
                        notes.append({
                            'name': md_file.stem,
                            'path': str(md_file.relative_to(self.vault_path)),
                            'tags': tags
                        })
            except:
                continue
        
        return notes
    
    # ==================== TEMPLATES ====================
    
    def create_template(self, template_name: str, variables: Dict) -> str:
        """Cria uma nota a partir de um template"""
        template_path = self.vault_path / 'Templates' / f'{template_name}.md'
        
        if not template_path.exists():
            return f"Template '{template_name}' não encontrado"
        
        with open(template_path, 'r', encoding='utf-8') as f:
            template = f.read()
        
        # Substituir variáveis
        for key, value in variables.items():
            template = template.replace(f'{{{{{key}}}}}', str(value))
        
        # Substituir variáveis de data/hora
        now = datetime.now()
        template = template.replace('{{date}}', now.strftime('%Y-%m-%d'))
        template = template.replace('{{time}}', now.strftime('%H:%M'))
        template = template.replace('{{datetime}}', now.strftime('%Y-%m-%d %H:%M'))
        
        return template
    
    # ==================== DATAVIEW ====================
    
    def simple_dataview_query(self, query_type: str, source: str, 
                             where: Optional[str] = None) -> List[Dict]:
        """Executa uma query Dataview simples"""
        results = []
        
        # Determinar fonte (tag ou pasta)
        if source.startswith('#'):
            # Query por tag
            tag = source[1:]
            results = self.find_notes_by_tag(tag)
        else:
            # Query por pasta
            folder = self.vault_path / source.strip('"')
            if folder.exists():
                for md_file in folder.rglob('*.md'):
                    results.append({
                        'name': md_file.stem,
                        'path': str(md_file.relative_to(self.vault_path))
                    })
        
        # Aplicar filtro WHERE
        if where and results:
            # Implementação simples de filtro
            filtered = []
            for note in results:
                # Carregar conteúdo para verificar condição
                note_path = self.vault_path / note['path']
                try:
                    with open(note_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        frontmatter, _ = self.parse_frontmatter(content)
                        
                        # Verificar condição simples (ex: status = "done")
                        if '=' in where:
                            field, value = where.split('=')
                            field = field.strip()
                            value = value.strip().strip('"')
                            
                            if frontmatter.get(field) == value:
                                filtered.append(note)
                except:
                    continue
            
            results = filtered
        
        return results
    
    # ==================== GRAPH ====================
    
    def generate_graph_data(self) -> Dict:
        """Gera dados para visualização de grafo"""
        nodes = []
        edges = []
        
        for md_file in self.vault_path.rglob('*.md'):
            try:
                # Adicionar nó
                node_id = md_file.stem
                nodes.append({
                    'id': node_id,
                    'label': node_id,
                    'path': str(md_file.relative_to(self.vault_path))
                })
                
                # Adicionar arestas (links)
                with open(md_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    links = self.extract_wikilinks(content)
                    
                    for link in links:
                        edges.append({
                            'from': node_id,
                            'to': link
                        })
            except:
                continue
        
        return {
            'nodes': nodes,
            'edges': edges
        }
    
    # ==================== CONFIGURAÇÃO ====================
    
    def get_workspace_config(self) -> Dict:
        """Retorna configuração do workspace"""
        workspace_file = self.obsidian_folder / 'workspace.json'
        
        if not workspace_file.exists():
            return {}
        
        with open(workspace_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def get_plugins_config(self) -> List[str]:
        """Retorna lista de plugins instalados"""
        plugins_file = self.obsidian_folder / 'community-plugins.json'
        
        if not plugins_file.exists():
            return []
        
        with open(plugins_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def get_hotkeys_config(self) -> Dict:
        """Retorna configuração de atalhos"""
        hotkeys_file = self.obsidian_folder / 'hotkeys.json'
        
        if not hotkeys_file.exists():
            return {}
        
        with open(hotkeys_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    # ==================== ESTATÍSTICAS ====================
    
    def get_vault_stats(self) -> Dict:
        """Retorna estatísticas do vault"""
        total_notes = 0
        total_words = 0
        total_links = 0
        all_tags = set()
        
        for md_file in self.vault_path.rglob('*.md'):
            try:
                total_notes += 1
                
                with open(md_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    frontmatter, body = self.parse_frontmatter(content)
                    
                    # Contar palavras
                    words = len(body.split())
                    total_words += words
                    
                    # Contar links
                    links = self.extract_wikilinks(content)
                    total_links += len(links)
                    
                    # Coletar tags
                    tags = self.extract_tags(content, frontmatter)
                    all_tags.update(tags)
            except:
                continue
        
        return {
            'total_notes': total_notes,
            'total_words': total_words,
            'total_links': total_links,
            'total_tags': len(all_tags),
            'tags': sorted(list(all_tags)),
            'avg_words_per_note': total_words // total_notes if total_notes > 0 else 0
        }
