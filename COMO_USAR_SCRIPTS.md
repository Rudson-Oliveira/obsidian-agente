# Como Usar os Scripts PowerShell 🚀

## 📋 Scripts Disponíveis

Este repositório contém scripts PowerShell para facilitar a instalação e uso do Obsidian Agente.

### 1. `INSTALAR_AGENTE.ps1`
**O que faz:**
- ✅ Verifica se Git e Python estão instalados
- ✅ Clona o repositório (ou atualiza se já existir)
- ✅ Instala todas as dependências Python
- ✅ Inicia o agente automaticamente
- ✅ Exibe a API Key para você copiar

**Como usar:**
```powershell
# Abra o PowerShell como Administrador
# Navegue até onde baixou o script
cd C:\Users\rudpa\Downloads

# Execute o script
.\INSTALAR_AGENTE.ps1
```

---

### 2. `INICIAR_AGENTE.ps1`
**O que faz:**
- ✅ Inicia o agente rapidamente (após instalação)
- ✅ Exibe a API Key

**Como usar:**
```powershell
# Abra o PowerShell
cd C:\Users\rudpa\obsidian-agente

# Execute o script
.\INICIAR_AGENTE.ps1
```

---

### 3. `INSTALAR_FRONTEND.ps1`
**O que faz:**
- ✅ Verifica se Node.js está instalado
- ✅ Instala as dependências do frontend
- ✅ Inicia a aplicação web em `http://localhost:5173`

**Como usar:**
```powershell
# Abra um NOVO PowerShell (deixe o agente rodando no outro)
cd C:\Users\rudpa\obsidian-agente

# Execute o script
.\INSTALAR_FRONTEND.ps1
```

---

## 🎯 Fluxo Completo de Instalação

### Primeira Vez (Instalação Completa)

**Passo 1: Instalar o Agente**
```powershell
# PowerShell 1 (como Administrador)
.\INSTALAR_AGENTE.ps1
# ⚠️ Copie a API Key que será exibida!
```

**Passo 2: Instalar o Frontend**
```powershell
# PowerShell 2 (novo terminal)
.\INSTALAR_FRONTEND.ps1
# Acesse http://localhost:5173
# Cole a API Key copiada
```

---

### Uso Diário (Após Instalação)

**Terminal 1: Iniciar Agente**
```powershell
cd C:\Users\rudpa\obsidian-agente
.\INICIAR_AGENTE.ps1
```

**Terminal 2: Iniciar Frontend**
```powershell
cd C:\Users\rudpa\obsidian-agente\frontend
npm run dev
```

---

## ⚠️ Solução de Problemas

### "Não é possível executar scripts neste sistema"

**Erro:**
```
.\INSTALAR_AGENTE.ps1 : O arquivo não pode ser carregado porque a execução de scripts foi desabilitada neste sistema.
```

**Solução:**
```powershell
# Execute como Administrador
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Depois tente novamente
.\INSTALAR_AGENTE.ps1
```

---

### "Git não está instalado"

**Solução:**
1. Baixe e instale o Git: https://git-scm.com/download/win
2. Reinicie o PowerShell
3. Execute o script novamente

---

### "Python não está instalado"

**Solução:**
1. Baixe e instale o Python 3.10+: https://www.python.org/downloads/
2. **IMPORTANTE:** Marque a opção "Add Python to PATH" durante a instalação
3. Reinicie o PowerShell
4. Execute o script novamente

---

### "Node.js não está instalado"

**Solução:**
1. Baixe e instale o Node.js 18+: https://nodejs.org/
2. Reinicie o PowerShell
3. Execute o script novamente

---

## 📝 Notas Importantes

1. **API Key**: Sempre copie a API Key exibida ao iniciar o agente. Você precisará dela na aplicação web.

2. **Dois Terminais**: Você precisa de dois terminais PowerShell abertos:
   - Terminal 1: Agente (rodando continuamente)
   - Terminal 2: Frontend (rodando continuamente)

3. **Porta 5001**: O agente roda em `http://localhost:5001`. Certifique-se de que essa porta não está em uso.

4. **Porta 5173**: O frontend roda em `http://localhost:5173`. Certifique-se de que essa porta não está em uso.

---

## 🔄 Atualizar o Repositório

Se houver atualizações no GitHub:

```powershell
cd C:\Users\rudpa\obsidian-agente
git pull origin master
```

---

## 🆘 Precisa de Ajuda?

Consulte a documentação completa:
- [GUIA_COMPLETO.md](./GUIA_COMPLETO.md)
- [docs/SETUP.md](./docs/SETUP.md)
- [docs/TROUBLESHOOTING.md](./docs/TROUBLESHOOTING.md)

---

**Desenvolvido para facilitar sua vida! 🚀**
