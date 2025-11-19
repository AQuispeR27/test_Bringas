@echo off
REM ==============================================================================
REM Script para generar un certificado digital autofirmado con Java keytool
REM Laboratorio de Seguridad de la Información
REM ==============================================================================

echo ╔══════════════════════════════════════════════════════════════╗
echo ║     GENERADOR DE CERTIFICADO DIGITAL AUTOFIRMADO             ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

REM Verificar que Java esté instalado
java -version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Java no está instalado o no está en el PATH
    echo Por favor instale Java JDK y agregue la carpeta bin al PATH
    pause
    exit /b 1
)

echo [INFO] Java detectado correctamente
echo.

REM Configuración del certificado
set ALIAS=mifirma
set KEYSTORE=mifirma.p12
set KEYALG=RSA
set KEYSIZE=2048
set VALIDITY=365
set STORETYPE=PKCS12
set SIGALG=SHA256withRSA

echo Configuración del certificado:
echo - Alias: %ALIAS%
echo - Algoritmo de clave: %KEYALG%
echo - Tamaño de clave: %KEYSIZE% bits
echo - Validez: %VALIDITY% días
echo - Tipo de almacén: %STORETYPE%
echo - Algoritmo de firma: %SIGALG%
echo.

echo ─────────────────────────────────────────────────────────────
echo A continuación se le solicitarán los datos del certificado:
echo ─────────────────────────────────────────────────────────────
echo.
echo Datos del sujeto del certificado:
echo   CN (Common Name): Su nombre completo o el nombre del titular
echo   OU (Organizational Unit): Departamento o unidad (ej: TI, Desarrollo)
echo   O (Organization): Nombre de la organización o universidad
echo   L (Locality): Ciudad
echo   ST (State): Departamento o región
echo   C (Country): Código de país de 2 letras (PE, MX, CO, etc.)
echo.
echo ─────────────────────────────────────────────────────────────
echo.

REM Generar el certificado
keytool -genkeypair ^
    -alias %ALIAS% ^
    -keyalg %KEYALG% ^
    -keysize %KEYSIZE% ^
    -validity %VALIDITY% ^
    -keystore %KEYSTORE% ^
    -storetype %STORETYPE% ^
    -sigalg %SIGALG%

if %errorlevel% equ 0 (
    echo.
    echo ╔══════════════════════════════════════════════════════════════╗
    echo ║           CERTIFICADO GENERADO EXITOSAMENTE                  ║
    echo ╚══════════════════════════════════════════════════════════════╝
    echo.
    echo Archivo generado: %KEYSTORE%
    echo.
    echo Para ver los detalles del certificado ejecute:
    echo   keytool -list -v -keystore %KEYSTORE%
    echo.
) else (
    echo.
    echo [ERROR] No se pudo generar el certificado
    echo Verifique los datos ingresados e intente nuevamente
)

echo.
pause
