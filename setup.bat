@echo off
setlocal enabledelayedexpansion
cd /d "%~dp0"

set "ALLURE_RESULTS=allure-results"
set "ALLURE_REPORT=allure-report"
set "VENV_DIR=.venv"
set "VENV_PYTHON=%VENV_DIR%\Scripts\python.exe"
set "VENV_ACTIVATE_BAT=%VENV_DIR%\Scripts\activate.bat"
set "VENV_ACTIVATE_PS1=%VENV_DIR%\Scripts\Activate.ps1"

echo ==============================
echo Townsq QA - Setup de Testes
echo ==============================

echo.
echo ==============================
echo Criando arquivo .env
echo ==============================
if not exist .env (
    set /p EMAIL="Digite um e-mail para teste: "
    set /p PASS="Digite uma senha para teste: "
    (
        echo BASE_URL=https://townsq.octadesk.com/login
        echo USERNAME=!EMAIL!
        echo PASSWORD=!PASS!
    ) > .env
    if errorlevel 1 (
        echo Falha ao criar o arquivo .env.
        pause
        exit /b 1
    )
    echo .env criado com sucesso.
) else (
    echo .env ja existe. Mantendo configuracao atual.
)

echo.
echo ==============================
echo Criando ambiente virtual
echo ==============================
if not exist "%VENV_PYTHON%" (
    python -m venv %VENV_DIR%
    if errorlevel 1 (
        echo Falha ao criar a virtualenv.
        pause
        exit /b 1
    )
)
if not exist "%VENV_PYTHON%" (
    echo Python da virtualenv nao encontrado em %VENV_PYTHON%
    pause
    exit /b 1
)

echo.
echo ==============================
echo Ativando ambiente virtual
echo ==============================
call "%VENV_ACTIVATE_BAT%" >nul 2>nul
if errorlevel 1 (
    powershell -NoProfile -ExecutionPolicy Bypass -Command "& '%VENV_ACTIVATE_PS1%'" >nul 2>nul
)
if errorlevel 1 (
    echo Falha ao ativar o ambiente virtual.
    pause
    exit /b 1
)

echo Ambiente virtual ativado: %VIRTUAL_ENV%

echo.
echo ==============================
echo Instalando dependencias
echo ==============================
python -m pip install --upgrade pip
if errorlevel 1 (
    echo Falha ao atualizar pip.
    pause
    exit /b 1
)
python -m pip install -r requirements.txt
if errorlevel 1 (
    echo Falha ao instalar dependencias do requirements.txt.
    pause
    exit /b 1
)

python -m pip show pytest >nul 2>nul
if errorlevel 1 python -m pip install pytest
python -m pip show playwright >nul 2>nul
if errorlevel 1 python -m pip install playwright
python -m pip show pytest-playwright >nul 2>nul
if errorlevel 1 python -m pip install pytest-playwright
python -m pip show allure-pytest >nul 2>nul
if errorlevel 1 python -m pip install allure-pytest
python -m pip show pytest-html >nul 2>nul
if errorlevel 1 python -m pip install pytest-html

echo.
echo ==============================
echo Instalando Scoop automaticamente
echo ==============================
where scoop >nul 2>nul
if errorlevel 1 (
    where powershell >nul 2>nul
    if errorlevel 1 (
        echo PowerShell nao encontrado. Nao foi possivel instalar Scoop.
        pause
        exit /b 1
    )
    powershell -NoProfile -ExecutionPolicy Bypass -Command "Set-ExecutionPolicy -Scope CurrentUser RemoteSigned -Force; irm get.scoop.sh | iex"
    if errorlevel 1 (
        echo Falha ao instalar Scoop.
        pause
        exit /b 1
    )
)

echo.
echo ==============================
echo Instalando CLI do Allure
echo ==============================
where allure >nul 2>nul
if errorlevel 1 (
    where scoop >nul 2>nul
    if errorlevel 1 (
        echo Scoop nao encontrado para instalar a CLI do Allure.
        pause
        exit /b 1
    )
    scoop install allure
    if errorlevel 1 (
        echo Falha ao instalar a CLI do Allure.
        pause
        exit /b 1
    )
)

echo.
echo ==============================
echo Instalando navegadores do Playwright
echo ==============================
python -m playwright install chromium
if errorlevel 1 (
    echo Falha ao instalar browsers do Playwright.
    pause
    exit /b 1
)

echo.
echo ==============================
echo Executando testes com pytest
echo ==============================
rd /s /q "%ALLURE_RESULTS%" 2>nul
rd /s /q "%ALLURE_REPORT%" 2>nul
python -m pytest --alluredir=%ALLURE_RESULTS% --headed
set TEST_EXIT=%ERRORLEVEL%

echo.
echo ==============================
echo Gerando Allure Report
echo ==============================
where allure >nul 2>nul
if errorlevel 1 (
    echo Allure CLI nao encontrado. Verifique a instalacao do Scoop/Allure.
) else (
    allure generate %ALLURE_RESULTS% -o %ALLURE_REPORT% --clean
    if errorlevel 1 (
        echo Falha ao gerar o Allure Report.
    ) else (
        allure open %ALLURE_REPORT%
    )
)

if not "%TEST_EXIT%"=="0" (
    pause
    exit /b %TEST_EXIT%
)

echo.
echo ==============================
echo Processo concluido com sucesso
echo ==============================
pause
endlocal