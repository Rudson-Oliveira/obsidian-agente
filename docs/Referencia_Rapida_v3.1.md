# Sistema IA v3.1 - Referência Rápida

**Data:** 26 de Dezembro de 2025

---

## Inicialização

**Script:** `C:\Users\rudpa\COMET\Iniciar_Sistema_IA.bat`

Clique duplo no script para iniciar todos os 9 serviços automaticamente.

---

## Serviços e Portas

| Serviço | Porta | Status |
|---------|-------|--------|
| Obsidian | - | Interface |
| Ollama | 11434 | LLM Local |
| COMET Bridge | 5000 | Ponte Remota |
| ngrok | - | Túnel |
| Obsidian Agent | 5001 | Agente |
| Hub Central | 5002 | Coordenador |
| Vision Server | 5003 | Visão |
| Frontend | 5173 | Web UI |
| Claude Code | - | Terminal IA |

---

## URLs Importantes

- **ngrok (Acesso Remoto):** https://charmless-maureen-subadministratively.ngrok-free.dev
- **Frontend Local:** http://localhost:5173
- **COMET Bridge Local:** http://localhost:5000

---

## Comandos Úteis

### Claude Code
```bash
claude -p "sua pergunta"    # Pergunta rápida
claude chat                 # Modo conversação
claude --help               # Ajuda
```

### Ollama
```bash
ollama list                 # Listar modelos
ollama run gemma3:4b        # Executar modelo
```

---

## Troubleshooting Rápido

| Problema | Solução |
|----------|---------|
| Painel Obsidian em branco | Feche e reabra o Obsidian |
| ngrok 502 | Reinicie o script (health check corrige) |
| Serviço não responde | Verifique a janela do serviço |

---

## Arquivos Importantes

- `C:\Users\rudpa\COMET\Iniciar_Sistema_IA.bat` - Script de inicialização
- `C:\Users\rudpa\COMET\manus_bridge_unified.py` - COMET Bridge
- `C:\Users\rudpa\.claude\` - Configuração Claude Code
- `C:\Users\rudpa\COMET\Documentacao\` - Documentação

---

**Versão:** 3.1 (Ollama + Health Check)
