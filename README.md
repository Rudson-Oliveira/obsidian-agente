# 🧠 Obsidian Agente Inteligente v2.0

**Seu assistente superinteligente para automação e gerenciamento de conhecimento no Obsidian.**

Este projeto implementa um agente de desktop autônomo que permite a interação com o Obsidian através de linguagem natural, com conhecimento profundo sobre o ecossistema Obsidian, incluindo plugins, temas, API e melhores práticas.

---

## ✨ Funcionalidades Principais

| Funcionalidade | Descrição |
|---|---|
| **Processamento de Linguagem Natural** | Entende comandos complexos em linguagem natural (português e inglês) |
| **Base de Conhecimento Integrada** | Conhecimento profundo sobre Obsidian (wikilinks, tags, dataview, etc.) |
| **Gerenciamento de Notas** | Criar, listar, buscar e abrir notas |
| **Funcionalidades Avançadas** | Extrair wikilinks, tags, frontmatter e executar queries Dataview |
| **Interface Inteligente** | Sugestões de comandos, histórico de conversas e visualização de dados |
| **Inicialização Automática** | Script para iniciar todo o sistema com um único clique |
| **Configuração Automática** | Detecta e configura automaticamente o caminho do Obsidian |
| **Segurança** | Autenticação via API Key para todas as requisições |

---

## 🚀 Como Usar (Instalação Rápida)

### **Requisitos**

- **Windows** 10 ou superior
- **Python 3.8+** (com `pip`)
- **Node.js 18+** (com `npm`)
- **Git**

### **Passo 1: Instalação Automática**

1.  **Abra o PowerShell como Administrador**
2.  **Execute o comando abaixo para baixar e executar o instalador:**

    ```powershell
    Invoke-WebRequest -Uri "https://raw.githubusercontent.com/Rudson-Oliveira/obsidian-agente/master/INSTALAR_AGENTE.ps1" -OutFile "INSTALAR_AGENTE.ps1"; .\INSTALAR_AGENTE.ps1
    ```

    O script irá:
    - Verificar os requisitos
    - Clonar o repositório para `C:\Users\seu_usuario\obsidian-agente`
    - Instalar todas as dependências (Python e Node.js)
    - Iniciar o agente e exibir a **API Key**

### **Passo 2: Uso Diário (Inicialização com 1 Clique)**

1.  **Navegue até a pasta do projeto:** `C:\Users\seu_usuario\obsidian-agente`
2.  **Execute o arquivo `INICIAR.bat`** (clique duplo)

    O script irá:
    - Abrir dois terminais (agente e frontend)
    - Iniciar todo o sistema automaticamente
    - Abrir a interface web no seu navegador (`http://localhost:5173`)

### **Passo 3: Configurar a API Key**

1.  **Copie a API Key** exibida no terminal do agente.
2.  **Cole a API Key** na interface web e clique em "Conectar".

**Pronto!** Agora você pode usar todos os comandos inteligentes.

---

## 🤖 Comandos Inteligentes

Você pode conversar naturalmente com o agente. Aqui estão alguns exemplos:

- **"Abrir Obsidian"**
- **"Listar todas as minhas notas"**
- **"Criar uma nova nota chamada Reunião Semanal"**
- **"Buscar por projeto X"**
- **"Explicar como funcionam os wikilinks"**
- **"Quais são os plugins mais populares?"**
- **"Ajuda"** (para ver todos os comandos)

---

## 📂 Estrutura do Projeto

```
obsidian-agente/
├── agent/                 # Agente Backend (Python + Flask)
│   ├── agent.py             # Servidor Flask e endpoints
│   ├── intelligent_agent.py # Processamento de NLP e IA
│   ├── obsidian_knowledge.py# Base de conhecimento do Obsidian
│   └── obsidian_advanced.py # Funções avançadas do Obsidian
├── frontend/              # Aplicação Web (React + TypeScript)
│   ├── src/
│   │   ├── App.tsx          # Componente principal da UI
│   │   └── services/api.ts  # Serviço de comunicação com a API
├── docs/                  # Documentação detalhada
├── INSTALAR_AGENTE.ps1    # Script de instalação automática
├── INICIAR_TUDO.ps1       # Script de inicialização completa
├── INICIAR.bat            # Atalho de inicialização
└── README.md
```

---

## 🛠️ Desenvolvimento

- **Backend:** Python 3.11, Flask, Waitress
- **Frontend:** React, TypeScript, Vite
- **Estilo:** CSS moderno com Flexbox e Grid

---

## 📄 Licença

Este projeto é licenciado sob a Licença MIT. Veja o arquivo `LICENSE` para mais detalhes.
