# 🧠 Sistema IA Autônomo - Obsidian Agent

Um ecossistema completo de inteligência artificial integrado ao Obsidian, com inicialização automática, roteamento inteligente de IAs e um Hub Central para coordenação de ações autônomas.

---

## ✨ Funcionalidades

- **🚀 Inicialização Automática:** Todos os componentes iniciam automaticamente com o Windows.
- **🔗 Domínio Fixo:** URL pública estática via ngrok para integrações permanentes.
- **🧠 Roteamento Inteligente:** Cada consulta é automaticamente direcionada para a IA mais adequada (OpenAI, Claude, Gemini, Perplexity).
- **⚡ Hub Central:** Cérebro do sistema que coordena gatilhos, eventos e armazenamento.
- **🔄 Sistema de Gatilhos:** Automações configuráveis via API (agendados, eventos, webhooks, inteligentes).
- **💾 Multi-Storage:** Suporte a Obsidian, Google Drive, OneDrive e MySQL.
- **🛡️ Backup Completo:** Sistema de backup e restauração para recuperação de desastres.

---

## 🏗️ Arquitetura

```
┌─────────────────────────────────────────────────────────────────┐
│                         SISTEMA IA AUTÔNOMO                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────────────┐  │
│  │  Obsidian   │◄──►│ COMET Bridge│◄──►│   Manus / Internet  │  │
│  │  (27124)    │    │   (5000)    │    │                     │  │
│  └─────────────┘    └─────────────┘    └─────────────────────┘  │
│         ▲                  ▲                                    │
│         │                  │                                    │
│         ▼                  ▼                                    │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────────────┐  │
│  │   Frontend  │◄──►│   Agent     │◄──►│     Hub Central     │  │
│  │   (5173)    │    │   (5001)    │    │       (5002)        │  │
│  └─────────────┘    └─────────────┘    └─────────────────────┘  │
│                                               │                 │
│                                               ▼                 │
│                            ┌─────────────────────────────────┐  │
│                            │   Gatilhos & Storage Connectors │  │
│                            │  (Obsidian, GDrive, MySQL, etc) │  │
│                            └─────────────────────────────────┘  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📦 Componentes

| Componente | Porta | Descrição |
|------------|-------|-----------|
| **Obsidian** | 27124 | Base de conhecimento com Local REST API |
| **ngrok** | 4040 | Túnel público com domínio fixo |
| **COMET Bridge** | 5000 | Ponte entre Manus e Obsidian |
| **Obsidian Agent** | 5001 | Agente inteligente com lógica de decisão |
| **Hub Central** | 5002 | Cérebro do sistema, coordena ações e gatilhos |
| **Frontend** | 5173 | Interface de chat integrada ao Obsidian |

---

## 🚀 Instalação

### Pré-requisitos

- Windows 10/11
- Python 3.10+
- Node.js 18+
- Obsidian com plugin `Local REST API`
- Conta ngrok (gratuita)

### Passos

1. Clone o repositório:
   ```bash
   git clone https://github.com/Rudson-Oliveira/obsidian-agente.git
   ```

2. Instale as dependências do Agent:
   ```bash
   cd obsidian-agente/agent
   pip install -r requirements.txt
   ```

3. Instale as dependências do Frontend:
   ```bash
   cd ../frontend
   npm install
   ```

4. Instale as dependências do Hub Central:
   ```bash
   cd ../../hub_central
   pip install -r requirements.txt
   ```

5. Configure o ngrok com seu authtoken e domínio.

6. Execute o script de inicialização:
   ```batch
   C:\Users\rudpa\COMET\Iniciar_Sistema_IA.bat
   ```

---

## ⚙️ Configuração

### APIs de IA

Configure suas API keys no arquivo `SYSTEM_CONTEXT.json`:

```json
{
  "api_keys": {
    "openai": "sk-...",
    "anthropic": "sk-ant-...",
    "gemini": "AIza...",
    "perplexity": "pplx-..."
  }
}
```

### Gatilhos

Os gatilhos são configurados no arquivo `triggers_config.json` ou via API:

```bash
# Criar gatilho agendado
curl -X POST http://localhost:5002/triggers -H "Content-Type: application/json" -d '{
  "name": "Resumo Diário",
  "type": "scheduled",
  "config": {
    "schedule_type": "daily",
    "time": "18:00"
  },
  "action": {
    "type": "generate_summary",
    "period": "day"
  }
}'
```

---

## 📚 Documentação

- [Documentação Completa](./docs/Sistema_IA_Autonomo_Documentacao.md)
- [Guia de Backup e Restauração](./docs/GUIA_BACKUP_RESTAURACAO.md)
- [Gerenciador de Gatilhos](./docs/Gerenciador_Gatilhos.md)
- [Hub Central](./docs/Hub_Central_Documentacao.md)

---

## 🛠️ API do Hub Central

### Endpoints Principais

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/health` | Health check do servidor |
| GET | `/status` | Status detalhado do sistema |
| GET | `/triggers` | Lista todos os gatilhos |
| POST | `/triggers` | Cria novo gatilho |
| PUT | `/triggers/:id` | Atualiza gatilho |
| DELETE | `/triggers/:id` | Remove gatilho |
| POST | `/triggers/:id/toggle` | Ativa/desativa gatilho |
| POST | `/triggers/:id/execute` | Executa gatilho manualmente |
| POST | `/webhook/:source` | Recebe webhooks externos |

---

## 🔄 Sistema de Gatilhos

### Tipos de Gatilhos

1. **📅 Agendados:** Executam em horários específicos (diário, semanal, intervalo).
2. **📝 Eventos:** Reagem a ações no Obsidian (nova nota, tag adicionada, etc.).
3. **🌐 Webhooks:** Recebem dados de serviços externos (N8N, WhatsApp, GitHub).
4. **🤖 Inteligentes:** Baseados em padrões e contexto (inatividade, análise de padrões).

### Gatilhos Pré-configurados

| Gatilho | Tipo | Quando |
|---------|------|--------|
| Resumo Semanal | Agendado | Segunda às 09:00 |
| Backup Diário | Agendado | Todo dia às 23:00 |
| Insights Diários | Agendado | Todo dia às 20:00 |
| Template de Projeto | Evento | Nova nota em `/Projetos` |
| Alerta Urgente | Evento | Nota com `#urgente` |
| Processar N8N | Webhook | Dados recebidos do N8N |
| WhatsApp para Nota | Webhook | Mensagem do WhatsApp |

---

## 💾 Backup e Restauração

### Criar Backup

```powershell
cd C:\Users\rudpa\COMET\backup
.\Backup_Sistema_IA.ps1
```

### Restaurar

```powershell
.\Restaurar_Sistema_IA.ps1 -BackupZip "C:\caminho\backup.zip"
```

---

## 🤝 Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou pull requests.

---

## 📄 Licença

Este projeto é de uso pessoal de Rudson Oliveira, desenvolvido por Manus.

---

**Criado com ❤️ por Manus para Rudson Oliveira**
