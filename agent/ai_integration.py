#!/usr/bin/env python3
"""
AI Integration Module v5.0
Módulo de integração com múltiplas IAs para o Obsidian Agente
Suporta: GPT, Claude, Gemini, Grok, Manus, Genspark, Abacus
"""

import os
import json
import requests
from typing import Dict, Any, Optional, List


class AIIntegration:
    """Classe para integração com múltiplas IAs"""
    
    VERSION = "5.0.0"
    
    def __init__(self):
        self.providers = {
            'openai': {
                'name': 'OpenAI GPT',
                'enabled': False,
                'api_key': None,
                'base_url': 'https://api.openai.com/v1',
                'model': 'gpt-4o-mini',
                'models_available': ['gpt-4o', 'gpt-4o-mini', 'gpt-4-turbo', 'gpt-3.5-turbo']
            },
            'claude': {
                'name': 'Anthropic Claude',
                'enabled': False,
                'api_key': None,
                'base_url': 'https://api.anthropic.com/v1',
                'model': 'claude-3-5-sonnet-20241022',
                'models_available': ['claude-3-5-sonnet-20241022', 'claude-3-opus-20240229', 'claude-3-haiku-20240307']
            },
            'gemini': {
                'name': 'Google Gemini',
                'enabled': False,
                'api_key': None,
                'base_url': 'https://generativelanguage.googleapis.com/v1beta',
                'model': 'gemini-2.0-flash-exp',
                'models_available': ['gemini-2.0-flash-exp', 'gemini-1.5-pro', 'gemini-1.5-flash']
            },
            'grok': {
                'name': 'xAI Grok',
                'enabled': False,
                'api_key': None,
                'base_url': 'https://api.x.ai/v1',
                'model': 'grok-beta',
                'models_available': ['grok-beta', 'grok-2-1212']
            },
            'manus': {
                'name': 'Manus AI',
                'enabled': False,
                'api_key': None,
                'base_url': None,  # URL do ngrok bridge
                'model': 'manus-1.6-max',
                'models_available': ['manus-1.6-max']
            },
            'genspark': {
                'name': 'Genspark AI',
                'enabled': False,
                'api_key': None,
                'base_url': 'https://api.genspark.ai/v1',
                'model': 'genspark-default',
                'models_available': ['genspark-default']
            },
            'abacus': {
                'name': 'Abacus AI',
                'enabled': False,
                'api_key': None,
                'base_url': 'https://api.abacus.ai/v1',
                'model': 'abacus-default',
                'models_available': ['abacus-default', 'abacus-pro']
            },
            'deepseek': {
                'name': 'DeepSeek AI',
                'enabled': False,
                'api_key': None,
                'base_url': 'https://api.deepseek.com/v1',
                'model': 'deepseek-chat',
                'models_available': ['deepseek-chat', 'deepseek-coder']
            },
            'groq': {
                'name': 'Groq',
                'enabled': False,
                'api_key': None,
                'base_url': 'https://api.groq.com/openai/v1',
                'model': 'llama-3.3-70b-versatile',
                'models_available': ['llama-3.3-70b-versatile', 'mixtral-8x7b-32768']
            }
        }
        self.active_provider = None
        self.fallback_providers = []  # Lista de provedores para fallback
        self.config_path = os.path.join(os.path.dirname(__file__), 'ai_config.json')
        self.load_config()
    
    def load_config(self):
        """Carrega configuração salva"""
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    for provider, settings in config.get('providers', {}).items():
                        if provider in self.providers:
                            self.providers[provider].update(settings)
                    self.active_provider = config.get('active_provider')
                    self.fallback_providers = config.get('fallback_providers', [])
        except Exception as e:
            print(f"Erro ao carregar config: {e}")
    
    def save_config(self):
        """Salva configuração"""
        try:
            config = {
                'version': self.VERSION,
                'providers': self.providers,
                'active_provider': self.active_provider,
                'fallback_providers': self.fallback_providers
            }
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Erro ao salvar config: {e}")
    
    def configure_provider(self, provider: str, api_key: str, base_url: Optional[str] = None, model: Optional[str] = None):
        """Configura um provedor de IA"""
        if provider not in self.providers:
            return {'success': False, 'error': f'Provedor {provider} não suportado. Disponíveis: {list(self.providers.keys())}'}
        
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
    
    def set_fallback_providers(self, providers: List[str]):
        """Define lista de provedores para fallback"""
        valid_providers = [p for p in providers if p in self.providers and self.providers[p]['enabled']]
        self.fallback_providers = valid_providers
        self.save_config()
        return {'success': True, 'fallback_providers': valid_providers}
    
    def get_status(self):
        """Retorna status de todos os provedores"""
        status = {
            'version': self.VERSION,
            'active_provider': self.active_provider,
            'fallback_providers': self.fallback_providers,
            'providers': {}
        }
        for name, config in self.providers.items():
            status['providers'][name] = {
                'name': config['name'],
                'enabled': config['enabled'],
                'model': config.get('model'),
                'models_available': config.get('models_available', []),
                'has_api_key': bool(config.get('api_key'))
            }
        return status
    
    def list_providers(self):
        """Lista todos os provedores disponíveis"""
        return {
            'providers': list(self.providers.keys()),
            'configured': [p for p, c in self.providers.items() if c['enabled']],
            'active': self.active_provider
        }
    
    def chat(self, message: str, context: Optional[str] = None, system_prompt: Optional[str] = None, provider: Optional[str] = None) -> Dict[str, Any]:
        """Envia mensagem para o provedor de IA (com fallback automático)"""
        
        # Determina qual provedor usar
        target_provider = provider or self.active_provider
        
        if not target_provider:
            return {'success': False, 'error': 'Nenhum provedor de IA configurado'}
        
        # Lista de provedores para tentar (principal + fallbacks)
        providers_to_try = [target_provider] + [p for p in self.fallback_providers if p != target_provider]
        
        # System prompt padrão para o Obsidian Agente v5.0
        default_system = """Você é o Obsidian Agente Inteligente v5.0, um assistente avançado especializado em:
- Gerenciamento inteligente de notas e conhecimento no Obsidian
- Organização de informações, produtividade e automação
- Criação de conteúdo estruturado em Markdown
- Integração com múltiplas IAs e plataformas
- Automação de tarefas complexas no ambiente do usuário

Responda de forma clara, útil e proativa. Use emojis quando apropriado para tornar a comunicação mais amigável.
Se o contexto incluir informações sobre notas ou arquivos do usuário, use-as para dar respostas mais personalizadas."""

        final_system = system_prompt or default_system
        if context:
            final_system += f"\n\nContexto atual:\n{context}"
        
        last_error = None
        
        for prov in providers_to_try:
            if prov not in self.providers:
                continue
                
            provider_config = self.providers[prov]
            
            if not provider_config['enabled'] or not provider_config.get('api_key'):
                continue
            
            try:
                result = self._chat_with_provider(prov, message, final_system, provider_config)
                if result.get('success'):
                    return result
                last_error = result.get('error')
            except Exception as e:
                last_error = str(e)
                continue
        
        return {'success': False, 'error': f'Todos os provedores falharam. Último erro: {last_error}'}
    
    def _chat_with_provider(self, provider_name: str, message: str, system: str, provider: dict) -> Dict[str, Any]:
        """Roteador para o método correto de cada provedor"""
        method_map = {
            'openai': self._chat_openai,
            'claude': self._chat_claude,
            'gemini': self._chat_gemini,
            'grok': self._chat_grok,
            'manus': self._chat_manus,
            'genspark': self._chat_genspark,
            'abacus': self._chat_abacus,
            'deepseek': self._chat_deepseek,
            'groq': self._chat_groq
        }
        
        if provider_name in method_map:
            return method_map[provider_name](message, system, provider)
        else:
            # Tenta usar formato OpenAI como padrão
            return self._chat_openai_compatible(message, system, provider, provider_name)
    
    def _chat_openai(self, message: str, system: str, provider: dict) -> Dict[str, Any]:
        """Chat com OpenAI GPT"""
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
            'max_tokens': 4000
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
                'model': provider['model'],
                'usage': result.get('usage', {})
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
            'max_tokens': 4000
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
                'model': provider['model'],
                'usage': result.get('usage', {})
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
                'maxOutputTokens': 4000
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
    
    def _chat_grok(self, message: str, system: str, provider: dict) -> Dict[str, Any]:
        """Chat com xAI Grok"""
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
            'max_tokens': 4000
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
                'provider': 'grok',
                'model': provider['model'],
                'usage': result.get('usage', {})
            }
        else:
            return {'success': False, 'error': f'Grok error: {response.text}'}
    
    def _chat_manus(self, message: str, system: str, provider: dict) -> Dict[str, Any]:
        """Chat via Manus Bridge (COMET)"""
        if not provider.get('base_url'):
            return {'success': False, 'error': 'URL do Manus Bridge não configurada'}
        
        # Envia comando para o Manus via COMET Bridge
        headers = {
            'Authorization': f'Bearer {provider.get("api_key", "")}',
            'Content-Type': 'application/json'
        }
        
        data = {
            'command': f'echo "MANUS_REQUEST: {message}"'
        }
        
        response = requests.post(
            f'{provider["base_url"]}/exec',
            headers=headers,
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
    
    def _chat_genspark(self, message: str, system: str, provider: dict) -> Dict[str, Any]:
        """Chat com Genspark AI"""
        # Genspark usa formato compatível com OpenAI
        return self._chat_openai_compatible(message, system, provider, 'genspark')
    
    def _chat_abacus(self, message: str, system: str, provider: dict) -> Dict[str, Any]:
        """Chat com Abacus AI"""
        # Abacus usa formato compatível com OpenAI
        return self._chat_openai_compatible(message, system, provider, 'abacus')
    
    def _chat_deepseek(self, message: str, system: str, provider: dict) -> Dict[str, Any]:
        """Chat com DeepSeek AI"""
        # DeepSeek usa formato compatível com OpenAI
        return self._chat_openai_compatible(message, system, provider, 'deepseek')
    
    def _chat_groq(self, message: str, system: str, provider: dict) -> Dict[str, Any]:
        """Chat com Groq"""
        # Groq usa formato compatível com OpenAI
        return self._chat_openai_compatible(message, system, provider, 'groq')
    
    def _chat_openai_compatible(self, message: str, system: str, provider: dict, provider_name: str) -> Dict[str, Any]:
        """Chat genérico para APIs compatíveis com OpenAI"""
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
            'max_tokens': 4000
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
                'provider': provider_name,
                'model': provider['model'],
                'usage': result.get('usage', {})
            }
        else:
            return {'success': False, 'error': f'{provider_name} error: {response.text}'}


# Instância global
ai_integration = AIIntegration()


# Funções de conveniência para uso no agente
def configure_ai(provider: str, api_key: str, **kwargs):
    """Configura um provedor de IA"""
    return ai_integration.configure_provider(provider, api_key, **kwargs)

def set_ai_provider(provider: str):
    """Define o provedor de IA ativo"""
    return ai_integration.set_active_provider(provider)

def set_fallback_providers(providers: list):
    """Define provedores de fallback"""
    return ai_integration.set_fallback_providers(providers)

def get_ai_status():
    """Retorna status dos provedores de IA"""
    return ai_integration.get_status()

def list_ai_providers():
    """Lista provedores disponíveis"""
    return ai_integration.list_providers()

def chat_with_ai(message: str, context: str = None, provider: str = None):
    """Envia mensagem para a IA"""
    return ai_integration.chat(message, context, provider=provider)

