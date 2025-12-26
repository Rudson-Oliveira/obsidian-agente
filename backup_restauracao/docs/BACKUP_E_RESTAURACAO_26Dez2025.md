# Backup e Restauração Completo - Sistema IA v3.1

**Data:** 26 de Dezembro de 2025
**Versão:** 3.1 (Ollama + Health Check)
**Autor:** Manus AI para Rudson-Oliveira

---

## 1. Visão Geral

Este documento contém todas as informações necessárias para restaurar o **Sistema IA v3.1** do zero em qualquer máquina Windows.

**IMPORTANTE:** As credenciais (API Keys, tokens) são armazenadas separadamente no arquivo `CREDENCIAIS_PRIVADAS.env` que NÃO deve ser compartilhado publicamente.

---

## 2. Pré-Requisitos para Restauração

### Software Necessário

| Software | Versão Mínima | Download |
|----------|---------------|----------|
| **Windows** | 10/11 | - |
| **Python** | 3.11+ | https://python.org |
| **Node.js** | 20+ | https://nodejs.org |
| **Git** | 2.40+ | https://git-scm.com |
| **Obsidian** | 1.4+ | https://obsidian.md |
| **Ollama** | 0.1+ | https://ollama.ai |
| **ngrok** | 3.0+ | https://ngrok.com |
| **Claude Code** | 2.0+ | `npm install -g @anthropic-ai/claude-code` |

---

## 3. Estrutura de Diretórios

```
C:\Users\{USERNAME}\
├── COMET\
│   ├── Iniciar_Sistema_IA.bat
│   ├── manus_bridge_unified.py
│   ├── autopilot\
│   ├── Documentacao\
│   ├── Backup_Restauracao\
│   │   ├── config\
│   │   │   ├── sistema_ia_config_SEGURO.json
│   │   │   └── CREDENCIAIS_PRIVADAS.env  (NÃO COMPARTILHAR)
│   │   ├── docs\
│   │   └── scripts\
│   └── logs\
│
├── obsidian-agente\  (GitHub)
│   ├── agent\
│   ├── hub_central\
│   ├── frontend\
│   └── docs\
│
└── .claude\
```

---

## 4. Portas do Sistema

| Serviço | Porta | Protocolo |
|---------|-------|-----------|
| COMET Bridge | 5000 | HTTP |
| Obsidian Agent | 5001 | HTTP |
| Hub Central | 5002 | HTTP |
| Vision Server | 5003 | HTTP |
| Frontend (Vite) | 5173 | HTTP |
| Ollama | 11434 | HTTP |

---

## 5. Restauração Rápida

### Passo 1: Clonar Repositório

```powershell
cd "C:\Users\$env:USERNAME"
git clone https://github.com/Rudson-Oliveira/obsidian-agente.git
```

### Passo 2: Configurar Credenciais

Crie o arquivo `CREDENCIAIS_PRIVADAS.env` com suas credenciais:

```powershell
# Definir variáveis de ambiente
$env:ANTHROPIC_API_KEY = "sua-api-key-aqui"
$env:OBSIDIAN_TOKEN = "seu-token-aqui"
$env:NGROK_URL = "sua-url-ngrok-aqui"

# Persistir para o usuário
[System.Environment]::SetEnvironmentVariable("ANTHROPIC_API_KEY", $env:ANTHROPIC_API_KEY, "User")
[System.Environment]::SetEnvironmentVariable("OBSIDIAN_TOKEN", $env:OBSIDIAN_TOKEN, "User")
[System.Environment]::SetEnvironmentVariable("NGROK_URL", $env:NGROK_URL, "User")
```

### Passo 3: Executar Script de Restauração

```powershell
.\Restaurar_Sistema_IA_v3.1.ps1
```

### Passo 4: Iniciar Sistema

```batch
C:\Users\{USERNAME}\COMET\Iniciar_Sistema_IA.bat
```

---

## 6. COMET Bridge - Código Fonte

O COMET Bridge é o servidor Flask que permite comunicação remota com o sistema.

```python
# manus_bridge_unified.py
import json, subprocess, os
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib import request as urllib_request, error as urllib_error

PORT = 5000
OBSIDIAN_API = "http://127.0.0.1:27123"
OBSIDIAN_TOKEN = os.environ.get("OBSIDIAN_TOKEN", "")

def obsidian_request(method, path, data=None, content_type="application/json"):
    try:
        url = f"{OBSIDIAN_API}{path}"
        headers = {"Authorization": f"Bearer {OBSIDIAN_TOKEN}"}
        if content_type: headers["Content-Type"] = content_type
        body = None
        if data:
            body = json.dumps(data).encode("utf-8") if isinstance(data, dict) else data.encode("utf-8")
        req = urllib_request.Request(url, data=body, headers=headers, method=method)
        with urllib_request.urlopen(req, timeout=10) as resp:
            return {"success": True, "data": json.loads(resp.read().decode("utf-8")) if resp.headers.get("Content-Type", "").startswith("application/json") else resp.read().decode("utf-8")}
    except urllib_error.HTTPError as e:
        return {"success": False, "error": str(e), "status": e.code}
    except Exception as e: 
        return {"success": False, "error": str(e)}

def execute_powershell(command, timeout=60):
    try:
        result = subprocess.run(["powershell", "-Command", command], capture_output=True, text=True, timeout=timeout)
        return {"success": result.returncode == 0, "output": result.stdout, "error": result.stderr}
    except subprocess.TimeoutExpired: 
        return {"success": False, "error": "Timeout"}
    except Exception as e: 
        return {"success": False, "error": str(e)}

# ... (resto do código igual)
```

---

## 7. Verificação Pós-Restauração

```powershell
# Verificar portas
netstat -an | findstr "5000 5001 5002 5003 5173 11434"

# Testar COMET Bridge
Invoke-WebRequest -Uri "http://localhost:5000" -UseBasicParsing

# Testar Ollama
Invoke-WebRequest -Uri "http://localhost:11434" -UseBasicParsing

# Verificar Claude Code
claude --version
```

---

## 8. Restauração Assistida pelo Manus

Para restauração assistida, forneça este documento ao **Manus AI** e solicite:

> "Restaurar Sistema IA v3.1 usando o backup. Minhas credenciais estão no arquivo CREDENCIAIS_PRIVADAS.env"

O Manus irá:
1. Verificar pré-requisitos
2. Clonar repositório do GitHub
3. Configurar variáveis de ambiente
4. Criar scripts de inicialização
5. Testar todos os serviços

---

## 9. Histórico de Versões

| Versão | Data | Alterações |
|--------|------|------------|
| 3.1 | 26/12/2025 | Ollama, Health Check, Claude Code, Backup Seguro |
| 3.0 | 25/12/2025 | Sistema unificado com Hub Central |
| 2.0 | 24/12/2025 | Integração COMET Bridge |
| 1.0 | 23/12/2025 | Versão inicial |

---

**Este documento + arquivo de credenciais são suficientes para restauração completa.**
