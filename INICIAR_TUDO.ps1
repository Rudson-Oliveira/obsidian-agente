# ====================================================================
# OBSIDIAN AGENTE - INICIALIZADOR AUTOMATICO COMPLETO
# ====================================================================
# Este script inicia automaticamente o agente e o frontend
# ====================================================================

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host " OBSIDIAN AGENTE - INICIALIZADOR" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Verificar se está no diretório correto
$projectPath = "C:\Users\rudpa\obsidian-agente"
if (-not (Test-Path $projectPath)) {
    Write-Host "[ERRO] Diretório do projeto não encontrado: $projectPath" -ForegroundColor Red
    Write-Host "Execute primeiro o script INSTALAR_AGENTE.ps1" -ForegroundColor Yellow
    pause
    exit 1
}

cd $projectPath

# ====================================================================
# ETAPA 1: Iniciar o Agente Backend
# ====================================================================

Write-Host "[1/3] Iniciando Agente Backend..." -ForegroundColor Yellow

# Verificar se Python está instalado
try {
    $pythonVersion = python --version 2>&1
    Write-Host "[OK] Python encontrado: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "[ERRO] Python não encontrado. Instale Python 3.8+" -ForegroundColor Red
    pause
    exit 1
}

# Iniciar agente em novo terminal
Write-Host "[INFO] Abrindo terminal para o agente..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$projectPath\agent'; python agent.py"

# Aguardar agente iniciar
Write-Host "[INFO] Aguardando agente inicializar (5 segundos)..." -ForegroundColor Cyan
Start-Sleep -Seconds 5

# ====================================================================
# ETAPA 2: Iniciar o Frontend
# ====================================================================

Write-Host ""
Write-Host "[2/3] Iniciando Frontend..." -ForegroundColor Yellow

# Verificar se Node.js está instalado
try {
    $nodeVersion = node --version 2>&1
    Write-Host "[OK] Node.js encontrado: $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "[ERRO] Node.js não encontrado. Instale Node.js 18+" -ForegroundColor Red
    pause
    exit 1
}

# Verificar se dependências estão instaladas
if (-not (Test-Path "$projectPath\frontend\node_modules")) {
    Write-Host "[INFO] Instalando dependências do frontend..." -ForegroundColor Cyan
    cd "$projectPath\frontend"
    npm install
}

# Iniciar frontend em novo terminal
Write-Host "[INFO] Abrindo terminal para o frontend..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$projectPath\frontend'; npm run dev"

# Aguardar frontend iniciar
Write-Host "[INFO] Aguardando frontend inicializar (10 segundos)..." -ForegroundColor Cyan
Start-Sleep -Seconds 10

# ====================================================================
# ETAPA 3: Abrir Navegador
# ====================================================================

Write-Host ""
Write-Host "[3/3] Abrindo navegador..." -ForegroundColor Yellow

# Abrir navegador automaticamente
Start-Process "http://localhost:5173"

# ====================================================================
# FINALIZAÇÃO
# ====================================================================

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host " SISTEMA INICIADO COM SUCESSO!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "IMPORTANTE:" -ForegroundColor Yellow
Write-Host "- Terminal 1: Agente Backend (porta 5001)" -ForegroundColor White
Write-Host "- Terminal 2: Frontend (porta 5173)" -ForegroundColor White
Write-Host "- Navegador: http://localhost:5173" -ForegroundColor White
Write-Host ""
Write-Host "PROXIMOS PASSOS:" -ForegroundColor Cyan
Write-Host "1. Copie a API Key exibida no terminal do agente" -ForegroundColor White
Write-Host "2. Cole a API Key na interface web" -ForegroundColor White
Write-Host "3. Comece a usar os comandos!" -ForegroundColor White
Write-Host ""
Write-Host "Para parar o sistema:" -ForegroundColor Yellow
Write-Host "- Pressione Ctrl+C em cada terminal" -ForegroundColor White
Write-Host ""
Write-Host "Pressione qualquer tecla para fechar este terminal..." -ForegroundColor Gray
pause
