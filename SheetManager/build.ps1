# ============================================
# Script de Build - SheetManager v1.0
# ============================================

Write-Host "Iniciando build do SheetManager..." -ForegroundColor Cyan

# 1. Limpar builds anteriores
Write-Host "`nLimpando builds anteriores..." -ForegroundColor Yellow
if (Test-Path "build") { Remove-Item -Recurse -Force build }
if (Test-Path "dist") { Remove-Item -Recurse -Force dist }
if (Test-Path "*.spec") { Remove-Item -Force *.spec }

# 2. Verificar se o icone existe
if (-Not (Test-Path "icon.ico")) {
    Write-Host "Aviso: icon.ico nao encontrado. O executavel sera gerado sem icone." -ForegroundColor Red
    $iconParam = ""
} else {
    $iconParam = "--icon=icon.ico"
}

# 3. Gerar o executavel
Write-Host "`nGerando executavel..." -ForegroundColor Green
pyinstaller --windowed `
    --name="SheetManager" `
    $iconParam `
    --add-data="..\README.md;." `
    --noconsole `
    --clean `
    app.py

# 4. Verificar se o build foi bem-sucedido
if ($LASTEXITCODE -eq 0) {
    Write-Host "`nBuild concluido com sucesso!" -ForegroundColor Green
    Write-Host "Executavel disponivel em: dist\SheetManager\" -ForegroundColor Cyan
    
    # 5. Copiar arquivos extras para a pasta dist
    Write-Host "`nCopiando arquivos extras..." -ForegroundColor Yellow
    Copy-Item "README.md" -Destination "dist\SheetManager\" -ErrorAction SilentlyContinue
    
    # 6. Criar um arquivo de versao
    $pythonVersion = python --version 2>&1
    $buildDate = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $versionInfo = "SheetManager v1.0`nBuild: $buildDate`nPython: $pythonVersion"
    
    $versionInfo | Out-File -FilePath "dist\SheetManager\VERSION.txt" -Encoding UTF8
    
    Write-Host "`nPronto para distribuicao!" -ForegroundColor Green
    Write-Host "Proximo passo: Gerar o instalador com Inno Setup" -ForegroundColor Cyan
} else {
    Write-Host "`nErro durante o build!" -ForegroundColor Red
    exit 1
}