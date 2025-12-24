#!/usr/bin/env python3
"""
MOTOR DE DECISÃO E EXECUÇÃO
Coordena a execução de tarefas usando múltiplas IAs e serviços
Criado por Manus para Rudson Oliveira
"""

import os
import json
import logging
import time
import asyncio
from datetime import datetime
from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

logger = logging.getLogger('ExecutionEngine')


class AIProvider(Enum):
    """Provedores de IA disponíveis"""
    OPENAI = "openai"
    CLAUDE = "claude"
    GEMINI = "gemini"
    PERPLEXITY = "perplexity"
    GROQ = "groq"
    DEEPSEEK = "deepseek"
    GROK = "grok"
    OLLAMA = "ollama"
    MANUS = "manus"


class TaskCategory(Enum):
    """Categorias de tarefas"""
    CODE = "code"               # Programação
    RESEARCH = "research"       # Pesquisa
    CREATIVE = "creative"       # Escrita criativa
    ANALYSIS = "analysis"       # Análise de dados
    CONVERSATION = "conversation" # Chat casual
    AUTOMATION = "automation"   # Automação
    SUMMARIZE = "summarize"     # Resumo
    TRANSLATE = "translate"     # Tradução


@dataclass
class ExecutionTask:
    """Representa uma tarefa a ser executada"""
    id: str
    category: TaskCategory
    prompt: str
    context: Dict[str, Any] = field(default_factory=dict)
    preferred_provider: Optional[AIProvider] = None
    fallback_providers: List[AIProvider] = field(default_factory=list)
    max_retries: int = 3
    timeout: int = 60
    created_at: datetime = field(default_factory=datetime.now)
    
    # Resultado
    result: Optional[str] = None
    provider_used: Optional[AIProvider] = None
    execution_time_ms: int = 0
    success: bool = False
    error: Optional[str] = None


class DecisionEngine:
    """
    Motor de decisão para roteamento inteligente de tarefas
    """
    
    # Mapeamento de categoria para provedores recomendados
    CATEGORY_PROVIDERS = {
        TaskCategory.CODE: [AIProvider.OPENAI, AIProvider.CLAUDE, AIProvider.DEEPSEEK],
        TaskCategory.RESEARCH: [AIProvider.PERPLEXITY, AIProvider.GEMINI, AIProvider.OPENAI],
        TaskCategory.CREATIVE: [AIProvider.CLAUDE, AIProvider.OPENAI, AIProvider.GEMINI],
        TaskCategory.ANALYSIS: [AIProvider.OPENAI, AIProvider.CLAUDE, AIProvider.GEMINI],
        TaskCategory.CONVERSATION: [AIProvider.GEMINI, AIProvider.CLAUDE, AIProvider.OPENAI],
        TaskCategory.AUTOMATION: [AIProvider.OPENAI, AIProvider.GROQ, AIProvider.GEMINI],
        TaskCategory.SUMMARIZE: [AIProvider.CLAUDE, AIProvider.GEMINI, AIProvider.OPENAI],
        TaskCategory.TRANSLATE: [AIProvider.GEMINI, AIProvider.OPENAI, AIProvider.CLAUDE]
    }
    
    # Palavras-chave para categorização
    CATEGORY_KEYWORDS = {
        TaskCategory.CODE: [
            "código", "code", "programar", "python", "javascript", "função",
            "debug", "erro", "bug", "api", "script", "algoritmo", "class",
            "método", "variável", "loop", "array", "json", "sql", "html", "css"
        ],
        TaskCategory.RESEARCH: [
            "pesquisar", "research", "buscar", "encontrar", "informação",
            "dados", "estatística", "fonte", "referência", "artigo", "notícia"
        ],
        TaskCategory.CREATIVE: [
            "escrever", "criar", "história", "poema", "criativo", "narrativa",
            "ficção", "personagem", "roteiro", "letra", "música"
        ],
        TaskCategory.ANALYSIS: [
            "analisar", "análise", "comparar", "avaliar", "revisar",
            "examinar", "interpretar", "dados", "gráfico", "tendência"
        ],
        TaskCategory.CONVERSATION: [
            "olá", "oi", "como vai", "tudo bem", "obrigado", "ajuda",
            "explique", "o que é", "quem é", "quando", "onde"
        ],
        TaskCategory.AUTOMATION: [
            "automatizar", "workflow", "tarefa", "agendar", "repetir",
            "integrar", "conectar", "webhook", "trigger", "bot"
        ],
        TaskCategory.SUMMARIZE: [
            "resumir", "resumo", "sintetizar", "principais pontos",
            "em poucas palavras", "tldr", "sumário"
        ],
        TaskCategory.TRANSLATE: [
            "traduzir", "translate", "inglês", "português", "espanhol",
            "francês", "idioma", "língua"
        ]
    }
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.provider_status = {p: True for p in AIProvider}  # Todos ativos por padrão
        self.provider_latency = {p: 0 for p in AIProvider}    # Latência média
    
    def categorize(self, prompt: str) -> TaskCategory:
        """Categoriza o prompt automaticamente"""
        prompt_lower = prompt.lower()
        
        scores = {category: 0 for category in TaskCategory}
        
        for category, keywords in self.CATEGORY_KEYWORDS.items():
            for keyword in keywords:
                if keyword in prompt_lower:
                    scores[category] += 1
        
        # Retorna categoria com maior score, ou CONVERSATION como padrão
        max_category = max(scores, key=scores.get)
        if scores[max_category] > 0:
            return max_category
        return TaskCategory.CONVERSATION
    
    def select_provider(
        self,
        category: TaskCategory,
        preferred: Optional[AIProvider] = None
    ) -> List[AIProvider]:
        """Seleciona provedores para uma categoria"""
        
        if preferred and self.provider_status.get(preferred, False):
            providers = [preferred]
        else:
            providers = []
        
        # Adicionar provedores recomendados para a categoria
        recommended = self.CATEGORY_PROVIDERS.get(category, [])
        for provider in recommended:
            if provider not in providers and self.provider_status.get(provider, False):
                providers.append(provider)
        
        # Ordenar por latência (menor primeiro)
        providers.sort(key=lambda p: self.provider_latency.get(p, 999))
        
        return providers
    
    def update_provider_status(self, provider: AIProvider, is_online: bool, latency_ms: int = 0):
        """Atualiza status de um provedor"""
        self.provider_status[provider] = is_online
        if latency_ms > 0:
            # Média móvel da latência
            current = self.provider_latency.get(provider, 0)
            self.provider_latency[provider] = (current + latency_ms) / 2


class ExecutionEngine:
    """
    Motor de execução de tarefas
    """
    
    def __init__(self, hub=None):
        self.hub = hub
        self.decision_engine = DecisionEngine()
        self.executor = ThreadPoolExecutor(max_workers=5)
        
        # Configurações de API
        self.api_configs = self._load_api_configs()
        
        # Histórico de execuções
        self.execution_history: List[ExecutionTask] = []
    
    def _load_api_configs(self) -> Dict[str, Any]:
        """Carrega configurações de API do SYSTEM_CONTEXT"""
        config_path = os.path.expanduser("~/COMET/SYSTEM_CONTEXT.json")
        
        if os.path.exists(config_path):
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass
        
        # Configuração padrão
        return {
            "api_keys": {},
            "endpoints": {
                "openai": "https://api.openai.com/v1/chat/completions",
                "claude": "https://api.anthropic.com/v1/messages",
                "gemini": "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
            }
        }
    
    def create_task(
        self,
        prompt: str,
        category: TaskCategory = None,
        context: Dict[str, Any] = None,
        preferred_provider: AIProvider = None
    ) -> ExecutionTask:
        """Cria uma nova tarefa"""
        
        # Auto-categorizar se não especificado
        if category is None:
            category = self.decision_engine.categorize(prompt)
        
        # Selecionar provedores
        providers = self.decision_engine.select_provider(category, preferred_provider)
        
        task = ExecutionTask(
            id=f"task_{int(time.time()*1000)}",
            category=category,
            prompt=prompt,
            context=context or {},
            preferred_provider=providers[0] if providers else None,
            fallback_providers=providers[1:] if len(providers) > 1 else []
        )
        
        logger.info(f"[TASK] Criada: {task.id} | Categoria: {category.value} | Provedor: {task.preferred_provider}")
        
        return task
    
    def execute(self, task: ExecutionTask) -> ExecutionTask:
        """Executa uma tarefa"""
        start_time = time.time()
        
        providers_to_try = [task.preferred_provider] + task.fallback_providers
        providers_to_try = [p for p in providers_to_try if p is not None]
        
        for attempt, provider in enumerate(providers_to_try):
            try:
                logger.info(f"[EXEC] Tentativa {attempt + 1} com {provider.value}")
                
                result = self._call_provider(provider, task)
                
                task.result = result
                task.provider_used = provider
                task.success = True
                task.execution_time_ms = int((time.time() - start_time) * 1000)
                
                # Atualizar latência do provedor
                self.decision_engine.update_provider_status(
                    provider, True, task.execution_time_ms
                )
                
                logger.info(f"[EXEC] Sucesso com {provider.value} em {task.execution_time_ms}ms")
                break
                
            except Exception as e:
                logger.error(f"[EXEC] Erro com {provider.value}: {e}")
                task.error = str(e)
                
                # Marcar provedor como problemático
                self.decision_engine.update_provider_status(provider, False)
        
        # Salvar no histórico
        self.execution_history.append(task)
        
        # Registrar no Hub se disponível
        if self.hub:
            from hub_central import EventType, Priority
            self.hub.create_event(
                EventType.AI_RESPONSE,
                "execution_engine",
                {
                    "task_id": task.id,
                    "provider": task.provider_used.value if task.provider_used else None,
                    "category": task.category.value,
                    "success": task.success,
                    "execution_time_ms": task.execution_time_ms,
                    "prompt": task.prompt[:100],
                    "response": task.result[:200] if task.result else None
                },
                Priority.LOW
            )
        
        return task
    
    def _call_provider(self, provider: AIProvider, task: ExecutionTask) -> str:
        """Chama um provedor de IA específico"""
        
        if provider == AIProvider.OPENAI:
            return self._call_openai(task)
        elif provider == AIProvider.CLAUDE:
            return self._call_claude(task)
        elif provider == AIProvider.GEMINI:
            return self._call_gemini(task)
        elif provider == AIProvider.PERPLEXITY:
            return self._call_perplexity(task)
        elif provider == AIProvider.GROQ:
            return self._call_groq(task)
        elif provider == AIProvider.OLLAMA:
            return self._call_ollama(task)
        elif provider == AIProvider.MANUS:
            return self._call_manus(task)
        else:
            raise ValueError(f"Provedor não implementado: {provider}")
    
    def _call_openai(self, task: ExecutionTask) -> str:
        """Chama OpenAI API"""
        api_key = self.api_configs.get("api_keys", {}).get("openai", "")
        
        if not api_key:
            raise ValueError("OpenAI API key não configurada")
        
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": "gpt-4o-mini",
                "messages": [
                    {"role": "system", "content": "Você é um assistente inteligente."},
                    {"role": "user", "content": task.prompt}
                ],
                "max_tokens": 2000
            },
            timeout=task.timeout
        )
        
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    
    def _call_claude(self, task: ExecutionTask) -> str:
        """Chama Claude API"""
        api_key = self.api_configs.get("api_keys", {}).get("claude", "")
        
        if not api_key:
            raise ValueError("Claude API key não configurada")
        
        response = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "x-api-key": api_key,
                "Content-Type": "application/json",
                "anthropic-version": "2023-06-01"
            },
            json={
                "model": "claude-3-haiku-20240307",
                "max_tokens": 2000,
                "messages": [
                    {"role": "user", "content": task.prompt}
                ]
            },
            timeout=task.timeout
        )
        
        response.raise_for_status()
        return response.json()["content"][0]["text"]
    
    def _call_gemini(self, task: ExecutionTask) -> str:
        """Chama Gemini API"""
        api_key = self.api_configs.get("api_keys", {}).get("gemini", "")
        
        if not api_key:
            raise ValueError("Gemini API key não configurada")
        
        response = requests.post(
            f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={api_key}",
            headers={"Content-Type": "application/json"},
            json={
                "contents": [{"parts": [{"text": task.prompt}]}]
            },
            timeout=task.timeout
        )
        
        response.raise_for_status()
        return response.json()["candidates"][0]["content"]["parts"][0]["text"]
    
    def _call_perplexity(self, task: ExecutionTask) -> str:
        """Chama Perplexity API"""
        api_key = self.api_configs.get("api_keys", {}).get("perplexity", "")
        
        if not api_key:
            raise ValueError("Perplexity API key não configurada")
        
        response = requests.post(
            "https://api.perplexity.ai/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": "llama-3.1-sonar-small-128k-online",
                "messages": [
                    {"role": "user", "content": task.prompt}
                ]
            },
            timeout=task.timeout
        )
        
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    
    def _call_groq(self, task: ExecutionTask) -> str:
        """Chama Groq API"""
        api_key = self.api_configs.get("api_keys", {}).get("groq", "")
        
        if not api_key:
            raise ValueError("Groq API key não configurada")
        
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": "llama3-8b-8192",
                "messages": [
                    {"role": "user", "content": task.prompt}
                ]
            },
            timeout=task.timeout
        )
        
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    
    def _call_ollama(self, task: ExecutionTask) -> str:
        """Chama Ollama local"""
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3",
                "prompt": task.prompt,
                "stream": False
            },
            timeout=task.timeout
        )
        
        response.raise_for_status()
        return response.json()["response"]
    
    def _call_manus(self, task: ExecutionTask) -> str:
        """Chama Manus Bridge"""
        response = requests.post(
            "http://localhost:5000/ai/query",
            json={
                "prompt": task.prompt,
                "context": task.context
            },
            timeout=task.timeout
        )
        
        response.raise_for_status()
        return response.json().get("response", "")
    
    # ==================== EXECUÇÃO PARALELA ====================
    
    def execute_parallel(self, tasks: List[ExecutionTask]) -> List[ExecutionTask]:
        """Executa múltiplas tarefas em paralelo"""
        futures = {
            self.executor.submit(self.execute, task): task
            for task in tasks
        }
        
        results = []
        for future in as_completed(futures):
            task = futures[future]
            try:
                result = future.result()
                results.append(result)
            except Exception as e:
                task.error = str(e)
                task.success = False
                results.append(task)
        
        return results
    
    # ==================== ESTATÍSTICAS ====================
    
    def get_stats(self) -> Dict[str, Any]:
        """Retorna estatísticas de execução"""
        total = len(self.execution_history)
        successful = sum(1 for t in self.execution_history if t.success)
        
        provider_usage = {}
        for task in self.execution_history:
            if task.provider_used:
                provider_usage[task.provider_used.value] = provider_usage.get(task.provider_used.value, 0) + 1
        
        avg_time = 0
        if total > 0:
            avg_time = sum(t.execution_time_ms for t in self.execution_history) / total
        
        return {
            "total_tasks": total,
            "successful": successful,
            "failed": total - successful,
            "success_rate": (successful / total * 100) if total > 0 else 0,
            "average_execution_time_ms": avg_time,
            "provider_usage": provider_usage,
            "provider_status": {p.value: s for p, s in self.decision_engine.provider_status.items()}
        }


# ==================== FUNÇÕES DE CONVENIÊNCIA ====================

engine = ExecutionEngine()

def ask_ai(prompt: str, category: str = None, provider: str = None) -> str:
    """
    Função simples para fazer perguntas à IA
    
    Args:
        prompt: A pergunta ou comando
        category: Categoria opcional (code, research, creative, etc)
        provider: Provedor preferido opcional (openai, claude, gemini, etc)
    
    Returns:
        Resposta da IA
    """
    task_category = TaskCategory(category) if category else None
    preferred = AIProvider(provider) if provider else None
    
    task = engine.create_task(prompt, task_category, preferred_provider=preferred)
    result = engine.execute(task)
    
    if result.success:
        return result.result
    else:
        raise Exception(f"Erro na execução: {result.error}")


def ask_multiple(prompts: List[str]) -> List[str]:
    """Executa múltiplas perguntas em paralelo"""
    tasks = [engine.create_task(p) for p in prompts]
    results = engine.execute_parallel(tasks)
    return [r.result if r.success else f"Erro: {r.error}" for r in results]


# ==================== TESTE ====================

if __name__ == "__main__":
    print("=" * 50)
    print("  MOTOR DE EXECUÇÃO - Teste")
    print("=" * 50)
    
    # Testar categorização
    test_prompts = [
        "Escreva um código Python para ordenar uma lista",
        "Pesquise sobre inteligência artificial",
        "Escreva uma história sobre um robô",
        "Analise os dados de vendas",
        "Olá, como você está?",
        "Automatize o envio de emails",
        "Resuma este artigo",
        "Traduza para inglês: Bom dia"
    ]
    
    print("\nCategorização automática:")
    for prompt in test_prompts:
        category = engine.decision_engine.categorize(prompt)
        providers = engine.decision_engine.select_provider(category)
        print(f"  '{prompt[:40]}...' -> {category.value} ({providers[0].value if providers else 'N/A'})")
    
    print("\nEstatísticas:")
    print(json.dumps(engine.get_stats(), indent=2))

