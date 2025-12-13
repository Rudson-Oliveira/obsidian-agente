# Referência da API - Obsidian Agente

## Base URL

```
http://localhost:5001
```

## Autenticação

Todas as requisições devem incluir a chave de API no header:

```
Authorization: Bearer YOUR_API_KEY
```

## Endpoints

### Health Check

**GET** `/health`

Verifica se o agente está online e respondendo.

**Response:**
```json
{
  "status": "online",
  "version": "1.1",
  "timestamp": "2025-12-13T15:20:00Z"
}
```

---

### Obsidian - Abrir

**POST** `/obsidian/open`

Abre a aplicação Obsidian.

**Request:**
```json
{}
```

**Response:**
```json
{
  "success": true,
  "message": "Obsidian aberto com sucesso"
}
```

---

### Arquivo - Ler

**POST** `/file/read`

Lê o conteúdo de um arquivo.

**Request:**
```json
{
  "path": "C:\\Users\\rudpa\\Obsidian\\vault\\nota.md"
}
```

**Response:**
```json
{
  "success": true,
  "content": "# Minha Nota\n\nConteúdo da nota...",
  "path": "C:\\Users\\rudpa\\Obsidian\\vault\\nota.md"
}
```

---

### Arquivo - Escrever

**POST** `/file/write`

Escreve conteúdo em um arquivo.

**Request:**
```json
{
  "path": "C:\\Users\\rudpa\\Obsidian\\vault\\nova-nota.md",
  "content": "# Nova Nota\n\nConteúdo aqui..."
}
```

**Response:**
```json
{
  "success": true,
  "message": "Arquivo escrito com sucesso",
  "path": "C:\\Users\\rudpa\\Obsidian\\vault\\nova-nota.md"
}
```

---

### Comando - Executar

**POST** `/command/execute`

Executa um comando no sistema.

**Request:**
```json
{
  "command": "dir C:\\Users\\rudpa\\Obsidian\\vault"
}
```

**Response:**
```json
{
  "success": true,
  "output": "Listagem de arquivos...",
  "exit_code": 0
}
```

---

### Obsidian - Listar Notas

**GET** `/obsidian/notes`

Lista todas as notas do vault.

**Response:**
```json
{
  "success": true,
  "notes": [
    {
      "name": "nota1.md",
      "path": "C:\\Users\\rudpa\\Obsidian\\vault\\nota1.md",
      "created": "2025-12-13T10:00:00Z",
      "modified": "2025-12-13T14:30:00Z"
    }
  ],
  "count": 1
}
```

---

## Códigos de Erro

| Código | Descrição |
|--------|-----------|
| 200 | Sucesso |
| 400 | Requisição inválida |
| 401 | Não autorizado (API Key inválida) |
| 404 | Recurso não encontrado |
| 500 | Erro interno do servidor |

---

## Exemplos de Uso

### Python

```python
import requests

BASE_URL = "http://localhost:5001"
API_KEY = "BO_1JSygh7Ia961cOdYcoc42GhxCVil9A1qvZQWFZ2c"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# Health check
response = requests.get(f"{BASE_URL}/health", headers=headers)
print(response.json())

# Ler arquivo
response = requests.post(
    f"{BASE_URL}/file/read",
    headers=headers,
    json={"path": "C:\\Users\\rudpa\\Obsidian\\vault\\nota.md"}
)
print(response.json())
```

### JavaScript

```javascript
const BASE_URL = "http://localhost:5001";
const API_KEY = "BO_1JSygh7Ia961cOdYcoc42GhxCVil9A1qvZQWFZ2c";

const headers = {
  "Authorization": `Bearer ${API_KEY}`,
  "Content-Type": "application/json"
};

// Health check
fetch(`${BASE_URL}/health`, { headers })
  .then(res => res.json())
  .then(data => console.log(data));

// Ler arquivo
fetch(`${BASE_URL}/file/read`, {
  method: "POST",
  headers,
  body: JSON.stringify({
    path: "C:\\Users\\rudpa\\Obsidian\\vault\\nota.md"
  })
})
  .then(res => res.json())
  .then(data => console.log(data));
```

---

## Rate Limiting

Não há rate limiting configurado no momento. Para produção, recomenda-se implementar.

---

## Changelog

### v1.1
- ✅ Endpoints básicos implementados
- ✅ Autenticação por API Key
- ✅ CORS configurado

### v1.0
- ✅ Versão inicial
