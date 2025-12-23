param([string]$P)
if(-not $P){Write-Host "Uso: llama sua_pergunta";return}
$b = @{model="llama3.2:latest";prompt=$P;stream=$false} | ConvertTo-Json
try {
    $r = Invoke-RestMethod -Uri "http://localhost:11434/api/generate" -Method Post -Body $b -ContentType "application/json" -TimeoutSec 120
    Write-Host "[LLAMA]" -ForegroundColor Cyan
    Write-Host $r.response
} catch {
    Write-Host "Erro: Ollama offline. Execute: ollama serve" -ForegroundColor Red
}
