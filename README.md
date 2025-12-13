# Obsidian Agente 🧠

**Seu assistente inteligente para automação e gerenciamento de conhecimento no Obsidian.**

Uma solução completa que integra um Agente de Desktop local com uma aplicação web para automação total do seu vault Obsidian.

## 🎯 O que é?

Obsidian Agente é um sistema de automação que permite:

- ✅ Controlar o Obsidian via comandos em linguagem natural
- ✅ Automatizar tarefas complexas no seu vault
- ✅ Sincronizar configurações via GitHub
- ✅ Comunicação segura entre aplicação web e agente local
- ✅ API REST poderosa para extensões

## 🏗️ Arquitetura

```
┌─────────────────────────────────────────────────────┐
│         Aplicação Web (React + TypeScript)          │
│     https://obsidianchat-csvxutae.manus.space/     │
└────────────────────┬────────────────────────────────┘
                     │ HTTP/REST
                     ↓
┌─────────────────────────────────────────────────────┐
│    Agente de Desktop (Python + Flask)               │
│         http://localhost:5001                       │
└────────────────────┬────────────────────────────────┘
                     │ Controle Local
                     ↓
┌─────────────────────────────────────────────────────┐
│              Obsidian (Local)                       │
│          Seu Vault de Conhecimento                  │
└─────────────────────────────────────────────────────┘
```

## 📁 Estrutura do Projeto

```
obsidian-agente/
├── frontend/              # Aplicação web React
│   ├── src/
│   ├── public/
│   └── package.json
├── agent/                 # Agente de Desktop Python
│   ├── agent.py
│   ├── requirements.txt
│   └── config.json
├── docs/                  # Documentação
│   ├── API.md
│   ├── SETUP.md
│   └── TROUBLESHOOTING.md
├── README.md
└── .gitignore
```

## 🚀 Quick Start

### Pré-requisitos

- Node.js 18+
- Python 3.10+
- Obsidian instalado

### Instalação do Agente

```bash
cd agent
pip install -r requirements.txt
python agent.py
```

O agente iniciará em `http://localhost:5001`

### Instalação da Aplicação Web

```bash
cd frontend
npm install
npm run dev
```

## 🔌 API Endpoints

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/health` | Verifica se o agente está online |
| POST | `/obsidian/open` | Abre o Obsidian |
| POST | `/file/read` | Lê um arquivo |
| POST | `/file/write` | Escreve em um arquivo |
| POST | `/command/execute` | Executa um comando |

## 📚 Documentação

- [Setup Completo](./docs/SETUP.md)
- [Referência da API](./docs/API.md)
- [Troubleshooting](./docs/TROUBLESHOOTING.md)

## 🔒 Segurança

- Agente roda apenas em `localhost`
- API Key obrigatória para operações sensíveis
- CORS configurado para origens específicas
- Sem compartilhamento de credenciais

## 📝 Licença

Propriedade de Rudson-Oliveira

## 🤝 Desenvolvido com

- **Frontend**: React, TypeScript, Vite, TailwindCSS
- **Backend**: Python, Flask, Flask-CORS
- **Integração**: Obsidian API, GitHub

---

**Desenvolvido para automação inteligente do Obsidian** 🚀
