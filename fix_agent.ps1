# Script para corrigir o endpoint /config no agent.py
$filePath = "C:\Users\rudpa\obsidian-agente\agent\agent.py"
$content = Get-Content $filePath -Raw

# Substituir versão 2.0 por 5.0
$content = $content -replace "'version': '2\.0'", "'version': '5.0'"

# Adicionar api_key se não existir
if ($content -notmatch "'api_key': config\.get\('api_key'\)") {
    $oldPattern = @"
return jsonify\(\{
        'port': config\.get\('port'\),
        'version': '5\.0',
        'obsidian_path': config\.get\('obsidian_path'\),
        'features': \['intelligent_processing', 'nlp_commands', 'obsidian_knowledge'\]
    \}\)
"@
    
    $newCode = @"
return jsonify({
        'port': config.get('port'),
        'version': '5.0',
        'api_key': config.get('api_key'),
        'obsidian_path': config.get('obsidian_path'),
        'vault_path': config.get('vault_path'),
        'features': ['intelligent_processing', 'nlp_commands', 'obsidian_knowledge', 'auto_config']
    })
"@
    
    # Tentar substituição mais simples
    $content = $content -replace "'features': \['intelligent_processing', 'nlp_commands', 'obsidian_knowledge'\]", "'api_key': config.get('api_key'),`n        'vault_path': config.get('vault_path'),`n        'features': ['intelligent_processing', 'nlp_commands', 'obsidian_knowledge', 'auto_config']"
}

# Salvar arquivo
$content | Set-Content $filePath -Encoding UTF8
Write-Host "agent.py corrigido com sucesso!"

