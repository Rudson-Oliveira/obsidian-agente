# 📜 Regras e Governança do Projeto
## 2026 - Autonomia de Sistema

**Data de criação:** 05/01/2026
**Autorizado por:** Rudson Oliveira
**Executor:** Manus AI

---

## 🔒 REGRAS INVIOLÁVEIS

### 1. Critério de Alteração do Planejamento

> **REGRA:** Qualquer alteração no planejamento só pode ser feita se a viabilidade for **maior que 90%** para o projeto.

| Condição | Ação |
|----------|------|
| Viabilidade ≥ 90% | ✅ Pode alterar planejamento |
| Viabilidade < 90% | ❌ Manter planejamento original |
| Viabilidade incerta | ⚠️ Consultar Rudson Oliveira |

### 2. Transparência Total

> **REGRA:** É **PROIBIDO** omitir ou ocultar dados em qualquer circunstância.

| Situação | Obrigação |
|----------|-----------|
| Erro encontrado | Reportar imediatamente |
| Risco identificado | Documentar com evidências |
| Limitação técnica | Informar alternativas |
| Dado sensível | Proteger mas não ocultar |
| Resultado negativo | Apresentar com análise |

### 3. Seguir o Planejamento

> **REGRA:** O planejamento deve ser seguido rigorosamente, etapa por etapa.

| Permitido | Proibido |
|-----------|----------|
| Executar etapa atual | Pular etapas |
| Testar antes de avançar | Avançar sem validação |
| Documentar progresso | Executar sem registro |
| Fazer backup | Alterar sem backup |
| Melhorias incrementais | Mudanças radicais |

---

## 📋 Checklist de Governança

Antes de cada ação, verificar:

- [ ] A ação está no planejamento?
- [ ] A viabilidade é > 90%?
- [ ] Todos os dados estão sendo reportados?
- [ ] O backup da etapa anterior foi feito?
- [ ] O teste em DEV foi realizado?

---

## 🔄 Processo de Alteração de Planejamento

```
1. IDENTIFICAR necessidade de alteração
   ↓
2. CALCULAR viabilidade (deve ser > 90%)
   ↓
3. DOCUMENTAR justificativa com dados
   ↓
4. APRESENTAR ao Rudson Oliveira
   ↓
5. AGUARDAR aprovação (se necessário)
   ↓
6. REGISTRAR alteração no GitHub
   ↓
7. ATUALIZAR roadmap
```

---

## 📊 Matriz de Decisão

| Cenário | Viabilidade | Ação | Autonomia |
|---------|-------------|------|-----------|
| Correção de bug | 99% | Executar | Total |
| Melhoria pequena | 95% | Executar | Total |
| Nova funcionalidade | 92% | Executar + Informar | Parcial |
| Mudança de arquitetura | 85% | Consultar primeiro | Nenhuma |
| Risco de dados | Qualquer | Parar + Consultar | Nenhuma |

---

## 🚨 Situações de Parada Obrigatória

O executor DEVE parar e consultar Rudson Oliveira quando:

1. **Risco de perda de dados** - Qualquer operação que possa deletar dados
2. **Acesso a produção** - Antes de qualquer deploy em produção
3. **Credenciais expostas** - Se detectar vazamento de senhas/tokens
4. **Viabilidade < 90%** - Quando análise indicar risco alto
5. **Conflito de requisitos** - Quando instruções forem ambíguas
6. **Custo não previsto** - Qualquer gasto financeiro não planejado

---

## 📝 Registro de Decisões

Toda decisão técnica deve ser registrada:

```markdown
## Decisão #XXX - [Data]

**Contexto:** [Descrição da situação]
**Opções analisadas:**
1. [Opção A] - Viabilidade: XX%
2. [Opção B] - Viabilidade: XX%

**Decisão:** [Opção escolhida]
**Justificativa:** [Baseada em dados]
**Impacto:** [Esperado]
```

---

## ✅ Compromissos do Executor (Manus AI)

1. **Transparência** - Nunca omitir ou ocultar informações
2. **Precisão** - Sempre basear decisões em dados verificáveis
3. **Prudência** - Testar em DEV antes de produção
4. **Documentação** - Registrar todas as ações e decisões
5. **Backup** - Criar ponto de restauração antes de mudanças
6. **Comunicação** - Informar progresso e problemas
7. **Integridade** - Proteger dados e credenciais

---

## 🔐 Assinatura

**Autorizado por:** Rudson Oliveira
**Data:** 05/01/2026
**Validade:** Durante todo o projeto

---

*Este documento é parte integrante do projeto e deve ser seguido em todas as etapas.*


---

## 🤖 ACORDO DE AUTONOMIA MANUS AI

> **AUTORIZADO POR:** Rudson Oliveira
> **DATA:** 05/01/2026
> **RESPONSABILIDADE:** Rudson Oliveira assume total responsabilidade

### Regras de Operação Autônoma

| Regra | Descrição | Prioridade |
|-------|-----------|------------|
| **CRÍTICO 1** | Jamais solicitar intervenção humana no PowerShell enquanto COMET Bridge estiver conectado | MÁXIMA |
| **CRÍTICO 2** | Decisões técnicas com viabilidade > 95% devem ser executadas autonomamente | MÁXIMA |
| **CRÍTICO 3** | Nunca omitir, ocultar ou manipular dados | MÁXIMA |
| **CRÍTICO 4** | Sempre testar antes de avançar para próxima etapa | ALTA |
| **CRÍTICO 5** | Implementar melhorias continuamente | ALTA |

### Quando Consultar o Humano

| Situação | Ação | Justificativa |
|----------|------|---------------|
| COMET Bridge desconectado | Solicitar reconexão | Sem acesso ao sistema |
| Viabilidade < 95% | Consultar antes de prosseguir | Risco de erro |
| Risco de perda de dados | Parar e informar | Segurança |
| Custo financeiro não previsto | Solicitar aprovação | Orçamento |
| Ambiguidade nos requisitos | Perguntar para esclarecer | Qualidade |

### Plano de Contingência de Reconexão

1. Tentar reconectar automaticamente (3 tentativas)
2. Aguardar 30 segundos entre tentativas
3. Se falhar após 3 tentativas, informar humano
4. Documentar causa da desconexão

---

**Documento atualizado em:** 05/01/2026


---

## 🚨 REGRA CRÍTICA: SISTEMA DEV E DOCKER

> **JAMAIS ALTERAR O SISTEMA DEV DIRETAMENTE**

### Fluxo Obrigatório de Alterações

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        FLUXO DE DEPLOY OBRIGATÓRIO                          │
└─────────────────────────────────────────────────────────────────────────────┘

    ┌─────────────┐         ┌─────────────┐         ┌─────────────┐
    │   DOCKER    │────────▶│   DEV       │────────▶│  PRODUÇÃO   │
    │   (Local)   │         │ (Automático)│         │  (Manual)   │
    └─────────────┘         └─────────────┘         └─────────────┘
          │                       │                       │
          │                       │                       │
    Desenvolvimento          Testes e               Aprovação
    e Alterações            Validação               Rudson Oliveira
```

### Regras de Deploy

| Ambiente | URL | Pode Alterar? | Quem Altera? |
|----------|-----|---------------|--------------|
| **Docker Local** | localhost | ✅ SIM | Manus AI |
| **DEV** | dev.hospitalarsaude.app.br | ❌ NÃO diretamente | Apenas via Docker→Produção |
| **Produção** | hospitalarsaude.app.br | ❌ NÃO | Apenas após aprovação |

### Processo de Alteração

1. **DESENVOLVER** no Docker local
2. **TESTAR** no Docker local
3. **VALIDAR** resultados
4. **ENVIAR** para produção (após aprovação)
5. **AGUARDAR** atualização automática no DEV
6. **TESTAR** no DEV
7. **CONFIRMAR** funcionamento
8. **APROVAR** para sistema original

### O que é PROIBIDO

| Ação | Status |
|------|--------|
| Alterar banco de dados do DEV diretamente | ❌ PROIBIDO |
| Modificar código no servidor DEV | ❌ PROIBIDO |
| Fazer deploy direto no DEV | ❌ PROIBIDO |
| Alterar configurações do DEV | ❌ PROIBIDO |

### O que é PERMITIDO

| Ação | Status |
|------|--------|
| Consultar dados do DEV (leitura) | ✅ PERMITIDO |
| Analisar estrutura do DEV | ✅ PERMITIDO |
| Testar endpoints do DEV | ✅ PERMITIDO |
| Desenvolver no Docker local | ✅ PERMITIDO |
| Criar automações que interagem com DEV (leitura) | ✅ PERMITIDO |

---

**Regra adicionada em:** 05/01/2026
**Autorizado por:** Rudson Oliveira
