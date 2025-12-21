# Obsidian Agente V5.0 - Script de Inicializacao
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   OBSIDIAN AGENTE V5.0 - INICIANDO    " -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

$projectPath = "C:\Users\rudpa\obsidian-agente"
Set-Location $projectPath

# Parar processos anteriores
Write-Host "`n[1/4] Parando processos anteriores..." -ForegroundColor Yellow
Get-Process -Name python -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 2

# Iniciar Agent API
Write-Host "[2/4] Iniciando Agent API (porta 5001)..." -ForegroundColor Yellow
Start-Process -FilePath "python" -ArgumentList "agent/agent.py" -WorkingDirectory $projectPath -WindowStyle Hidden
Start-Sleep -Seconds 3

# Iniciar Frontend
Write-Host "[3/4] Iniciando Frontend (porta 5173)..." -ForegroundColor Yellow
Set-Location "$projectPath\frontend"
Start-Process -FilePath "cmd" -ArgumentList "/c npm run dev" -WindowStyle Hidden
Set-Location $projectPath
Start-Sleep -Seconds 3

# Iniciar COMET Bridge
Write-Host "[4/4] Iniciando COMET Bridge (porta 5000)..." -ForegroundColor Yellow
Start-Process -FilePath "python" -ArgumentList "agent/comet_bridge.py" -WorkingDirectory $projectPath -WindowStyle Hidden
Start-Sleep -Seconds 3

# Verificar status
Write-Host "`n========================================" -ForegroundColor Green
Write-Host "   VERIFICANDO SERVICOS...             " -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green

try {
    $health = Invoke-RestMethod -Uri "http://127.0.0.1:5001/health" -TimeoutSec 5
    Write-Host "Agent API: ONLINE (v$($health.version ))" -ForegroundColor Green
} catch {
    Write-Host "Agent API: OFFLINE" -ForegroundColor Red
}

try {
    $frontend = Invoke-WebRequest -Uri "http://127.0.0.1:5173" -TimeoutSec 5
    Write-Host "Frontend: ONLINE" -ForegroundColor Green
} catch {
    Write-Host "Frontend: OFFLINE" -ForegroundColor Red
}

Write-Host "`nSISTEMA PRONTO! Abra o Obsidian." -ForegroundColor Cyan
