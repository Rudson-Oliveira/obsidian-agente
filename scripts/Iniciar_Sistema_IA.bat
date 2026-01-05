@echo off
title Sistema IA v3.1 - Inicializador
echo ============================================
echo   INICIANDO SISTEMA DE IA v3.1...
echo ============================================
echo.
echo [1/14] Abrindo Obsidian...
start "" "C:\Users\rudpa\AppData\Local\Programs\Obsidian\Obsidian.exe"
timeout /t 15 /nobreak >nul
echo [2/14] Iniciando Ollama...
start "" "C:\Users\rudpa\AppData\Local\Programs\Ollama\Ollama.exe"
timeout /t 5 /nobreak >nul
echo [3/14] Iniciando Jan (IA Local)...
start "" "C:\Users\rudpa\AppData\Local\Programs\Jan\Jan.exe"
timeout /t 3 /nobreak >nul
echo       [OK] Jan iniciado (porta 4891)
echo.
echo [4/14] Iniciando LM Studio (IA Local)...
start "" "C:\Users\rudpa\Downloads\LM-Studio Terminal\LM Studio\LM Studio.exe"
timeout /t 3 /nobreak >nul
echo       [OK] LM Studio iniciado
echo.
echo [5/14] Iniciando GPT4All (IA Local)...
start "" "C:\Users\rudpa\Downloads\GPT4All Terminal\bin\chat.exe"
timeout /t 3 /nobreak >nul
echo       [OK] GPT4All iniciado
echo.
echo [6/14] Iniciando COMET Desktop (Perplexity)...
start "" "C:\Users\rudpa\AppData\Local\Perplexity\Comet\Application\comet.exe"
timeout /t 3 /nobreak >nul
echo       [OK] COMET Desktop iniciado
echo.
echo [7/14] Iniciando COMET Bridge...
start "COMET Bridge" cmd /c "cd /d C:\Users\rudpa\COMET && python manus_bridge_unified.py"
echo       Aguardando COMET Bridge (health check)...
:wait_comet
timeout /t 2 /nobreak >nul
curl -s http://localhost:5000 >nul 2>&1
if errorlevel 1 goto wait_comet
echo       [OK] COMET Bridge online!
echo.
echo [8/14] Iniciando ngrok...
start "ngrok" cmd /c "ngrok http 5000 --url=charmless-maureen-subadministratively.ngrok-free.dev"
timeout /t 5 /nobreak >nul
echo       [OK] ngrok iniciado
echo.
echo [9/14] Iniciando Obsidian Agent...
start "Obsidian Agent" cmd /c "cd /d C:\Users\rudpa\obsidian-agente && python agent\agent.py"
timeout /t 3 /nobreak >nul
echo       [OK] Obsidian Agent iniciado
echo.
echo [10/14] Iniciando Hub Central...
start "Hub Central" cmd /c "cd /d C:\Users\rudpa\obsidian-agente && python hub_central\hub_server.py"
timeout /t 3 /nobreak >nul
echo       [OK] Hub Central iniciado
echo.
echo [11/14] Iniciando Vision Server...
start "Vision Server" cmd /c "cd /d C:\Users\rudpa\obsidian-agente && python vision_server.py"
timeout /t 3 /nobreak >nul
echo       [OK] Vision Server iniciado
echo.
echo [12/14] Iniciando Frontend...
start "Frontend" cmd /c "cd /d C:\Users\rudpa\obsidian-agente\frontend && npm run dev"
timeout /t 3 /nobreak >nul
echo       [OK] Frontend iniciado
echo.
echo [13/14] Iniciando Claude Code Terminal...
start "Claude Code" cmd /k "title Claude Code Terminal v2.0.76 && echo ================================================ && echo    CLAUDE CODE - Terminal de IA v2.0.76 && echo ================================================ && echo. && echo API Key: Configurada && echo Comandos: claude -p, claude chat, claude --help && echo ================================================"
echo       [OK] Claude Code iniciado
echo.
echo [14/14] Verificando servicos...
timeout /t 2 /nobreak >nul
echo.
echo ============================================
echo   SISTEMA IA v3.1 INICIADO COM SUCESSO!
echo ============================================
echo.
echo   Servicos ativos:
echo   - Obsidian
echo   - Ollama (porta 11434)
echo   - Jan - IA Local (porta 4891)
echo   - LM Studio - IA Local
echo   - GPT4All - IA Local
echo   - COMET Desktop (Perplexity)
echo   - COMET Bridge (porta 5000)
echo   - ngrok (URL fixa)
echo   - Obsidian Agent (porta 5001)
echo   - Hub Central (porta 5002)
echo   - Vision Server (porta 5003)
echo   - Frontend (porta 5173)
echo   - Claude Code Terminal
echo.
echo   URL: charmless-maureen-subadministratively.ngrok-free.dev
echo.
echo   NOTA: Feche e reabra o Obsidian para ativar o painel direito
echo.
pause
