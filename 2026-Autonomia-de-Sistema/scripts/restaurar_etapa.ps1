# ============================================================
# SCRIPT DE RESTAURAÇÃO DE ETAPA
# 2026 - Autonomia de Sistema
# ============================================================
# Uso: .\restaurar_etapa.ps1 -Etapa "01" -BackupDate "2026-01-05_10-30"
# ============================================================

param(
    [Parameter(Mandatory=$true)]
    [string]$Etapa,
    
    [string]$BackupDate,
    
    [string]$BasePath = "C:\Users\rudpa\2026-Autonomia-de-Sistema"
)

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  RESTAURAÇÃO DE ETAPA - 2026 Autonomia de Sistema" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Encontrar backup
$BackupsPath = "$BasePath\backups"
if ($BackupDate) {
    $BackupName = "BACKUP_ETAPA_${Etapa}_${BackupDate}"
    $BackupPath = "$BackupsPath\$BackupName"
} else {
    # Encontrar o backup mais recente da etapa
    $Backups = Get-ChildItem -Path $BackupsPath -Directory | Where-Object { $_.Name -like "BACKUP_ETAPA_${Etapa}_*" } | Sort-Object Name -Descending
    if ($Backups.Count -eq 0) {
        Write-Host "ERRO: Nenhum backup encontrado para a Etapa $Etapa" -ForegroundColor Red
        exit 1
    }
    $BackupPath = $Backups[0].FullName
    $BackupName = $Backups[0].Name
}

if (-not (Test-Path $BackupPath)) {
    Write-Host "ERRO: Backup nao encontrado: $BackupPath" -ForegroundColor Red
    exit 1
}

Write-Host "Backup encontrado: $BackupName" -ForegroundColor Yellow
Write-Host "Caminho: $BackupPath" -ForegroundColor Yellow
Write-Host ""

# Confirmação
Write-Host "ATENCAO: Esta operacao ira restaurar o sistema para o estado da Etapa $Etapa" -ForegroundColor Red
$Confirm = Read-Host "Deseja continuar? (S/N)"
if ($Confirm -ne "S" -and $Confirm -ne "s") {
    Write-Host "Operacao cancelada." -ForegroundColor Yellow
    exit 0
}

Write-Host ""
Write-Host "[1/4] Lendo metadados do backup..." -ForegroundColor Green
if (Test-Path "$BackupPath\METADATA.md") {
    Get-Content "$BackupPath\METADATA.md" | Select-Object -First 15
}

Write-Host ""
Write-Host "[2/4] Restaurando configuracoes..." -ForegroundColor Green
if (Test-Path "$BackupPath\configs") {
    Copy-Item -Path "$BackupPath\configs\*" -Destination "$BasePath\configs" -Recurse -Force
    Write-Host "  - Configuracoes restauradas" -ForegroundColor Cyan
}

Write-Host ""
Write-Host "[3/4] Restaurando docker-compose..." -ForegroundColor Green
$DockerComposePath = "C:\Users\rudpa\hospitalar-docker-upgrade"
if (Test-Path "$BackupPath\docker\docker-compose*.yml") {
    Copy-Item -Path "$BackupPath\docker\docker-compose*.yml" -Destination $DockerComposePath -Force
    Write-Host "  - docker-compose restaurado" -ForegroundColor Cyan
}
if (Test-Path "$BackupPath\docker\.env") {
    Copy-Item -Path "$BackupPath\docker\.env" -Destination $DockerComposePath -Force
    Write-Host "  - .env restaurado" -ForegroundColor Cyan
}

Write-Host ""
Write-Host "[4/4] Reiniciando containers Docker..." -ForegroundColor Green
Set-Location $DockerComposePath
Write-Host "  Executando: docker-compose down" -ForegroundColor Cyan
docker-compose down
Write-Host "  Executando: docker-compose up -d" -ForegroundColor Cyan
docker-compose up -d

Write-Host ""
Write-Host "============================================================" -ForegroundColor Green
Write-Host "  RESTAURAÇÃO CONCLUÍDA!" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Green
Write-Host ""
Write-Host "O sistema foi restaurado para o estado da Etapa $Etapa" -ForegroundColor Cyan
Write-Host ""
Write-Host "Verifique os containers com: docker ps" -ForegroundColor Yellow
