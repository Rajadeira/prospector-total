# gerar_relatorio.ps1
$json = Get-Content "oportunidades_completas.json" -Raw | ConvertFrom-Json

$html = @"
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <title>Prospector - Oportunidades de Negócio</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
        h1 { color: #2c3e50; }
        .categoria { background: #3498db; color: white; padding: 10px; margin-top: 20px; border-radius: 5px; }
        .oportunidade { background: white; padding: 15px; margin: 10px 0; border-radius: 5px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
        .titulo { font-size: 16px; font-weight: bold; }
        .link { color: #2980b9; text-decoration: none; }
        .palavra { color: #e74c3c; font-size: 12px; margin-top: 5px; }
        .data { color: #7f8c8d; font-size: 12px; }
        .nenhuma { color: #999; text-align: center; padding: 40px; }
    </style>
</head>
<body>
    <h1>🚀 Prospector - Oportunidades de Negócio</h1>
    <p>Última atualização: $([DateTime]::Now.ToString('dd/MM/yyyy HH:mm:ss'))</p>
"@

if ($json.Count -gt 0) {
    $porCategoria = $json | Group-Object categoria
    
    foreach ($cat in $porCategoria) {
        $html += @"
    <div class="categoria">📌 $($cat.Name) ($($cat.Count))</div>
"@
        foreach ($item in $cat.Group) {
            $html += @"
    <div class="oportunidade">
        <div class="titulo">$($item.titulo)</div>
        <div class="data">$($item.data)</div>
        <div><a href="$($item.link)" target="_blank" class="link">🔗 Ver notícia</a></div>
        <div class="palavra">🏷️ Palavra-chave: $($item.palavra_chave)</div>
    </div>
"@
        }
    }
} else {
    $html += @'
    <div class="nenhuma">
        ⚠️ Nenhuma oportunidade encontrada.<br>
        Execute <strong>python mega_prospector.py</strong> para buscar novas oportunidades.
    </div>
'@
}

$html += @"
</body>
</html>
"@

$html | Out-File -FilePath "relatorio_oportunidades.html" -Encoding UTF8

Write-Host "✅ Relatório gerado: relatorio_oportunidades.html"
Write-Host "📁 Abrindo no navegador..."
Start-Process "relatorio_oportunidades.html"