@echo off
SETLOCAL EnableDelayedExpansion
TITLE Casino Bot - Windows Starter

echo ====================================================
echo           CASINO BOT - AUTOMATED STARTER
echo ====================================================
echo.

:: 1. Verificar se o Python está instalado
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERRO] Python nao encontrado! 
    echo Por favor, instale o Python 3.11+ e marque "Add Python to PATH".
    echo Baixe em: https://www.python.org/downloads/
    pause
    exit /b
)

:: 2. Verificar se o arquivo .env existe
if not exist .env (
    if exist .env.example (
        echo [AVISO] Arquivo .env nao encontrado. Criando a partir do .env.example...
        copy .env.example .env
        echo [!] Por favor, edite o arquivo .env e coloque seu TELEGRAM_TOKEN antes de continuar.
        notepad .env
        echo.
        echo [?] Apos configurar o .env, pressione qualquer tecla para continuar o setup.
        pause >nul
    ) else (
        echo [ERRO] Arquivo .env ou .env.example nao encontrados!
        pause
        exit /b
    )
)

:: 3. Criar ambiente virtual se nao existir
if not exist venv (
    echo [1/3] Criando ambiente virtual (venv)...
    python -m venv venv
    if %errorlevel% neq 0 (
        echo [ERRO] Falha ao criar ambiente virtual.
        pause
        exit /b
    )
)

:: 4. Instalar/Atualizar dependencias
echo [2/3] Ativando ambiente e instalando dependencias...
call venv\Scripts\activate
python -m pip install --upgrade pip >nul
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [ERRO] Falha ao instalar dependencias. Verifique sua conexao.
    pause
    exit /b
)

:: 5. Validar se o Token foi preenchido
findstr /C:"seu_token_aqui" .env >nul
if %errorlevel% equ 0 (
    echo [ERRO] Voce ainda nao configurou seu TELEGRAM_TOKEN no arquivo .env!
    echo Abrindo o arquivo para voce...
    notepad .env
    pause
    exit /b
)

:: 6. Iniciar o Bot
echo [3/3] Tudo pronto! Iniciando o Bot...
echo.
echo ----------------------------------------------------
echo DICA: Para fechar o bot, pressione CTRL+C
echo ----------------------------------------------------
echo.
python main.py

if %errorlevel% neq 0 (
    echo.
    echo [ERRO] O Bot parou inesperadamente. Verifique as mensagens acima.
    pause
)

ENDLOCAL
