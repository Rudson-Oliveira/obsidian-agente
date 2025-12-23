# Integracao Manus + Llama - Obsidian Agent v5.0

## Status: ATIVO
- **Ollama**: Rodando em localhost:11434
- **Modelos**: llama3.2:latest, gemma3:4b
- **Integracao**: Backend-only (sem alteracoes no frontend)

## Como Usar

### Prefixos Explicitos
| Prefixo | Destino | Exemplo |
|---------|---------|--------|
| Manus: | Manus Cloud | Manus: pesquise sobre Angular |
| Llama: | Ollama Local | Llama: o que e Python? |
| Local: | Ollama Local | Local: traduza hello world |
| Ollama: | Ollama Local | Ollama: explique machine learning |
| Sem prefixo | Automatico | explique o que e uma API |

### Decisao Automatica
**Vai para Manus (Cloud):**
- browser, navegador, pesquisar, internet, site
- desktop, arquivo, instalar, executar, api
- docker, git, baixar, email, obsidian, nota
- sistema, windows, powershell, imagem, pdf

**Vai para Llama (Local):**
- explique, o que e, defina, resuma, traduza
- calcule, liste, como funciona, diferenca
- escreva, codigo, simples, basico

## Arquivos
- agent/ollama_integration.py - Modulo de integracao v2.0
- agent/ai_integration.py - Atualizado com suporte Ollama
- agent/intelligent_agent.py - Roteador AIRouter

## Economia Estimada
- 70%+ das tarefas -> Llama local = R$ 0/mes
- Dados sensíveis -> Privacidade total
- Tarefas complexas -> Manus Cloud

## Testes Realizados
- [x] Roteamento por prefixo explicito
- [x] Roteamento automatico por keywords
- [x] Conexao com Ollama local
- [x] Listagem de modelos
- [x] Fallback para Manus quando Ollama indisponivel

---
*Atualizado: 2025-12-23 04:26*
