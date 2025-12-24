# Obsidian Agent v5.0

Agente inteligente para automacao do Obsidian com integracao COMET Bridge.

## Status do Sistema

| Componente | Porta | Status |
|------------|-------|--------|
| Obsidian Agent | 5001 | Backend API |
| Frontend Agent | 5173 | Interface Web |
| COMET Bridge | 5000 | Ponte Manus |
| ngrok (FIXO) | - | charmless-maureen-subadministratively.ngrok-free.dev |

## Instalacao Rapida

### 1. Iniciar Backend:
cd agent
python agent.py

### 2. Iniciar Frontend:
cd frontend
npm install
npm run dev

### 3. Abrir no Obsidian:
- Ctrl+P -> Open Gate -> Obsidian Agente V5.0
- URL: http://localhost:5173

## Inicializacao Automatica

O sistema pode ser iniciado automaticamente ao ligar o PC:
- Script: C:\Users\rudpa\COMET\Iniciar_Sistema_IA.bat
- Health Check: C:\Users\rudpa\COMET\Health_Check.ps1

## Estrutura do Projeto

obsidian-agente/
├── agent/           # Backend Python (Flask)
│   ├── agent.py
│   └── intelligent_agent.py
├── frontend/        # Frontend React (Vite)
│   ├── src/
│   └── dist/
└── docs/            # Documentacao

## API Endpoints

| Endpoint | Metodo | Descricao |
|----------|--------|----------|
| /health | GET | Status do sistema |
| /ai/status | GET | Status da IA |
| /ai/chat | POST | Chat com IA |
| /obsidian/notes | GET | Listar notas |
| /obsidian/note/search | POST | Buscar notas |
| /obsidian/note/create | POST | Criar nota |

## Changelog

### v5.0.0 (24-12-2025)
- URL ngrok fixa (nunca muda)
- Script de inicializacao automatica
- Health Check com auto-recuperacao
- Frontend integrado com Open Gate
- Documentacao completa V4

## Credenciais

Ver arquivo de configuracao: ~/.obsidian-agent/config.json

## Autor

Rudson Oliveira - Projeto COMET/Manus
