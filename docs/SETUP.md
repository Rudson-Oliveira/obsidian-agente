# Setup Completo - Obsidian Agente

## Pré-requisitos

- **Node.js** 18+ ([Download](https://nodejs.org/))
- **Python** 3.10+ ([Download](https://www.python.org/))
- **Obsidian** instalado no seu computador
- **Git** instalado

## Instalação Passo a Passo

### 1. Clonar o Repositório

```bash
git clone https://github.com/Rudson-Oliveira/obsidian-agente.git
cd obsidian-agente
```

### 2. Instalar e Executar o Agente

#### Windows

```bash
cd agent
pip install -r requirements.txt
python agent.py
```

#### macOS/Linux

```bash
cd agent
python3 -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
pip install -r requirements.txt
python3 agent.py
```

**Saída esperada:**
```
2025-12-13 15:20:00,000 - __main__ - INFO - Iniciando Obsidian Desktop Agent...
2025-12-13 15:20:00,001 - __main__ - INFO - Servidor rodando em http://localhost:5001
```

**Guarde a API Key que será exibida!** Exemplo:
```
API Key: BO_1JSygh7Ia961cOdYcoc42GhxCVil9A1qvZQWFZ2c
```

### 3. Instalar e Executar a Aplicação Web

Em um **novo terminal**:

```bash
cd frontend
npm install
npm run dev
```

A aplicação abrirá em `http://localhost:5173`

### 4. Configurar a Aplicação Web

Na interface web, você verá um campo para inserir a **API Key**. Cole a chave que foi gerada no passo 2.

## Verificar se Tudo Está Funcionando

### Teste 1: Health Check

```bash
curl http://localhost:5001/health
```

Resposta esperada:
```json
{
  "status": "online",
  "version": "1.1"
}
```

### Teste 2: Abrir Obsidian via API

```bash
curl -X POST http://localhost:5001/obsidian/open \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json"
```

O Obsidian deve abrir automaticamente.

### Teste 3: Usar a Aplicação Web

1. Acesse `http://localhost:5173`
2. Insira um comando como: "Abra o Obsidian"
3. O Obsidian deve abrir

## Configuração Avançada

### Mudar a Porta do Agente

Edite `agent/config.json`:

```json
{
  "port": 5002,
  "api_key": "BO_1JSygh7Ia961cOdYcoc42GhxCVil9A1qvZQWFZ2c",
  "obsidian_path": "C:\\Users\\rudpa\\AppData\\Local\\Programs\\Obsidian"
}
```

### Configurar CORS

Edite `agent/agent.py` e procure por:

```python
CORS(app, resources={r"/api/*": {"origins": ["http://localhost:5173"]}})
```

Modifique `origins` conforme necessário.

## Troubleshooting

### "Conexão recusada" em localhost:5001

**Solução:**
1. Verifique se o agente está rodando
2. Verifique se a porta 5001 não está sendo usada por outro programa
3. Tente mudar a porta em `config.json`

### "API Key inválida"

**Solução:**
1. Copie a chave exata que foi exibida ao iniciar o agente
2. Verifique se não há espaços extras
3. Reinicie o agente para gerar uma nova chave

### Obsidian não abre via API

**Solução:**
1. Verifique se o Obsidian está instalado
2. Verifique o caminho em `config.json`
3. Tente abrir o Obsidian manualmente primeiro

## Próximos Passos

1. Leia a [Referência da API](./API.md)
2. Explore os exemplos em `frontend/src/`
3. Customize a aplicação web conforme necessário

## Suporte

Para problemas, consulte [TROUBLESHOOTING.md](./TROUBLESHOOTING.md)
