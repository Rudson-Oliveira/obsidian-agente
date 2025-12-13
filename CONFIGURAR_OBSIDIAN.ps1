# ============================================
# Script de Configuracao do Caminho do Obsidian
# Obsidian Agente - Desktop Agent
# ============================================

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Configuracao do Obsidian" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Caminhos comuns do Obsidian no Windows
$possiblePaths = @(
    "$env:LOCALAPPDATA\Programs\Obsidian\Obsidian.exe",
    "$env:LOCALAPPDATA\Obsidian\Obsidian.exe",
    "$env:ProgramFiles\Obsidian\Obsidian.exe",
    "${env:ProgramFiles(x86)}\Obsidian\Obsidian.exe"
)

Write-Host "Procurando Obsidian instalado..." -ForegroundColor Yellow
Write-Host ""

$obsidianPath = $null

# Procurar pelo Obsidian nos caminhos comuns
foreach ($path in $possiblePaths) {
    if (Test-Path $path) {
        $obsidianPath = $path
        Write-Host "[OK] Obsidian encontrado em:" -ForegroundColor Green
        Write-Host "     $path" -ForegroundColor White
        break
    }
}

# Se nao encontrou, pedir ao usuario
if (-not $obsidianPath) {
    Write-Host "[AVISO] Obsidian nao encontrado nos caminhos padrao." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Por favor, digite o caminho completo do Obsidian.exe:" -ForegroundColor Cyan
    Write-Host "(Exemplo: C:\Users\rudpa\AppData\Local\Programs\Obsidian\Obsidian.exe)" -ForegroundColor Gray
    Write-Host ""
    $obsidianPath = Read-Host "Caminho"
    
    if (-not (Test-Path $obsidianPath)) {
        Write-Host ""
        Write-Host "[ERRO] Caminho invalido ou arquivo nao encontrado!" -ForegroundColor Red
        pause
        exit 1
    }
}

Write-Host ""
Write-Host "Configurando agente..." -ForegroundColor Yellow

# Criar diretorio de configuracao se nao existir
$configDir = "$env:USERPROFILE\.obsidian-agent"
if (-not (Test-Path $configDir)) {
    New-Item -ItemType Directory -Path $configDir -Force | Out-Null
}

# Criar arquivo de configuracao JSON
$configPath = "$configDir\config.json"
$config = @{
    obsidian_path = $obsidianPath.Replace("\", "\\")
    vault_path = ""
} | ConvertTo-Json

$config | Out-File -FilePath $configPath -Encoding UTF8

Write-Host "[OK] Configuracao salva em:" -ForegroundColor Green
Write-Host "     $configPath" -ForegroundColor White
Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  CONFIGURACAO CONCLUIDA!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Agora reinicie o agente:" -ForegroundColor Yellow
Write-Host "1. Pressione Ctrl+C no terminal do agente" -ForegroundColor White
Write-Host "2. Execute: .\INICIAR_AGENTE.ps1" -ForegroundColor White
Write-Host ""
pause
