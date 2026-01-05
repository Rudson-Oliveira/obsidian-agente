# 🤖 Assistentes e APIs - 2026 Autonomia de Sistema

**Data:** 05/01/2026
**Autor:** Manus AI

---

## 📋 Visão Geral

Este documento descreve todos os assistentes (agentes de IA) e APIs disponíveis para o projeto, priorizando soluções locais de baixo ou zero custo, evitando dependência de uma única big tech.

---

## 🔒 ACORDO DE AUTONOMIA

> **AUTORIZADO POR:** Rudson Oliveira
> **DATA:** 05/01/2026

### Regras de Operação Autônoma

| Regra | Descrição |
|-------|-----------|
| **CRÍTICO 1** | Jamais solicitar intervenção humana no PowerShell enquanto COMET Bridge estiver conectado |
| **CRÍTICO 2** | Decisões técnicas com viabilidade > 95% devem ser executadas autonomamente |
| **CRÍTICO 3** | Nunca omitir, ocultar ou manipular dados |
| **CRÍTICO 4** | Sempre testar antes de avançar para próxima etapa |
| **CRÍTICO 5** | Implementar melhorias continuamente |

### Quando Consultar o Humano

| Situação | Ação |
|----------|------|
| COMET Bridge desconectado | Solicitar reconexão |
| Viabilidade < 95% | Consultar antes de prosseguir |
| Risco de perda de dados | Parar e informar |
| Custo financeiro não previsto | Solicitar aprovação |
| Ambiguidade nos requisitos | Perguntar para esclarecer |

---

## 🏠 ASSISTENTES LOCAIS (Custo Zero)

### 1. Ollama - Motor Principal de IA

| Característica | Valor |
|----------------|-------|
| **Porta** | 11434 |
| **URL** | http://localhost:11434 |
| **Custo** | R$ 0 |
| **Modelos disponíveis** | llama3, mistral, codellama, llava |

**API de Uso:**
```bash
# Gerar texto
curl http://localhost:11434/api/generate -d '{
  "model": "llama3",
  "prompt": "Explique o processo de orçamento hospitalar"
}'

# Chat
curl http://localhost:11434/api/chat -d '{
  "model": "llama3",
  "messages": [{"role": "user", "content": "Olá"}]
}'
```

### 2. Jan - Interface Amigável

| Característica | Valor |
|----------------|-------|
| **Porta** | 4891 |
| **URL** | http://localhost:4891 |
| **Custo** | R$ 0 |
| **Especialidade** | Interface gráfica para IA |

**API de Uso:**
```bash
curl http://localhost:4891/v1/chat/completions -d '{
  "model": "default",
  "messages": [{"role": "user", "content": "Analise este orçamento"}]
}'
```

### 3. LM Studio - Modelos Especializados

| Característica | Valor |
|----------------|-------|
| **Porta** | 1234 |
| **URL** | http://localhost:1234 |
| **Custo** | R$ 0 |
| **Especialidade** | Modelos médicos e especializados |

**API de Uso (compatível OpenAI):**
```bash
curl http://localhost:1234/v1/chat/completions -d '{
  "model": "local-model",
  "messages": [{"role": "user", "content": "Diagnóstico diferencial para..."}]
}'
```

### 4. GPT4All - Alternativa Leve

| Característica | Valor |
|----------------|-------|
| **Porta** | Variável |
| **Custo** | R$ 0 |
| **Especialidade** | Modelos leves para hardware limitado |

---

## 🌐 ASSISTENTES EXTERNOS (Baixo Custo)

### 5. Perplexity AI (COMET Desktop)

| Característica | Valor |
|----------------|-------|
| **Acesso** | Via COMET Desktop V2.0 |
| **Custo** | Gratuito (com limites) |
| **Especialidade** | Pesquisa em tempo real |

### 6. DeepSeek (Recomendado pelo ChatGPT)

| Característica | Valor |
|----------------|-------|
| **URL** | https://api.deepseek.com |
| **Custo** | ~$0.14/1M tokens (muito barato) |
| **Especialidade** | Código e raciocínio |

**API de Uso:**
```bash
curl https://api.deepseek.com/v1/chat/completions \
  -H "Authorization: Bearer $DEEPSEEK_API_KEY" \
  -d '{
    "model": "deepseek-chat",
    "messages": [{"role": "user", "content": "Otimize este código"}]
  }'
```

### 7. Groq (Alta Velocidade)

| Característica | Valor |
|----------------|-------|
| **URL** | https://api.groq.com |
| **Custo** | Gratuito (com limites generosos) |
| **Especialidade** | Inferência ultra-rápida |

---

## 🔧 AGENTES DE AUTOMAÇÃO

### 8. COMET Bridge - Executor Principal

| Característica | Valor |
|----------------|-------|
| **Porta Local** | 5000 |
| **URL Externa** | https://charmless-maureen-subadministratively.ngrok-free.dev |
| **Token** | heDuf3s4Y_EXwISRm2q2O1UPgi0zWbskf4_suT3cdus |
| **Função** | Execução remota de comandos PowerShell |

**API de Uso:**
```bash
curl -X POST "$COMET_URL/powershell" \
  -H "Content-Type: application/json" \
  -H "X-Auth-Token: $TOKEN" \
  -d '{"command": "Get-Process"}'
```

### 9. Vision Server (PicaPau) - Análise Visual

| Característica | Valor |
|----------------|-------|
| **Porta** | 5003 |
| **URL** | http://localhost:5003 |
| **Função** | Análise de imagens e documentos |

**API de Uso:**
```bash
curl -X POST http://localhost:5003/analyze \
  -d '{"image": "base64...", "prompt": "Extraia dados deste documento"}'
```

### 10. Browser-Use - Automação Web

| Característica | Valor |
|----------------|-------|
| **Porta** | 3002 |
| **URL** | http://localhost:3002 |
| **Função** | Automação de navegador com IA |

### 11. N8N - Orquestração de Workflows

| Característica | Valor |
|----------------|-------|
| **Porta** | 5678 |
| **URL** | http://localhost:5678 |
| **Função** | Automação visual de processos |

### 12. UiPath - RPA Avançado

| Característica | Valor |
|----------------|-------|
| **URL** | https://cloud.uipath.com |
| **Custo** | ~$25/mês |
| **Função** | Automação robótica de processos |

---

## 📊 MATRIZ DE DECISÃO DE USO

| Tarefa | Assistente Primário | Fallback | Custo |
|--------|---------------------|----------|-------|
| Chat com usuário | Ollama | Jan | R$ 0 |
| Análise de código | DeepSeek | Ollama | ~R$ 0 |
| Pesquisa web | Perplexity | Groq | R$ 0 |
| Análise de imagem | Vision Server | Ollama+llava | R$ 0 |
| Automação web | Browser-Use | UiPath | R$ 0-150 |
| Workflows | N8N | UiPath | R$ 0-150 |
| Execução remota | COMET Bridge | - | R$ 0 |
| Modelos médicos | LM Studio | Jan | R$ 0 |

---

## 🔄 ESTRATÉGIA MULTI-PROVIDER

Para evitar dependência de uma única big tech, o sistema usa a seguinte estratégia:

```
┌─────────────────────────────────────────────────────────────┐
│                    REQUISIÇÃO DE IA                         │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                   ROUTER INTELIGENTE                        │
│                                                             │
│  1. Verificar se tarefa pode ser feita localmente           │
│  2. Se sim → Ollama/Jan/LM Studio (custo zero)              │
│  3. Se não → Escolher provider externo mais barato          │
│  4. Se falhar → Tentar próximo provider                     │
└─────────────────────────────────────────────────────────────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
        ▼                  ▼                  ▼
┌───────────────┐  ┌───────────────┐  ┌───────────────┐
│   LOCAL       │  │   BAIXO       │  │   PREMIUM     │
│   (Prioridade)│  │   CUSTO       │  │   (Último)    │
│               │  │               │  │               │
│ • Ollama      │  │ • DeepSeek    │  │ • OpenAI      │
│ • Jan         │  │ • Groq        │  │ • Anthropic   │
│ • LM Studio   │  │ • Perplexity  │  │ • Google      │
│ • GPT4All     │  │               │  │               │
└───────────────┘  └───────────────┘  └───────────────┘
     R$ 0              ~R$ 0.01           ~R$ 0.10
```

---

## 🔐 CREDENCIAIS E TOKENS

| Serviço | Variável de Ambiente | Onde Obter |
|---------|---------------------|------------|
| COMET Bridge | `COMET_TOKEN` | Já configurado |
| DeepSeek | `DEEPSEEK_API_KEY` | https://platform.deepseek.com |
| Groq | `GROQ_API_KEY` | https://console.groq.com |
| UiPath | `UIPATH_TOKEN` | https://cloud.uipath.com |
| Obsidian | `OBSIDIAN_TOKEN` | Plugin Local REST API |

---

## 📋 CHECKLIST DE INTEGRAÇÃO

### Assistentes Locais
- [x] Ollama instalado e rodando (porta 11434)
- [x] Jan instalado e rodando (porta 4891)
- [x] LM Studio instalado e rodando (porta 1234)
- [x] GPT4All instalado

### Agentes de Automação
- [x] COMET Bridge ativo (porta 5000)
- [x] Vision Server ativo (porta 5003)
- [x] Browser-Use ativo (porta 3002)
- [x] N8N ativo (porta 5678)
- [x] UiPath configurado (cloud)

### APIs Externas
- [ ] DeepSeek API key configurada
- [ ] Groq API key configurada

---

## 🚀 PRÓXIMOS PASSOS

1. **Configurar DeepSeek** como fallback para tarefas complexas
2. **Integrar Ollama** ao Chat IA do sistema
3. **Criar workflow N8N** que usa múltiplos assistentes
4. **Testar redundância** entre providers

---

**Documento atualizado em:** 05/01/2026
