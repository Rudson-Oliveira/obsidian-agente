# ============================================================
# SCRIPT DE BACKUP DE ETAPA
# 2026 - Autonomia de Sistema
# ============================================================
# Uso: .\backup_etapa.ps1 -Etapa "01" -Descricao "Docker corrigido"
# ============================================================

param(
    [Parameter(Mandatory=$true)]
    [string]$Etapa,
    
    [Parameter(Mandatory=$true)]
    [string]$Descricao,
    
    [string]$BasePath = "C:\Users\rudpa\2026-Autonomia-de-Sistema"
)

# Configurações
$Data = Get-Date -Format "yyyy-MM-dd_HH-mm"
$BackupName = "BACKUP_ETAPA_${Etapa}_${Data}"
$BackupPath = "$BasePath\backups\$BackupName"

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  BACKUP DE ETAPA - 2026 Autonomia de Sistema" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Etapa: $Etapa" -ForegroundColor Yellow
Write-Host "Descricao: $Descricao" -ForegroundColor Yellow
Write-Host "Data: $Data" -ForegroundColor Yellow
Write-Host "Destino: $BackupPath" -ForegroundColor Yellow
Write-Host ""

# Criar diretório de backup
Write-Host "[1/6] Criando diretorio de backup..." -ForegroundColor Green
New-Item -ItemType Directory -Path $BackupPath -Force | Out-Null
New-Item -ItemType Directory -Path "$BackupPath\docker" -Force | Out-Null
New-Item -ItemType Directory -Path "$BackupPath\configs" -Force | Out-Null
New-Item -ItemType Directory -Path "$BackupPath\databases" -Force | Out-Null

# Backup dos containers Docker
Write-Host "[2/6] Salvando estado dos containers Docker..." -ForegroundColor Green
docker ps -a --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" > "$BackupPath\docker\containers_status.txt"
docker images --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}" > "$BackupPath\docker\images_list.txt"

# Backup das configurações do projeto
Write-Host "[3/6] Copiando configuracoes do projeto..." -ForegroundColor Green
if (Test-Path "$BasePath\configs") {
    Copy-Item -Path "$BasePath\configs\*" -Destination "$BackupPath\configs" -Recurse -Force
}

# Backup do docker-compose (se existir)
Write-Host "[4/6] Salvando docker-compose..." -ForegroundColor Green
$DockerComposePath = "C:\Users\rudpa\hospitalar-docker-upgrade"
if (Test-Path "$DockerComposePath\docker-compose*.yml") {
    Copy-Item -Path "$DockerComposePath\docker-compose*.yml" -Destination "$BackupPath\docker" -Force
}
if (Test-Path "$DockerComposePath\.env") {
    Copy-Item -Path "$DockerComposePath\.env" -Destination "$BackupPath\docker" -Force
}

# Criar arquivo de metadados
Write-Host "[5/6] Criando arquivo de metadados..." -ForegroundColor Green
$Metadata = @"
# BACKUP ETAPA $Etapa
# ==================

Data: $Data
Descricao: $Descricao
Criado por: Manus AI
Autorizado por: Rudson Oliveira

## Conteudo do Backup

- docker/containers_status.txt - Estado dos containers
- docker/images_list.txt - Lista de imagens
- docker/docker-compose*.yml - Arquivos de compose
- configs/ - Configuracoes do projeto
- databases/ - Dumps de banco (se aplicavel)

## Como Restaurar

1. Execute: .\scripts\restaurar_etapa.ps1 -Etapa "$Etapa" -BackupDate "$Data"
2. Ou manualmente: Copie os arquivos de volta para os locais originais

## Verificacao

Containers ativos no momento do backup:
$(docker ps --format "{{.Names}}" | Out-String)
"@

$Metadata | Out-File -FilePath "$BackupPath\METADATA.md" -Encoding UTF8

# Commit no Git
Write-Host "[6/6] Registrando backup no Git..." -ForegroundColor Green
Set-Location $BasePath
git add .
git commit -m "backup: Etapa $Etapa - $Descricao ($Data)"

Write-Host ""
Write-Host "============================================================" -ForegroundColor Green
Write-Host "  BACKUP CONCLUIDO COM SUCESSO!" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Green
Write-Host ""
Write-Host "Local: $BackupPath" -ForegroundColor Cyan
Write-Host ""
Write-Host "Para restaurar, execute:" -ForegroundColor Yellow
Write-Host ".\scripts\restaurar_etapa.ps1 -Etapa `"$Etapa`" -BackupDate `"$Data`"" -ForegroundColor White
