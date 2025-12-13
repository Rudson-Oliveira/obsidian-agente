# Troubleshooting - Obsidian Agente

## Problemas Comuns

### 1. "Erro de Demonstração" - Agente não responde

**Sintoma:** A aplicação web diz "Como sou uma demonstração..."

**Causa:** A aplicação web não está se conectando ao agente local.

**Solução:**

```bash
# 1. Verifique se o agente está rodando
curl http://localhost:5001/health

# 2. Se não responder, reinicie o agente
cd agent
python agent.py

# 3. Verifique a porta em config.json
cat agent/config.json

# 4. Se a porta for diferente, atualize na aplicação web
# Edite frontend/src/config.ts e mude BASE_URL
```

---

### 2. "Conexão recusada" em localhost:5001

**Sintoma:** `Error: connect ECONNREFUSED 127.0.0.1:5001`

**Causa:** O agente não está rodando ou a porta está bloqueada.

**Solução:**

```bash
# Verifique se algo está usando a porta 5001
netstat -ano | findstr :5001  # Windows
lsof -i :5001                  # macOS/Linux

# Se estiver em uso, mude a porta em config.json
# Ou mate o processo que está usando

# Reinicie o agente
cd agent
python agent.py
```

---

### 3. "API Key inválida"

**Sintoma:** Erro 401 ao fazer requisições

**Solução:**

```bash
# 1. Verifique a chave em config.json
cat agent/config.json

# 2. Copie a chave exata (sem espaços)
# 3. Cole na aplicação web

# 4. Se não funcionar, regenere uma nova chave
# Edite config.json e mude o valor de api_key

# 5. Reinicie o agente
python agent.py
```

---

### 4. Obsidian não abre via API

**Sintoma:** Comando `/obsidian/open` retorna erro

**Solução:**

```bash
# 1. Verifique se Obsidian está instalado
# Windows: Procure em C:\Users\[USER]\AppData\Local\Programs\Obsidian

# 2. Verifique o caminho em config.json
# Deve apontar para Obsidian.exe

# 3. Tente abrir manualmente primeiro
# Isso garante que Obsidian está funcionando

# 4. Se ainda não funcionar, verifique os logs
# Eles devem mostrar o erro específico
```

---

### 5. "Arquivo não encontrado"

**Sintoma:** Erro ao tentar ler/escrever arquivo

**Solução:**

```bash
# 1. Verifique se o caminho está correto
# Use barras invertidas duplas: C:\\Users\\...

# 2. Verifique se o arquivo existe
# Use o explorador de arquivos

# 3. Verifique as permissões
# O agente precisa de permissão de leitura/escrita

# 4. Teste com um arquivo simples primeiro
# Exemplo: C:\\Users\\rudpa\\test.txt
```

---

### 6. Aplicação web não carrega

**Sintoma:** Página em branco ou erro de conexão

**Solução:**

```bash
# 1. Verifique se o servidor web está rodando
# Deve estar em http://localhost:5173

# 2. Reinicie o servidor
cd frontend
npm run dev

# 3. Limpe o cache do navegador
# Pressione Ctrl+Shift+Delete

# 4. Verifique o console do navegador
# F12 > Console para ver erros específicos
```

---

### 7. CORS Error

**Sintoma:** `Access to XMLHttpRequest blocked by CORS policy`

**Solução:**

```bash
# 1. Verifique a configuração de CORS no agente
# Arquivo: agent/agent.py

# 2. Adicione a origem correta
# Exemplo: http://localhost:5173

# 3. Reinicie o agente
python agent.py
```

---

### 8. Porta 5173 já está em uso

**Sintoma:** `Error: listen EADDRINUSE :::5173`

**Solução:**

```bash
# Mude a porta
npm run dev -- --port 5174

# Ou mate o processo que está usando
netstat -ano | findstr :5173  # Windows
lsof -i :5173                  # macOS/Linux
```

---

## Logs e Debugging

### Ver logs do agente

```bash
# Os logs aparecem no terminal onde o agente está rodando
# Procure por mensagens de erro
```

### Ver logs da aplicação web

```bash
# Abra o navegador
# Pressione F12
# Vá para a aba Console
# Procure por mensagens de erro em vermelho
```

### Ativar modo debug

No `agent/agent.py`, mude:

```python
app.run(debug=True)  # Ativa modo debug
```

---

## Checklist de Diagnóstico

- [ ] Agente está rodando em `http://localhost:5001`?
- [ ] Aplicação web está rodando em `http://localhost:5173`?
- [ ] API Key está correta?
- [ ] Obsidian está instalado?
- [ ] Portas 5001 e 5173 não estão bloqueadas?
- [ ] Firewall permite conexões locais?
- [ ] Python 3.10+ instalado?
- [ ] Node.js 18+ instalado?

---

## Ainda não funcionou?

1. Verifique os logs completos (agente + navegador)
2. Tente reproduzir o erro com um comando simples
3. Reinicie tudo (agente + aplicação web + navegador)
4. Consulte a [Documentação da API](./API.md)

---

## Contato

Para problemas não resolvidos, abra uma issue no GitHub.
