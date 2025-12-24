# RESTAURACAO COMPLETA - SISTEMA IA AUTONOMO
# Criado por Manus para Rudson-Oliveira
# Data: 24-12-2025

param(
    [Parameter(Mandatory=$true)][string]$BackupZip,
    [string]$TargetUser = $env:USERNAME
)

$tempFolder = "$env:TEMP\restore_sistema_ia_$(Get-Random)"
$userHome = "C:\Users\$TargetUser"

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  RESTAURACAO SISTEMA IA AUTONOMO" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan

if (-not (Test-Path $BackupZip)) { Write-Host "ERRO: Backup nao encontrado!" -ForegroundColor Red; exit 1 }

Write-Host "[1/6] Extraindo backup..." -ForegroundColor Yellow
Expand-Archive -Path $BackupZip -DestinationPath $tempFolder -Force
$backupContent = Get-ChildItem $tempFolder | Select-Object -First 1
$backupPath = $backupContent.FullName

Write-Host "[2/6] Criando estrutura..." -ForegroundColor Yellow
New-Item -ItemType Directory -Force -Path "$userHome\COMET" | Out-Null
New-Item -ItemType Directory -Force -Path "$userHome\obsidian-agente" | Out-Null
New-Item -ItemType Directory -Force -Path "$userHome\.obsidian-agent" | Out-Null
New-Item -ItemType Directory -Force -Path "$userHome\AppData\Local\ngrok" | Out-Null

Write-Host "[3/6] Restaurando COMET..." -ForegroundColor Yellow
Copy-Item -Path "$backupPath\COMET\*" -Destination "$userHome\COMET" -Recurse -Force

Write-Host "[4/6] Restaurando Agent..." -ForegroundColor Yellow
Copy-Item -Path "$backupPath\obsidian-agente\*" -Destination "$userHome\obsidian-agente" -Recurse -Force

Write-Host "[5/6] Restaurando configs..." -ForegroundColor Yellow
if (Test-Path "$backupPath\config\config.json") { Copy-Item -Path "$backupPath\config\config.json" -Destination "$userHome\.obsidian-agent\config.json" -Force }
if (Test-Path "$backupPath\ngrok\ngrok.yml") { Copy-Item -Path "$backupPath\ngrok\ngrok.yml" -Destination "$userHome\AppData\Local\ngrok\ngrok.yml" -Force }
if (Test-Path "$backupPath\config\.env") { Copy-Item -Path "$backupPath\config\.env" -Destination "$userHome\obsidian-agente\frontend\.env" -Force }

Write-Host "[6/6] Configurando startup..." -ForegroundColor Yellow
$startupPath = "$userHome\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup"
$WshShell = New-Object -ComObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut("$startupPath\Sistema-IA-Unificado.lnk")
$Shortcut.TargetPath = "$userHome\COMET\Iniciar_Sistema_IA.bat"
$Shortcut.WorkingDirectory = "$userHome\COMET"
$Shortcut.Save()

Remove-Item -Path $tempFolder -Recurse -Force

Write-Host "============================================" -ForegroundColor Green
Write-Host "  RESTAURACAO CONCLUIDA!" -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Green
Write-Host "Reinicie o PC para iniciar automaticamente" -ForegroundColor White
