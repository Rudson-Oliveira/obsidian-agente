#!/usr/bin/env python3
"""
Módulo de Lógica de Decisão para Consulta Automática de IAs Externas
Obsidian Agent v5.0 - Sistema de Decisão Inteligente

Este módulo analisa perguntas/comandos e decide automaticamente:
1. Se precisa consultar uma IA externa
2. Qual IA é mais adequada para a tarefa
3. Como formatar a consulta para melhor resultado
"""

import re
import json
import logging
from typing import Dict, Any, Optional, List, Tuple
from datetime import datetime

logger = logging.getLogger(__name__)

class DecisionLogic:
    """
    Sistema de decisão inteligente para roteamento de consultas.
    Analisa o contexto e decide qual IA externa consultar.
    """
    
    def __init__(self, ai_integration=None):
        self.ai_integration = ai_integration
        self.decision_history = []
        
        # Categorias de tarefas e IAs recomendadas
        self.task_categories = {
            'code': {
                'keywords': ['código', 'code', 'python', 'javascript', 'programar', 'função', 'classe', 
                            'debug', 'erro', 'bug', 'script', 'api', 'json', 'html', 'css', 'sql',
                            'implementar', 'desenvolver', 'criar função', 'refatorar'],
                'preferred_ias': ['openai', 'deepseek', 'groq'],
                'priority': 1,
                'description': 'Tarefas de programação e código'
            },
            'research': {
                'keywords': ['pesquisar', 'pesquisa', 'buscar', 'encontrar', 'informação', 'dados',
                            'estatística', 'fonte', 'referência', 'artigo', 'estudo', 'análise',
                            'comparar', 'diferença entre', 'o que é', 'como funciona'],
                'preferred_ias': ['openai', 'grok', 'abacus'],
                'priority': 2,
                'description': 'Pesquisa e busca de informações'
            },
            'creative': {
                'keywords': ['criar', 'escrever', 'texto', 'história', 'poema', 'criativo',
                            'ideia', 'sugestão', 'brainstorm', 'nome', 'título', 'slogan',
                            'marketing', 'conteúdo', 'post', 'artigo'],
                'preferred_ias': ['openai', 'claude', 'grok'],
                'priority': 3,
                'description': 'Tarefas criativas e geração de conteúdo'
            },
            'analysis': {
                'keywords': ['analisar', 'análise', 'avaliar', 'revisar', 'verificar', 'checar',
                            'problema', 'solução', 'otimizar', 'melhorar', 'feedback',
                            'opinião', 'sugestão de melhoria'],
                'preferred_ias': ['openai', 'deepseek', 'abacus'],
                'priority': 2,
                'description': 'Análise e avaliação'
            },
            'automation': {
                'keywords': ['automatizar', 'automação', 'workflow', 'n8n', 'integração',
                            'webhook', 'trigger', 'agendamento', 'rotina', 'processo',
                            'pipeline', 'fluxo'],
                'preferred_ias': ['manus', 'openai', 'abacus'],
                'priority': 1,
                'description': 'Automação e workflows'
            },
            'obsidian': {
                'keywords': ['nota', 'notas', 'vault', 'obsidian', 'markdown', 'link',
                            'tag', 'template', 'canvas', 'graph', 'buscar nota',
                            'criar nota', 'organizar'],
                'preferred_ias': ['local', 'ollama'],  # Preferir processamento local
                'priority': 1,
                'description': 'Operações do Obsidian'
            },
            'conversation': {
                'keywords': ['olá', 'oi', 'bom dia', 'boa tarde', 'boa noite', 'tudo bem',
                            'como vai', 'obrigado', 'valeu', 'ajuda', 'help'],
                'preferred_ias': ['ollama', 'openai'],  # Conversação simples
                'priority': 4,
                'description': 'Conversação geral'
            }
        }
        
        # Regras de decisão especiais
        self.special_rules = {
            'urgent': {
                'keywords': ['urgente', 'rápido', 'agora', 'imediato'],
                'action': 'use_fastest_ia',
                'preferred_ias': ['groq', 'ollama']  # IAs mais rápidas
            },
            'complex': {
                'keywords': ['complexo', 'difícil', 'avançado', 'detalhado'],
                'action': 'use_best_ia',
                'preferred_ias': ['openai', 'claude', 'deepseek']
            },
            'local_only': {
                'keywords': ['offline', 'local', 'privado', 'sem internet'],
                'action': 'use_local_only',
                'preferred_ias': ['ollama']
            }
        }
    
    def analyze_query(self, query: str) -> Dict[str, Any]:
        """
        Analisa a query e retorna informações sobre a decisão.
        
        Args:
            query: Texto da pergunta/comando do usuário
            
        Returns:
            Dict com categoria, IA recomendada, confiança, etc.
        """
        query_lower = query.lower()
        
        # Detectar categoria principal
        category_scores = {}
        for cat_name, cat_info in self.task_categories.items():
            score = 0
            matched_keywords = []
            for keyword in cat_info['keywords']:
                if keyword in query_lower:
                    score += 1
                    matched_keywords.append(keyword)
            if score > 0:
                category_scores[cat_name] = {
                    'score': score,
                    'keywords': matched_keywords,
                    'priority': cat_info['priority']
                }
        
        # Detectar regras especiais
        special_rules_matched = []
        for rule_name, rule_info in self.special_rules.items():
            for keyword in rule_info['keywords']:
                if keyword in query_lower:
                    special_rules_matched.append(rule_name)
                    break
        
        # Determinar categoria principal
        if category_scores:
            # Ordenar por score e prioridade
            sorted_cats = sorted(
                category_scores.items(),
                key=lambda x: (x[1]['score'], -x[1]['priority']),
                reverse=True
            )
            main_category = sorted_cats[0][0]
            confidence = min(sorted_cats[0][1]['score'] / 3, 1.0)  # Normalizar
        else:
            main_category = 'conversation'
            confidence = 0.5
        
        # Determinar IA recomendada
        recommended_ia = self._select_ia(main_category, special_rules_matched)
        
        result = {
            'query': query,
            'category': main_category,
            'category_description': self.task_categories[main_category]['description'],
            'confidence': confidence,
            'recommended_ia': recommended_ia,
            'all_categories': category_scores,
            'special_rules': special_rules_matched,
            'timestamp': datetime.now().isoformat(),
            'should_consult_external': self._should_consult_external(main_category, query)
        }
        
        # Registrar decisão
        self.decision_history.append(result)
        
        return result
    
    def _select_ia(self, category: str, special_rules: List[str]) -> str:
        """Seleciona a IA mais adequada baseado na categoria e regras especiais."""
        
        # Verificar regras especiais primeiro
        if 'local_only' in special_rules:
            return 'ollama'
        if 'urgent' in special_rules:
            return 'groq'  # Mais rápido
        if 'complex' in special_rules:
            return 'openai'  # Mais capaz
        
        # Usar preferência da categoria
        preferred = self.task_categories.get(category, {}).get('preferred_ias', ['openai'])
        return preferred[0] if preferred else 'openai'
    
    def _should_consult_external(self, category: str, query: str) -> bool:
        """Decide se deve consultar uma IA externa ou processar localmente."""
        
        # Operações do Obsidian podem ser locais
        if category == 'obsidian':
            # Verificar se é uma operação simples
            simple_ops = ['abrir', 'criar', 'listar', 'buscar nota']
            if any(op in query.lower() for op in simple_ops):
                return False
        
        # Conversação simples pode ser local
        if category == 'conversation':
            if len(query.split()) < 5:  # Mensagens curtas
                return False
        
        # Para outras categorias, consultar IA externa
        return True
    
    def get_system_prompt(self, category: str) -> str:
        """Retorna um system prompt otimizado para a categoria."""
        
        prompts = {
            'code': """Você é um especialista em programação. Forneça código limpo, 
                      bem comentado e seguindo boas práticas. Explique o raciocínio 
                      quando necessário.""",
            
            'research': """Você é um pesquisador experiente. Forneça informações 
                          precisas, cite fontes quando possível, e organize a 
                          resposta de forma clara.""",
            
            'creative': """Você é um criativo talentoso. Seja original, inspirador 
                          e adapte o tom ao contexto solicitado.""",
            
            'analysis': """Você é um analista detalhista. Avalie todos os aspectos, 
                          identifique pontos fortes e fracos, e sugira melhorias 
                          concretas.""",
            
            'automation': """Você é um especialista em automação. Sugira soluções 
                            práticas, workflows eficientes e integrações úteis.""",
            
            'obsidian': """Você é um assistente do Obsidian. Ajude com organização 
                          de notas, links, tags e uso eficiente do vault.""",
            
            'conversation': """Você é um assistente amigável e prestativo. Responda 
                              de forma natural e útil em português brasileiro."""
        }
        
        return prompts.get(category, prompts['conversation'])
    
    def format_query_for_ia(self, query: str, category: str, context: str = None) -> str:
        """Formata a query de forma otimizada para a IA."""
        
        formatted = query
        
        # Adicionar contexto se disponível
        if context:
            formatted = f"Contexto: {context}\n\nPergunta: {query}"
        
        # Adicionar instruções específicas por categoria
        if category == 'code':
            formatted += "\n\n(Por favor, forneça código funcional e bem comentado)"
        elif category == 'research':
            formatted += "\n\n(Por favor, seja preciso e cite fontes se possível)"
        elif category == 'analysis':
            formatted += "\n\n(Por favor, seja detalhado e sugira melhorias)"
        
        return formatted
    
    def process_with_decision(self, query: str, context: str = None) -> Dict[str, Any]:
        """
        Processa uma query com lógica de decisão completa.
        
        Args:
            query: Pergunta/comando do usuário
            context: Contexto adicional (opcional)
            
        Returns:
            Dict com análise, decisão e resposta
        """
        # Analisar query
        analysis = self.analyze_query(query)
        
        # Se não precisa consultar externa, retornar indicação
        if not analysis['should_consult_external']:
            return {
                'analysis': analysis,
                'action': 'process_locally',
                'response': None,
                'message': f"Processamento local recomendado para: {analysis['category']}"
            }
        
        # Preparar consulta
        system_prompt = self.get_system_prompt(analysis['category'])
        formatted_query = self.format_query_for_ia(query, analysis['category'], context)
        
        # Consultar IA (se ai_integration disponível)
        response = None
        if self.ai_integration:
            try:
                result = self.ai_integration.chat(
                    message=formatted_query,
                    context=system_prompt,
                    provider=analysis['recommended_ia']
                )
                if result.get('success'):
                    response = result.get('response')
            except Exception as e:
                logger.error(f"Erro ao consultar IA: {e}")
        
        return {
            'analysis': analysis,
            'action': 'consulted_external',
            'ia_used': analysis['recommended_ia'],
            'response': response,
            'system_prompt': system_prompt,
            'formatted_query': formatted_query
        }
    
    def get_decision_stats(self) -> Dict[str, Any]:
        """Retorna estatísticas das decisões tomadas."""
        if not self.decision_history:
            return {'total': 0, 'categories': {}, 'ias_used': {}}
        
        categories = {}
        ias_used = {}
        
        for decision in self.decision_history:
            cat = decision['category']
            ia = decision['recommended_ia']
            
            categories[cat] = categories.get(cat, 0) + 1
            ias_used[ia] = ias_used.get(ia, 0) + 1
        
        return {
            'total': len(self.decision_history),
            'categories': categories,
            'ias_used': ias_used,
            'last_decision': self.decision_history[-1] if self.decision_history else None
        }


# Instância global
decision_logic = DecisionLogic()


# Funções de conveniência
def analyze(query: str) -> Dict[str, Any]:
    """Analisa uma query e retorna a decisão."""
    return decision_logic.analyze_query(query)


def process(query: str, context: str = None) -> Dict[str, Any]:
    """Processa uma query com lógica de decisão."""
    return decision_logic.process_with_decision(query, context)


def get_stats() -> Dict[str, Any]:
    """Retorna estatísticas de decisões."""
    return decision_logic.get_decision_stats()


# Teste
if __name__ == "__main__":
    # Testes
    test_queries = [
        "Crie uma função Python para ordenar uma lista",
        "O que é machine learning?",
        "Escreva um poema sobre o mar",
        "Analise este código e sugira melhorias",
        "Configure um workflow no N8N",
        "Abra minha nota diária",
        "Olá, tudo bem?",
        "Preciso urgente de ajuda com um bug",
    ]
    
    print("=== TESTE DE LÓGICA DE DECISÃO ===\n")
    
    for query in test_queries:
        result = analyze(query)
        print(f"Query: {query}")
        print(f"  Categoria: {result['category']} ({result['category_description']})")
        print(f"  IA Recomendada: {result['recommended_ia']}")
        print(f"  Confiança: {result['confidence']:.2f}")
        print(f"  Consultar Externa: {result['should_consult_external']}")
        print()
    
    print("\n=== ESTATÍSTICAS ===")
    print(json.dumps(get_stats(), indent=2, ensure_ascii=False))
