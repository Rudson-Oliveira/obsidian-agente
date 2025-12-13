# ============================================
# Script de Instalacao Automatica
# Obsidian Agente - Desktop Agent
# ============================================

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Obsidian Agente - Instalacao" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Verificar se Git esta instalado
Write-Host "[1/5] Verificando Git..." -ForegroundColor Yellow
if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Host "[ERRO] Git nao esta instalado!" -ForegroundColor Red
    Write-Host "Por favor, instale o Git: https://git-scm.com/download/win" -ForegroundColor Red
    pause
    exit 1
}
Write-Host "[OK] Git encontrado!" -ForegroundColor Green
Write-Host ""

# Verificar se Python esta instalado
Write-Host "[2/5] Verificando Python..." -ForegroundColor Yellow
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "[ERRO] Python nao esta instalado!" -ForegroundColor Red
    Write-Host "Por favor, instale o Python 3.10+: https://www.python.org/downloads/" -ForegroundColor Red
    pause
    exit 1
}
$pythonVersion = python --version
Write-Host "[OK] Python encontrado: $pythonVersion" -ForegroundColor Green
Write-Host ""

# Definir diretorio de instalacao
$installDir = "$env:USERPROFILE\obsidian-agente"

# Verificar se o diretorio ja existe
if (Test-Path $installDir) {
    Write-Host "[3/5] Diretorio ja existe. Atualizando..." -ForegroundColor Yellow
    Set-Location $installDir
    git pull origin master
} else {
    Write-Host "[3/5] Clonando repositorio..." -ForegroundColor Yellow
    git clone https://github.com/Rudson-Oliveira/obsidian-agente.git $installDir
    Set-Location $installDir
}
Write-Host "[OK] Repositorio pronto!" -ForegroundColor Green
Write-Host ""

# Instalar dependencias Python
Write-Host "[4/5] Instalando dependencias Python..." -ForegroundColor Yellow
Set-Location "$installDir\agent"
python -m pip install --upgrade pip --quiet
pip install -r requirements.txt --quiet
Write-Host "[OK] Dependencias instaladas!" -ForegroundColor Green
Write-Host ""

# Iniciar o agente
Write-Host "[5/5] Iniciando Obsidian Desktop Agent..." -ForegroundColor Yellow
Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  AGENTE INICIADO COM SUCESSO!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "IMPORTANTE: Copie a API Key abaixo!" -ForegroundColor Yellow
Write-Host ""

# Executar o agente
python agent.py
