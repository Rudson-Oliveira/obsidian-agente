# MAPA CENTRAL: Integracao Manus e Llama

> **AVISO PARA ASSISTENTES DE IA:** Este documento e a fonte unica de verdade para a integracao Manus/Llama. LEIA COMPLETAMENTE antes de alteracoes.

---

## 1. Visao Geral

| Componente | Tecnologia | Proposito |
|------------|------------|----------|
| Agente Principal | Obsidian Agent v5.0 | Interface do usuario |
| Roteador Hibrido | Python (ollama_integration.py) | Decide destino da tarefa |
| IA na Nuvem | Manus | Tarefas complexas |
| IA Local | Ollama + Llama/Gemma | Tarefas simples |

---

## 2. Mapa de Arquivos e Caminhos

| Componente | Caminho |
|------------|--------|
| Vault Principal | C:\Users\rudpa\Downloads\OneDrive\...\Vida & Estudo\Vida & Estudo |
| Pasta Documentacao | ...\Vida & Estudo\IA |
| Backend Obsidian Agent | C:\Users\rudpa\obsidian-agente\agent |
| Modulo Integracao | C:\Users\rudpa\obsidian-agente\agent\ollama_integration.py |
| Este Mapa | ...\Vida & Estudo\IA\MAPA_CENTRAL_MANUS_LLAMA.md |

---

## 3. Como Chamar os Agentes

### Prefixos Explicitos
| Prefixo | Destino | Exemplo |
|---------|---------|--------|
| Manus: | Manus Cloud | Manus: pesquise sobre Angular |
| Llama: | Ollama Local | Llama: o que e Python? |
| Local: | Ollama Local | Local: traduza hello world |
| Ollama: | Ollama Local | Ollama: explique machine learning |

### Deteccao Automatica
**Vai para MANUS:** pesquisar, internet, browser, navegador, abrir, instalar, arquivo, desktop, api, docker, git, email, obsidian, nota, sistema, windows, powershell

**Vai para LLAMA:** explique, o que e, defina, resuma, traduza, calcule, liste, como funciona, diferenca, escreva, codigo, simples

---

## 4. Comandos PowerShell

### Verificar Ollama
Invoke-RestMethod -Uri http://localhost:11434/api/tags

### Listar Modelos
ollama list

### Pergunta Direta ao Llama
\ = @{model="llama3.2:latest"; prompt="O que e Python?"; stream=\False} | ConvertTo-Json
Invoke-RestMethod -Uri http://localhost:11434/api/generate -Method Post -Body \

### Reiniciar Ollama
Stop-Process -Name ollama -Force; Start-Process ollama -ArgumentList serve -WindowStyle Hidden

### Testar Integracao
cd \C:\Users\rudpa\obsidian-agente\agent
python -c "from ollama_integration import get_ai_router; r = get_ai_router(); print(r.ollama.is_available)"

---

## 5. Solucao de Problemas

| Problema | Solucao |
|----------|--------|
| Ollama offline | Executar: ollama serve |
| Modelo nao encontrado | Executar: ollama pull llama3.2 |
| Integracao nao funciona | Verificar ollama_integration.py existe |

---

*Versao 2.0 - 23/12/2025*
