@echo off
chcp 65001 > nul
title Instalador do Mod Pokemon No-Trade para Nintendo 3DS
cls
echo ====================================================================
echo    INSTALADOR DO MOD POKEMON NO-TRADE EVOLUTIONS PARA NINTENDO 3DS
echo ====================================================================
echo.
echo Este script vai copiar os arquivos do Mod diretamente para o seu
echo Cartao SD do 3DS na estrutura correta do Luma3DS.
echo.

setlocal enabledelayedexpansion

:: Lista unidades disponiveis
echo Unidades de disco encontradas no seu computador:
powershell -NoProfile -Command "Get-Volume | Where-Object { $_.DriveLetter -ne $null } | Select-Object DriveLetter, FileSystemLabel, DriveType, SizeRemaining | Format-Table -AutoSize"
echo.

set /p SD_LETTER="Digite a LETRA da unidade do seu Cartao SD (Exemplo: E, F, G): "

:: Remove dois pontos ou espacos se o usuario digitou "E:" ou "e"
set SD_LETTER=%SD_LETTER:~0,1%
set TARGET_DIR=%SD_LETTER%:\luma\titles

if not exist "%SD_LETTER%:\" (
    echo.
    echo [ERRO] A unidade %SD_LETTER%:\ nao foi encontrada!
    echo Certifique-se de conectar o cartao SD e digite a letra correta.
    echo.
    pause
    exit /b 1
)

echo.
echo [1/2] Copiando arquivos do mod para %SD_LETTER%:\luma\ ...

:: Origem dos arquivos do Luma
set SOURCE_DIR=%~dp0Mod-Package\3DS_Luma3DS\luma

if not exist "%SOURCE_DIR%" (
    echo [ERRO] Pasta de origem %SOURCE_DIR% nao encontrada!
    pause
    exit /b 1
)

xcopy "%SOURCE_DIR%" "%SD_LETTER%:\luma" /E /I /H /Y > nul

if %ERRORLEVEL% equ 0 (
    echo [OK] Arquivos copiados com sucesso para o Cartao SD!
) else (
    echo [ERRO] Ocorreu uma falha ao copiar os arquivos.
    pause
    exit /b 1
)

echo.
echo ====================================================================
echo                   [2/2] ATIVACAO NO NINTENDO 3DS
echo ====================================================================
echo 1. Ejete o Cartao SD com seguranca do PC e insira-o no seu 3DS.
echo 2. Segure o botao [SELECT] e ligue o console no botao [POWER].
echo 3. No menu do Luma3DS, certifique-se de marcar com (x) a opcao:
echo.
echo       (x) Enable game patching
echo.
echo 4. Pressione [START] para salvar e iniciar o console.
echo 5. Abra o seu jogo de Pokemon e divirta-se!
echo ====================================================================
echo.
pause
