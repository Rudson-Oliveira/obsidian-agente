# Plano B - Inicialização Manual do Sistema IA v3.1

**Data:** 26 de Dezembro de 2025
**Versão:** 3.1

---

## Quando Usar Este Plano B

Use este guia quando:
- O script `Iniciar_Sistema_IA.bat` não funcionar
- Precisar iniciar serviços individualmente
- Quiser ter controle manual sobre cada serviço
- Precisar debugar algum serviço específico

---

## Script PowerShell Completo

Copie e cole no PowerShell (executar como Administrador):

```powershell
# ============================================
# PLANO B - INICIALIZAÇÃO MANUAL v3.1
# Sistema IA - Rudson Oliveira
# Data: 26/12/2025
# ============================================

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  PLANO B - INICIALIZAÇÃO MANUAL v3.1" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# 1. OBSIDIAN
Write-Host "[1/9] Iniciando Obsidian..." -ForegroundColor Yellow
Start-Process "C:\Users\rudpa\AppData\Local\Programs\Obsidian\Obsidian.exe"
Start-Sleep -Seconds 10
Write-Host "      [OK] Obsidian iniciado" -ForegroundColor Green

# 2. OLLAMA
Write-Host "[2/9] Iniciando Ollama..." -ForegroundColor Yellow
Start-Process "C:\Users\rudpa\AppData\Local\Programs\Ollama\Ollama.exe"
Start-Sleep -Seconds 5
Write-Host "      [OK] Ollama iniciado" -ForegroundColor Green

# 3. COMET BRIDGE
Write-Host "[3/9] Iniciando COMET Bridge..." -ForegroundColor Yellow
Start-Process cmd -ArgumentList "/c", "cd /d C:\Users\rudpa\COMET && python manus_bridge_unified.py" -WindowStyle Normal
Write-Host "      Aguardando COMET Bridge (health check)..." -ForegroundColor Gray
do {
    Start-Sleep -Seconds 2
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:5000" -UseBasicParsing -TimeoutSec 2 -ErrorAction SilentlyContinue
        $online = $true
    } catch {
        $online = $false
    }
} while (-not $online)
Write-Host "      [OK] COMET Bridge online!" -ForegroundColor Green

# 4. NGROK
Write-Host "[4/9] Iniciando ngrok..." -ForegroundColor Yellow
Start-Process cmd -ArgumentList "/c", "ngrok http 5000 --url=charmless-maureen-subadministratively.ngrok-free.dev" -WindowStyle Normal
Start-Sleep -Seconds 5
Write-Host "      [OK] ngrok iniciado" -ForegroundColor Green

# 5. OBSIDIAN AGENT
Write-Host "[5/9] Iniciando Obsidian Agent..." -ForegroundColor Yellow
Start-Process cmd -ArgumentList "/c", "cd /d C:\Users\rudpa\obsidian-agente && python obsidian_agent.py" -WindowStyle Normal
Start-Sleep -Seconds 3
Write-Host "      [OK] Obsidian Agent iniciado" -ForegroundColor Green

# 6. HUB CENTRAL
Write-Host "[6/9] Iniciando Hub Central..." -ForegroundColor Yellow
Start-Process cmd -ArgumentList "/c", "cd /d C:\Users\rudpa\obsidian-agente && python hub_central.py" -WindowStyle Normal
Start-Sleep -Seconds 3
Write-Host "      [OK] Hub Central iniciado" -ForegroundColor Green

# 7. VISION SERVER
Write-Host "[7/9] Iniciando Vision Server..." -ForegroundColor Yellow
Start-Process cmd -ArgumentList "/c", "cd /d C:\Users\rudpa\obsidian-agente && python vision_server.py" -WindowStyle Normal
Start-Sleep -Seconds 3
Write-Host "      [OK] Vision Server iniciado" -ForegroundColor Green

# 8. FRONTEND
Write-Host "[8/9] Iniciando Frontend..." -ForegroundColor Yellow
Start-Process cmd -ArgumentList "/c", "cd /d C:\Users\rudpa\obsidian-agente\frontend && npm run dev" -WindowStyle Normal
Start-Sleep -Seconds 5
Write-Host "      [OK] Frontend iniciado" -ForegroundColor Green

# 9. CLAUDE CODE TERMINAL
Write-Host "[9/9] Iniciando Claude Code Terminal..." -ForegroundColor Yellow
Start-Process cmd -ArgumentList "/k", "title Claude Code Terminal v2.0.76 && echo. && echo ================================================ && echo    CLAUDE CODE - Terminal de IA v2.0.76 && echo ================================================ && echo. && echo API Key: Configurada && echo Comandos: claude -p, claude chat, claude --help && echo ================================================"
Write-Host "      [OK] Claude Code iniciado" -ForegroundColor Green

# FINALIZAÇÃO
Write-Host ""
Write-Host "============================================" -ForegroundColor Green
Write-Host "  SISTEMA IA v3.1 INICIADO COM SUCESSO!" -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Green
Write-Host ""
Write-Host "  Servicos ativos:" -ForegroundColor White
Write-Host "  - Obsidian, Ollama, COMET Bridge, ngrok" -ForegroundColor Gray
Write-Host "  - Obsidian Agent, Hub Central, Vision Server" -ForegroundColor Gray
Write-Host "  - Frontend, Claude Code" -ForegroundColor Gray
Write-Host ""
Write-Host "  URL: charmless-maureen-subadministratively.ngrok-free.dev" -ForegroundColor Cyan
Write-Host ""
Write-Host "  NOTA: Feche e reabra o Obsidian para ativar o painel direito." -ForegroundColor Yellow
Write-Host ""
```

---

## Comandos Individuais (Copiar e Colar)

Se precisar iniciar apenas um serviço específico:

### 1. Obsidian
```powershell
Start-Process "C:\Users\rudpa\AppData\Local\Programs\Obsidian\Obsidian.exe"
```

### 2. Ollama
```powershell
Start-Process "C:\Users\rudpa\AppData\Local\Programs\Ollama\Ollama.exe"
```

### 3. COMET Bridge
```powershell
cd C:\Users\rudpa\COMET
python manus_bridge_unified.py
```

### 4. ngrok
```powershell
ngrok http 5000 --url=charmless-maureen-subadministratively.ngrok-free.dev
```

### 5. Obsidian Agent
```powershell
cd C:\Users\rudpa\obsidian-agente
python obsidian_agent.py
```

### 6. Hub Central
```powershell
cd C:\Users\rudpa\obsidian-agente
python hub_central.py
```

### 7. Vision Server
```powershell
cd C:\Users\rudpa\obsidian-agente
python vision_server.py
```

### 8. Frontend
```powershell
cd C:\Users\rudpa\obsidian-agente\frontend
npm run dev
```

### 9. Claude Code
```powershell
claude chat
```

---

## Verificação de Serviços

Para verificar se os serviços estão rodando:

```powershell
# Verificar portas ativas
netstat -an | findstr "5000 5001 5002 5003 5173 11434"

# Testar COMET Bridge
Invoke-WebRequest -Uri "http://localhost:5000" -UseBasicParsing

# Testar Ollama
Invoke-WebRequest -Uri "http://localhost:11434" -UseBasicParsing

# Testar Frontend
Invoke-WebRequest -Uri "http://localhost:5173" -UseBasicParsing
```

---

## Parar Todos os Serviços

```powershell
# Parar processos Python (servidores)
Get-Process python -ErrorAction SilentlyContinue | Stop-Process -Force

# Parar ngrok
Get-Process ngrok -ErrorAction SilentlyContinue | Stop-Process -Force

# Parar Node (Frontend)
Get-Process node -ErrorAction SilentlyContinue | Stop-Process -Force

Write-Host "Todos os serviços foram parados." -ForegroundColor Yellow
```

---

## Portas e Serviços

| Serviço | Porta | Verificação |
|---------|-------|-------------|
| COMET Bridge | 5000 | `curl http://localhost:5000` |
| Obsidian Agent | 5001 | `curl http://localhost:5001` |
| Hub Central | 5002 | `curl http://localhost:5002` |
| Vision Server | 5003 | `curl http://localhost:5003` |
| Frontend | 5173 | `curl http://localhost:5173` |
| Ollama | 11434 | `curl http://localhost:11434` |

---

**Criado por Manus AI para Rudson-Oliveira**
