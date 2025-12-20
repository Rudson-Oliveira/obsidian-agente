\# Obsidian Agente V5.0 - Script de Inicializacao Completa
# Este script inicia todos os servicos e abre o Obsidian + Agente

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   Obsidian Agente V5.0 - Iniciando    " -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

# Diretorio do projeto
\ = "C:\Users\rudpa\obsidian-agente"

# 1. Iniciar COMET Bridge (se nao estiver rodando)
\ = Get-NetTCPConnection -LocalPort 5000 -ErrorAction SilentlyContinue
if (-not \) {
    Write-Host "[1/5] Iniciando COMET Bridge..." -ForegroundColor Yellow
    Start-Process -FilePath python -ArgumentList "\\agent\comet_bridge.py" -WindowStyle Hidden
    Start-Sleep -Seconds 3
} else {
    Write-Host "[1/5] COMET Bridge ja esta rodando" -ForegroundColor Green
}

# 2. Iniciar Agent API (se nao estiver rodando)
\ = Get-NetTCPConnection -LocalPort 5001 -ErrorAction SilentlyContinue
if (-not \) {
    Write-Host "[2/5] Iniciando Agent API..." -ForegroundColor Yellow
    Start-Process -FilePath python -ArgumentList "\\agent\agent.py" -WorkingDirectory "\\agent" -WindowStyle Hidden
    Start-Sleep -Seconds 3
} else {
    Write-Host "[2/5] Agent API ja esta rodando" -ForegroundColor Green
}

# 3. Iniciar Frontend (se nao estiver rodando)
\ = Get-NetTCPConnection -LocalPort 5173 -ErrorAction SilentlyContinue
if (-not \) {
    Write-Host "[3/5] Iniciando Frontend..." -ForegroundColor Yellow
    Start-Process cmd -ArgumentList "/c", "cd \\frontend && npm run dev -- --host 0.0.0.0" -WindowStyle Hidden
    Start-Sleep -Seconds 5
} else {
    Write-Host "[3/5] Frontend ja esta rodando" -ForegroundColor Green
}

# 4. Abrir Obsidian (se nao estiver rodando)
\ = Get-Process -Name Obsidian -ErrorAction SilentlyContinue
if (-not \) {
    Write-Host "[4/5] Abrindo Obsidian..." -ForegroundColor Yellow
    Start-Process -FilePath "C:\Users\rudpa\AppData\Local\Programs\Obsidian\Obsidian.exe"
    Start-Sleep -Seconds 5
} else {
    Write-Host "[4/5] Obsidian ja esta aberto" -ForegroundColor Green
}

# 5. Verificar servicos
Write-Host "[5/5] Verificando servicos..." -ForegroundColor Yellow
Start-Sleep -Seconds 2

try {
    \ = Invoke-RestMethod -Uri "http://127.0.0.1:5001/health" -Method GET -TimeoutSec 5
    Write-Host "" -ForegroundColor White
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "   Obsidian Agente V5.0 - ONLINE!      " -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "" -ForegroundColor White
    Write-Host "Servicos disponiveis:" -ForegroundColor Cyan
    Write-Host "  - Agent API:     http://127.0.0.1:5001" -ForegroundColor White
    Write-Host "  - Frontend:      http://127.0.0.1:5173" -ForegroundColor White
    Write-Host "  - COMET Bridge:  http://127.0.0.1:5000" -ForegroundColor White
    Write-Host "  - Obsidian API:  http://127.0.0.1:27123" -ForegroundColor White
    Write-Host "" -ForegroundColor White
} catch {
    Write-Host "Aguardando servicos iniciarem..." -ForegroundColor Yellow
}
