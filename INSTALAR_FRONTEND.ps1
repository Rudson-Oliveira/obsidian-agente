# ============================================
# Script de Instalacao do Frontend
# Obsidian Agente - Aplicacao Web
# ============================================

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Obsidian Agente - Frontend" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Verificar se Node.js esta instalado
Write-Host "[1/3] Verificando Node.js..." -ForegroundColor Yellow
if (-not (Get-Command node -ErrorAction SilentlyContinue)) {
    Write-Host "[ERRO] Node.js nao esta instalado!" -ForegroundColor Red
    Write-Host "Por favor, instale o Node.js 18+: https://nodejs.org/" -ForegroundColor Red
    pause
    exit 1
}
$nodeVersion = node --version
Write-Host "[OK] Node.js encontrado: $nodeVersion" -ForegroundColor Green
Write-Host ""

# Definir diretorio do frontend
$frontendDir = "$env:USERPROFILE\obsidian-agente\frontend"

# Verificar se o diretorio existe
if (-not (Test-Path $frontendDir)) {
    Write-Host "[ERRO] Frontend nao encontrado!" -ForegroundColor Red
    Write-Host "Execute primeiro: INSTALAR_AGENTE.ps1" -ForegroundColor Yellow
    pause
    exit 1
}

# Ir para o diretorio do frontend
Set-Location $frontendDir

# Instalar dependencias
Write-Host "[2/3] Instalando dependencias do frontend..." -ForegroundColor Yellow
npm install
Write-Host "[OK] Dependencias instaladas!" -ForegroundColor Green
Write-Host ""

# Iniciar o servidor de desenvolvimento
Write-Host "[3/3] Iniciando aplicacao web..." -ForegroundColor Yellow
Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  APLICACAO WEB INICIADA!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Acesse: http://localhost:5173" -ForegroundColor Cyan
Write-Host "Cole a API Key do agente quando solicitado" -ForegroundColor Yellow
Write-Host ""

npm run dev
