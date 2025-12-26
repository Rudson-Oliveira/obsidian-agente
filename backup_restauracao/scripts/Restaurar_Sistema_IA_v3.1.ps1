# ============================================
# RESTAURAÇÃO AUTOMÁTICA - SISTEMA IA v3.1
# Versão SEGURA (sem credenciais hardcoded)
# Data: 26 de Dezembro de 2025
# Autor: Manus AI para Rudson-Oliveira
# ============================================

param(
    [switch]$SkipDownloads,
    [switch]$SkipOllama,
    [string]$Username = $env:USERNAME,
    [string]$CredentialsFile = ""
)

$ErrorActionPreference = "Stop"

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  RESTAURAÇÃO DO SISTEMA IA v3.1" -ForegroundColor Cyan
Write-Host "  Versão SEGURA" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# Diretórios base
$BaseDir = "C:\Users\$Username"
$CometDir = "$BaseDir\COMET"
$AgentDir = "$BaseDir\obsidian-agente"
$ClaudeDir = "$BaseDir\.claude"

# ============================================
# FASE 0: CARREGAR CREDENCIAIS
# ============================================
Write-Host "[FASE 0] Verificando credenciais..." -ForegroundColor Yellow

# Verificar variáveis de ambiente
$ApiKey = $env:ANTHROPIC_API_KEY
$ObsidianToken = $env:OBSIDIAN_TOKEN
$NgrokUrl = $env:NGROK_URL

# Se não encontrou, tentar carregar do arquivo
if (-not $ApiKey -and $CredentialsFile -and (Test-Path $CredentialsFile)) {
    Write-Host "  Carregando credenciais de $CredentialsFile..." -ForegroundColor Gray
    Get-Content $CredentialsFile | ForEach-Object {
        if ($_ -match "^([^#=]+)=(.+)$") {
            $name = $matches[1].Trim()
            $value = $matches[2].Trim()
            Set-Item -Path "env:$name" -Value $value
        }
    }
    $ApiKey = $env:ANTHROPIC_API_KEY
    $ObsidianToken = $env:OBSIDIAN_TOKEN
    $NgrokUrl = $env:NGROK_URL
}

if (-not $ApiKey) {
    Write-Host "  [AVISO] ANTHROPIC_API_KEY não configurada" -ForegroundColor Yellow
    Write-Host "  Configure com: `$env:ANTHROPIC_API_KEY = 'sua-chave'" -ForegroundColor Gray
} else {
    Write-Host "  [OK] ANTHROPIC_API_KEY configurada" -ForegroundColor Green
}

if (-not $ObsidianToken) {
    Write-Host "  [AVISO] OBSIDIAN_TOKEN não configurado" -ForegroundColor Yellow
} else {
    Write-Host "  [OK] OBSIDIAN_TOKEN configurado" -ForegroundColor Green
}

if (-not $NgrokUrl) {
    $NgrokUrl = "sua-url-ngrok.ngrok-free.dev"
    Write-Host "  [AVISO] NGROK_URL não configurada, usando placeholder" -ForegroundColor Yellow
} else {
    Write-Host "  [OK] NGROK_URL: $NgrokUrl" -ForegroundColor Green
}

Write-Host ""

# ============================================
# FASE 1: VERIFICAR PRÉ-REQUISITOS
# ============================================
Write-Host "[FASE 1] Verificando pré-requisitos..." -ForegroundColor Yellow

# Verificar Python
try {
    $pythonVersion = python --version 2>&1
    Write-Host "  [OK] Python: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "  [ERRO] Python não encontrado. Instale em https://python.org" -ForegroundColor Red
    exit 1
}

# Verificar Node.js
try {
    $nodeVersion = node --version 2>&1
    Write-Host "  [OK] Node.js: $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "  [ERRO] Node.js não encontrado. Instale em https://nodejs.org" -ForegroundColor Red
    exit 1
}

# Verificar Git
try {
    $gitVersion = git --version 2>&1
    Write-Host "  [OK] Git: $gitVersion" -ForegroundColor Green
} catch {
    Write-Host "  [ERRO] Git não encontrado. Instale em https://git-scm.com" -ForegroundColor Red
    exit 1
}

Write-Host ""

# ============================================
# FASE 2: CRIAR ESTRUTURA DE DIRETÓRIOS
# ============================================
Write-Host "[FASE 2] Criando estrutura de diretórios..." -ForegroundColor Yellow

$directories = @(
    $CometDir,
    "$CometDir\Documentacao",
    "$CometDir\backup",
    "$CometDir\logs",
    "$CometDir\autopilot",
    $AgentDir,
    $ClaudeDir
)

foreach ($dir in $directories) {
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Force -Path $dir | Out-Null
        Write-Host "  [CRIADO] $dir" -ForegroundColor Green
    }
}

Write-Host ""

# ============================================
# FASE 3: CLONAR REPOSITÓRIO GITHUB
# ============================================
Write-Host "[FASE 3] Clonando repositório GitHub..." -ForegroundColor Yellow

if (-not (Test-Path "$AgentDir\.git")) {
    Set-Location $BaseDir
    git clone https://github.com/Rudson-Oliveira/obsidian-agente.git
    Write-Host "  [OK] Repositório clonado" -ForegroundColor Green
} else {
    Set-Location $AgentDir
    git pull origin master
    Write-Host "  [OK] Repositório atualizado" -ForegroundColor Green
}

Write-Host ""

# ============================================
# FASE 4: INSTALAR DEPENDÊNCIAS
# ============================================
Write-Host "[FASE 4] Instalando dependências..." -ForegroundColor Yellow

pip install flask requests --quiet
Write-Host "  [OK] Flask e Requests instalados" -ForegroundColor Green

npm install -g @anthropic-ai/claude-code --silent 2>$null
Write-Host "  [OK] Claude Code instalado" -ForegroundColor Green

Write-Host ""

# ============================================
# FASE 5: CRIAR COMET BRIDGE
# ============================================
Write-Host "[FASE 5] Criando COMET Bridge..." -ForegroundColor Yellow

$cometBridgeCode = @"
import json, subprocess, os
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib import request as urllib_request, error as urllib_error

PORT = 5000
OBSIDIAN_API = "http://127.0.0.1:27123"
OBSIDIAN_TOKEN = os.environ.get("OBSIDIAN_TOKEN", "$ObsidianToken")

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
    except Exception as e: return {"success": False, "error": str(e)}

def execute_powershell(command, timeout=60):
    try:
        result = subprocess.run(["powershell", "-Command", command], capture_output=True, text=True, timeout=timeout)
        return {"success": result.returncode == 0, "output": result.stdout, "error": result.stderr}
    except subprocess.TimeoutExpired: return {"success": False, "error": "Timeout"}
    except Exception as e: return {"success": False, "error": str(e)}

class UnifiedBridgeHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args): print(f"[{datetime.now().strftime('%H:%M:%S')}] {args[0]}")
    def send_json(self, data, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode("utf-8"))
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
    def get_body(self):
        cl = int(self.headers.get("Content-Length", 0))
        if cl > 0:
            body = self.rfile.read(cl).decode("utf-8")
            try: return json.loads(body)
            except: return body
        return {}
    def do_GET(self):
        path = self.path.split("?")[0]
        if path in ["/", "/health"]:
            obs = obsidian_request("GET", "/")
            self.send_json({"status": "online", "service": "MANUS-COMET-OBSIDIAN Bridge", "obsidian": "online" if obs.get("success") else "offline"})
        elif path.startswith("/obsidian/vault"):
            self.send_json(obsidian_request("GET", path.replace("/obsidian", "")))
        else: self.send_json({"error": "Not found"}, 404)
    def do_POST(self):
        path = self.path.split("?")[0]
        body = self.get_body()
        if path in ["/exec", "/powershell"]:
            cmd = body.get("command", "") if isinstance(body, dict) else ""
            if not cmd: self.send_json({"error": "No command"}, 400); return
            self.send_json(execute_powershell(cmd))
        elif path.startswith("/obsidian/vault/"):
            note = path.replace("/obsidian/vault/", "")
            content = body.get("content", "") if isinstance(body, dict) else body
            self.send_json(obsidian_request("PUT", f"/vault/{note}", content, "text/markdown"))
        else: self.send_json({"error": "Not found"}, 404)
    def do_PUT(self): self.do_POST()

if __name__ == "__main__":
    print("="*50)
    print("  MANUS-COMET-OBSIDIAN BRIDGE v1.0")
    print("="*50)
    print(f"Servidor: http://localhost:{PORT}")
    HTTPServer(("0.0.0.0", PORT), UnifiedBridgeHandler).serve_forever()
"@

$cometBridgeCode | Out-File -FilePath "$CometDir\manus_bridge_unified.py" -Encoding UTF8
Write-Host "  [OK] COMET Bridge criado" -ForegroundColor Green

Write-Host ""

# ============================================
# FASE 6: CRIAR SCRIPT DE INICIALIZAÇÃO
# ============================================
Write-Host "[FASE 6] Criando script de inicialização..." -ForegroundColor Yellow

$startupScript = @"
@echo off
title Sistema IA v3.1 - Inicializador
echo ============================================
echo   INICIANDO SISTEMA DE IA v3.1...
echo ============================================
echo.
echo [1/9] Abrindo Obsidian...
start "" "C:\Users\$Username\AppData\Local\Programs\Obsidian\Obsidian.exe"
timeout /t 15 /nobreak >nul
echo [2/9] Iniciando Ollama...
start "" "C:\Users\$Username\AppData\Local\Programs\Ollama\Ollama.exe"
timeout /t 5 /nobreak >nul
echo [3/9] Iniciando COMET Bridge...
start "COMET Bridge" cmd /c "cd /d C:\Users\$Username\COMET && python manus_bridge_unified.py"
echo       Aguardando COMET Bridge (health check)...
:wait_comet
timeout /t 2 /nobreak >nul
curl -s http://localhost:5000 >nul 2>&1
if errorlevel 1 goto wait_comet
echo       [OK] COMET Bridge online!
echo.
echo [4/9] Iniciando ngrok...
start "ngrok" cmd /c "ngrok http 5000 --url=$NgrokUrl"
timeout /t 5 /nobreak >nul
echo [5/9] Iniciando Obsidian Agent...
start "Obsidian Agent" cmd /c "cd /d C:\Users\$Username\obsidian-agente && python obsidian_agent.py"
timeout /t 3 /nobreak >nul
echo [6/9] Iniciando Hub Central...
start "Hub Central" cmd /c "cd /d C:\Users\$Username\obsidian-agente && python hub_central.py"
timeout /t 3 /nobreak >nul
echo [7/9] Iniciando Vision Server...
start "Vision Server" cmd /c "cd /d C:\Users\$Username\obsidian-agente && python vision_server.py"
timeout /t 3 /nobreak >nul
echo [8/9] Iniciando Frontend...
start "Frontend" cmd /c "cd /d C:\Users\$Username\obsidian-agente\frontend && npm run dev"
timeout /t 3 /nobreak >nul
echo [9/9] Iniciando Claude Code Terminal...
start "Claude Code" cmd /k "title Claude Code Terminal && echo Claude Code pronto!"
echo.
echo ============================================
echo   SISTEMA IA v3.1 INICIADO COM SUCESSO!
echo ============================================
echo   URL: $NgrokUrl
pause
"@

$startupScript | Out-File -FilePath "$CometDir\Iniciar_Sistema_IA.bat" -Encoding ASCII
Write-Host "  [OK] Script de inicialização criado" -ForegroundColor Green

Write-Host ""

# ============================================
# FINALIZAÇÃO
# ============================================
Write-Host "============================================" -ForegroundColor Green
Write-Host "  RESTAURAÇÃO CONCLUÍDA COM SUCESSO!" -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Green
Write-Host ""
Write-Host "  Próximos passos:" -ForegroundColor White
Write-Host "  1. Configure as credenciais (se ainda não fez)" -ForegroundColor Gray
Write-Host "  2. Instale Obsidian e Ollama" -ForegroundColor Gray
Write-Host "  3. Execute: $CometDir\Iniciar_Sistema_IA.bat" -ForegroundColor Gray
Write-Host ""

Set-Location $BaseDir
