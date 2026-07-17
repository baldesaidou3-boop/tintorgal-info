$projectDir = "C:\Users\MAMADOU SAIDOU\CODEs\tintorgal-info"
Set-Location -LiteralPath $projectDir
python scripts/update_news.py
git add index.html
git commit -m "auto: mise a jour des articles ($(Get-Date -Format 'dd/MM/yyyy'))"
git push
