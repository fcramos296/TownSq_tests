@echo off
setlocal enabledelayedexpansion
cd /d "%~dp0"

set "VENV_DIR=.venv"
set "VENV_PYTHON=%VENV_DIR%\Scripts\python.exe"
set "VENV_ACTIVATE_BAT=%VENV_DIR%\Scripts\activate.bat"
set "VENV_ACTIVATE_PS1=%VENV_DIR%\Scripts\Activate.ps1"
set "ALLURE_RESULTS=allure-results"
set "ALLURE_REPORT=allure-report"

if not exist ".env" (
    if exist ".env.example" (
        copy /Y ".env.example" ".env" >nul
        echo .env created from .env.example.
    ) else (
        echo ERRO: .env.example not found.
        pause
        exit /b 1
    )
)

echo.
echo Informe credenciais VALIDAS para execucao dos testes.
echo Elas serao gravadas no arquivo .env local.
echo.

set /p TEST_USERNAME=USERNAME de teste: 
if "%TEST_USERNAME%"=="" (
    echo ERRO: USERNAME nao pode ficar vazio.
    pause
    exit /b 1
)

for /f "usebackq delims=" %%i in (`powershell -NoProfile -Command "$p = Read-Host 'PASSWORD de teste' -AsSecureString; $b=[Runtime.InteropServices.Marshal]::SecureStringToBSTR($p); try { [Runtime.InteropServices.Marshal]::PtrToStringAuto($b) } finally { [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($b) }"`) do set "TEST_PASSWORD=%%i"
if "%TEST_PASSWORD%"=="" (
    echo ERRO: PASSWORD nao pode ficar vazia.
    pause
    exit /b 1
)

powershell -NoProfile -ExecutionPolicy Bypass -Command ^
    "$envPath = '.env';" ^
    "$lines = Get-Content $envPath -ErrorAction SilentlyContinue;" ^
    "if (-not $lines) { $lines = @() }" ^
    "$map = [ordered]@{};" ^
    "foreach ($line in $lines) { if ($line -match '^[A-Za-z_][A-Za-z0-9_]*=') { $k,$v = $line -split '=',2; $map[$k]=$v } else { $map[$line]=$null } }" ^
    "$map['USERNAME'] = '%TEST_USERNAME%';" ^
    "$map['PASSWORD'] = '%TEST_PASSWORD%';" ^
    "$out = New-Object System.Collections.Generic.List[string];" ^
    "foreach ($entry in $map.GetEnumerator()) { if ($entry.Value -eq $null) { if ($entry.Key -ne '') { $out.Add($entry.Key) } } else { $out.Add(('{0}={1}' -f $entry.Key, $entry.Value)) } }" ^
    "Set-Content -Path $envPath -Value $out -Encoding UTF8"
if errorlevel 1 (
    echo ERRO: falha ao atualizar o arquivo .env com as credenciais.
    pause
    exit /b 1
)

if not exist "%VENV_PYTHON%" (
    echo Creating virtual environment...
    python -m venv %VENV_DIR%
)

if not exist "%VENV_PYTHON%" (
    echo ERRO: could not create virtual environment.
    pause
    exit /b 1
)

echo Activating virtual environment...
set "TERM_TYPE=cmd"
if defined PSModulePath set "TERM_TYPE=powershell"

if /i "!TERM_TYPE!"=="powershell" (
    powershell -NoProfile -ExecutionPolicy Bypass -Command "& '%VENV_ACTIVATE_PS1%'; python -V"
    if errorlevel 1 (
        echo ERRO: failed to activate .venv in PowerShell.
        pause
        exit /b 1
    )
) else (
    call "%VENV_ACTIVATE_BAT%"
    if errorlevel 1 (
        echo ERRO: failed to activate .venv in Command Prompt.
        pause
        exit /b 1
    )
)

echo Installing dependencies...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
if errorlevel 1 (
    echo ERRO: failed to install dependencies.
    pause
    exit /b 1
)

echo Installing Chromium from Playwright...
python -m playwright install chromium
if errorlevel 1 (
    echo ERRO: failed to install Playwright Chromium.
    pause
    exit /b 1
)

where allure >nul 2>nul
if errorlevel 1 (
    where scoop >nul 2>nul
    if errorlevel 1 (
        echo Scoop not found. Installing Scoop...
        powershell -NoProfile -ExecutionPolicy Bypass -Command "Set-ExecutionPolicy -Scope CurrentUser RemoteSigned -Force; irm get.scoop.sh | iex"
        if errorlevel 1 (
            echo ERRO: failed to install Scoop.
            pause
            exit /b 1
        )
    )
    echo Installing Allure CLI...
    scoop install allure
    if errorlevel 1 (
        echo ERRO: failed to install Allure CLI.
        pause
        exit /b 1
    )
)

echo Running tests...
rd /s /q "%ALLURE_RESULTS%" 2>nul
rd /s /q "%ALLURE_REPORT%" 2>nul
python -m pytest --alluredir=%ALLURE_RESULTS% --headed
set TEST_EXIT=%ERRORLEVEL%

where allure >nul 2>nul
if errorlevel 1 (
    echo Allure CLI not found. Skipping report generation.
) else (
    allure generate %ALLURE_RESULTS% -o %ALLURE_REPORT% --clean
    if errorlevel 1 (
        echo ERRO: failed to generate Allure report.
    ) else (
        start "" allure open %ALLURE_REPORT%
    )
)

if not "%TEST_EXIT%"=="0" (
    pause
    exit /b %TEST_EXIT%
)

pause
endlocal