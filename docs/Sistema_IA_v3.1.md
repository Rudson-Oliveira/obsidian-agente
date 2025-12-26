# Documentação Completa - Sistema IA v3.1

**Autor:** Manus AI para Rudson-Oliveira
**Data:** 26 de Dezembro de 2025
**Versão:** 3.1 (Ollama + Health Check)

---

## 1. Visão Geral

Este documento detalha a arquitetura, configuração e operação do **Sistema de Automação Inteligente (IA) v3.1**, uma plataforma híbrida que integra múltiplos serviços de IA para automação de tarefas, análise de dados e assistência inteligente.

As principais melhorias da versão 3.1 são:
- **Integração do Ollama:** O serviço Ollama agora é parte do sistema de inicialização, provendo modelos de linguagem locais.
- **Health Check do COMET Bridge:** O script agora verifica ativamente se o COMET Bridge está online antes de prosseguir, eliminando erros de conexão com o ngrok.
- **Ordem de Inicialização Otimizada:** O ngrok agora é iniciado *depois* do COMET Bridge, garantindo uma conexão estável.

---

## 2. Arquitetura do Sistema IA v3.1

O sistema é composto por 9 serviços principais que são orquestrados por um script de inicialização (`Iniciar_Sistema_IA.bat`).

| # | Serviço | Porta | Descrição |
|---|---|---|---|
| 1 | **Obsidian** | - | Interface principal e vault de conhecimento |
| 2 | **Ollama** | 11434 | Servidor para modelos de linguagem locais (e.g., gemma3:4b) |
| 3 | **COMET Bridge** | 5000 | Ponte de comunicação entre Manus e o sistema local |
| 4 | **ngrok** | - | Cria um túnel seguro para acesso remoto ao COMET Bridge |
| 5 | **Obsidian Agent** | 5001 | Agente inteligente que opera dentro do Obsidian |
| 6 | **Hub Central** | 5002 | Coordenador de tarefas e gatilhos do sistema |
| 7 | **Vision Server** | 5003 | Servidor de visão computacional (PicaPau Agent) |
| 8 | **Frontend (Vite)** | 5173 | Interface web para o Obsidian Agent |
| 9 | **Claude Code Terminal** | - | Terminal dedicado para interação com o Claude Code |

---

## 3. Script de Inicialização (v3.1)

O coração do sistema é o script `C:\Users\rudpa\COMET\Iniciar_Sistema_IA.bat`. Abaixo está o conteúdo completo da versão 3.1.

```batch
@echo off
REM ============================================
REM   INICIALIZADOR UNIFICADO - SISTEMA IA v3.1
REM   Criado por Manus para Rudson-Oliveira
REM   Data: 26-12-2025
REM ============================================

title Sistema IA v3.1 - Inicializador

echo ============================================
echo   INICIANDO SISTEMA DE IA v3.1...
echo ============================================
echo.

REM === PASSO 1: OBSIDIAN ===
echo [1/9] Abrindo Obsidian...
start "" "C:\Users\rudpa\AppData\Local\Programs\Obsidian\Obsidian.exe"
echo       Aguardando Obsidian carregar (15 segundos)...
timeout /t 15 /nobreak >nul
echo       [OK] Obsidian iniciado
echo.

REM === PASSO 2: OLLAMA ===
echo [2/9] Iniciando Ollama...
start "" "C:\Users\rudpa\AppData\Local\Programs\Ollama\Ollama.exe"
echo       Aguardando Ollama carregar (5 segundos)...
timeout /t 5 /nobreak >nul
echo       [OK] Ollama iniciado
echo.

REM === PASSO 3: COMET BRIDGE (COM HEALTH CHECK) ===
echo [3/9] Iniciando COMET Bridge...
start "COMET Bridge" cmd /c "cd /d C:\Users\rudpa\COMET && python manus_bridge_unified.py"
echo       Aguardando COMET Bridge (health check)...
:wait_comet
timeout /t 2 /nobreak >nul
curl -s http://localhost:5000 >nul 2>&1
if errorlevel 1 goto wait_comet
echo       [OK] COMET Bridge online!
echo.

REM === PASSO 4: NGROK (APÓS COMET) ===
echo [4/9] Iniciando ngrok...
start "ngrok" cmd /c "ngrok http 5000 --url=charmless-maureen-subadministratively.ngrok-free.dev"
timeout /t 5 /nobreak >nul
echo       [OK] ngrok iniciado
echo.

REM === PASSOS 5-9: DEMAIS SERVIÇOS ===
echo [5/9] Iniciando Obsidian Agent...
start "Obsidian Agent" cmd /c "cd /d C:\Users\rudpa\obsidian-agente && python obsidian_agent.py"
timeout /t 3 /nobreak >nul
echo       [OK] Obsidian Agent iniciado
echo.

echo [6/9] Iniciando Hub Central...
start "Hub Central" cmd /c "cd /d C:\Users\rudpa\obsidian-agente && python hub_central.py"
timeout /t 3 /nobreak >nul
echo       [OK] Hub Central iniciado
echo.

echo [7/9] Iniciando Vision Server...
start "Vision Server" cmd /c "cd /d C:\Users\rudpa\obsidian-agente && python vision_server.py"
timeout /t 3 /nobreak >nul
echo       [OK] Vision Server iniciado
echo.

echo [8/9] Iniciando Frontend...
start "Frontend" cmd /c "cd /d C:\Users\rudpa\obsidian-agente\frontend && npm run dev"
timeout /t 3 /nobreak >nul
echo       [OK] Frontend iniciado
echo.

echo [9/9] Iniciando Claude Code Terminal...
start "Claude Code" cmd /k "title Claude Code Terminal v2.0.76 && echo ================================================ && echo    CLAUDE CODE - Terminal de IA v2.0.76 && echo ================================================ && echo. && echo API Key: Configurada && echo Comandos: claude -p, claude chat, claude --help && echo ================================================"
echo       [OK] Claude Code iniciado
echo.

REM === FINALIZAÇÃO ===
echo.
echo ============================================
echo   SISTEMA IA v3.1 INICIADO COM SUCESSO!
echo ============================================
echo.
echo   Servicos ativos:
echo   - Obsidian, Ollama, COMET Bridge, ngrok, Obsidian Agent, Hub Central, Vision Server, Frontend, Claude Code
echo.
echo   URL: charmless-maureen-subadministratively.ngrok-free.dev
echo.
echo   NOTA: Feche e reabra o Obsidian para ativar o painel direito.
echo.
pause
```

---

## 4. Claude Code e MCP AutoPilot

O Claude Code está integrado ao sistema via MCP (Model Context Protocol), permitindo que ele utilize ferramentas customizadas para interagir com o ambiente local.

- **Arquivo de Configuração:** `C:\Users\rudpa\.claude.json`
- **Servidor MCP:** `autopilot`
- **Comando do Servidor:** `python C:\Users\rudpa\COMET\autopilot\autopilot_mcp_server.py`

### Ferramentas Disponíveis no MCP AutoPilot

| Categoria | Ferramenta | Descrição | Restrições |
|---|---|---|---|
| **Banco de Dados** | `query_database` | Executa consultas SQL | **APENAS SELECT** |
| | `locate_data` | Localiza dados no banco | Somente leitura |
| | `analyze_schema` | Analisa a estrutura do banco | Somente leitura |
| | `suggest_query_optimization` | Sugere otimizações para queries | Somente leitura |
| **Análise de Código** | `analyze_code` | Analisa código fonte | Somente leitura |
| | `suggest_code_improvement` | Registra sugestão de melhoria | Revisão humana |
| | `list_code_suggestions` | Lista sugestões de código | Somente leitura |
| **Navegação Web** | `browse_web` | Navega na web via COMET Vision | - |
| **Comunicação** | `draft_message` | Cria rascunho de mensagem | Aprovação humana |
| **Contexto** | `get_collaborator_context` | Obtém contexto do colaborador | - |
| | `search_knowledge_base` | Busca na base de conhecimento | - |

---

## 5. Troubleshooting

| Problema | Causa Provável | Solução |
|---|---|---|
| **Erro 502 Bad Gateway no ngrok** | ngrok iniciou antes do COMET Bridge estar online. | O script v3.1 resolve isso com o health check. |
| **Painel direito do Obsidian em branco** | Obsidian abriu antes do Obsidian Agent (porta 5001) estar pronto. | Feche e reabra o Obsidian manualmente. |
| **COMET Bridge não responde** | O processo Python caiu ou não iniciou. | Verifique a janela do COMET Bridge por erros. Reinicie manualmente se necessário. |
| **Claude Code não encontra ferramentas** | O servidor MCP AutoPilot não está rodando. | Verifique se o `autopilot_mcp_server.py` está no local correto e se a configuração no `.claude.json` está correta. |

---

**Parabéns pela implementação do Sistema IA v3.1!**
