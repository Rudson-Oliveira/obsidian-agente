#!/usr/bin/env python3
"""
Obsidian Desktop Agent
Agente local que fornece uma API REST para automaÃ§Ã£o do Obsidian
"""

import os
import sys
import json
import logging
import subprocess
import secrets
from pathlib import Path
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS
from intelligent_agent import IntelligentAgent

# Importar lógica de decisão
try:
    from decision_logic import analyze as analyze_query
    DECISION_LOGIC_AVAILABLE = True
    logger.info("[AGENT] Módulo de lógica de decisão carregado!")
except ImportError:
    DECISION_LOGIC_AVAILABLE = False
    def analyze_query(q): return {'category': 'conversation', 'recommended_ia': 'openai', 'confidence': 0.5}

# ConfiguraÃ§Ã£o de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Inicializar Flask
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": ["*"]}})

# Inicializar Agente Inteligente
intelligent_agent = IntelligentAgent()

# ConfiguraÃ§Ã£o
CONFIG_DIR = Path.home() / '.obsidian-agent'
CONFIG_FILE = CONFIG_DIR / 'config.json'
DEFAULT_CONFIG = {
    'port': 5001,
    'api_key': f'BO_{secrets.token_urlsafe(32)}',
    'obsidian_path': None,
}

def load_config():
    """Carrega configuraÃ§Ã£o do arquivo ou cria uma nova"""
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    else:
        CONFIG_DIR.mkdir(exist_ok=True)
        with open(CONFIG_FILE, 'w') as f:
            json.dump(DEFAULT_CONFIG, f, indent=2)
        return DEFAULT_CONFIG

def save_config(config):
    """Salva configuraÃ§Ã£o no arquivo"""
    CONFIG_DIR.mkdir(exist_ok=True)
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)

def find_obsidian_path():
    """Encontra o caminho do Obsidian no sistema"""
    if sys.platform == 'win32':
        possible_paths = [
            Path.home() / 'AppData' / 'Local' / 'Programs' / 'Obsidian' / 'Obsidian.exe',
            Path('C:') / 'Program Files' / 'Obsidian' / 'Obsidian.exe',
        ]
    elif sys.platform == 'darwin':
        possible_paths = [
            Path('/Applications/Obsidian.app/Contents/MacOS/Obsidian'),
        ]
    else:  # Linux
        possible_paths = [
            Path('/usr/bin/obsidian'),
            Path('/usr/local/bin/obsidian'),
        ]
    
    for path in possible_paths:
        if path.exists():
            return str(path)
    
    return None

def verify_api_key():
    """Verifica se a API Key estÃ¡ correta"""
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer '):
        return False
    
    provided_key = auth_header[7:]
    config = load_config()
    return provided_key == config.get('api_key')

def require_auth(f):
    """Decorator para verificar autenticaÃ§Ã£o"""
    def decorated_function(*args, **kwargs):
        if not verify_api_key():
            return jsonify({'success': False, 'error': 'Unauthorized'}), 401
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

# ==================== ENDPOINTS ====================

@app.route('/health', methods=['GET'])
def health():
    """Verifica se o agente estÃ¡ online"""
    return jsonify({
        'status': 'online',
        'version': '5.0.0',
        'timestamp': datetime.now().isoformat(),
    })

@app.route('/obsidian/open', methods=['POST'])
@require_auth
def obsidian_open():
    """Abre a aplicaÃ§Ã£o Obsidian"""
    try:
        config = load_config()
        obsidian_path = config.get('obsidian_path') or find_obsidian_path()
        
        if not obsidian_path or not Path(obsidian_path).exists():
            return jsonify({
                'success': False,
                'error': 'Obsidian nÃ£o encontrado no sistema'
            }), 404
        
        subprocess.Popen([obsidian_path])
        logger.info('Obsidian aberto com sucesso')
        
        return jsonify({
            'success': True,
            'message': 'Obsidian aberto com sucesso'
        })
    except Exception as e:
        logger.error(f'Erro ao abrir Obsidian: {str(e)}')
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/obsidian/close', methods=['POST'])
@require_auth
def obsidian_close():
    """Fecha a aplicacao Obsidian"""
    try:
        # Tenta fechar o processo do Obsidian no Windows
        result = subprocess.run(['taskkill', '/IM', 'Obsidian.exe', '/F'], capture_output=True, text=True)
        
        logger.info('Obsidian fechado com sucesso')
        
        return jsonify({
            'success': True,
            'message': 'Obsidian fechado com sucesso'
        })
    except Exception as e:
        logger.error(f'Erro ao fechar Obsidian: {str(e)}')
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/file/read', methods=['POST'])
@require_auth
def file_read():
    """LÃª o conteÃºdo de um arquivo"""
    try:
        data = request.get_json()
        file_path = data.get('path')
        
        if not file_path:
            return jsonify({
                'success': False,
                'error': 'Caminho do arquivo nÃ£o fornecido'
            }), 400
        
        path = Path(file_path)
        if not path.exists():
            return jsonify({
                'success': False,
                'error': f'Arquivo nÃ£o encontrado: {file_path}'
            }), 404
        
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        logger.info(f'Arquivo lido: {file_path}')
        
        return jsonify({
            'success': True,
            'content': content,
            'path': file_path
        })
    except Exception as e:
        logger.error(f'Erro ao ler arquivo: {str(e)}')
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/file/write', methods=['POST'])
@require_auth
def file_write():
    """Escreve conteÃºdo em um arquivo"""
    try:
        data = request.get_json()
        file_path = data.get('path')
        content = data.get('content', '')
        
        if not file_path:
            return jsonify({
                'success': False,
                'error': 'Caminho do arquivo nÃ£o fornecido'
            }), 400
        
        path = Path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        logger.info(f'Arquivo escrito: {file_path}')
        
        return jsonify({
            'success': True,
            'message': 'Arquivo escrito com sucesso',
            'path': file_path
        })
    except Exception as e:
        logger.error(f'Erro ao escrever arquivo: {str(e)}')
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/command/execute', methods=['POST'])
@require_auth
def command_execute():
    """Executa um comando no sistema"""
    try:
        data = request.get_json()
        command = data.get('command')
        
        if not command:
            return jsonify({
                'success': False,
                'error': 'Comando nÃ£o fornecido'
            }), 400
        
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        logger.info(f'Comando executado: {command}')
        
        return jsonify({
            'success': result.returncode == 0,
            'output': result.stdout,
            'error': result.stderr if result.stderr else None,
            'exit_code': result.returncode
        })
    except subprocess.TimeoutExpired:
        logger.error('Timeout ao executar comando')
        return jsonify({
            'success': False,
            'error': 'Timeout ao executar comando'
        }), 504
    except Exception as e:
        logger.error(f'Erro ao executar comando: {str(e)}')
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/obsidian/notes', methods=['GET'])
@require_auth
def obsidian_notes():
    """Lista todas as notas do vault"""
    try:
        config = load_config()
        vault_path = config.get('vault_path')
        
        if not vault_path or not Path(vault_path).exists():
            return jsonify({
                'success': False,
                'error': 'Caminho do vault nÃ£o configurado ou nÃ£o encontrado'
            }), 404
        
        notes = []
        vault = Path(vault_path)
        
        for md_file in vault.rglob('*.md'):
            notes.append({
                'name': md_file.stem,
                'path': str(md_file.relative_to(vault)),
                'full_path': str(md_file),
                'size': md_file.stat().st_size,
                'modified': datetime.fromtimestamp(md_file.stat().st_mtime).isoformat()
            })
        
        logger.info(f'Listadas {len(notes)} notas')
        
        return jsonify({
            'success': True,
            'notes': notes,
            'count': len(notes)
        })
    except Exception as e:
        logger.error(f'Erro ao listar notas: {str(e)}')
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/obsidian/note/create', methods=['POST'])
@require_auth
def obsidian_note_create():
    """Cria uma nova nota no vault"""
    try:
        data = request.get_json()
        title = data.get('title')
        content = data.get('content', '')
        
        if not title:
            return jsonify({
                'success': False,
                'error': 'TÃ­tulo da nota nÃ£o fornecido'
            }), 400
        
        config = load_config()
        vault_path = config.get('vault_path')
        
        if not vault_path or not Path(vault_path).exists():
            return jsonify({
                'success': False,
                'error': 'Caminho do vault nÃ£o configurado ou nÃ£o encontrado'
            }), 404
        
        # Criar arquivo da nota
        note_path = Path(vault_path) / f'{title}.md'
        
        if note_path.exists():
            return jsonify({
                'success': False,
                'error': f'Nota "{title}" jÃ¡ existe'
            }), 409
        
        with open(note_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        logger.info(f'Nota criada: {title}')
        
        return jsonify({
            'success': True,
            'message': f'Nota "{title}" criada com sucesso',
            'path': str(note_path)
        })
    except Exception as e:
        logger.error(f'Erro ao criar nota: {str(e)}')
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/obsidian/note/search', methods=['POST'])
@require_auth
def obsidian_note_search():
    """Busca conteÃºdo nas notas do vault"""
    try:
        data = request.get_json()
        query = data.get('query', '').lower()
        
        if not query:
            return jsonify({
                'success': False,
                'error': 'Termo de busca nÃ£o fornecido'
            }), 400
        
        config = load_config()
        vault_path = config.get('vault_path')
        
        if not vault_path or not Path(vault_path).exists():
            return jsonify({
                'success': False,
                'error': 'Caminho do vault nÃ£o configurado ou nÃ£o encontrado'
            }), 404
        
        results = []
        vault = Path(vault_path)
        
        for md_file in vault.rglob('*.md'):
            try:
                with open(md_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if query in content.lower():
                        # Encontrar contexto
                        lines = content.split('\n')
                        matches = []
                        for i, line in enumerate(lines):
                            if query in line.lower():
                                matches.append({
                                    'line': i + 1,
                                    'text': line.strip()
                                })
                        
                        results.append({
                            'name': md_file.stem,
                            'path': str(md_file.relative_to(vault)),
                            'full_path': str(md_file),
                            'matches': matches[:5]  # Limitar a 5 matches por arquivo
                        })
            except Exception as e:
                logger.warning(f'Erro ao ler arquivo {md_file}: {str(e)}')
                continue
        
        logger.info(f'Busca por "{query}" retornou {len(results)} resultados')
        
        return jsonify({
            'success': True,
            'query': query,
            'results': results,
            'count': len(results)
        })
    except Exception as e:
        logger.error(f'Erro ao buscar em notas: {str(e)}')
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/obsidian/vault/configure', methods=['POST'])
@require_auth
def obsidian_vault_configure():
    """Configura o caminho do vault"""
    try:
        data = request.get_json()
        vault_path = data.get('vault_path')
        
        if not vault_path:
            return jsonify({
                'success': False,
                'error': 'Caminho do vault nÃ£o fornecido'
            }), 400
        
        path = Path(vault_path)
        if not path.exists() or not path.is_dir():
            return jsonify({
                'success': False,
                'error': f'DiretÃ³rio nÃ£o encontrado: {vault_path}'
            }), 404
        
        config = load_config()
        config['vault_path'] = str(path)
        save_config(config)
        
        logger.info(f'Vault configurado: {vault_path}')
        
        return jsonify({
            'success': True,
            'message': 'Vault configurado com sucesso',
            'vault_path': str(path)
        })
    except Exception as e:
        logger.error(f'Erro ao configurar vault: {str(e)}')
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/intelligent/process', methods=['POST'])
@require_auth
def intelligent_process():
    """Processa comando em linguagem natural usando IA"""
    try:
        data = request.get_json()
        text = data.get('text', '')
        
        if not text:
            return jsonify({
                'success': False,
                'error': 'Texto nÃ£o fornecido'
            }), 400
        
        # Analisar query com lógica de decisão
        analysis = analyze_query(text)
        logger.info(f"[DECISION] Query: {text[:50]}...")
        logger.info(f"[DECISION] Categoria: {analysis.get('category')}")
        logger.info(f"[DECISION] IA Recomendada: {analysis.get('recommended_ia')}")
        logger.info(f"[DECISION] Confiança: {analysis.get('confidence', 0):.2f}")
        
        # Processar comando com IA
        command_result = intelligent_agent.process_command(text)
        command_result['decision_analysis'] = analysis  # Adicionar análise ao resultado
        command = command_result['command']
        params = command_result['parameters']
        
        # Executar comando correspondente
        api_result = {}
        
        if command == 'open_obsidian':
            config = load_config()
            obsidian_path = config.get('obsidian_path') or find_obsidian_path()
            if obsidian_path and Path(obsidian_path).exists():
                subprocess.Popen([obsidian_path])
                api_result = {'success': True}
            else:
                api_result = {'success': False, 'error': 'Obsidian nÃ£o encontrado'}
        
        elif command == 'list_notes':
            config = load_config()
            vault_path = config.get('vault_path')
            if vault_path and Path(vault_path).exists():
                notes = []
                for md_file in Path(vault_path).rglob('*.md'):
                    notes.append({
                        'name': md_file.stem,
                        'path': str(md_file.relative_to(vault_path))
                    })
                api_result = {'success': True, 'data': notes}
            else:
                api_result = {'success': False, 'error': 'Vault nÃ£o configurado'}
        
        elif command == 'create_note':
            title = params.get('title')
            content = params.get('content', '')
            if title:
                config = load_config()
                vault_path = config.get('vault_path')
                if vault_path and Path(vault_path).exists():
                    note_path = Path(vault_path) / f'{title}.md'
                    if not note_path.exists():
                        with open(note_path, 'w', encoding='utf-8') as f:
                            f.write(content)
                        api_result = {'success': True}
                    else:
                        api_result = {'success': False, 'error': 'Nota jÃ¡ existe'}
                else:
                    api_result = {'success': False, 'error': 'Vault nÃ£o configurado'}
            else:
                api_result = {'success': False, 'error': 'TÃ­tulo nÃ£o fornecido'}
        
        elif command == 'search_notes':
            query = params.get('query', '')
            if query:
                config = load_config()
                vault_path = config.get('vault_path')
                if vault_path and Path(vault_path).exists():
                    results = []
                    for md_file in Path(vault_path).rglob('*.md'):
                        try:
                            with open(md_file, 'r', encoding='utf-8') as f:
                                if query.lower() in f.read().lower():
                                    results.append({'name': md_file.stem})
                        except:
                            continue
                    api_result = {'success': True, 'data': results}
                else:
                    api_result = {'success': False, 'error': 'Vault nÃ£o configurado'}
            else:
                api_result = {'success': False, 'error': 'Query nÃ£o fornecida'}
        
        elif command == 'configure_vault':
            vault_path = params.get('vault_path')
            if vault_path and Path(vault_path).exists():
                config = load_config()
                config['vault_path'] = str(vault_path)
                save_config(config)
                api_result = {'success': True}
            else:
                api_result = {'success': False, 'error': 'Caminho invÃ¡lido'}
        

        elif command == "plugin_command":
            plugin_cmd = params.get("plugin_command")
            if plugin_cmd:
                try:
                    import requests
                    obsidian_api_key = "475ba2e794a2f8312e05dbe801debaf55f232ee98aafd68c7b0b44de19d628fd"
                    headers = {"Authorization": f"Bearer {obsidian_api_key}"}
                    response = requests.post(f"http://127.0.0.1:27123/commands/{plugin_cmd}", headers=headers, timeout=10)
                    if response.status_code == 200:
                        api_result = {"success": True, "message": f"Comando {plugin_cmd} executado"}
                    else:
                        api_result = {"success": False, "error": f"Erro: {response.text}"}
                except Exception as e:
                    api_result = {"success": False, "error": f"Erro: {str(e)}"}
            else:
                api_result = {"success": False, "error": "Comando nao especificado"}
        
        # Gerar resposta inteligente
        response_text = intelligent_agent.generate_response(command_result, api_result)
        
        # Adicionar informação da decisão na resposta
        if command == 'ask_ai' and DECISION_LOGIC_AVAILABLE:
            category = analysis.get('category', 'conversation').upper()
            confidence = analysis.get('confidence', 0)
            decision_info = f"\n\n[🧠 Decisão: {category} | Confiança: {confidence:.0%}]"
            if '[Via ' in response_text:
                response_text = response_text.replace('[Via ', f'{decision_info}\n[Via ')
            else:
                response_text += decision_info
        
        logger.info(f'Comando processado: {command}')
        
        return jsonify({
            'success': True,
            'command': command,
            'response': response_text,
            'decision': analysis if DECISION_LOGIC_AVAILABLE else None,
            'data': api_result.get('data')
        })
    
    except Exception as e:
        logger.error(f'Erro ao processar comando: {str(e)}')
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/config', methods=['GET'])
def get_config():
    """Retorna informaÃ§Ãµes de configuraÃ§Ã£o (sem API Key)"""
    config = load_config()
    return jsonify({
        'port': config.get('port'),
        'version': '5.0',
        'obsidian_path': config.get('obsidian_path'),
        'api_key': config.get('api_key'),
        'vault_path': config.get('vault_path'),
        'features': ['intelligent_processing', 'nlp_commands', 'obsidian_knowledge', 'auto_config']
    })



# ==================== AI INTEGRATION ENDPOINTS ====================

from ai_integration import ai_integration, configure_ai, set_ai_provider, get_ai_status, list_ai_providers, chat_with_ai, set_fallback_providers

@app.route('/ai/status', methods=['GET'])
def ai_status():
    """Retorna status de todos os provedores de IA"""
    return jsonify(get_ai_status())

@app.route('/ai/providers', methods=['GET'])
def ai_providers():
    """Lista provedores de IA disponíveis"""
    return jsonify(list_ai_providers())

@app.route('/ai/configure', methods=['POST'])
@require_auth
def ai_configure():
    """Configura um provedor de IA"""
    data = request.get_json()
    provider = data.get('provider')
    api_key = data.get('api_key')
    base_url = data.get('base_url')
    model = data.get('model')
    
    if not provider or not api_key:
        return jsonify({'success': False, 'error': 'provider e api_key são obrigatórios'}), 400
    
    result = configure_ai(provider, api_key, base_url=base_url, model=model)
    return jsonify(result)

@app.route('/ai/set-provider', methods=['POST'])
@require_auth
def ai_set_provider():
    """Define o provedor de IA ativo"""
    data = request.get_json()
    provider = data.get('provider')
    
    if not provider:
        return jsonify({'success': False, 'error': 'provider é obrigatório'}), 400
    
    result = set_ai_provider(provider)
    return jsonify(result)

@app.route('/ai/set-fallback', methods=['POST'])
@require_auth
def ai_set_fallback():
    """Define provedores de fallback"""
    data = request.get_json()
    providers = data.get('providers', [])
    
    result = set_fallback_providers(providers)
    return jsonify(result)

@app.route('/ai/chat', methods=['POST'])
@require_auth
def ai_chat():
    """Envia mensagem para a IA"""
    data = request.get_json()
    message = data.get('message')
    context = data.get('context')
    provider = data.get('provider')  # Opcional: força um provedor específico
    
    if not message:
        return jsonify({'success': False, 'error': 'message é obrigatório'}), 400
    
    result = chat_with_ai(message, context, provider=provider)
    return jsonify(result)

@app.route('/ai/test', methods=['POST'])
@require_auth
def ai_test():
    """Testa a conexão com um provedor de IA"""
    data = request.get_json()
    provider = data.get('provider')
    
    if not provider:
        return jsonify({'success': False, 'error': 'provider é obrigatório'}), 400
    
    # Envia uma mensagem de teste
    result = chat_with_ai("Olá! Responda apenas com 'OK' se você está funcionando.", provider=provider)
    
    if result.get('success'):
        return jsonify({
            'success': True,
            'message': f'Teste com {provider} realizado com sucesso!',
            'response': result.get('response'),
            'model': result.get('model')
        })
    else:
        return jsonify({
            'success': False,
            'error': result.get('error')
        })


# ==================== MAIN ====================

def main():
    """FunÃ§Ã£o principal"""
    logger.info('Iniciando Obsidian Desktop Agent...')
    
    config = load_config()
    logger.info('ConfiguraÃ§Ã£o carregada')
    logger.info(f'API Key: {config.get("api_key")}')
    logger.info(f'Arquivo de configuraÃ§Ã£o: {CONFIG_FILE}')
    
    port = config.get('port', 5001)
    logger.info(f'Servidor rodando em http://localhost:{port}')
    logger.info('Pressione Ctrl+C para parar')
    
    try:
        app.run(
            host='0.0.0.0',
            port=port,
            debug=False,
            use_reloader=False
        )
    except KeyboardInterrupt:
        logger.info('Agente parado pelo usuÃ¡rio')
        sys.exit(0)



if __name__ == '__main__':
    main()



