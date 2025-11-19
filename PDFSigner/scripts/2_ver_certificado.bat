@echo off
REM ==============================================================================
REM Script para ver los detalles del certificado en el keystore
REM ==============================================================================

echo ╔══════════════════════════════════════════════════════════════╗
echo ║          VISUALIZADOR DE CERTIFICADO DIGITAL                 ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

set KEYSTORE=mifirma.p12

if not exist "%KEYSTORE%" (
    echo [ERROR] No se encontró el archivo %KEYSTORE%
    echo Por favor genere primero el certificado usando 1_generar_keystore.bat
    pause
    exit /b 1
)

echo [INFO] Mostrando detalles del certificado en %KEYSTORE%
echo.
echo ═════════════════════════════════════════════════════════════════
echo.

keytool -list -v -keystore %KEYSTORE%

echo.
echo ═════════════════════════════════════════════════════════════════
echo.
pause
