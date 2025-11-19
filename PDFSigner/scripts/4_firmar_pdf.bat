@echo off
REM ==============================================================================
REM Script para ejecutar el programa de firma de PDFs
REM ==============================================================================

echo ╔══════════════════════════════════════════════════════════════╗
echo ║          FIRMA DIGITAL DE DOCUMENTOS PDF                     ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

cd ..

if not exist "target\pdf-signer.jar" (
    echo [ERROR] No se encontró el JAR compilado
    echo Por favor compile primero el proyecto usando 3_compilar.bat
    pause
    exit /b 1
)

echo [INFO] Ejecutando aplicación de firma digital...
echo.

java -jar target\pdf-signer.jar

echo.
pause
