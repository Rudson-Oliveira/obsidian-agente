---
tags: [ollama, llama, ia-local, hospitalar, manus, abacus, comet]
created: 2025-12-21
status: ativo
---

# Ollama - Central de IA Local

## Visao Geral

O **Ollama** e a plataforma de IA local que permite rodar modelos de linguagem diretamente no computador.

### Beneficios
- Casto R$ 0/mes para requisicoes locais
- Privacidade total - dados nao saem do computador
- Baixa latencia - respostas instantaneas
- Funciona offline

## Status da Instalacao

| Item | Status | Detalhes |
|------|--------|----------|
| Ollama | Instalado | v0.13.5 |
| Startup | Configurado | Inicia com Windows |
| gemma3:4b | Ativo | 3.3 GB |
| llama3.2 | Disponibel | ~2 GB |

## Comandos Essenciais

```powershell
ollama list              # Listar modelos
ollama pull llama3.2     # Baixar modelo
ollama run gemma3:4b     # Chat interativo
```

## Integracao Manus + Ollama

| Tipo | Usar Ollama | Usar Manus |
|------|-------------|------------|
| Perguntas simples | Sim | Nao |
| Dados sensiveis | Sim | Nao |
| Operacoes browser | Nao | Sim |
| Pesquisas internet | Nao | Sim |

## Links

- [[Llama-Stack-Hospitalar]]
- [[COMET Bridge]]
- [[Manus Integration]]

