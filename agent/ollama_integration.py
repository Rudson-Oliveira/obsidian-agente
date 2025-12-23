#!/usr/bin/env python3
"""
Ollama Integration Module v2.0
Modulo de integracao com Ollama (IA Local) para o Obsidian Agente
"""
import os
import json
import requests
from typing import Dict, Any, Optional, List
from datetime import datetime

class OllamaIntegration:
    VERSION = "2.0.0"
    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url
        self.default_model = "gemma3:4b"
        self.available_models = []
        self.is_available = False
        self._check_availability()
    def _check_availability(self) -> bool:
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            if response.status_code == 200:
                data = response.json()
                self.available_models = [m.get("name", "") for m in data.get("models", [])]
                self.is_available = True
                if self.available_models:
                    self.default_model = self.available_models[0]
                return True
        except:
            self.is_available = False
        return False
    def generate(self, prompt: str, model: str = None) -> Dict[str, Any]:
        if not self.is_available:
            self._check_availability()
            if not self.is_available:
                return {"success": False, "error": "Ollama nao disponivel"}
        model = model or self.default_model
        try:
            response = requests.post(f"{self.base_url}/api/generate", json={"model": model, "prompt": prompt, "stream": False}, timeout=120)
            if response.status_code == 200:
                data = response.json()
                return {"success": True, "response": data.get("response", ""), "model": model, "provider": "ollama"}
            return {"success": False, "error": f"Erro HTTP {response.status_code}"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    def get_status(self) -> Dict[str, Any]:
        self._check_availability()
        return {"available": self.is_available, "models": self.available_models, "default": self.default_model, "version": self.VERSION}

class AIRouter:
    MANUS_KEYWORDS = ["browser", "navegador", "pesquisar", "pesquise", "internet", "site", "web", "desktop", "arquivo", "instalar", "instale", "executar", "execute", "abrir", "abra", "api", "docker", "git", "baixar", "baixe", "download", "email", "enviar", "envie", "obsidian", "nota", "vault", "criar nota", "crie nota", "sistema", "windows", "powershell", "terminal", "cmd", "imagem", "foto", "screenshot", "captura", "pdf", "documento", "word", "excel", "n8n", "automacao", "workflow", "mcp", "servidor", "deploy"]
    LOCAL_KEYWORDS = ["explique", "explica", "explicar", "o que e", "o que sao", "qual e", "quais sao", "defina", "definir", "definicao", "resuma", "resumir", "resumo", "traduza", "traduzir", "traducao", "calcule", "calcular", "calculo", "liste", "listar", "lista", "como funciona", "como fazer", "diferenca", "diferente", "comparar", "compare", "escreva", "escrever", "redija", "codigo", "funcao", "script", "programa", "simples", "basico", "rapido", "historia", "significado", "conceito"]
    def __init__(self, ollama: OllamaIntegration = None):
        self.ollama = ollama or OllamaIntegration()
    def route(self, message: str) -> Dict[str, Any]:
        msg_lower = message.lower().strip()
        if msg_lower.startswith("manus:"):
            return {"provider": "manus", "message": message[6:].strip(), "reason": "explicit_prefix"}
        if msg_lower.startswith("llama:"):
            return {"provider": "ollama", "message": message[6:].strip(), "reason": "explicit_prefix"}
        if msg_lower.startswith("ollama:"):
            return {"provider": "ollama", "message": message[7:].strip(), "reason": "explicit_prefix"}
        if msg_lower.startswith("local:"):
            return {"provider": "ollama", "message": message[6:].strip(), "reason": "explicit_prefix"}
        manus_score = sum(1 for kw in self.MANUS_KEYWORDS if kw in msg_lower)
        local_score = sum(1 for kw in self.LOCAL_KEYWORDS if kw in msg_lower)
        if manus_score > local_score:
            return {"provider": "manus", "message": message, "reason": "auto_manus_keywords", "scores": {"manus": manus_score, "local": local_score}}
        if self.ollama.is_available and local_score >= manus_score:
            return {"provider": "ollama", "message": message, "reason": "auto_local_keywords", "scores": {"manus": manus_score, "local": local_score}}
        return {"provider": "manus", "message": message, "reason": "fallback_manus"}
    def process(self, message: str) -> Dict[str, Any]:
        routing = self.route(message)
        if routing["provider"] == "ollama":
            result = self.ollama.generate(routing["message"])
            result["routing"] = routing
            return result
        return {"success": True, "provider": "manus", "message": routing["message"], "routing": routing, "requires_manus": True}
    def get_stats(self) -> Dict[str, Any]:
        return {"ollama_available": self.ollama.is_available, "ollama_models": self.ollama.available_models, "manus_keywords_count": len(self.MANUS_KEYWORDS), "local_keywords_count": len(self.LOCAL_KEYWORDS)}

def get_ai_router() -> AIRouter:
    return AIRouter()

if __name__ == "__main__":
    print("=== Teste de Integracao Ollama v2.0 ===")
    router = get_ai_router()
    print(f"Ollama disponivel: {router.ollama.is_available}")
    print(f"Modelos: {router.ollama.available_models}")
