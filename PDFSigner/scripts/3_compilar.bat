@echo off
REM ==============================================================================
REM Script para compilar el proyecto con Maven
REM ==============================================================================

echo ╔══════════════════════════════════════════════════════════════╗
echo ║            COMPILADOR DEL PROYECTO PDF SIGNER                ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

REM Verificar que Maven esté instalado
mvn --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Maven no está instalado o no está en el PATH
    echo Por favor instale Apache Maven
    pause
    exit /b 1
)

echo [INFO] Compilando proyecto con Maven...
echo.

cd ..
mvn clean package

if %errorlevel% equ 0 (
    echo.
    echo ╔══════════════════════════════════════════════════════════════╗
    echo ║           COMPILACIÓN EXITOSA                                ║
    echo ╚══════════════════════════════════════════════════════════════╝
    echo.
    echo JAR generado: target\pdf-signer.jar
    echo.
    echo Para ejecutar: java -jar target\pdf-signer.jar
    echo.
) else (
    echo.
    echo [ERROR] La compilación falló
)

pause
