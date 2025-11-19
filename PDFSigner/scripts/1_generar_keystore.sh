#!/bin/bash
# ==============================================================================
# Script para generar un certificado digital autofirmado con Java keytool
# Laboratorio de Seguridad de la Información
# ==============================================================================

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║     GENERADOR DE CERTIFICADO DIGITAL AUTOFIRMADO             ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# Verificar que Java esté instalado
if ! command -v java &> /dev/null; then
    echo "[ERROR] Java no está instalado o no está en el PATH"
    echo "Por favor instale Java JDK"
    exit 1
fi

echo "[INFO] Java detectado correctamente"
echo ""

# Configuración del certificado
ALIAS="mifirma"
KEYSTORE="mifirma.p12"
KEYALG="RSA"
KEYSIZE="2048"
VALIDITY="365"
STORETYPE="PKCS12"
SIGALG="SHA256withRSA"

echo "Configuración del certificado:"
echo "- Alias: $ALIAS"
echo "- Algoritmo de clave: $KEYALG"
echo "- Tamaño de clave: $KEYSIZE bits"
echo "- Validez: $VALIDITY días"
echo "- Tipo de almacén: $STORETYPE"
echo "- Algoritmo de firma: $SIGALG"
echo ""

echo "─────────────────────────────────────────────────────────────"
echo "A continuación se le solicitarán los datos del certificado:"
echo "─────────────────────────────────────────────────────────────"
echo ""
echo "Datos del sujeto del certificado:"
echo "  CN (Common Name): Su nombre completo o el nombre del titular"
echo "  OU (Organizational Unit): Departamento o unidad (ej: TI, Desarrollo)"
echo "  O (Organization): Nombre de la organización o universidad"
echo "  L (Locality): Ciudad"
echo "  ST (State): Departamento o región"
echo "  C (Country): Código de país de 2 letras (PE, MX, CO, etc.)"
echo ""
echo "─────────────────────────────────────────────────────────────"
echo ""

# Generar el certificado
keytool -genkeypair \
    -alias "$ALIAS" \
    -keyalg "$KEYALG" \
    -keysize "$KEYSIZE" \
    -validity "$VALIDITY" \
    -keystore "$KEYSTORE" \
    -storetype "$STORETYPE" \
    -sigalg "$SIGALG"

if [ $? -eq 0 ]; then
    echo ""
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║           CERTIFICADO GENERADO EXITOSAMENTE                  ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo ""
    echo "Archivo generado: $KEYSTORE"
    echo ""
    echo "Para ver los detalles del certificado ejecute:"
    echo "  keytool -list -v -keystore $KEYSTORE"
    echo ""
else
    echo ""
    echo "[ERROR] No se pudo generar el certificado"
    echo "Verifique los datos ingresados e intente nuevamente"
fi
