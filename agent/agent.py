#!/usr/bin/env python3
"""
Obsidian Desktop Agent
Agente local que fornece uma API REST para automação do Obsidian
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

# Configuração de logging
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

# Configuração
CONFIG_DIR = Path.home() / '.obsidian-agent'
CONFIG_FILE = CONFIG_DIR / 'config.json'
DEFAULT_CONFIG = {
    'port': 5001,
    'api_key': f'BO_{secrets.token_urlsafe(32)}',
    'obsidian_path': None,
}

def load_config():
    """Carrega configuração do arquivo ou cria uma nova"""
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    else:
        CONFIG_DIR.mkdir(exist_ok=True)
        with open(CONFIG_FILE, 'w') as f:
            json.dump(DEFAULT_CONFIG, f, indent=2)
        return DEFAULT_CONFIG

def save_config(config):
    """Salva configuração no arquivo"""
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
    """Verifica se a API Key está correta"""
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer '):
        return False
    
    provided_key = auth_header[7:]
    config = load_config()
    return provided_key == config.get('api_key')

def require_auth(f):
    """Decorator para verificar autenticação"""
    def decorated_function(*args, **kwargs):
        if not verify_api_key():
            return jsonify({'success': False, 'error': 'Unauthorized'}), 401
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

# ==================== ENDPOINTS ====================

@app.route('/health', methods=['GET'])
def health():
    """Verifica se o agente está online"""
    return jsonify({
        'status': 'online',
        'version': '1.1',
        'timestamp': datetime.now().isoformat(),
    })

@app.route('/obsidian/open', methods=['POST'])
@require_auth
def obsidian_open():
    """Abre a aplicação Obsidian"""
    try:
        config = load_config()
        obsidian_path = config.get('obsidian_path') or find_obsidian_path()
        
        if not obsidian_path or not Path(obsidian_path).exists():
            return jsonify({
                'success': False,
                'error': 'Obsidian não encontrado no sistema'
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

@app.route('/file/read', methods=['POST'])
@require_auth
def file_read():
    """Lê o conteúdo de um arquivo"""
    try:
        data = request.get_json()
        file_path = data.get('path')
        
        if not file_path:
            return jsonify({
                'success': False,
                'error': 'Caminho do arquivo não fornecido'
            }), 400
        
        path = Path(file_path)
        if not path.exists():
            return jsonify({
                'success': False,
                'error': f'Arquivo não encontrado: {file_path}'
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
    """Escreve conteúdo em um arquivo"""
    try:
        data = request.get_json()
        file_path = data.get('path')
        content = data.get('content', '')
        
        if not file_path:
            return jsonify({
                'success': False,
                'error': 'Caminho do arquivo não fornecido'
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
                'error': 'Comando não fornecido'
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
                'error': 'Caminho do vault não configurado ou não encontrado'
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
                'error': 'Título da nota não fornecido'
            }), 400
        
        config = load_config()
        vault_path = config.get('vault_path')
        
        if not vault_path or not Path(vault_path).exists():
            return jsonify({
                'success': False,
                'error': 'Caminho do vault não configurado ou não encontrado'
            }), 404
        
        # Criar arquivo da nota
        note_path = Path(vault_path) / f'{title}.md'
        
        if note_path.exists():
            return jsonify({
                'success': False,
                'error': f'Nota "{title}" já existe'
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
    """Busca conteúdo nas notas do vault"""
    try:
        data = request.get_json()
        query = data.get('query', '').lower()
        
        if not query:
            return jsonify({
                'success': False,
                'error': 'Termo de busca não fornecido'
            }), 400
        
        config = load_config()
        vault_path = config.get('vault_path')
        
        if not vault_path or not Path(vault_path).exists():
            return jsonify({
                'success': False,
                'error': 'Caminho do vault não configurado ou não encontrado'
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
                'error': 'Caminho do vault não fornecido'
            }), 400
        
        path = Path(vault_path)
        if not path.exists() or not path.is_dir():
            return jsonify({
                'success': False,
                'error': f'Diretório não encontrado: {vault_path}'
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
                'error': 'Texto não fornecido'
            }), 400
        
        # Processar comando com IA
        command_result = intelligent_agent.process_command(text)
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
                api_result = {'success': False, 'error': 'Obsidian não encontrado'}
        
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
                api_result = {'success': False, 'error': 'Vault não configurado'}
        
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
                        api_result = {'success': False, 'error': 'Nota já existe'}
                else:
                    api_result = {'success': False, 'error': 'Vault não configurado'}
            else:
                api_result = {'success': False, 'error': 'Título não fornecido'}
        
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
                    api_result = {'success': False, 'error': 'Vault não configurado'}
            else:
                api_result = {'success': False, 'error': 'Query não fornecida'}
        
        elif command == 'configure_vault':
            vault_path = params.get('vault_path')
            if vault_path and Path(vault_path).exists():
                config = load_config()
                config['vault_path'] = str(vault_path)
                save_config(config)
                api_result = {'success': True}
            else:
                api_result = {'success': False, 'error': 'Caminho inválido'}
        
        # Gerar resposta inteligente
        response_text = intelligent_agent.generate_response(command_result, api_result)
        
        logger.info(f'Comando processado: {command}')
        
        return jsonify({
            'success': True,
            'command': command,
            'response': response_text,
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
    """Retorna informações de configuração (sem API Key)"""
    config = load_config()
    return jsonify({
        'port': config.get('port'),
        'version': '2.0',
        'obsidian_path': config.get('obsidian_path'),
        'features': ['intelligent_processing', 'nlp_commands', 'obsidian_knowledge']
    })

# ==================== MAIN ====================

def main():
    """Função principal"""
    logger.info('Iniciando Obsidian Desktop Agent...')
    
    config = load_config()
    logger.info('Configuração carregada')
    logger.info(f'API Key: {config.get("api_key")}')
    logger.info(f'Arquivo de configuração: {CONFIG_FILE}')
    
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
        logger.info('Agente parado pelo usuário')
        sys.exit(0)

if __name__ == '__main__':
    main()
