# 📚 Referência da API - Obsidian Agente v2.0

Esta documentação descreve os endpoints da API do Obsidian Agente.

**URL Base:** `http://localhost:5001`

---

## 🔐 Autenticação

Todas as requisições (exceto `/health`) exigem um token de autenticação no cabeçalho:

`Authorization: Bearer <SUA_API_KEY>`

---

## 🧠 Endpoint Inteligente

### `POST /intelligent/process`

Processa um comando em linguagem natural e executa a ação correspondente.

**Request Body:**

```json
{
  "text": "Criar uma nova nota chamada Teste"
}
```

**Response (Sucesso):**

```json
{
  "success": true,
  "command": "create_note",
  "response": "✅ Nota 'Teste' criada com sucesso!",
  "data": null
}
```

**Response (Erro):**

```json
{
  "success": false,
  "error": "Texto não fornecido"
}
```

---

## ⚙️ Endpoints de Gerenciamento

### `GET /health`

Verifica se o agente está online.

**Response:**

```json
{
  "status": "online",
  "version": "2.0"
}
```

### `GET /config`

Retorna informações de configuração do agente.

**Response:**

```json
{
  "port": 5001,
  "version": "2.0",
  "obsidian_path": "C:\\Users\\...\\Obsidian.exe",
  "features": [
    "intelligent_processing",
    "nlp_commands",
    "obsidian_knowledge"
  ]
}
```

---

## 📂 Endpoints de Vault

### `POST /obsidian/vault/configure`

Configura o caminho do vault do Obsidian.

**Request Body:**

```json
{
  "vault_path": "C:\\Users\\...\\Meu Vault"
}
```

### `GET /obsidian/vault/stats`

Retorna estatísticas do vault (número de notas, palavras, links, etc.).

---

## 📝 Endpoints de Notas

### `GET /obsidian/notes`

Lista todas as notas do vault.

### `POST /obsidian/note/create`

Cria uma nova nota.

**Request Body:**

```json
{
  "title": "Nova Nota",
  "content": "Conteúdo da nota"
}
```

### `POST /obsidian/note/search`

Busca notas por conteúdo.

**Request Body:**

```json
{
  "query": "termo de busca"
}
```

---

## 🔗 Endpoints Avançados

### `POST /obsidian/advanced/backlinks`

Encontra backlinks para uma nota específica.

**Request Body:**

```json
{
  "note_name": "Nome da Nota"
}
```

### `POST /obsidian/advanced/tags`

Encontra notas por uma tag específica.

**Request Body:**

```json
{
  "tag": "minha-tag"
}
```

### `GET /obsidian/advanced/graph`

Gera dados para visualização de grafo do vault.
