"""
CHAT IA INTEGRATION - Sistema Hospitalar
Integração do Chat existente com base de conhecimento e IA local

Autor: Manus AI
Data: 05/01/2026
Versão: 1.0
"""

import requests
import json
from typing import Optional, Dict, Any

# Configurações
OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_DOCKER_URL = "http://localhost:11435/api/generate"  # Via Docker
SYSTEM_API_URL = "https://dev.hospitalarsaude.app.br/api"

# Contexto base para o Chat IA
SYSTEM_CONTEXT = """
Você é o Assistente Virtual da Hospitalar Soluções em Saúde.
Seu objetivo é ajudar colaboradores com:

1. ORÇAMENTOS:
   - Consultar status de orçamentos
   - Verificar pendências de retificação
   - Calcular valores e procedimentos

2. PACIENTES:
   - Buscar informações de pacientes
   - Verificar histórico de atendimentos
   - Consultar convênios

3. PROCEDIMENTOS:
   - Listar procedimentos disponíveis
   - Verificar preços e tabelas
   - Consultar cobertura de convênios

4. ADMINISTRATIVO:
   - Ajudar com dúvidas do sistema
   - Orientar sobre processos internos
   - Reportar problemas técnicos

Sempre responda em português de forma clara e profissional.
Se não souber a resposta, indique que vai verificar com a equipe.
"""


class ChatIAIntegration:
    """Classe para integração do Chat IA com o sistema hospitalar"""
    
    def __init__(self, use_docker: bool = True):
        self.ollama_url = OLLAMA_DOCKER_URL if use_docker else OLLAMA_URL
        self.model = "llama3.2"
        self.context = SYSTEM_CONTEXT
        self.conversation_history = []
    
    def query_ollama(self, prompt: str, context: Optional[str] = None) -> str:
        """Envia query para Ollama e retorna resposta"""
        full_prompt = f"{self.context}\n\n{context or ''}\n\nUsuário: {prompt}\n\nAssistente:"
        
        try:
            response = requests.post(
                self.ollama_url,
                json={
                    "model": self.model,
                    "prompt": full_prompt,
                    "stream": False
                },
                timeout=60
            )
            
            if response.status_code == 200:
                return response.json().get("response", "Desculpe, não consegui processar sua solicitação.")
            else:
                return f"Erro ao conectar com IA: {response.status_code}"
                
        except requests.exceptions.ConnectionError:
            return "IA local não disponível. Verifique se o Ollama está rodando."
        except Exception as e:
            return f"Erro: {str(e)}"
    
    def get_orcamento_context(self, codigo: str) -> str:
        """Busca contexto de um orçamento específico"""
        # Aqui seria integrado com a API do sistema
        # Por enquanto retorna contexto simulado
        return f"""
        Contexto do Orçamento {codigo}:
        - Status: Pendente de retificação
        - Paciente: [Nome do Paciente]
        - Valor: R$ [Valor]
        - Procedimentos: [Lista de procedimentos]
        """
    
    def process_message(self, user_message: str, user_id: Optional[str] = None) -> Dict[str, Any]:
        """Processa mensagem do usuário e retorna resposta estruturada"""
        
        # Detectar intenção
        intent = self._detect_intent(user_message)
        
        # Buscar contexto adicional se necessário
        context = ""
        if "orçamento" in user_message.lower() or "orcamento" in user_message.lower():
            # Extrair código se mencionado
            import re
            match = re.search(r'\d{5,6}', user_message)
            if match:
                context = self.get_orcamento_context(match.group())
        
        # Gerar resposta
        response = self.query_ollama(user_message, context)
        
        # Salvar no histórico
        self.conversation_history.append({
            "user": user_message,
            "assistant": response,
            "intent": intent,
            "user_id": user_id
        })
        
        return {
            "success": True,
            "response": response,
            "intent": intent,
            "suggestions": self._get_suggestions(intent)
        }
    
    def _detect_intent(self, message: str) -> str:
        """Detecta a intenção da mensagem"""
        message_lower = message.lower()
        
        if any(word in message_lower for word in ["orçamento", "orcamento", "valor", "preço"]):
            return "orcamento"
        elif any(word in message_lower for word in ["paciente", "cliente", "nome"]):
            return "paciente"
        elif any(word in message_lower for word in ["procedimento", "exame", "consulta"]):
            return "procedimento"
        elif any(word in message_lower for word in ["ajuda", "como", "dúvida"]):
            return "ajuda"
        else:
            return "geral"
    
    def _get_suggestions(self, intent: str) -> list:
        """Retorna sugestões baseadas na intenção"""
        suggestions = {
            "orcamento": [
                "Ver orçamentos pendentes",
                "Criar novo orçamento",
                "Consultar status"
            ],
            "paciente": [
                "Buscar paciente",
                "Ver histórico",
                "Atualizar cadastro"
            ],
            "procedimento": [
                "Lista de procedimentos",
                "Tabela de preços",
                "Cobertura de convênios"
            ],
            "ajuda": [
                "Manual do sistema",
                "Contato suporte",
                "FAQ"
            ],
            "geral": [
                "Orçamentos",
                "Pacientes",
                "Procedimentos"
            ]
        }
        return suggestions.get(intent, suggestions["geral"])


# API Endpoint para integração com o frontend
def create_chat_endpoint():
    """Cria endpoint Flask para o Chat IA"""
    from flask import Flask, request, jsonify
    from flask_cors import CORS
    
    app = Flask(__name__)
    CORS(app)
    
    chat = ChatIAIntegration()
    
    @app.route('/api/chat', methods=['POST'])
    def chat_endpoint():
        data = request.json
        user_message = data.get('message', '')
        user_id = data.get('user_id')
        
        if not user_message:
            return jsonify({"success": False, "error": "Mensagem vazia"})
        
        result = chat.process_message(user_message, user_id)
        return jsonify(result)
    
    @app.route('/api/chat/health', methods=['GET'])
    def health():
        return jsonify({"status": "online", "service": "Chat IA Integration"})
    
    return app


if __name__ == "__main__":
    # Teste local
    chat = ChatIAIntegration(use_docker=False)
    
    print("=== Chat IA Integration - Teste ===")
    print("Digite 'sair' para encerrar\n")
    
    while True:
        user_input = input("Você: ")
        if user_input.lower() == 'sair':
            break
        
        result = chat.process_message(user_input)
        print(f"\nAssistente: {result['response']}")
        print(f"Intenção: {result['intent']}")
        print(f"Sugestões: {result['suggestions']}\n")
