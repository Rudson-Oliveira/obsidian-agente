param([string]$M)
if(-not $M){Write-Host "Uso: ia sua_mensagem";Write-Host "Prefixos: Manus: Llama: Local:";return}
$m = $M.ToLower()
$manus = @("pesquisar","pesquise","navegador","browser","abrir","abra","instalar","instale","arquivo","desktop","api","docker","git","baixar","email","obsidian","nota","sistema","windows","powershell")
if($m.StartsWith("manus:")){Write-Host "[MANUS] Abra manus.im e envie:" -ForegroundColor Yellow;Write-Host $M.Substring(6);return}
if($m.StartsWith("llama:") -or $m.StartsWith("local:") -or $m.StartsWith("ollama:")){
    $len=6;if($m.StartsWith("ollama:")){$len=7}
    $p=$M.Substring($len)
    $b=@{model="llama3.2:latest";prompt=$p;stream=$false}|ConvertTo-Json
    try{$r=Invoke-RestMethod -Uri "http://localhost:11434/api/generate" -Method Post -Body $b -ContentType "application/json" -TimeoutSec 120;Write-Host "[LLAMA]" -ForegroundColor Cyan;Write-Host $r.response}catch{Write-Host "Erro: Ollama offline" -ForegroundColor Red}
    return
}
$useManus=$false;foreach($k in $manus){if($m -like "*$k*"){$useManus=$true;break}}
if($useManus){Write-Host "[MANUS] Abra manus.im e envie:" -ForegroundColor Yellow;Write-Host $M}else{
    $b=@{model="llama3.2:latest";prompt=$M;stream=$false}|ConvertTo-Json
    try{$r=Invoke-RestMethod -Uri "http://localhost:11434/api/generate" -Method Post -Body $b -ContentType "application/json" -TimeoutSec 120;Write-Host "[LLAMA]" -ForegroundColor Cyan;Write-Host $r.response}catch{Write-Host "Erro: Ollama offline" -ForegroundColor Red}
}
