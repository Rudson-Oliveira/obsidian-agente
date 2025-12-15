"""
Módulo de Integração com IA Externa para Obsidian Agente
Suporta: OpenAI/GPT, Claude, Gemini, Manus
"""

import os
import json
import requests
from typing import Optional, Dict, Any

class AIIntegration:
    """Gerencia conexões com diferentes provedores de IA"""
    
    def __init__(self):
        self.providers = {
            'openai': {
                'name': 'OpenAI/GPT',
                'base_url': 'https://api.openai.com/v1',
                'model': 'gpt-4o-mini',
                'api_key': None,
                'enabled': False
            },
            'claude': {
                'name': 'Claude (Anthropic)',
                'base_url': 'https://api.anthropic.com/v1',
                'model': 'claude-3-haiku-20240307',
                'api_key': None,
                'enabled': False
            },
            'gemini': {
                'name': 'Google Gemini',
                'base_url': 'https://generativelanguage.googleapis.com/v1beta',
                'model': 'gemini-1.5-flash',
                'api_key': None,
                'enabled': False
            },
            'manus': {
                'name': 'Manus Bridge',
                'base_url': None,  # URL do ngrok
                'api_key': None,
                'enabled': False
            }
        }
        self.active_provider = None
        self.config_path = os.path.join(os.path.dirname(__file__), 'ai_config.json')
        self.load_config()
    
    def load_config(self):
        """Carrega configuração salva"""
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r') as f:
                    config = json.load(f)
                    for provider, settings in config.get('providers', {}).items():
                        if provider in self.providers:
                            self.providers[provider].update(settings)
                    self.active_provider = config.get('active_provider')
        except Exception as e:
            print(f"Erro ao carregar config: {e}")
    
    def save_config(self):
        """Salva configuração"""
        try:
            config = {
                'providers': self.providers,
                'active_provider': self.active_provider
            }
            with open(self.config_path, 'w') as f:
                json.dump(config, f, indent=2)
        except Exception as e:
            print(f"Erro ao salvar config: {e}")
    
    def configure_provider(self, provider: str, api_key: str, base_url: Optional[str] = None, model: Optional[str] = None):
        """Configura um provedor de IA"""
        if provider not in self.providers:
            return {'success': False, 'error': f'Provedor {provider} não suportado'}
        
        self.providers[provider]['api_key'] = api_key
        self.providers[provider]['enabled'] = True
        
        if base_url:
            self.providers[provider]['base_url'] = base_url
        if model:
            self.providers[provider]['model'] = model
        
        self.save_config()
        return {'success': True, 'message': f'{provider} configurado com sucesso'}
    
    def set_active_provider(self, provider: str):
        """Define o provedor ativo"""
        if provider not in self.providers:
            return {'success': False, 'error': f'Provedor {provider} não suportado'}
        
        if not self.providers[provider]['enabled']:
            return {'success': False, 'error': f'Provedor {provider} não está configurado'}
        
        self.active_provider = provider
        self.save_config()
        return {'success': True, 'message': f'{provider} definido como provedor ativo'}
    
    def get_status(self):
        """Retorna status de todos os provedores"""
        status = {
            'active_provider': self.active_provider,
            'providers': {}
        }
        for name, config in self.providers.items():
            status['providers'][name] = {
                'name': config['name'],
                'enabled': config['enabled'],
                'model': config.get('model'),
                'has_api_key': bool(config.get('api_key'))
            }
        return status
    
    def chat(self, message: str, context: Optional[str] = None, system_prompt: Optional[str] = None) -> Dict[str, Any]:
        """Envia mensagem para o provedor de IA ativo"""
        if not self.active_provider:
            return {'success': False, 'error': 'Nenhum provedor de IA configurado'}
        
        provider = self.providers[self.active_provider]
        
        if not provider['enabled'] or not provider['api_key']:
            return {'success': False, 'error': f'Provedor {self.active_provider} não está configurado corretamente'}
        
        # System prompt padrão para o Obsidian Agente
        default_system = """Você é o Obsidian Agente Inteligente v2.0, um assistente especializado em:
- Gerenciamento de notas e conhecimento no Obsidian
- Organização de informações e produtividade
- Criação de conteúdo estruturado em Markdown
- Automação de tarefas no ambiente do usuário

Responda de forma clara, útil e proativa. Use emojis quando apropriado para tornar a comunicação mais amigável.
Se o contexto incluir informações sobre notas ou arquivos do usuário, use-as para dar respostas mais personalizadas."""

        final_system = system_prompt or default_system
        if context:
            final_system += f"\n\nContexto atual:\n{context}"
        
        try:
            if self.active_provider == 'openai':
                return self._chat_openai(message, final_system, provider)
            elif self.active_provider == 'claude':
                return self._chat_claude(message, final_system, provider)
            elif self.active_provider == 'gemini':
                return self._chat_gemini(message, final_system, provider)
            elif self.active_provider == 'manus':
                return self._chat_manus(message, final_system, provider)
            else:
                return {'success': False, 'error': 'Provedor não implementado'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def _chat_openai(self, message: str, system: str, provider: dict) -> Dict[str, Any]:
        """Chat com OpenAI/GPT"""
        headers = {
            'Authorization': f'Bearer {provider["api_key"]}',
            'Content-Type': 'application/json'
        }
        
        data = {
            'model': provider['model'],
            'messages': [
                {'role': 'system', 'content': system},
                {'role': 'user', 'content': message}
            ],
            'temperature': 0.7,
            'max_tokens': 2000
        }
        
        response = requests.post(
            f'{provider["base_url"]}/chat/completions',
            headers=headers,
            json=data,
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            return {
                'success': True,
                'response': result['choices'][0]['message']['content'],
                'provider': 'openai',
                'model': provider['model']
            }
        else:
            return {'success': False, 'error': f'OpenAI error: {response.text}'}
    
    def _chat_claude(self, message: str, system: str, provider: dict) -> Dict[str, Any]:
        """Chat com Claude"""
        headers = {
            'x-api-key': provider['api_key'],
            'Content-Type': 'application/json',
            'anthropic-version': '2023-06-01'
        }
        
        data = {
            'model': provider['model'],
            'system': system,
            'messages': [
                {'role': 'user', 'content': message}
            ],
            'max_tokens': 2000
        }
        
        response = requests.post(
            f'{provider["base_url"]}/messages',
            headers=headers,
            json=data,
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            return {
                'success': True,
                'response': result['content'][0]['text'],
                'provider': 'claude',
                'model': provider['model']
            }
        else:
            return {'success': False, 'error': f'Claude error: {response.text}'}
    
    def _chat_gemini(self, message: str, system: str, provider: dict) -> Dict[str, Any]:
        """Chat com Google Gemini"""
        url = f'{provider["base_url"]}/models/{provider["model"]}:generateContent?key={provider["api_key"]}'
        
        data = {
            'contents': [
                {
                    'parts': [
                        {'text': f'{system}\n\nUsuário: {message}'}
                    ]
                }
            ],
            'generationConfig': {
                'temperature': 0.7,
                'maxOutputTokens': 2000
            }
        }
        
        response = requests.post(url, json=data, timeout=60)
        
        if response.status_code == 200:
            result = response.json()
            return {
                'success': True,
                'response': result['candidates'][0]['content']['parts'][0]['text'],
                'provider': 'gemini',
                'model': provider['model']
            }
        else:
            return {'success': False, 'error': f'Gemini error: {response.text}'}
    
    def _chat_manus(self, message: str, system: str, provider: dict) -> Dict[str, Any]:
        """Chat via Manus Bridge (COMET)"""
        if not provider.get('base_url'):
            return {'success': False, 'error': 'URL do Manus Bridge não configurada'}
        
        # Envia comando para o Manus via COMET Bridge
        data = {
            'command': f'echo "MANUS_REQUEST: {message}"'
        }
        
        response = requests.post(
            f'{provider["base_url"]}/exec',
            json=data,
            timeout=60
        )
        
        if response.status_code == 200:
            return {
                'success': True,
                'response': f'Comando enviado ao Manus: {message}',
                'provider': 'manus',
                'note': 'Integração bidirecional com Manus ativa'
            }
        else:
            return {'success': False, 'error': f'Manus Bridge error: {response.text}'}


# Instância global
ai_integration = AIIntegration()


# Funções de conveniência para uso no agente
def configure_ai(provider: str, api_key: str, **kwargs):
    """Configura um provedor de IA"""
    return ai_integration.configure_provider(provider, api_key, **kwargs)

def set_ai_provider(provider: str):
    """Define o provedor de IA ativo"""
    return ai_integration.set_active_provider(provider)

def get_ai_status():
    """Retorna status dos provedores de IA"""
    return ai_integration.get_status()

def chat_with_ai(message: str, context: str = None):
    """Envia mensagem para a IA"""
    return ai_integration.chat(message, context)

