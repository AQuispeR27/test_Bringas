# Firma Digital de Documentos PDF con Certificados X.509

![Java](https://img.shields.io/badge/Java-11+-orange.svg)
![Maven](https://img.shields.io/badge/Maven-3.6+-blue.svg)
![License](https://img.shields.io/badge/License-Educational-green.svg)

Proyecto académico para el laboratorio de **Seguridad de la Información** que implementa la firma digital de documentos PDF utilizando certificados digitales autofirmados generados con Java keytool.

## 📋 Descripción

Este proyecto demuestra el uso de **criptografía de clave pública (PKI)** para garantizar:
- ✅ **Autenticidad**: Verificación de la identidad del firmante
- ✅ **Integridad**: Garantía de que el documento no ha sido modificado
- ✅ **No repudio**: El firmante no puede negar haber firmado el documento

## 🎯 Objetivos del Laboratorio

### Objetivo General
Implementar el proceso completo de firma digital de un documento PDF utilizando un certificado digital autofirmado generado con Java keytool, para comprender los conceptos fundamentales de PKI.

### Objetivos Específicos
1. Generar un par de claves RSA y un certificado X.509 autofirmado con keytool
2. Gestionar un keystore en formato PKCS#12
3. Aplicar firmas digitales visibles a documentos PDF usando Java
4. Analizar el resultado y discutir las implicaciones de seguridad

## 🛠️ Requisitos del Sistema

### Software Necesario

- **Java JDK**: 11 o superior
  ```bash
  java -version
  # Debe mostrar: java version "11" o superior
  ```

- **Apache Maven**: 3.6 o superior
  ```bash
  mvn -version
  # Debe mostrar: Apache Maven 3.6.x o superior
  ```

- **Lector de PDF**: Adobe Acrobat Reader DC (recomendado) o alternativas como Foxit Reader

### Bibliotecas Utilizadas

- **iText 8.0.2**: Manipulación y firma de PDFs
- **BouncyCastle 1.70**: Proveedor criptográfico
- **SLF4J**: Logging

(Todas las dependencias se descargan automáticamente con Maven)

## 📂 Estructura del Proyecto

```
PDFSigner/
├── src/
│   └── main/
│       └── java/
│           └── com/
│               └── seguridad/
│                   └── pdfsigner/
│                       └── PDFSigner.java    # Clase principal
├── scripts/
│   ├── 1_generar_keystore.bat              # Script Windows para generar certificado
│   ├── 1_generar_keystore.sh               # Script Linux/Mac para generar certificado
│   ├── 2_ver_certificado.bat               # Ver detalles del certificado
│   ├── 3_compilar.bat                      # Compilar con Maven
│   └── 4_firmar_pdf.bat                    # Ejecutar aplicación de firma
├── docs/
│   └── INFORME_TECNICO_LABORATORIO.md      # Informe técnico completo
├── pom.xml                                  # Configuración Maven
└── README.md                                # Este archivo
```

## 🚀 Guía de Uso Paso a Paso

### Paso 1: Clonar el Repositorio

```bash
git clone <URL_DEL_REPOSITORIO>
cd PDFSigner
```

### Paso 2: Generar el Certificado Digital Autofirmado

#### En Windows:

```bash
cd scripts
1_generar_keystore.bat
```

#### En Linux/Mac:

```bash
cd scripts
chmod +x 1_generar_keystore.sh
./1_generar_keystore.sh
```

#### Manualmente con keytool:

```bash
keytool -genkeypair \
  -alias mifirma \
  -keyalg RSA \
  -keysize 2048 \
  -validity 365 \
  -keystore mifirma.p12 \
  -storetype PKCS12 \
  -sigalg SHA256withRSA
```

**Datos a ingresar:**

- **Contraseña del keystore**: Mínimo 6 caracteres (¡recuérdala!)
- **CN (Common Name)**: Tu nombre completo
- **OU (Organizational Unit)**: Ej. "Facultad de Ingeniería"
- **O (Organization)**: Ej. "Universidad Nacional"
- **L (Locality)**: Tu ciudad
- **ST (State)**: Tu región/departamento
- **C (Country)**: Código de 2 letras (PE, MX, CO, etc.)

### Paso 3: Verificar el Certificado (Opcional)

```bash
keytool -list -v -keystore mifirma.p12
```

Esto mostrará todos los detalles del certificado generado.

### Paso 4: Compilar el Proyecto

#### Desde la raíz del proyecto:

```bash
mvn clean package
```

Esto generará el archivo `target/pdf-signer.jar`

#### Usando el script (Windows):

```bash
cd scripts
3_compilar.bat
```

### Paso 5: Preparar el PDF a Firmar

Coloca el archivo PDF que deseas firmar en la carpeta raíz del proyecto (ej. `documento.pdf`)

### Paso 6: Firmar el PDF

#### Ejecutar la aplicación:

```bash
java -jar target/pdf-signer.jar
```

#### Usando el script (Windows):

```bash
cd scripts
4_firmar_pdf.bat
```

#### Datos a ingresar:

1. **Ruta del PDF a firmar**: `documento.pdf`
2. **Ruta del PDF de salida**: (dejar en blanco para `documento_signed.pdf`)
3. **Ruta del keystore**: `mifirma.p12`
4. **Contraseña del keystore**: La que configuraste en el Paso 2
5. **Alias**: (dejar en blanco para usar "mifirma")
6. **Razón de la firma**: Ej. "Aprobación del documento"
7. **Ubicación**: Ej. "Lima, Perú"

### Paso 7: Verificar la Firma

1. Abre el PDF firmado en **Adobe Acrobat Reader**
2. Verás un panel azul superior indicando que el documento está firmado
3. Haz clic en el panel de firmas para ver los detalles:
   - Nombre del firmante
   - Fecha y hora de firma
   - Razón y ubicación
   - Estado de validación

**Nota**: Verás una advertencia sobre "certificado no confiable" porque es autofirmado. Esto es normal y esperado en entornos de laboratorio.

## 📖 Conceptos Técnicos Clave

### Certificado X.509
Credencial digital que vincula una identidad con una clave pública. Contiene:
- Información del titular (Subject DN)
- Clave pública
- Periodo de validez
- Firma digital del emisor

### Keystore PKCS#12
Archivo protegido por contraseña que almacena:
- Clave privada (secreta, nunca compartir)
- Certificado X.509 (público)
- Cadena de certificados

### Firma Digital
Proceso que:
1. Calcula el hash SHA-256 del documento
2. Cifra el hash con la clave privada RSA
3. Incrusta el hash cifrado + certificado en el PDF
4. Cualquiera puede verificar con la clave pública

### Algoritmos Utilizados
- **RSA-2048**: Criptografía asimétrica (par de claves)
- **SHA-256**: Función hash criptográfica
- **SHA256withRSA**: Combinación para firma digital

## ⚠️ Certificado Autofirmado vs. CA

### Certificado Autofirmado (este laboratorio)

**Ventajas:**
- ✅ Gratuito e inmediato
- ✅ Ideal para desarrollo y educación
- ✅ Mismas capacidades criptográficas

**Limitaciones:**
- ❌ No confiable por defecto
- ❌ Sin verificación de identidad por terceros
- ❌ No apto para producción pública

### Certificado de CA Reconocida

**Ventajas:**
- ✅ Confianza automática en sistemas
- ✅ Verificación de identidad por CA
- ✅ Aceptación legal y comercial

**Limitaciones:**
- ❌ Costo económico
- ❌ Proceso de validación extenso

## 🔒 Buenas Prácticas de Seguridad

1. **Proteger la clave privada**:
   - Usar contraseñas robustas (12+ caracteres)
   - Nunca compartir el archivo `.p12`
   - Hacer backup cifrado

2. **Usar algoritmos robustos**:
   - RSA mínimo 2048 bits
   - SHA-256 o superior
   - Evitar MD5, SHA-1 (obsoletos)

3. **Gestión de certificados**:
   - Renovar antes de expirar
   - Revocar si se compromete la clave
   - Documentar el inventario de certificados

4. **Para producción**:
   - Usar certificados de CA reconocida
   - Implementar sellado de tiempo (timestamp)
   - Cumplir normativas locales (firma electrónica avanzada)

## 🧪 Casos de Uso

### Entornos Apropiados para Certificados Autofirmados:
- ✅ Laboratorios educativos
- ✅ Desarrollo y pruebas
- ✅ Sistemas internos cerrados
- ✅ Aprendizaje de conceptos PKI

### Cuándo Usar Certificados de CA:
- ⚡ Sitios web públicos (HTTPS)
- ⚡ Documentos con valor legal
- ⚡ Aplicaciones empresariales
- ⚡ Comunicación con clientes externos

## 📚 Documentación Adicional

- **[Informe Técnico Completo](docs/INFORME_TECNICO_LABORATORIO.md)**: Documento académico detallado con marco teórico, procedimiento, análisis y conclusiones

- **Java keytool Docs**: https://docs.oracle.com/en/java/javase/11/tools/keytool.html

- **iText Documentation**: https://api.itextpdf.com/

- **BouncyCastle**: https://www.bouncycastle.org/

## ❓ Troubleshooting

### Error: "Java no reconocido"
```bash
# Verificar instalación de Java
java -version

# Agregar Java al PATH del sistema si es necesario
```

### Error: "Maven no reconocido"
```bash
# Descargar Maven de: https://maven.apache.org/download.cgi
# Agregar Maven al PATH del sistema
```

### Error: "No se puede leer el archivo keystore"
- Verificar que el archivo `mifirma.p12` existe en la ubicación correcta
- Verificar que la contraseña es correcta

### Error de compilación con Maven
```bash
# Limpiar y recompilar
mvn clean
mvn package
```

### La firma no se muestra en el PDF
- Verificar que el PDF no esté protegido o cifrado
- Usar Adobe Reader actualizado
- Revisar logs de la aplicación

## 📝 Notas Importantes

1. **Periodo de validez**: El certificado generado es válido por 365 días. Después de expirar, no podrá usarse para nuevas firmas (pero las firmas existentes siguen siendo válidas).

2. **Sellado de tiempo**: Este laboratorio NO implementa timestamp. Para firmas de largo plazo, considerar usar servicios TSA (Time Stamping Authority).

3. **Valor legal**: Los certificados autofirmados NO tienen valor legal en la mayoría de jurisdicciones. Para documentos legales, usar certificados de CA acreditadas.

4. **Seguridad**: Este código es para fines educativos. Para producción, implementar validaciones adicionales, manejo de errores robusto y auditoría.

## 👥 Contribuciones

Este es un proyecto educativo. Las sugerencias y mejoras son bienvenidas mediante pull requests.

## 📄 Licencia

Proyecto educativo para uso académico - Laboratorio de Seguridad de la Información

---

## 📞 Contacto

Para preguntas sobre el laboratorio, consultar con el docente del curso de Seguridad de la Información.

---

**Desarrollado para fines educativos** | Asignatura: Seguridad de la Información
