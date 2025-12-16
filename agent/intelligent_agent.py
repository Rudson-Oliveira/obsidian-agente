#!/usr/bin/env python3
"""
Intelligent Agent v2.0 - Sistema de IA com Fallback Multi-Provedor
Corrigido para usar OpenAI, Claude e Gemini com fallback automático
"""
import re
import json
import os
import requests
from pathlib import Path
from obsidian_knowledge import get_knowledge, search_knowledge

CONTEXT_FILE = Path.home() / "COMET" / "SYSTEM_CONTEXT.json"

def load_system_context():
    """Carrega o contexto do sistema do arquivo JSON"""
    if CONTEXT_FILE.exists():
        with open(CONTEXT_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


class AIProvider:
    """Provedor de IA com fallback automático entre OpenAI, Claude e Gemini"""
    
    def __init__(self, context):
        self.context = context
        self.apis = context.get("apis", {})
        self.last_provider = None
        self.last_error = None
    
    def call_openai(self, prompt):
        """Chama a API da OpenAI"""
        api_key = self.apis.get("openai", {}).get("key")
        if not api_key:
            return None, "Chave OpenAI não configurada"
        
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
                return content, None
            else:
                return None, f"OpenAI erro {r.status_code}: {r.text[:200]}"
        except Exception as e:
            return None, f"OpenAI exceção: {str(e)}"
    
    def call_claude(self, prompt):
        """Chama a API do Claude (Anthropic)"""
        api_key = self.apis.get("claude", {}).get("key")
        if not api_key:
            return None, "Chave Claude não configurada"
        
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
                return content, None
            else:
                return None, f"Claude erro {r.status_code}: {r.text[:200]}"
        except Exception as e:
            return None, f"Claude exceção: {str(e)}"
    
    def call_gemini(self, prompt):
        """Chama a API do Google Gemini"""
        # Tenta a primeira chave
        api_key = self.apis.get("gemini", {}).get("key")
        if not api_key:
            api_key = self.apis.get("gemini", {}).get("key2")
        
        if not api_key:
            return None, "Chave Gemini não configurada"
        
        # Tenta diferentes modelos do Gemini
        models = ["gemini-1.5-flash-latest", "gemini-1.5-pro-latest", "gemini-pro"]
        
        for model in models:
            try:
                url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
                r = requests.post(
                    url,
                    json={
                        "contents": [{"parts": [{"text": prompt}]}],
                        "generationConfig": {
                            "temperature": 0.7,
                            "maxOutputTokens": 1000
                        }
                    },
                    timeout=30
                )
                if r.status_code == 200:
                    result = r.json()
                    content = result.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "")
                    self.last_provider = f"Gemini ({model})"
                    return content, None
            except Exception as e:
                continue
        
        return None, "Gemini: Todos os modelos falharam"
    
    def call_perplexity(self, prompt):
        """Chama a API do Perplexity"""
        api_key = self.apis.get("perplexity", {}).get("key")
        if not api_key:
            return None, "Chave Perplexity não configurada"
        
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
                return content, None
            else:
                return None, f"Perplexity erro {r.status_code}: {r.text[:200]}"
        except Exception as e:
            return None, f"Perplexity exceção: {str(e)}"
    
    def get_response(self, prompt, provider="auto"):
        """
        Obtém resposta da IA com fallback automático.
        Ordem de prioridade: OpenAI → Claude → Perplexity → Gemini
        """
        errors = []
        
        # Ordem de fallback
        providers = [
            ("openai", self.call_openai),
            ("claude", self.call_claude),
            ("perplexity", self.call_perplexity),
            ("gemini", self.call_gemini)
        ]
        
        # Se um provedor específico foi solicitado, tenta ele primeiro
        if provider != "auto":
            for name, func in providers:
                if name == provider.lower():
                    result, error = func(prompt)
                    if result:
                        return result
                    errors.append(f"{name}: {error}")
                    break
        
        # Tenta todos os provedores em ordem
        for name, func in providers:
            result, error = func(prompt)
            if result:
                return result
            if error:
                errors.append(f"{name}: {error}")
        
        # Se todos falharam, retorna mensagem de erro
        self.last_error = "; ".join(errors)
        return f"Erro ao processar. Nenhum provedor de IA disponível. Detalhes: {self.last_error}"
    
    def get_status(self):
        """Retorna o status dos provedores de IA"""
        status = {
            "openai": bool(self.apis.get("openai", {}).get("key")),
            "claude": bool(self.apis.get("claude", {}).get("key")),
            "gemini": bool(self.apis.get("gemini", {}).get("key")),
            "perplexity": bool(self.apis.get("perplexity", {}).get("key")),
            "last_provider": self.last_provider,
            "last_error": self.last_error
        }
        return status


class IntelligentAgent:
    """Agente inteligente para processamento de comandos e integração com IA"""
    
    def __init__(self):
        self.context = load_system_context()
        self.knowledge = get_knowledge()
        self.ai_provider = AIProvider(self.context)
        self.paths = self.context.get("paths", {})
        self.command_patterns = self._build_command_patterns()
    
    def _build_command_patterns(self):
        """Constrói os padrões de reconhecimento de comandos"""
        return {
            "open_obsidian": [r"abr.*obsidian", r"open.*obsidian"],
            "list_notes": [r"list.*nota", r"mostrar.*nota", r"listar.*nota"],
            "create_note": [r"cri.*nota", r"nova.*nota", r"criar.*nota"],
            "search_notes": [r"busc.*nota", r"procur.*nota", r"pesquis.*nota"],
            "help": [r"ajuda", r"help", r"comandos"],
            "status": [r"status", r"estado", r"verificar"],
            "ai_status": [r"status.*ia", r"status.*ai", r"provedores"],
            "ask_ai": [r"perguntar", r"pesquisar", r"me diga", r"me fale", r"o que", r"como", r"qual", r"quem", r"quando", r"onde", r"por que"]
        }
    
    def get_system_status(self):
        """Retorna o status do sistema"""
        status = "=== STATUS DO SISTEMA ===\n\n"
        
        # Status dos caminhos
        status += "📁 CAMINHOS:\n"
        for name, path in self.paths.items():
            exists = Path(path).exists() if path else False
            icon = "✅" if exists else "❌"
            status += f"  {icon} {name}: {path}\n"
        
        # Status das APIs
        status += "\n🤖 PROVEDORES DE IA:\n"
        ai_status = self.ai_provider.get_status()
        for provider in ["openai", "claude", "gemini", "perplexity"]:
            icon = "✅" if ai_status.get(provider) else "❌"
            status += f"  {icon} {provider.upper()}\n"
        
        if ai_status.get("last_provider"):
            status += f"\n📌 Último provedor usado: {ai_status['last_provider']}\n"
        
        return status
    
    def get_ai_status(self):
        """Retorna o status detalhado dos provedores de IA"""
        ai_status = self.ai_provider.get_status()
        
        status = "=== STATUS DOS PROVEDORES DE IA ===\n\n"
        
        providers_info = {
            "openai": ("OpenAI", "gpt-3.5-turbo"),
            "claude": ("Claude", "claude-3-haiku"),
            "gemini": ("Google Gemini", "gemini-1.5-flash"),
            "perplexity": ("Perplexity", "llama-3.1-sonar")
        }
        
        for key, (name, model) in providers_info.items():
            configured = ai_status.get(key, False)
            icon = "✅" if configured else "❌"
            status_text = "Configurado" if configured else "Não configurado"
            status += f"{icon} {name}\n"
            status += f"   Modelo: {model}\n"
            status += f"   Status: {status_text}\n\n"
        
        if ai_status.get("last_provider"):
            status += f"📌 Último provedor usado: {ai_status['last_provider']}\n"
        
        if ai_status.get("last_error"):
            status += f"⚠️ Último erro: {ai_status['last_error']}\n"
        
        return status
    
    def process_command(self, text):
        """Processa o texto e identifica o comando"""
        text_lower = text.lower()
        detected = None
        
        for cmd, patterns in self.command_patterns.items():
            for p in patterns:
                if re.search(p, text_lower):
                    detected = cmd
                    break
            if detected:
                break
        
        # Se não detectou nenhum comando específico, assume que é uma pergunta para a IA
        if not detected:
            detected = "ask_ai"
        
        return {
            "command": detected,
            "parameters": {"query": text},
            "original_text": text
        }
    
    def get_help_message(self):
        """Retorna a mensagem de ajuda"""
        return """=== AJUDA - COMANDOS DISPONÍVEIS ===

📝 NOTAS:
  • criar nota [título] - Cria uma nova nota
  • listar notas - Lista todas as notas
  • buscar [termo] - Busca nas notas

📊 STATUS:
  • status - Status geral do sistema
  • status ia - Status dos provedores de IA

🤖 IA:
  • Qualquer pergunta será processada pela IA
  • Sistema de fallback: OpenAI → Claude → Perplexity → Gemini

❓ AJUDA:
  • ajuda - Mostra esta mensagem
"""
    
    def generate_response(self, command_result, api_result):
        """Gera a resposta baseada no comando e resultado da API"""
        cmd = command_result["command"]
        
        if cmd == "help":
            return self.get_help_message()
        
        if cmd == "status":
            return self.get_system_status()
        
        if cmd == "ai_status":
            return self.get_ai_status()
        
        if cmd == "ask_ai":
            query = command_result["parameters"].get("query", "")
            system_prompt = "Você é um assistente inteligente integrado ao Obsidian. Responda em português brasileiro de forma clara, concisa e útil."
            full_prompt = f"{system_prompt}\n\nPergunta do usuário: {query}"
            
            response = self.ai_provider.get_response(full_prompt)
            
            # Adiciona informação sobre qual provedor foi usado
            if self.ai_provider.last_provider:
                response += f"\n\n[Respondido via {self.ai_provider.last_provider}]"
            
            return response
        
        if api_result.get("success"):
            return f"✅ Comando '{cmd}' executado com sucesso!"
        
        error = api_result.get("error", "desconhecido")
        return f"❌ Erro ao executar '{cmd}': {error}"


# Instância global para uso no agent.py
intelligent_agent = IntelligentAgent()


def process_text(text):
    """Função de conveniência para processar texto"""
    command_result = intelligent_agent.process_command(text)
    api_result = {"success": True}  # Placeholder
    return intelligent_agent.generate_response(command_result, api_result)


def get_ai_response(prompt, provider="auto"):
    """Função de conveniência para obter resposta da IA"""
    return intelligent_agent.ai_provider.get_response(prompt, provider)


def get_status():
    """Função de conveniência para obter status"""
    return intelligent_agent.get_system_status()
