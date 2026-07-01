@echo off
setlocal enabledelayedexpansion
cd /d "%~dp0"

set "PYTHON=.venv\Scripts\python.exe"
set "VENV_PYTHON=.venv\Scripts\python.exe"

if not exist .env (
    echo ==========================================
    echo  Townsq QA - Environment Setup
    echo ==========================================
    set /p CPF="Digite um CPF valido para teste (ou deixe em branco): "
    set /p EMAIL="Digite um e-mail para teste (ou deixe em branco): "
    set /p PASS="Digite uma senha para teste (ou deixe em branco): "
    (
        echo BASE_URL=https://townsq.octadesk.com/login
        echo USERNAME=!EMAIL!
        echo PASSWORD=!PASS!
    ) > .env
    echo .env criado com sucesso.
)

if not exist .venv (
    echo Criando ambiente virtual...
    python -m venv .venv
)

echo Instalando dependencias...
"%VENV_PYTHON%" -m pip install --upgrade pip
"%VENV_PYTHON%" -m pip install -r requirements.txt

echo Instalando navegadores do Playwright...
"%VENV_PYTHON%" -m playwright install chromium

echo Executando testes...
"%VENV_PYTHON%" -m pytest --html=reports/report.html --self-contained-html -m e2e

echo.
echo Relatorio gerado em: reports\report.html
pause
