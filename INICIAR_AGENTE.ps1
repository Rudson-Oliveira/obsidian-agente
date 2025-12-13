# ============================================
# Script de Inicializacao Rapida
# Obsidian Agente - Desktop Agent
# ============================================

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Obsidian Agente - Iniciando" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Definir diretorio do agente
$agentDir = "$env:USERPROFILE\obsidian-agente\agent"

# Verificar se o diretorio existe
if (-not (Test-Path $agentDir)) {
    Write-Host "[ERRO] Agente nao encontrado!" -ForegroundColor Red
    Write-Host "Execute primeiro: INSTALAR_AGENTE.ps1" -ForegroundColor Yellow
    pause
    exit 1
}

# Ir para o diretorio do agente
Set-Location $agentDir

# Iniciar o agente
Write-Host "Iniciando Obsidian Desktop Agent..." -ForegroundColor Green
Write-Host ""
Write-Host "Copie a API Key que sera exibida abaixo!" -ForegroundColor Yellow
Write-Host ""

python agent.py
