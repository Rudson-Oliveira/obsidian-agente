# Sistema IA v3.1 - Backup Completo

**Data:** 26 de Dezembro de 2025
**Versão:** 3.1 (Ollama + Health Check)

---

## Restauração Rápida

### Opção 1: Script Automático (Recomendado)

```powershell
# 1. Primeiro, configure suas credenciais
$env:ANTHROPIC_API_KEY = "sua-api-key"
$env:OBSIDIAN_TOKEN = "seu-token"
$env:NGROK_URL = "sua-url.ngrok-free.dev"

# 2. Execute o script de restauração
.\scripts\Restaurar_Sistema_IA_v3.1_SEGURO.ps1
```

### Opção 2: Com arquivo de credenciais

```powershell
.\scripts\Restaurar_Sistema_IA_v3.1_SEGURO.ps1 -CredentialsFile ".\config\CREDENCIAIS_PRIVADAS.env"
```

### Opção 3: Restauração Manual

1. Instale os pré-requisitos (Python, Node.js, Git, Obsidian, Ollama)
2. Clone o repositório: `git clone https://github.com/Rudson-Oliveira/obsidian-agente.git`
3. Siga o guia em `docs/BACKUP_E_RESTAURACAO_SEGURO_26Dez2025.md`

---

## Estrutura do Backup

```
Sistema_IA_Backup_v3.1/
├── README.md                              # Este arquivo
├── config/
│   ├── sistema_ia_config_SEGURO.json      # Configurações (sem credenciais)
│   └── CREDENCIAIS_PRIVADAS.env           # Suas credenciais (NÃO COMPARTILHAR)
├── docs/
│   └── BACKUP_E_RESTAURACAO_SEGURO_26Dez2025.md
└── scripts/
    └── Restaurar_Sistema_IA_v3.1_SEGURO.ps1
```

---

## Arquivos Importantes

| Arquivo | Descrição | Compartilhar? |
|---------|-----------|---------------|
| `sistema_ia_config_SEGURO.json` | Configurações do sistema | ✅ Sim |
| `CREDENCIAIS_PRIVADAS.env` | API Keys e tokens | ❌ NÃO |
| `Restaurar_Sistema_IA_v3.1_SEGURO.ps1` | Script de restauração | ✅ Sim |
| `BACKUP_E_RESTAURACAO_SEGURO_26Dez2025.md` | Documentação completa | ✅ Sim |

---

## Restauração pelo Manus AI

Para restauração assistida, forneça este backup ao **Manus AI** e diga:

> "Restaurar Sistema IA v3.1 usando o backup fornecido. Minhas credenciais são:
> - API Key: [sua-key]
> - Obsidian Token: [seu-token]
> - ngrok URL: [sua-url]"

---

## GitHub

**Repositório:** https://github.com/Rudson-Oliveira/obsidian-agente

O código fonte completo está no GitHub. Este backup contém apenas os scripts de restauração e configurações.

---

**Criado por Manus AI para Rudson-Oliveira**
