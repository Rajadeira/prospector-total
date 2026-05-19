@echo off
echo Atualizando oportunidades...
python mega_prospector.py
echo.
echo Gerando relatorio HTML...
python -c "import json; from datetime import datetime; f=open('oportunidades_completas.json','r',encoding='utf-8'); dados=json.load(f); html='<html><head><meta charset=\'UTF-8\'><title>Oportunidades</title><style>body{font-family:Arial;margin:20px;background:#f0f0f0;}h1{color:#2c3e50;}.card{background:white;margin:15px 0;padding:15px;border-radius:8px;box-shadow:0 2px 5px rgba(0,0,0,0.1);}.cat{background:#3498db;color:white;padding:5px 10px;border-radius:5px;display:inline-block;font-size:12px;}.titulo{font-size:16px;font-weight:bold;margin:10px 0;}.link{color:#2980b9;}.palavra{color:#e74c3c;font-size:12px;}</style></head><body><h1>🚀 Prospector - Oportunidades</h1><p>Gerado: '+datetime.now().strftime('%d/%m/%Y %H:%M:%S')+'</p>'; [html+='<div class=\'card\'><div class=\'cat\'>'+i['categoria']+'</div><div class=\'titulo\'>'+i['titulo']+'</div><a href=\''+i['link']+'\' target=\'_blank\' class=\'link\'>🔗 Ver noticia</a><div class=\'palavra\'>🏷️ '+i['palavra_chave']+'</div></div>' for i in dados]; html+='</body></html>'; open('relatorio.html','w',encoding='utf-8').write(html); print(f'✅ {len(dados)} oportunidades salvas'); f.close()"
echo.
echo Abrindo relatorio...
start relatorio.html
echo.
pause