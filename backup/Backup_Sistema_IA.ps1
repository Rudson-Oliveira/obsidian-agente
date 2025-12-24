# BACKUP COMPLETO - SISTEMA IA AUTONOMO
$BackupPath = "C:\Backup_Sistema_IA"
$timestamp = Get-Date -Format "yyyy-MM-dd_HH-mm"
$backupFolder = "$BackupPath\backup_$timestamp"

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  BACKUP SISTEMA IA AUTONOMO" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan

New-Item -ItemType Directory -Force -Path $backupFolder | Out-Null
New-Item -ItemType Directory -Force -Path "$backupFolder\COMET" | Out-Null
New-Item -ItemType Directory -Force -Path "$backupFolder\obsidian-agente" | Out-Null
New-Item -ItemType Directory -Force -Path "$backupFolder\config" | Out-Null
New-Item -ItemType Directory -Force -Path "$backupFolder\ngrok" | Out-Null

Write-Host "[1/5] Copiando COMET Bridge..." -ForegroundColor Yellow
Copy-Item -Path "C:\Users\rudpa\COMET\*" -Destination "$backupFolder\COMET" -Recurse -Force

Write-Host "[2/5] Copiando Obsidian Agent..." -ForegroundColor Yellow
Copy-Item -Path "C:\Users\rudpa\obsidian-agente\*" -Destination "$backupFolder\obsidian-agente" -Recurse -Force -Exclude node_modules,.git

Write-Host "[3/5] Copiando configuracoes..." -ForegroundColor Yellow
Copy-Item -Path "C:\Users\rudpa\.obsidian-agent\config.json" -Destination "$backupFolder\config\" -Force -ErrorAction SilentlyContinue
Copy-Item -Path "C:\Users\rudpa\AppData\Local\ngrok\ngrok.yml" -Destination "$backupFolder\ngrok\" -Force -ErrorAction SilentlyContinue
Copy-Item -Path "C:\Users\rudpa\obsidian-agente\frontend\.env" -Destination "$backupFolder\config\" -Force -ErrorAction SilentlyContinue

Write-Host "[4/5] Compactando..." -ForegroundColor Yellow
$zipPath = "$BackupPath\Sistema_IA_Backup_$timestamp.zip"
Compress-Archive -Path $backupFolder -DestinationPath $zipPath -Force

Write-Host "[5/5] Concluido!" -ForegroundColor Green
Write-Host "ZIP: $zipPath" -ForegroundColor White

