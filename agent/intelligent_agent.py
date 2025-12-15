#!/usr/bin/env python3
import re
import json
import os
import requests
from pathlib import Path
from obsidian_knowledge import get_knowledge, search_knowledge

CONTEXT_FILE = Path.home() / "COMET" / "SYSTEM_CONTEXT.json"

def load_system_context():
    if CONTEXT_FILE.exists():
        with open(CONTEXT_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

class AIProvider:
    def __init__(self, context):
        self.context = context
        self.apis = context.get("apis", {})
    
    def call_gemini(self, prompt):
        api_key = self.apis.get("gemini", {}).get("key")
        if not api_key: return None
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={api_key}"
            r = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}]}, timeout=30)
            if r.status_code == 200:
                return r.json().get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "")
        except: pass
        return None
    
    def get_response(self, prompt, provider="auto"):
        if provider == "auto":
            r = self.call_gemini(prompt)
            if r: return r
            return "Erro ao processar. Verifique as APIs."
        return "Provedor nao reconhecido"

class IntelligentAgent:
    def __init__(self):
        self.context = load_system_context()
        self.knowledge = get_knowledge()
        self.ai_provider = AIProvider(self.context)
        self.paths = self.context.get("paths", {})
        self.command_patterns = self._build_command_patterns()
    
    def _build_command_patterns(self):
        return {
            "open_obsidian": [r"abr.*obsidian", r"open.*obsidian"],
            "list_notes": [r"list.*nota", r"mostrar.*nota"],
            "create_note": [r"cri.*nota", r"nova.*nota"],
            "search_notes": [r"busc.*nota", r"procur.*nota"],
            "help": [r"ajuda", r"help", r"comandos"],
            "status": [r"status", r"estado"],
            "ask_ai": [r"perguntar", r"pesquisar", r"me diga", r"me fale"]
        }
    
    def get_system_status(self):
        status = "STATUS DO SISTEMA\n\n"
        for name, path in self.paths.items():
            exists = Path(path).exists() if path else False
            icon = "OK" if exists else "ERRO"
            status += f"{icon} {name}: {path}\n"
        return status
    
    def process_command(self, text):
        text_lower = text.lower()
        detected = None
        for cmd, patterns in self.command_patterns.items():
            for p in patterns:
                if re.search(p, text_lower):
                    detected = cmd
                    break
            if detected: break
        if not detected:
            detected = "ask_ai"
        return {"command": detected, "parameters": {"query": text}, "original_text": text}
    
    def get_help_message(self):
        return "AJUDA - Comandos: criar nota, listar notas, buscar, status, ajuda. Perguntas sao processadas pela IA."
    
    def generate_response(self, command_result, api_result):
        cmd = command_result["command"]
        if cmd == "help": return self.get_help_message()
        if cmd == "status": return self.get_system_status()
        if cmd == "ask_ai":
            query = command_result["parameters"].get("query", "")
            return self.ai_provider.get_response(f"Responda em portugues: {query}")
        if api_result.get("success"):
            return f"Comando {cmd} executado com sucesso!"
        return f"Erro: {api_result.get("error", "desconhecido")}"
