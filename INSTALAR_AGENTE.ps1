# ============================================
# Script de Instalação Automática
# Obsidian Agente - Desktop Agent
# ============================================

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Obsidian Agente - Instalação" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Verificar se Git está instalado
Write-Host "[1/5] Verificando Git..." -ForegroundColor Yellow
if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Git não está instalado!" -ForegroundColor Red
    Write-Host "Por favor, instale o Git: https://git-scm.com/download/win" -ForegroundColor Red
    pause
    exit 1
}
Write-Host "✅ Git encontrado!" -ForegroundColor Green
Write-Host ""

# Verificar se Python está instalado
Write-Host "[2/5] Verificando Python..." -ForegroundColor Yellow
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Python não está instalado!" -ForegroundColor Red
    Write-Host "Por favor, instale o Python 3.10+: https://www.python.org/downloads/" -ForegroundColor Red
    pause
    exit 1
}
$pythonVersion = python --version
Write-Host "✅ Python encontrado: $pythonVersion" -ForegroundColor Green
Write-Host ""

# Definir diretório de instalação
$installDir = "$env:USERPROFILE\obsidian-agente"

# Verificar se o diretório já existe
if (Test-Path $installDir) {
    Write-Host "[3/5] Diretório já existe. Atualizando..." -ForegroundColor Yellow
    Set-Location $installDir
    git pull origin master
} else {
    Write-Host "[3/5] Clonando repositório..." -ForegroundColor Yellow
    git clone https://github.com/Rudson-Oliveira/obsidian-agente.git $installDir
    Set-Location $installDir
}
Write-Host "✅ Repositório pronto!" -ForegroundColor Green
Write-Host ""

# Instalar dependências Python
Write-Host "[4/5] Instalando dependências Python..." -ForegroundColor Yellow
Set-Location "$installDir\agent"
python -m pip install --upgrade pip --quiet
pip install -r requirements.txt --quiet
Write-Host "✅ Dependências instaladas!" -ForegroundColor Green
Write-Host ""

# Iniciar o agente
Write-Host "[5/5] Iniciando Obsidian Desktop Agent..." -ForegroundColor Yellow
Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  AGENTE INICIADO COM SUCESSO!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "📋 IMPORTANTE: Copie a API Key abaixo!" -ForegroundColor Yellow
Write-Host ""

# Executar o agente
python agent.py
