# gerar_html.ps1 - Versão corrigida
$json = Get-Content "oportunidades_completas.json" -Raw | ConvertFrom-Json

$html = @'
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <title>Prospector - Oportunidades</title>
    <style>
        body { font-family: Arial; margin: 20px; background: #f0f0f0; }
        h1 { color: #2c3e50; }
        .card { background: white; margin: 15px 0; padding: 15px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
        .categoria { background: #3498db; color: white; padding: 5px 10px; display: inline-block; border-radius: 5px; font-size: 12px; }
        .titulo { font-size: 16px; font-weight: bold; margin: 10px 0; }
        .link { color: #2980b9; text-decoration: none; }
        .palavra { color: #e74c3c; font-size: 12px; margin-top: 10px; }
        .data { color: #7f8c8d; font-size: 11px; }
    </style>
</head>
<body>
    <h1>🚀 Prospector - Oportunidades de Negócio</h1>
    <p>Gerado em: ' + (Get-Date -Format "dd/MM/yyyy HH:mm:ss") + '</p>
'@

if ($json.Count -gt 0) {
    foreach ($item in $json) {
        $html += @'
    <div class="card">
        <div class="categoria">' + $item.categoria + '</div>
        <div class="titulo">' + $item.titulo + '</div>
        <div class="data">' + $item.data + '</div>
        <div><a href="' + $item.link + '" target="_blank" class="link">🔗 Ver notícia</a></div>
        <div class="palavra">🏷️ Palavra-chave: ' + $item.palavra_chave + '</div>
    </div>
'@
    }
} else {
    $html += '<p>⚠️ Nenhuma oportunidade encontrada. Execute python mega_prospector.py</p>'
}

$html += @'
</body>
</html>
'@

$html | Out-File -FilePath "relatorio.html" -Encoding UTF8

Write-Host "✅ Relatório gerado: relatorio.html"
Start-Process "relatorio.html"