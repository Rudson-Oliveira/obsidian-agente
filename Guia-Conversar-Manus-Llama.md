# Guia: Como Conversar com Manus e Llama

## Introducao
Voce agora tem dois assistentes de IA disponiveis:
- **Manus** (Cloud) - Para tarefas complexas que precisam de internet, browser, arquivos
- **Llama** (Local) - Para perguntas rapidas, explicacoes, traducoes (gratis e privado)

---

## Como Escrever suas Perguntas

### Para MANUS (Cloud)
Use quando precisar de:
- Pesquisas na internet
- Automacao de browser/desktop
- Criar/editar arquivos
- Instalar programas
- Acessar APIs externas

**Exemplos de escrita:**
`
Manus: pesquise sobre as novidades do Angular 18
Manus: abra o navegador e acesse github.com
Manus: crie uma nota no Obsidian chamada "Ideias"
Manus: instale o Node.js no meu computador
Manus: baixe o arquivo do link xyz
Manus: envie um email para fulano@email.com
`

### Para LLAMA (Local)
Use quando precisar de:
- Explicacoes e definicoes
- Traducoes
- Calculos
- Resumos de texto
- Codigo simples
- Perguntas gerais

**Exemplos de escrita:**
`
Llama: o que e machine learning?
Llama: traduza "hello world" para portugues
Llama: explique a diferenca entre Python e JavaScript
Llama: escreva uma funcao que soma dois numeros
Llama: resuma o conceito de API REST
Local: calcule a raiz quadrada de 144
Ollama: liste 5 frameworks JavaScript populares
`

### Deteccao Automatica (sem prefixo)
Se voce nao usar prefixo, o sistema decide automaticamente:
`
explique o que e Docker          -> vai para Llama (local)
pesquise sobre React na internet -> vai para Manus (cloud)
calcule 25 * 4                   -> vai para Llama (local)
abra o navegador                 -> vai para Manus (cloud)
`

---

## Comandos PowerShell

### Verificar se Ollama esta rodando
`powershell
# Verificar status do Ollama
Invoke-RestMethod -Uri "http://localhost:11434/api/tags" | ConvertTo-Json
`

### Listar modelos instalados
`powershell
# Ver modelos disponiveis
(Invoke-RestMethod -Uri "http://localhost:11434/api/tags").models.name
`

### Fazer uma pergunta direta ao Llama via PowerShell
`powershell
# Pergunta simples ao Llama
$body = @{
    model = "llama3.2:latest"
    prompt = "O que e Python em uma frase?"
    stream = $false
} | ConvertTo-Json

$response = Invoke-RestMethod -Uri "http://localhost:11434/api/generate" -Method Post -Body $body -ContentType "application/json"
$response.response
`

### Iniciar Ollama (se nao estiver rodando)
`powershell
# Iniciar Ollama
Start-Process "ollama" -ArgumentList "serve" -WindowStyle Hidden
`

### Parar Ollama
`powershell
# Parar Ollama
Stop-Process -Name "ollama" -Force
`

### Testar a integracao Python
`powershell
# Testar modulo de integracao
cd $env:USERPROFILE\obsidian-agente\agent
python -c "from ollama_integration import get_ai_router; r = get_ai_router(); print(Ollama:, r.ollama.is_available); print(Modelos:, r.ollama.available_models)"
`

---

## Dicas de Escrita

### Seja especifico
| Ruim | Bom |
|------|-----|
| pesquise algo | Manus: pesquise sobre React 18 hooks |
| explique isso | Llama: explique o que e uma API REST |
| faca um codigo | Llama: escreva uma funcao Python que ordena uma lista |

### Use o prefixo certo
| Tarefa | Prefixo |
|--------|--------|
| Precisa de internet | Manus: |
| Pergunta simples | Llama: |
| Criar arquivo | Manus: |
| Traducao | Llama: |
| Instalar programa | Manus: |
| Explicacao | Llama: |

---

## Palavras-chave que ativam cada IA

### Palavras que vao para MANUS:
browser, navegador, pesquisar, internet, site, desktop, arquivo, instalar, executar, abrir, api, docker, git, baixar, email, obsidian, nota, sistema, windows, powershell, imagem, pdf

### Palavras que vao para LLAMA:
explique, o que e, defina, resuma, traduza, calcule, liste, como funciona, diferenca, escreva, codigo, simples

---

## Solucao de Problemas

### Ollama nao responde
`powershell
# Reiniciar Ollama
Stop-Process -Name "ollama" -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 2
Start-Process "ollama" -ArgumentList "serve" -WindowStyle Hidden
`

### Verificar se modelos estao instalados
`powershell
ollama list
`

### Baixar modelo adicional
`powershell
ollama pull codellama  # Para codigo
ollama pull mistral    # Alternativa ao Llama
`

---

*Guia criado em: 2025-12-23*
*Versao: 1.0*
