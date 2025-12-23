# Hub Central de IA - Manus + Llama

## Visão Geral
Interface unificada para acesso às IAs locais (Ollama/Llama) e cloud (Manus).

## Inicialização Automática
- **Inicia com o Windows** automaticamente
- Localização: C:\Users\rudpa\COMET\IA-Hub-Central.pyw

## Como Usar

### Prefixos
| Prefixo | Destino | Exemplo |
|---------|---------|----------|
| Manus: | Envia para Manus (cloud) | Manus: pesquise sobre IA |
| Llama: | Envia para Ollama (local) | Llama: explique machine learning |
| Sem prefixo | Decide automaticamente | o que é Python? |

### Decisão Automática
Quando não há prefixo, o sistema decide baseado em palavras-chave:

**Vai para Manus:**
- browser, pesquisar, internet, site, desktop, arquivo
- instalar, executar, api, docker, git, baixar, email

**Vai para Llama:**
- simples, traduzir, resumir, explicar, definir
- calcular, o que é, como funciona

## Economia
| Tipo | IA | Custo |
|------|-----|-------|
| Tarefas simples | Llama (local) | R$ 0 |
| Dados sensíveis | Llama (local) | R$ 0 |
| Browser/Desktop | Manus (cloud) | Tokens |
| APIs complexas | Manus (cloud) | Tokens |

## Status
- **Llama: OK** = Ollama rodando (porta 11434)
- **Manus: OK** = COMET Bridge ativo

## Arquivos Relacionados
- Script: COMET\IA-Hub-Central.pyw
- Startup: IA-Hub-Central.lnk
- Modelos: gemma3:4b, llama3.2

---
*Atualizado: 23/12/2025 04:09*
