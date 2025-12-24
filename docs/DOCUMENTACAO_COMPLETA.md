# 🚀 Sistema IA Autônomo - Documentação Completa

**Autor:** Manus para Rudson Oliveira  
**Data:** 24 de Dezembro de 2025  
**Versão:** 3.0

---

## 📋 Índice

1. [Visão Geral do Sistema](#1-visão-geral-do-sistema)
2. [Componentes Principais](#2-componentes-principais)
3. [Hub Central: O Cérebro do Sistema](#3-hub-central-o-cérebro-do-sistema)
4. [Sistema de Gatilhos Automatizados](#4-sistema-de-gatilhos-automatizados)
5. [Conectores de Armazenamento](#5-conectores-de-armazenamento)
6. [Motor de Execução e Roteamento de IA](#6-motor-de-execução-e-roteamento-de-ia)
7. [API Completa do Hub Central](#7-api-completa-do-hub-central)
8. [Sistema de Backup e Restauração](#8-sistema-de-backup-e-restauração)
9. [Estrutura de Arquivos](#9-estrutura-de-arquivos)
10. [Comandos Úteis](#10-comandos-úteis)
11. [Próximos Passos](#11-próximos-passos)

---

## 1. Visão Geral do Sistema

O **Sistema IA Autônomo** é um ecossistema completo de inteligência artificial integrado ao Obsidian, projetado para funcionar de forma autônoma com:

- **Auto-inicialização** com o Windows
- **Auto-recuperação** de falhas
- **Roteamento inteligente** de consultas para diferentes IAs
- **Hub Central** para coordenação de ações e gatilhos
- **Multi-storage** para escalabilidade de dados

### URL Fixa do Sistema

```
https://charmless-maureen-subadministratively.ngrok-free.dev
```

> **Importante:** Este domínio é estático e nunca muda, permitindo integrações permanentes com N8N, WhatsApp, webhooks externos, etc.

---

## 2. Componentes Principais

O sistema é composto por 6 componentes que iniciam automaticamente:

| Componente | Porta | Função | Status |
|------------|-------|--------|--------|
| **Obsidian** | 27124 | Base de conhecimento com Local REST API | ✅ Ativo |
| **ngrok** | 4040 | Túnel público com domínio fixo | ✅ Ativo |
| **COMET Bridge** | 5000 | Ponte entre Manus e Obsidian | ✅ Ativo |
| **Obsidian Agent** | 5001 | Agente inteligente com lógica de decisão | ✅ Ativo |
| **Hub Central** | 5002 | Cérebro do sistema, coordena ações e gatilhos | ✅ Ativo |
| **Frontend** | 5173 | Interface de chat integrada ao Obsidian | ✅ Ativo |

### Ordem de Inicialização

1. Obsidian (15 segundos de espera)
2. ngrok com domínio fixo (5 segundos)
3. COMET Bridge (10 segundos)
4. Obsidian Agent (5 segundos)
5. Hub Central (5 segundos)
6. Frontend

---

## 3. Hub Central: O Cérebro do Sistema

O **Hub Central v1.1** é o componente que orquestra todo o ecossistema. Ele é responsável por:

- **Gerenciar Gatilhos:** Executar ações automáticas baseadas em tempo, eventos ou webhooks
- **Coordenar Agentes:** Distribuir tarefas para diferentes IAs ou serviços
- **Gerenciar Armazenamento:** Salvar e carregar dados de múltiplos destinos
- **Processar Eventos:** Reagir a ações do sistema e do usuário

### Arquitetura do Hub Central

```
┌─────────────────────────────────────────────────────────────────┐
│                         HUB CENTRAL v1.1                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────┐    ┌─────────────────┐                     │
│  │   hub_central   │◄──►│   hub_server    │◄──► API REST        │
│  │     (Core)      │    │    (Flask)      │     (porta 5002)    │
│  └─────────────────┘    └─────────────────┘                     │
│           │                     │                               │
│           ▼                     ▼                               │
│  ┌─────────────────┐    ┌─────────────────┐                     │
│  │ triggers_manager│    │execution_engine │                     │
│  │  (16 gatilhos)  │    │ (roteamento IA) │                     │
│  └─────────────────┘    └─────────────────┘                     │
│           │                     │                               │
│           ▼                     ▼                               │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │              storage_connectors                          │    │
│  │  (Obsidian | Google Drive | OneDrive | MySQL)           │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Arquivos do Hub Central

| Arquivo | Função |
|---------|--------|
| `hub_central.py` | Core do sistema, gerencia ciclo de vida de eventos |
| `hub_server.py` | Servidor Flask com API REST |
| `triggers_manager.py` | Gerenciador de gatilhos com CRUD completo |
| `triggers_api.py` | Endpoints REST para gerenciar gatilhos |
| `triggers_config.json` | Configuração dos 16 gatilhos |
| `execution_engine.py` | Motor de execução e roteamento de IA |
| `storage_connectors.py` | Conectores para múltiplos destinos |

---

## 4. Sistema de Gatilhos Automatizados

O Hub Central possui um sistema de **16 gatilhos** 100% configuráveis via API. Os gatilhos podem ser de 4 tipos:

### 4.1 Tipos de Gatilhos

| Tipo | Descrição | Exemplo |
|------|-----------|---------|
| 📅 **Agendados** | Executam em horários específicos | "Toda segunda às 9h, criar resumo semanal" |
| 📝 **Eventos** | Reagem a ações no Obsidian | "Quando criar nota na pasta 'Projetos', gerar template" |
| 🌐 **Webhooks** | Recebem dados externos | "Quando N8N enviar dados, processar e salvar" |
| 🤖 **Inteligentes** | Baseados em padrões/contexto | "Analisar notas do dia e gerar insights" |

### 4.2 Gatilhos Pré-configurados

#### 📅 Gatilhos Agendados

| Gatilho | ID | Quando | Status |
|---------|-----|--------|--------|
| Resumo Semanal | `trg_weekly_summary` | Segunda às 09:00 | ✅ Ativo |
| Check de Emails | `trg_email_check` | A cada 2 horas | ⏸️ Desativado |
| Backup Diário | `trg_daily_backup` | Todo dia às 23:00 | ✅ Ativo |
| Limpeza de Logs | `trg_cleanup_logs` | Domingo às 03:00 | ✅ Ativo |
| Insights Diários | `trg_daily_insights` | Todo dia às 20:00 | ✅ Ativo |

#### 📝 Gatilhos de Eventos

| Gatilho | ID | Evento | Status |
|---------|-----|--------|--------|
| Template de Projeto | `trg_project_template` | Nova nota em `/Projetos` | ✅ Ativo |
| Alerta Urgente | `trg_urgent_alert` | Nota com `#urgente` | ✅ Ativo |
| Índice Automático | `trg_auto_index` | Nova nota criada | ⏸️ Desativado |
| Processar com IA | `trg_process_tag` | Nota com `#processar` | ✅ Ativo |
| Resumo de Reunião | `trg_meeting_summary` | Nota com `#reuniao` | ✅ Ativo |

#### 🌐 Webhooks

| Gatilho | ID | Endpoint | Status |
|---------|-----|----------|--------|
| Processar N8N | `trg_webhook_n8n` | `/webhook/n8n` | ✅ Ativo |
| WhatsApp para Nota | `trg_webhook_whatsapp` | `/webhook/whatsapp` | ✅ Ativo |
| Email para Nota | `trg_webhook_email` | `/webhook/email` | ✅ Ativo |
| GitHub Events | `trg_webhook_github` | `/webhook/github` | ✅ Ativo |

#### 🤖 Gatilhos Inteligentes

| Gatilho | ID | Condição | Status |
|---------|-----|----------|--------|
| Sugestão de Tarefas | `trg_task_suggestion` | Inatividade > 60 min | ⏸️ Desativado |
| Detector de Padrões | `trg_pattern_detector` | Análise a cada 24h | ⏸️ Desativado |

### 4.3 Configurações de Agendamento

| Tipo | Parâmetros | Exemplo |
|------|------------|---------|
| `interval` | `interval`, `unit` | A cada 2 horas |
| `daily` | `time` | Todo dia às 09:00 |
| `weekly` | `day`, `time` | Segunda às 09:00 |

**Unidades de tempo disponíveis:** `seconds`, `minutes`, `hours`, `days`

### 4.4 Tipos de Ação

| Ação | Descrição |
|------|-----------|
| `create_note` | Cria nova nota no Obsidian |
| `update_note` | Atualiza nota existente |
| `send_notification` | Envia notificação |
| `run_ai_analysis` | Executa análise com IA |
| `backup_vault` | Faz backup do vault |
| `generate_summary` | Gera resumo |
| `apply_template` | Aplica template |
| `process_with_ai` | Processa conteúdo com IA |
| `send_webhook` | Envia para webhook externo |
| `log_event` | Registra no log |
| `custom_script` | Executa script PowerShell |

---

## 5. Conectores de Armazenamento

O Hub Central suporta múltiplos destinos de armazenamento para garantir escalabilidade:

| Destino | Conector | Status | Uso Ideal |
|---------|----------|--------|-----------|
| **Obsidian** | `ObsidianConnector` | ✅ Ativo | Notas, conhecimento, dados não-estruturados |
| **Google Drive** | `GoogleDriveConnector` | 🔄 Pronto | Documentos, planilhas, arquivos grandes |
| **OneDrive** | `OneDriveConnector` | 🔄 Pronto | Integração com ecossistema Microsoft |
| **MySQL** | `MySQLConnector` | 🔄 Pronto | Logs, histórico de eventos, dados massivos |

### Como Configurar Novos Conectores

```bash
# Configurar MySQL
curl -X POST http://localhost:5002/storage/configure \
  -H "Content-Type: application/json" \
  -d '{
    "connector": "mysql",
    "config": {
      "host": "seu_host",
      "database": "seu_db",
      "user": "seu_user",
      "password": "sua_senha"
    }
  }'
```

---

## 6. Motor de Execução e Roteamento de IA

O módulo `decision_logic.py` analisa cada consulta e categoriza automaticamente:

| Categoria | Descrição | IA Recomendada |
|-----------|-----------|----------------|
| **CODE** | Programação e desenvolvimento | OpenAI GPT-4 |
| **RESEARCH** | Pesquisa e informações | Perplexity |
| **CREATIVE** | Escrita criativa | Claude |
| **ANALYSIS** | Análise de dados/código | OpenAI GPT-4 |
| **CONVERSATION** | Chat casual | Gemini |

### APIs de IA Configuradas

| Provedor | Status | Uso Principal |
|----------|--------|---------------|
| OpenAI | ✅ Ativo | Código e análise |
| Claude | ✅ Ativo | Escrita criativa |
| Gemini | ✅ Ativo | Conversação |
| Perplexity | ✅ Ativo | Pesquisa |
| DeepAI | ✅ Ativo | Imagens |
| Abacus | ✅ Ativo | Drive e GPT |
| Groq | ✅ Configurado | Respostas rápidas |
| DeepSeek | ✅ Configurado | Código |
| Grok | ✅ Configurado | Análise |

---

## 7. API Completa do Hub Central

### 7.1 Endpoints Principais

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/health` | Health check do servidor |
| GET | `/status` | Status detalhado do sistema |
| POST | `/event` | Dispara um novo evento |
| POST | `/ai/ask` | Envia prompt para IA |

### 7.2 Endpoints de Gatilhos

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/triggers` | Lista todos os gatilhos |
| GET | `/triggers/:id` | Obtém gatilho específico |
| POST | `/triggers` | Cria novo gatilho |
| PUT | `/triggers/:id` | Atualiza gatilho |
| DELETE | `/triggers/:id` | Remove gatilho |
| POST | `/triggers/:id/toggle` | Ativa/desativa gatilho |
| POST | `/triggers/:id/execute` | Executa gatilho manualmente |
| POST | `/triggers/:id/test` | Testa gatilho sem executar |
| GET | `/triggers/stats` | Estatísticas dos gatilhos |
| GET | `/triggers/templates` | Lista templates disponíveis |
| POST | `/triggers/templates/:name/create` | Cria a partir de template |
| GET | `/triggers/export` | Exporta gatilhos em JSON |
| POST | `/triggers/import` | Importa gatilhos de JSON |
| POST | `/triggers/bulk/enable` | Ativa múltiplos gatilhos |
| POST | `/triggers/bulk/disable` | Desativa múltiplos gatilhos |
| POST | `/triggers/bulk/delete` | Remove múltiplos gatilhos |

### 7.3 Endpoints de Webhooks

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| POST | `/webhook/n8n` | Recebe dados do N8N |
| POST | `/webhook/whatsapp` | Recebe mensagens do WhatsApp |
| POST | `/webhook/email` | Recebe emails |
| POST | `/webhook/github` | Recebe eventos do GitHub |
| POST | `/webhook/:source` | Webhook genérico |

### 7.4 Endpoints de Storage

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| POST | `/storage/save` | Salva dados em destino(s) |
| GET | `/storage/load` | Carrega dados de destino |
| GET | `/storage/health` | Verifica saúde dos conectores |
| POST | `/storage/configure` | Configura conector |

### 7.5 Exemplos de Uso

```bash
# Listar todos os gatilhos
curl http://localhost:5002/triggers

# Criar novo gatilho agendado
curl -X POST http://localhost:5002/triggers \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Meu Gatilho",
    "type": "scheduled",
    "config": {
      "schedule_type": "interval",
      "interval": 30,
      "unit": "minutes"
    },
    "action": {
      "type": "log_event",
      "message": "Gatilho executado!"
    }
  }'

# Ativar/Desativar gatilho
curl -X POST http://localhost:5002/triggers/trg_email_check/toggle

# Executar gatilho manualmente
curl -X POST http://localhost:5002/triggers/trg_daily_backup/execute

# Deletar gatilho
curl -X DELETE http://localhost:5002/triggers/ID_DO_GATILHO

# Enviar prompt para IA
curl -X POST http://localhost:5002/ai/ask \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Analise as notas de hoje", "provider": "auto"}'
```

---

## 8. Sistema de Backup e Restauração

### 8.1 Criar Backup

```powershell
cd C:\Users\rudpa\COMET\backup
.\Backup_Sistema_IA.ps1
```

O backup será salvo em `C:\Backup_Sistema_IA\` como um arquivo ZIP.

### 8.2 O que é Incluído no Backup

| Componente | Conteúdo |
|------------|----------|
| **COMET** | Scripts, servidor Python, logs |
| **Obsidian Agent** | Agente, frontend, configurações |
| **Hub Central** | Todos os módulos e configurações |
| **Config** | API keys, tokens, variáveis de ambiente |
| **ngrok** | Configuração do domínio fixo |

### 8.3 Restaurar em Nova Máquina

1. Instale o Obsidian: [obsidian.md](https://obsidian.md)
2. Instale o plugin `Local REST API`
3. Configure a mesma API Key do backup
4. Execute:
   ```powershell
   .\Restaurar_Sistema_IA.ps1 -BackupZip "C:\caminho\para\backup.zip"
   ```
5. Reinicie o computador

---

## 9. Estrutura de Arquivos

```
C:\Users\rudpa\
├── COMET\
│   ├── manus_bridge_unified.py     # Servidor COMET Bridge
│   ├── Iniciar_Sistema_IA.bat      # Script de inicialização
│   ├── Health_Check.ps1            # Monitoramento de saúde
│   ├── SYSTEM_CONTEXT.json         # Contexto do sistema
│   ├── plugin_registry.json        # Registro de plugins
│   └── backup\
│       ├── Backup_Sistema_IA.ps1   # Script de backup
│       └── Restaurar_Sistema_IA.ps1 # Script de restauração
│
├── obsidian-agente\
│   ├── agent\
│   │   ├── agent.py                # Servidor Flask principal
│   │   ├── intelligent_agent.py    # Lógica do agente
│   │   ├── decision_logic.py       # Módulo de decisão
│   │   └── ai_integration.py       # Integração com IAs
│   │
│   ├── frontend\
│   │   ├── src\
│   │   │   └── App.tsx             # Interface React
│   │   └── .env                    # Variáveis de ambiente
│   │
│   └── hub_central\                # NOVO - Cérebro do Sistema
│       ├── hub_central.py          # Core do Hub
│       ├── hub_server.py           # Servidor Flask
│       ├── triggers_manager.py     # Gerenciador de gatilhos
│       ├── triggers_api.py         # API de gatilhos
│       ├── triggers_config.json    # Configuração dos gatilhos
│       ├── execution_engine.py     # Motor de execução
│       ├── storage_connectors.py   # Conectores de storage
│       └── README.md               # Documentação
│
├── hub_central\                    # Cópia local do Hub
│   └── (mesmos arquivos acima)
│
├── .obsidian-agent\
│   └── config.json                 # Configuração do agente
│
└── AppData\Local\ngrok\
    └── ngrok.yml                   # Configuração do ngrok
```

---

## 10. Comandos Úteis

### Iniciar Sistema Manualmente

```batch
C:\Users\rudpa\COMET\Iniciar_Sistema_IA.bat
```

### Executar Health Check

```powershell
powershell -ExecutionPolicy Bypass -File C:\Users\rudpa\COMET\Health_Check.ps1
```

### Criar Backup

```powershell
powershell -ExecutionPolicy Bypass -File C:\Users\rudpa\COMET\backup\Backup_Sistema_IA.ps1
```

### Iniciar Componentes Individualmente

```powershell
# COMET Bridge
cd C:\Users\rudpa\COMET
python manus_bridge_unified.py

# Obsidian Agent
cd C:\Users\rudpa\obsidian-agente\agent
python agent.py

# Hub Central
cd C:\Users\rudpa\hub_central
python hub_server.py

# Frontend
cd C:\Users\rudpa\obsidian-agente\frontend
npm run dev
```

---

## 11. Próximos Passos

### ✅ Implementado

- [x] Hub Central com coordenação de ações autônomas
- [x] Sistema de gatilhos configuráveis (16 gatilhos)
- [x] API REST completa para gerenciamento
- [x] Conectores de armazenamento multi-destino
- [x] Motor de execução com roteamento de IA
- [x] Sistema de backup e restauração

### 🔄 Em Planejamento

- [ ] **Integração com N8N:** Conectar o Hub Central ao N8N para automações visuais
- [ ] **Integração com WhatsApp:** Permitir comunicação direta com o sistema via WhatsApp
- [ ] **Integração com Email:** Automatizar o processamento de emails importantes
- [ ] **Ciclo de Aprendizado Contínuo:** Sistema que aprende com o uso e sugere novas automações
- [ ] **Dashboard Web:** Interface visual para gerenciar gatilhos e monitorar o sistema

---

## 📚 Referências

- **Repositório GitHub:** [github.com/Rudson-Oliveira/obsidian-agente](https://github.com/Rudson-Oliveira/obsidian-agente)
- **Obsidian:** [obsidian.md](https://obsidian.md)
- **ngrok:** [ngrok.com](https://ngrok.com)

---

**Criado com ❤️ por Manus para Rudson Oliveira**

*Última atualização: 24 de Dezembro de 2025*
