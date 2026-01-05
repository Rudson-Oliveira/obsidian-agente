# 🔧 Ferramentas e Portas - 2026 Autonomia de Sistema

**Data:** 05/01/2026
**Autor:** Manus AI

---

## 📋 Resumo Executivo

Este documento descreve todas as ferramentas utilizadas no projeto, suas respectivas portas de acesso e função no ecossistema de automação do setor de Orçamentos da Hospitalar Soluções em Saúde.

---

## 🖥️ MAPA COMPLETO DE PORTAS

### Infraestrutura Core

| Porta | Serviço | Função | URL de Acesso | Status |
|-------|---------|--------|---------------|--------|
| **80** | Traefik | Proxy reverso HTTP | http://localhost | ✅ Ativo |
| **443** | Traefik | Proxy reverso HTTPS | https://localhost | ✅ Ativo |
| **8082** | Traefik Dashboard | Painel do Traefik | http://localhost:8082 | ✅ Ativo |
| **9000** | Portainer | Gerenciamento Docker | http://localhost:9000 | ⚠️ Unhealthy |

### Automação e Workflows

| Porta | Serviço | Função | URL de Acesso | Status |
|-------|---------|--------|---------------|--------|
| **5678** | N8N | Automação de workflows | http://localhost:5678 | ✅ Ativo |
| **3002** | Browser-Use | Automação web com IA | http://localhost:3002 | ✅ Ativo |

### Inteligência Artificial Local

| Porta | Serviço | Função | URL de Acesso | Status |
|-------|---------|--------|---------------|--------|
| **11434** | Ollama | Modelos LLM locais | http://localhost:11434 | ⚠️ Unhealthy |
| **4891** | Jan | Interface IA amigável | http://localhost:4891 | ✅ Ativo |
| **1234** | LM Studio | Modelos médicos especializados | http://localhost:1234 | ✅ Ativo |

### Banco de Dados

| Porta | Serviço | Função | URL de Acesso | Status |
|-------|---------|--------|---------------|--------|
| **5432** | PostgreSQL | Banco de dados principal | localhost:5432 | ✅ Ativo |
| **6379** | Redis | Cache e filas | localhost:6379 | ✅ Ativo |
| **8086** | PgAdmin | Administração PostgreSQL | http://localhost:8086 | ✅ Ativo |
| **8083** | Adminer | Administração BD genérico | http://localhost:8083 | ✅ Ativo |
| **8084** | Redis UI | Administração Redis | http://localhost:8084 | ✅ Ativo |

### Monitoramento e Observabilidade

| Porta | Serviço | Função | URL de Acesso | Status |
|-------|---------|--------|---------------|--------|
| **3001** | Grafana | Dashboards e visualização | http://localhost:3001 | ✅ Ativo |
| **9090** | Prometheus | Coleta de métricas | http://localhost:9090 | ✅ Ativo |
| **3100** | Loki | Agregação de logs | http://localhost:3100 | ⚠️ Unhealthy |
| **9009** | Mimir | Métricas long-term | http://localhost:9009 | ✅ Ativo |
| **9093** | Alertmanager | Gerenciamento de alertas | http://localhost:9093 | ✅ Ativo |
| **9100** | Node Exporter | Métricas do sistema | http://localhost:9100 | ✅ Ativo |
| **19999** | Netdata | Monitoramento real-time | http://localhost:19999 | ✅ Ativo |

### CI/CD e DevOps

| Porta | Serviço | Função | URL de Acesso | Status |
|-------|---------|--------|---------------|--------|
| **8087** | Jenkins | CI/CD pipelines | http://localhost:8087 | ✅ Ativo |

### Sistema IA v3.1 (Agentes Locais)

| Porta | Serviço | Função | URL de Acesso | Status |
|-------|---------|--------|---------------|--------|
| **5000** | COMET Bridge | Execução remota PowerShell | http://localhost:5000 | ✅ Ativo |
| **5001** | Obsidian Agent | Agente inteligente Obsidian | http://localhost:5001 | ✅ Ativo |
| **5002** | Hub Central | Orquestração de agentes | http://localhost:5002 | ✅ Ativo |
| **5003** | Vision Server | Análise de imagens (PicaPau) | http://localhost:5003 | ✅ Ativo |
| **5173** | Frontend | Interface web do sistema IA | http://localhost:5173 | ✅ Ativo |
| **27123** | Obsidian API | API REST do Obsidian | http://localhost:27123 | ✅ Ativo |

### Acesso Externo

| Porta | Serviço | Função | URL de Acesso | Status |
|-------|---------|--------|---------------|--------|
| **ngrok** | COMET Bridge Externo | Acesso remoto ao COMET | https://charmless-maureen-subadministratively.ngrok-free.dev | ✅ Ativo |

---

## 🏗️ ARQUITETURA DE PORTAS

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           INTERNET / NGROK                                  │
│                    (charmless-maureen-...ngrok-free.dev)                    │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         PROXY REVERSO (Traefik)                             │
│                          Portas: 80, 443, 8082                              │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
        ┌───────────────────────────┼───────────────────────────┐
        │                           │                           │
        ▼                           ▼                           ▼
┌───────────────────┐   ┌───────────────────┐   ┌───────────────────┐
│   AUTOMAÇÃO       │   │   INTELIGÊNCIA    │   │   MONITORAMENTO   │
│                   │   │   ARTIFICIAL      │   │                   │
│ N8N (5678)        │   │                   │   │ Grafana (3001)    │
│ Browser-Use(3002) │   │ Ollama (11434)    │   │ Prometheus (9090) │
│ COMET (5000)      │   │ Jan (4891)        │   │ Loki (3100)       │
│ Vision (5003)     │   │ LM Studio (1234)  │   │ Netdata (19999)   │
└───────────────────┘   └───────────────────┘   └───────────────────┘
        │                           │                           │
        └───────────────────────────┼───────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           BANCO DE DADOS                                    │
│              PostgreSQL (5432) │ Redis (6379)                               │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 🔌 FERRAMENTAS PERTINENTES (Da conversa com ChatGPT)

Baseado na análise da conversa com ChatGPT, as seguintes ferramentas são **pertinentes** para o projeto de Orçamentos:

### Essenciais (Usar Imediatamente)

| Ferramenta | Porta | Pertinência | Justificativa |
|------------|-------|-------------|---------------|
| **N8N** | 5678 | ⭐⭐⭐⭐⭐ | Automação de workflows sem código |
| **Browser-Use** | 3002 | ⭐⭐⭐⭐⭐ | Automação web com IA para preencher formulários |
| **Ollama** | 11434 | ⭐⭐⭐⭐⭐ | IA local gratuita para Chat do sistema |
| **Grafana** | 3001 | ⭐⭐⭐⭐ | Dashboard de métricas de orçamentos |
| **COMET Bridge** | 5000 | ⭐⭐⭐⭐⭐ | Execução remota de comandos |

### Importantes (Usar na Fase 2)

| Ferramenta | Porta | Pertinência | Justificativa |
|------------|-------|-------------|---------------|
| **Jan** | 4891 | ⭐⭐⭐⭐ | Interface amigável para IA médica |
| **LM Studio** | 1234 | ⭐⭐⭐⭐ | Modelos especializados em saúde |
| **Vision Server** | 5003 | ⭐⭐⭐⭐ | Análise de documentos/imagens |
| **Redis** | 6379 | ⭐⭐⭐ | Cache para performance |

### Suporte (Já funcionando)

| Ferramenta | Porta | Pertinência | Justificativa |
|------------|-------|-------------|---------------|
| **PostgreSQL** | 5432 | ⭐⭐⭐⭐⭐ | Banco de dados do sistema |
| **Prometheus** | 9090 | ⭐⭐⭐ | Métricas para alertas |
| **Jenkins** | 8087 | ⭐⭐ | CI/CD para deploys |

### Não Pertinentes para Fase 1 (Manter desligado)

| Ferramenta | Motivo |
|------------|--------|
| Mongo Express | Não usamos MongoDB no sistema |
| Tempo | Tracing avançado, não necessário agora |
| Watchtower | Auto-update pode causar instabilidade |

---

## 🔗 INTEGRAÇÕES PLANEJADAS

### Fluxo de Dados entre Portas

```
LEAD (WhatsApp)
     │
     ▼
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   N8N       │────▶│ Browser-Use │────▶│  Sistema    │
│   (5678)    │     │   (3002)    │     │ Hospitalar  │
└─────────────┘     └─────────────┘     └─────────────┘
     │                                        │
     │                                        ▼
     │                               ┌─────────────┐
     │                               │ PostgreSQL  │
     │                               │   (5432)    │
     │                               └─────────────┘
     │                                        │
     ▼                                        ▼
┌─────────────┐                      ┌─────────────┐
│   Ollama    │◀─────────────────────│   Grafana   │
│  (11434)    │                      │   (3001)    │
└─────────────┘                      └─────────────┘
     │
     ▼
┌─────────────┐
│  Chat IA    │
│  (Sistema)  │
└─────────────┘
```

---

## 📋 CHECKLIST DE VERIFICAÇÃO DE PORTAS

Antes de iniciar cada etapa, verificar se as portas necessárias estão acessíveis:

### Etapa 1 (Docker)
- [ ] Porta 9000 (Portainer) - Acessível
- [ ] Porta 8082 (Traefik) - Acessível

### Etapa 2 (N8N)
- [ ] Porta 5678 (N8N) - Acessível
- [ ] Porta 5000 (COMET Bridge) - Acessível

### Etapa 3 (Chat IA)
- [ ] Porta 11434 (Ollama) - Acessível e saudável
- [ ] Porta 4891 (Jan) - Acessível

### Etapa 4 (Validação)
- [ ] Porta 3002 (Browser-Use) - Acessível
- [ ] Porta 5432 (PostgreSQL) - Acessível

---

## 🔒 SEGURANÇA DE PORTAS

| Porta | Exposição | Recomendação |
|-------|-----------|--------------|
| 80, 443 | Pública (via ngrok) | OK - Traefik gerencia |
| 5678 | Local | Manter local, acessar via ngrok se necessário |
| 11434 | Local | Manter local |
| 5432 | Local | **NUNCA expor publicamente** |
| 9000 | Local | Manter local |

---

**Documento atualizado em:** 05/01/2026
