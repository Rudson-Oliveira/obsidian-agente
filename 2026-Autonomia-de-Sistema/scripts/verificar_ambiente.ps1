# ============================================================
# SCRIPT DE VERIFICAÇÃO DO AMBIENTE
# 2026 - Autonomia de Sistema
# ============================================================

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  VERIFICAÇÃO DO AMBIENTE - 2026 Autonomia de Sistema" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

$Erros = 0
$Avisos = 0

# Função para testar porta
function Test-Port {
    param($Port, $Service)
    try {
        $tcp = New-Object System.Net.Sockets.TcpClient
        $tcp.Connect("localhost", $Port)
        $tcp.Close()
        return $true
    } catch {
        return $false
    }
}

# Verificar Docker
Write-Host "[1/5] Verificando Docker..." -ForegroundColor Yellow
$DockerRunning = docker info 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "  [OK] Docker esta rodando" -ForegroundColor Green
} else {
    Write-Host "  [ERRO] Docker nao esta rodando" -ForegroundColor Red
    $Erros++
}

# Verificar portas essenciais
Write-Host ""
Write-Host "[2/5] Verificando portas essenciais..." -ForegroundColor Yellow

$PortasEssenciais = @(
    @{Porta=5678; Servico="N8N"},
    @{Porta=11434; Servico="Ollama"},
    @{Porta=3002; Servico="Browser-Use"},
    @{Porta=5000; Servico="COMET Bridge"},
    @{Porta=3001; Servico="Grafana"},
    @{Porta=5432; Servico="PostgreSQL"},
    @{Porta=6379; Servico="Redis"}
)

foreach ($p in $PortasEssenciais) {
    if (Test-Port -Port $p.Porta -Service $p.Servico) {
        Write-Host "  [OK] $($p.Servico) (porta $($p.Porta))" -ForegroundColor Green
    } else {
        Write-Host "  [ERRO] $($p.Servico) (porta $($p.Porta)) - NAO ACESSIVEL" -ForegroundColor Red
        $Erros++
    }
}

# Verificar portas opcionais
Write-Host ""
Write-Host "[3/5] Verificando portas opcionais..." -ForegroundColor Yellow

$PortasOpcionais = @(
    @{Porta=4891; Servico="Jan"},
    @{Porta=1234; Servico="LM Studio"},
    @{Porta=5003; Servico="Vision Server"},
    @{Porta=9000; Servico="Portainer"},
    @{Porta=9090; Servico="Prometheus"}
)

foreach ($p in $PortasOpcionais) {
    if (Test-Port -Port $p.Porta -Service $p.Servico) {
        Write-Host "  [OK] $($p.Servico) (porta $($p.Porta))" -ForegroundColor Green
    } else {
        Write-Host "  [AVISO] $($p.Servico) (porta $($p.Porta)) - nao acessivel" -ForegroundColor Yellow
        $Avisos++
    }
}

# Verificar containers Docker
Write-Host ""
Write-Host "[4/5] Verificando containers Docker..." -ForegroundColor Yellow

$Containers = docker ps --format "{{.Names}}:{{.Status}}" 2>&1
$Unhealthy = $Containers | Where-Object { $_ -like "*unhealthy*" }
$Restarting = $Containers | Where-Object { $_ -like "*Restarting*" }

$TotalContainers = ($Containers | Measure-Object).Count
$UnhealthyCount = ($Unhealthy | Measure-Object).Count
$RestartingCount = ($Restarting | Measure-Object).Count

Write-Host "  Total de containers: $TotalContainers" -ForegroundColor Cyan
Write-Host "  Saudaveis: $($TotalContainers - $UnhealthyCount - $RestartingCount)" -ForegroundColor Green

if ($UnhealthyCount -gt 0) {
    Write-Host "  Unhealthy: $UnhealthyCount" -ForegroundColor Yellow
    $Avisos += $UnhealthyCount
}

if ($RestartingCount -gt 0) {
    Write-Host "  Restarting: $RestartingCount" -ForegroundColor Red
    $Erros += $RestartingCount
}

# Verificar ngrok
Write-Host ""
Write-Host "[5/5] Verificando ngrok..." -ForegroundColor Yellow

try {
    $NgrokResponse = Invoke-WebRequest -Uri "https://charmless-maureen-subadministratively.ngrok-free.dev" -TimeoutSec 5 -UseBasicParsing
    Write-Host "  [OK] ngrok esta acessivel" -ForegroundColor Green
} catch {
    Write-Host "  [AVISO] ngrok nao esta acessivel externamente" -ForegroundColor Yellow
    $Avisos++
}

# Resumo
Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  RESUMO DA VERIFICAÇÃO" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

if ($Erros -eq 0 -and $Avisos -eq 0) {
    Write-Host "  AMBIENTE 100% OPERACIONAL!" -ForegroundColor Green
    Write-Host "  Pronto para iniciar o projeto." -ForegroundColor Green
} elseif ($Erros -eq 0) {
    Write-Host "  AMBIENTE OPERACIONAL COM AVISOS" -ForegroundColor Yellow
    Write-Host "  Erros: $Erros | Avisos: $Avisos" -ForegroundColor Yellow
    Write-Host "  Pode prosseguir, mas verifique os avisos." -ForegroundColor Yellow
} else {
    Write-Host "  AMBIENTE COM PROBLEMAS" -ForegroundColor Red
    Write-Host "  Erros: $Erros | Avisos: $Avisos" -ForegroundColor Red
    Write-Host "  Corrija os erros antes de prosseguir." -ForegroundColor Red
}

Write-Host ""
