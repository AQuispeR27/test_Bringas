# INFORME TÉCNICO DE LABORATORIO

**Tema:** Firma digital de un documento PDF utilizando un Certificado Digital autofirmado generado con Java keytool

**Asignatura:** Seguridad de la Información / Seguridad en Aplicaciones

---

## 1. Introducción

En el contexto actual de la transformación digital, la seguridad de la información se ha convertido en un pilar fundamental para garantizar la confiabilidad de los procesos electrónicos. La autenticación, integridad y no repudio son propiedades esenciales que deben asegurarse en el intercambio de documentos digitales, especialmente en entornos donde se manejan datos sensibles o documentos con valor legal.

Las firmas digitales constituyen un mecanismo criptográfico que permite verificar la autenticidad del origen de un documento electrónico, garantizar que su contenido no ha sido alterado desde el momento de la firma, y proporcionar evidencia irrefutable de que el firmante efectivamente realizó dicha acción. A diferencia de una simple imagen escaneada de una firma manuscrita, que puede ser fácilmente copiada y replicada sin control, una firma digital se basa en criptografía de clave pública y funciones hash criptográficas, lo que la hace técnicamente imposible de falsificar sin poseer la clave privada del firmante.

Los certificados digitales, por su parte, funcionan como credenciales electrónicas que vinculan una identidad (persona, organización o dispositivo) con un par de claves criptográficas. En el ámbito académico, empresarial y gubernamental, las firmas digitales aplicadas a documentos PDF son ampliamente utilizadas para firmar contratos, boletas de pago, actas académicas, reportes técnicos, trámites administrativos y documentos legales, proporcionando trazabilidad y cumplimiento normativo.

El presente laboratorio explora el proceso técnico de generación de un certificado digital autofirmado mediante la herramienta Java keytool, así como su aplicación práctica en la firma digital de documentos PDF, con el objetivo de comprender los fundamentos criptográficos y de infraestructura de clave pública (PKI) que sustentan estos mecanismos de seguridad.

---

## 2. Marco Teórico

### 2.1. Criptografía de clave pública (asimétrica)

La criptografía de clave pública, también conocida como criptografía asimétrica, es un esquema criptográfico que utiliza un par de claves matemáticamente relacionadas: una clave pública y una clave privada. La clave pública puede distribuirse libremente y se utiliza para cifrar mensajes o verificar firmas digitales, mientras que la clave privada debe mantenerse en secreto absoluto y se emplea para descifrar mensajes cifrados con la clave pública correspondiente o para generar firmas digitales.

Este sistema se basa en problemas matemáticos de difícil resolución computacional, como la factorización de números primos grandes (algoritmo RSA) o el problema del logaritmo discreto en curvas elípticas (ECDSA). La propiedad fundamental es que, conociendo la clave pública, resulta computacionalmente inviable derivar la clave privada en un tiempo razonable.

En el contexto de las firmas digitales, la relación funciona de manera inversa al cifrado: el firmante utiliza su clave privada para "firmar" (cifrar) un resumen del documento, y cualquier persona que posea la clave pública puede verificar que efectivamente ese resumen fue generado por el poseedor de la clave privada correspondiente.

### 2.2. Resumen criptográfico (hash) y su rol en la firma digital

Un resumen criptográfico o hash es el resultado de aplicar una función hash criptográfica a un conjunto de datos de longitud arbitraria, produciendo una cadena de bits de tamaño fijo. Las funciones hash criptográficas, como SHA-256, SHA-384 o SHA-512, poseen propiedades específicas:

- **Determinismo:** El mismo mensaje siempre produce el mismo hash.
- **Eficiencia:** El cálculo del hash es rápido.
- **Resistencia a preimagen:** Es computacionalmente inviable encontrar un mensaje que produzca un hash dado.
- **Resistencia a segunda preimagen:** Dado un mensaje, es inviable encontrar otro mensaje diferente con el mismo hash.
- **Resistencia a colisiones:** Es inviable encontrar dos mensajes diferentes que produzcan el mismo hash.

En el proceso de firma digital, en lugar de cifrar todo el documento con la clave privada (operación costosa computacionalmente), se calcula primero el hash del documento y luego se cifra únicamente ese hash con la clave privada del firmante. Esto genera la firma digital. Para verificar la firma, el destinatario calcula el hash del documento recibido y lo compara con el hash descifrado usando la clave pública del firmante. Si coinciden, se confirma tanto la autenticidad como la integridad del documento.

### 2.3. Firma digital: garantías y diferencias con firma manuscrita escaneada

Una firma digital es un esquema criptográfico que proporciona tres garantías fundamentales:

1. **Autenticidad:** Permite verificar la identidad del firmante mediante el uso de su certificado digital.
2. **Integridad:** Garantiza que el contenido del documento no ha sido modificado después de la firma, ya que cualquier alteración cambiaría el hash del documento.
3. **No repudio:** El firmante no puede negar haber firmado el documento, pues solo él posee la clave privada necesaria para generar esa firma específica.

A diferencia de una imagen escaneada de una firma manuscrita, que es simplemente un elemento gráfico insertado en el documento sin ninguna protección criptográfica, una firma digital está matemáticamente vinculada tanto al contenido del documento como a la identidad del firmante. Una firma escaneada puede ser copiada y pegada en cualquier documento por cualquier persona, mientras que una firma digital solo puede ser generada por quien posee la clave privada asociada al certificado.

### 2.4. Infraestructura de Clave Pública (PKI) y Autoridad Certificadora (CA)

La Infraestructura de Clave Pública (PKI, por sus siglas en inglés) es un conjunto de roles, políticas, hardware, software y procedimientos necesarios para crear, gestionar, distribuir, usar, almacenar y revocar certificados digitales. Los componentes principales de una PKI incluyen:

- **Autoridad Certificadora (CA):** Entidad confiable que emite, revoca y gestiona certificados digitales. La CA verifica la identidad de los solicitantes antes de emitir un certificado.
- **Autoridad de Registro (RA):** Verifica la identidad de los usuarios que solicitan certificados.
- **Repositorio de certificados:** Base de datos pública donde se almacenan los certificados emitidos.
- **Lista de Revocación de Certificados (CRL):** Lista de certificados que han sido revocados antes de su fecha de expiración.

Las CA públicas reconocidas (como DigiCert, GlobalSign, Sectigo) son confiadas por defecto en navegadores y sistemas operativos. Cuando un certificado es emitido por una CA reconocida, los sistemas confían automáticamente en él porque confían en la CA raíz que lo emitió.

### 2.5. Certificados digitales X.509: campos principales

El estándar X.509 define el formato de los certificados de clave pública utilizados en PKI. Un certificado X.509 contiene información estructurada en campos específicos:

- **Versión:** Versión del estándar X.509 (generalmente v3).
- **Número de serie:** Identificador único asignado por la CA emisora.
- **Algoritmo de firma:** Algoritmo criptográfico utilizado para firmar el certificado (ej. SHA256withRSA).
- **Emisor (Issuer):** Nombre distinguido (DN) de la entidad que emitió el certificado.
- **Sujeto (Subject):** Nombre distinguido del titular del certificado, compuesto por campos como:
  - **CN (Common Name):** Nombre común del titular.
  - **OU (Organizational Unit):** Unidad organizacional.
  - **O (Organization):** Organización.
  - **L (Locality):** Localidad o ciudad.
  - **ST (State):** Estado o provincia.
  - **C (Country):** Código de país (2 letras).
- **Validez:** Periodo durante el cual el certificado es válido (fecha de inicio y fecha de expiración).
- **Clave pública:** La clave pública del titular del certificado.
- **Extensiones:** Información adicional como uso de la clave, restricciones, identificadores, etc.
- **Firma digital:** Firma del emisor sobre todos los campos anteriores.

### 2.6. Certificado autofirmado: concepto, ventajas y limitaciones

Un certificado autofirmado es un certificado digital en el cual el emisor y el sujeto son la misma entidad. Es decir, el certificado no es emitido por una Autoridad Certificadora externa reconocida, sino que es firmado por la propia clave privada del titular.

**Ventajas:**
- Gratuito y rápido de generar.
- Útil para entornos de desarrollo, pruebas y laboratorios académicos.
- Proporciona las mismas capacidades criptográficas que un certificado emitido por una CA.
- Adecuado para sistemas internos donde todos los usuarios pueden importar manualmente el certificado como confiable.

**Limitaciones:**
- No está anclado a una cadena de confianza reconocida públicamente.
- Los navegadores y aplicaciones muestran advertencias de seguridad al encontrar certificados autofirmados.
- No proporciona verificación de identidad por parte de un tercero confiable.
- Vulnerable a ataques de tipo "man-in-the-middle" si no se valida manualmente la autenticidad del certificado.
- No es adecuado para entornos de producción que requieren confianza pública.

A pesar de estas limitaciones, los certificados autofirmados son valiosos para fines educativos y para comprender el funcionamiento técnico de PKI sin depender de servicios externos de pago.

### 2.7. Keystore y formato PKCS#12

Un keystore es un repositorio seguro que almacena claves criptográficas y certificados digitales. Java proporciona diferentes formatos de keystore, siendo PKCS#12 uno de los más utilizados y estándar en la industria.

**PKCS#12** (Public Key Cryptography Standard #12) es un formato de archivo binario protegido por contraseña que puede almacenar:
- Claves privadas
- Certificados X.509 asociados
- Cadenas de certificados completas
- Otros datos criptográficos

La extensión de archivo típica es `.p12` o `.pfx`. El keystore PKCS#12 utiliza cifrado simétrico (basado en contraseña) para proteger las claves privadas almacenadas, asegurando que solo quien conozca la contraseña pueda acceder a ellas.

En Java, la herramienta `keytool` permite crear y gestionar keystores, generando pares de claves, certificados autofirmados, importando certificados de CA, y exportando claves públicas.

### 2.8. Algoritmos criptográficos: RSA y SHA-256

**RSA (Rivest-Shamir-Adleman)** es uno de los algoritmos de criptografía asimétrica más ampliamente utilizados. Su seguridad se basa en la dificultad computacional de factorizar números primos muy grandes. Para firma digital, se recomienda utilizar claves RSA de al menos 2048 bits, aunque 3072 o 4096 bits ofrecen mayor seguridad a largo plazo.

**SHA-256** (Secure Hash Algorithm 256-bit) pertenece a la familia SHA-2 y produce un hash de 256 bits. Es considerado seguro contra ataques de colisión conocidos y es ampliamente aceptado en estándares de seguridad modernos. SHA-1, su predecesor, ya no se considera seguro y ha sido deprecado en la mayoría de aplicaciones.

La combinación **SHA256withRSA** significa que se utiliza SHA-256 para calcular el hash del documento y RSA para cifrar ese hash con la clave privada, generando así la firma digital. Esta combinación es apropiada para firmas digitales porque proporciona un equilibrio entre seguridad robusta y rendimiento aceptable.

### 2.9. Periodo de validez del certificado

Todo certificado digital posee un periodo de validez definido por dos fechas: "Valid From" (válido desde) y "Valid To" (válido hasta). Este periodo limita el tiempo durante el cual el certificado se considera confiable para operaciones criptográficas.

**Significado:**
- Un certificado solo debe utilizarse para firmar documentos mientras se encuentre dentro de su periodo de validez.
- La limitación temporal reduce el riesgo de compromiso de claves a largo plazo.
- Obliga a renovar periódicamente los certificados, permitiendo actualizar algoritmos y tamaños de clave según evolucionen las amenazas.

**Qué ocurre cuando expira:**
- El certificado ya no puede utilizarse para firmar nuevos documentos.
- Las aplicaciones mostrarán advertencias indicando que el certificado ha expirado.
- Sin embargo, esto no invalida las firmas realizadas cuando el certificado estaba vigente.

**Impacto en firmas ya realizadas:**
- Idealmente, las firmas digitales incluyen un sello de tiempo (timestamp) de una Autoridad de Sellado de Tiempo (TSA).
- El timestamp certifica el momento exacto en que se realizó la firma.
- Si existe timestamp y demuestra que la firma se realizó cuando el certificado estaba vigente, la firma sigue siendo válida incluso después de que el certificado expire.
- Sin timestamp, los validadores pueden mostrar advertencias, aunque técnicamente la firma sigue siendo verificable criptográficamente.

En entornos de producción críticos, es fundamental implementar sellado de tiempo para asegurar la validez a largo plazo de las firmas digitales.

---

## 3. Objetivos del Laboratorio

### 3.1. Objetivo general

Implementar el proceso completo de firma digital de un documento PDF utilizando un certificado digital autofirmado generado con Java keytool, con el fin de comprender de manera práctica los conceptos fundamentales de criptografía de clave pública, infraestructura PKI y los mecanismos técnicos que garantizan autenticidad, integridad y no repudio en documentos electrónicos.

### 3.2. Objetivos específicos

1. Generar un par de claves criptográficas (pública y privada) y un certificado digital autofirmado en formato X.509 utilizando la herramienta Java keytool, aplicando algoritmos criptográficos robustos (RSA-2048 y SHA-256).

2. Crear y gestionar un keystore en formato PKCS#12 que almacene de forma segura la clave privada y el certificado digital, comprendiendo la importancia de la protección mediante contraseña.

3. Aplicar una firma digital visible a un documento PDF mediante programación en Java, utilizando bibliotecas especializadas (iText) y el certificado previamente generado.

4. Analizar y verificar el resultado de la firma digital en lectores de PDF estándar, discutiendo el impacto del periodo de validez del certificado y las limitaciones inherentes al uso de certificados autofirmados en comparación con certificados emitidos por Autoridades Certificadoras reconocidas.

---

## 4. Materiales y Herramientas

Para la realización de este laboratorio se utilizaron los siguientes recursos tecnológicos:

### 4.1. Software base

- **Sistema operativo:** Windows 10/11 (64 bits)
- **Java Development Kit (JDK):** Versión 11 o superior, que incluye las herramientas:
  - `keytool`: Utilidad de línea de comandos para gestión de claves y certificados
  - `java`: Máquina virtual Java para ejecutar aplicaciones
  - `javac`: Compilador de Java

### 4.2. Herramientas de desarrollo

- **Apache Maven:** Sistema de gestión de proyectos y dependencias (versión 3.6 o superior)
- **Editor de código:** Visual Studio Code, IntelliJ IDEA, Eclipse o similar
- **Terminal/Consola:** CMD, PowerShell o Git Bash

### 4.3. Bibliotecas Java utilizadas

- **iText 8.0.2:** Biblioteca para manipulación y firma de documentos PDF
  - Módulos: kernel, layout, io, sign
- **BouncyCastle 1.70:** Proveedor criptográfico que implementa algoritmos adicionales
  - bcprov-jdk15on: Proveedor de algoritmos criptográficos
  - bcpkix-jdk15on: Soporte para PKI y certificados X.509

### 4.4. Herramientas de visualización

- **Adobe Acrobat Reader DC:** Lector de PDF con capacidad de verificación de firmas digitales
- **Foxit Reader** o **PDF-XChange Viewer:** Alternativas para visualización y verificación de firmas

### 4.5. Documentos de prueba

- **Archivo PDF de prueba:** Documento académico (boleta de matrícula, certificado de estudios, informe técnico, o cualquier documento PDF de prueba) para aplicar la firma digital.

---

## 5. Desarrollo del Procedimiento

El desarrollo del laboratorio se llevó a cabo siguiendo una metodología estructurada en seis fases secuenciales, desde la preparación del entorno hasta la verificación final de la firma digital aplicada.

### 5.1. Creación de la carpeta de trabajo

Se inició el laboratorio creando una estructura de directorios organizada para almacenar todos los archivos del proyecto. Se creó una carpeta principal denominada `PDFSigner` en el directorio de trabajo del usuario. Dentro de esta carpeta se organizaron las siguientes subcarpetas:

- `src/main/java/com/seguridad/pdfsigner`: Código fuente Java
- `scripts`: Scripts auxiliares para automatización
- `docs`: Documentación del proyecto
- `lib`: Bibliotecas externas (si se requieren)

Adicionalmente, se colocó en la carpeta raíz del proyecto el archivo PDF de prueba que sería firmado digitalmente (en este caso, una boleta de matrícula académica en formato PDF).

### 5.2. Generación del certificado digital autofirmado con keytool

Se procedió a generar el certificado digital autofirmado utilizando la herramienta `keytool` incluida en el JDK. Se abrió una terminal en la carpeta del proyecto y se ejecutó el siguiente comando:

```bash
keytool -genkeypair -alias mifirma -keyalg RSA -keysize 2048 -validity 365 -keystore mifirma.p12 -storetype PKCS12 -sigalg SHA256withRSA
```

**Explicación detallada de los parámetros utilizados:**

- **`-genkeypair`**: Indica a keytool que genere un par de claves (pública y privada) junto con un certificado autofirmado.

- **`-alias mifirma`**: Define un alias o nombre identificador para la entrada del keystore. Este alias se utilizará posteriormente para referenciar esta clave específica cuando se requiera firmar documentos.

- **`-keyalg RSA`**: Especifica el algoritmo criptográfico para la generación del par de claves. RSA es el algoritmo asimétrico más ampliamente utilizado y aceptado.

- **`-keysize 2048`**: Define el tamaño de la clave en bits. 2048 bits es el mínimo recomendado actualmente para garantizar seguridad adecuada. Valores mayores (3072 o 4096 bits) ofrecen mayor seguridad pero con mayor costo computacional.

- **`-validity 365`**: Establece el periodo de validez del certificado en días. En este caso, 365 días (un año). Después de este periodo, el certificado expirará y no podrá utilizarse para nuevas firmas.

- **`-keystore mifirma.p12`**: Especifica el nombre y ruta del archivo keystore donde se almacenará la clave privada y el certificado. La extensión `.p12` es estándar para archivos PKCS#12.

- **`-storetype PKCS12`**: Indica el formato del keystore. PKCS#12 es un estándar internacional portable y compatible con múltiples plataformas y aplicaciones.

- **`-sigalg SHA256withRSA`**: Define el algoritmo de firma que se utilizará para firmar el propio certificado. SHA256withRSA combina la función hash SHA-256 con el algoritmo de firma RSA.

Al ejecutar el comando, keytool solicitó interactivamente la siguiente información:

1. **Contraseña del keystore**: Se ingresó una contraseña segura (mínimo 6 caracteres) que protegerá el acceso al archivo PKCS#12. Esta contraseña se solicitará cada vez que se requiera acceder a la clave privada.

2. **Confirmación de contraseña**: Se reingresó la misma contraseña para verificación.

3. **Datos del sujeto del certificado (Distinguished Name)**: Keytool solicitó los siguientes campos que conforman el nombre distinguido del certificado:

   - **¿Cuál es su nombre y apellido?** (CN - Common Name): Se ingresó el nombre completo del titular, por ejemplo: "Juan Carlos Pérez García"

   - **¿Cuál es el nombre de su unidad de organización?** (OU - Organizational Unit): Se ingresó el departamento o unidad, por ejemplo: "Facultad de Ingeniería de Sistemas"

   - **¿Cuál es el nombre de su organización?** (O - Organization): Se ingresó el nombre de la institución, por ejemplo: "Universidad Nacional de Ingeniería"

   - **¿Cuál es el nombre de su ciudad o localidad?** (L - Locality): Se ingresó la ciudad, por ejemplo: "Lima"

   - **¿Cuál es el nombre de su estado o provincia?** (ST - State): Se ingresó la región, por ejemplo: "Lima"

   - **¿Cuál es el código de país de dos letras para esta unidad?** (C - Country): Se ingresó el código ISO de dos letras, por ejemplo: "PE"

4. **Confirmación de datos**: Keytool mostró un resumen de todos los datos ingresados y solicitó confirmar si eran correctos (sí/no).

5. **Contraseña de la clave**: Opcionalmente, keytool preguntó si se deseaba utilizar una contraseña diferente específicamente para la clave privada. Por simplicidad, se presionó Enter para utilizar la misma contraseña del keystore.

Una vez completado el proceso, se generó exitosamente el archivo `mifirma.p12` en el directorio actual, conteniendo el par de claves y el certificado autofirmado.

### 5.3. Verificación del contenido del keystore

Para verificar que el certificado se generó correctamente y examinar sus propiedades, se ejecutó el siguiente comando:

```bash
keytool -list -v -keystore mifirma.p12
```

**Parámetros:**
- **`-list`**: Lista las entradas contenidas en el keystore.
- **`-v`**: Modo verbose (detallado), muestra información completa de cada entrada.
- **`-keystore mifirma.p12`**: Especifica el archivo keystore a examinar.

Al ejecutar este comando, keytool solicitó la contraseña del keystore y luego desplegó información detallada, incluyendo:

- **Tipo de keystore**: PKCS12
- **Proveedor del keystore**: SUN
- **Alias de entrada**: mifirma
- **Tipo de entrada**: PrivateKeyEntry (indica que contiene una clave privada asociada a un certificado)
- **Longitud de la cadena de certificados**: 1 (certificado autofirmado, sin cadena de CA)

**Información del certificado:**
- **Propietario (Subject)**: CN=Juan Carlos Pérez García, OU=Facultad de Ingeniería de Sistemas, O=Universidad Nacional de Ingeniería, L=Lima, ST=Lima, C=PE
- **Emisor (Issuer)**: Idéntico al propietario (característica de certificados autofirmados)
- **Número de serie**: Un valor hexadecimal único generado automáticamente
- **Válido desde**: Fecha y hora de generación del certificado
- **Válido hasta**: Fecha de expiración (365 días después de la generación)
- **Huellas digitales del certificado**:
  - SHA256: Valor hexadecimal de 64 caracteres
  - SHA1: Valor hexadecimal de 40 caracteres
- **Algoritmo de firma**: SHA256withRSA
- **Algoritmo de clave pública del sujeto**: RSA de 2048 bits
- **Versión**: 3

Esta verificación confirmó que el certificado se generó correctamente con los parámetros especificados y que contiene tanto la clave privada como el certificado público asociado.

### 5.4. Preparación del documento PDF a firmar

Se seleccionó un documento PDF de prueba para aplicar la firma digital. En este laboratorio se utilizó una boleta de matrícula académica en formato PDF, documento representativo del tipo de archivos que comúnmente requieren firma digital en entornos universitarios.

El archivo PDF (denominado `boleta_matricula.pdf`) se copió a la carpeta raíz del proyecto `PDFSigner` para facilitar su acceso durante el proceso de firma. Se verificó que el archivo no estuviera corrupto abriéndolo previamente en un lector de PDF estándar.

### 5.5. Desarrollo de la aplicación Java para firma digital del PDF

En lugar de utilizar herramientas gráficas de terceros como JSignPDF, se desarrolló una aplicación Java personalizada que implementa el proceso completo de firma digital utilizando la biblioteca iText 8 y el proveedor criptográfico BouncyCastle.

**5.5.1. Configuración del proyecto Maven**

Se creó un archivo `pom.xml` en la raíz del proyecto con las dependencias necesarias:

- iText versión 8.0.2 (módulos: kernel, layout, io, sign)
- BouncyCastle versión 1.70 (bcprov-jdk15on, bcpkix-jdk15on)
- SLF4J para logging

El archivo POM también configuró el plugin Maven Shade para generar un JAR ejecutable con todas las dependencias incluidas (fat JAR).

**5.5.2. Implementación del código Java**

Se desarrolló la clase `PDFSigner.java` en el paquete `com.seguridad.pdfsigner` con las siguientes funcionalidades principales:

**Método `signPDF`**: Método estático que recibe como parámetros:
- Ruta del PDF de entrada
- Ruta del PDF firmado de salida
- Ruta del keystore PKCS#12
- Contraseña del keystore
- Alias de la clave
- Razón de la firma
- Ubicación de la firma

Este método realiza las siguientes operaciones:

1. Registra el proveedor criptográfico BouncyCastle mediante `Security.addProvider(new BouncyCastleProvider())`

2. Carga el keystore PKCS#12:
   ```java
   KeyStore keystore = KeyStore.getInstance("PKCS12");
   keystore.load(new FileInputStream(keystorePath), keystorePassword);
   ```

3. Extrae la clave privada y la cadena de certificados:
   ```java
   PrivateKey privateKey = (PrivateKey) keystore.getKey(alias, keystorePassword);
   Certificate[] chain = keystore.getCertificateChain(alias);
   ```

4. Crea un `PdfReader` para leer el PDF de entrada y un `PdfSigner` para aplicar la firma

5. Configura la apariencia visual de la firma mediante `PdfSignatureAppearance`:
   - Establece la razón de la firma
   - Establece la ubicación
   - Define las coordenadas y dimensiones del recuadro de firma visible en la primera página

6. Crea el firmante externo utilizando `PrivateKeySignature` con el algoritmo SHA-256

7. Ejecuta la firma mediante `signer.signDetached()` utilizando el estándar CMS (Cryptographic Message Syntax)

**Método `displayCertificateInfo`**: Muestra información detallada del certificado almacenado en el keystore, útil para verificación previa a la firma.

**Método `main`**: Proporciona una interfaz de usuario por consola que solicita interactivamente:
- Ruta del PDF a firmar
- Ruta del PDF de salida (opcionalmente genera un nombre automático agregando `_signed`)
- Ruta del keystore
- Contraseña del keystore
- Alias de la clave (por defecto "mifirma")
- Razón de la firma
- Ubicación

**5.5.3. Compilación del proyecto**

Se compiló el proyecto ejecutando desde la raíz del proyecto:

```bash
mvn clean package
```

Maven descargó automáticamente todas las dependencias especificadas en el POM, compiló el código fuente y generó el archivo JAR ejecutable `pdf-signer.jar` en la carpeta `target`.

**5.5.4. Ejecución de la aplicación y firma del PDF**

Se ejecutó la aplicación mediante:

```bash
java -jar target/pdf-signer.jar
```

La aplicación mostró una interfaz de consola solicitando los datos necesarios. Se ingresaron los siguientes valores:

- **Ruta del PDF a firmar**: `boleta_matricula.pdf`
- **Ruta del PDF firmado de salida**: Se dejó en blanco para generar automáticamente `boleta_matricula_signed.pdf`
- **Ruta del keystore PKCS#12**: `mifirma.p12`
- **Contraseña del keystore**: La contraseña configurada previamente
- **Alias de la clave**: Se dejó en blanco para usar el valor por defecto "mifirma"
- **Razón de la firma**: "Firma de boleta de matrícula académica"
- **Ubicación**: "Lima, Perú"

La aplicación procesó la solicitud, mostrando primero la información detallada del certificado y luego ejecutando el proceso de firma digital. Al finalizar, mostró el mensaje de confirmación:

```
✓ PDF firmado exitosamente: boleta_matricula_signed.pdf
```

El archivo firmado `boleta_matricula_signed.pdf` fue generado exitosamente en el directorio del proyecto.

### 5.6. Verificación de la firma en el lector de PDF

Se abrió el archivo `boleta_matricula_signed.pdf` en Adobe Acrobat Reader DC para verificar la firma digital aplicada.

**Observaciones realizadas:**

1. **Panel de firmas**: En la parte superior del documento, Adobe Reader mostró una barra azul indicando: "Firmado y todas las firmas son válidas", aunque con una advertencia adicional sobre la confianza.

2. **Recuadro de firma visible**: En la primera página del PDF, en las coordenadas especificadas, apareció un recuadro visual conteniendo:
   - Nombre del firmante (extraído del campo CN del certificado)
   - Razón: "Firma de boleta de matrícula académica"
   - Ubicación: "Lima, Perú"
   - Fecha y hora de la firma
   - Icono indicativo del estado de validación

3. **Panel de firmas digitales**: Al hacer clic en el panel de firmas o en el recuadro de firma, se desplegó información detallada:
   - **Estado de la firma**: Válida (la firma no ha sido modificada desde que se firmó el documento)
   - **Identidad del firmante**: CN=Juan Carlos Pérez García, OU=Facultad de Ingeniería de Sistemas, O=Universidad Nacional de Ingeniería, L=Lima, ST=Lima, C=PE
   - **Fecha y hora de firma**: Fecha exacta en que se aplicó la firma
   - **Algoritmo utilizado**: SHA-256 con encriptación RSA (2048 bits)

4. **Advertencia de confianza**: Adobe Reader mostró una advertencia indicando: "Al menos una firma tiene problemas" o "La identidad del firmante es desconocida porque no está incluida en su lista de certificados de confianza y ninguna de las certificaciones principales está incluida en certificados de confianza".

Esta advertencia es esperada y normal cuando se utiliza un certificado autofirmado, ya que:
- El certificado no fue emitido por una Autoridad Certificadora reconocida públicamente
- No está en la lista de certificados raíz confiables del sistema operativo
- Adobe Reader no puede verificar la cadena de confianza hasta una CA conocida

5. **Propiedades de la firma**: Al revisar las propiedades detalladas de la firma, se confirmó:
   - La firma cubre todo el documento
   - No se han detectado modificaciones desde la firma
   - El resumen del documento (hash) coincide con el resumen firmado
   - El certificado utilizado estaba dentro de su periodo de validez al momento de firmar

6. **Validación criptográfica**: A pesar de la advertencia de confianza, la validación criptográfica fue exitosa, confirmando que:
   - La firma es matemáticamente válida
   - Fue generada con la clave privada correspondiente al certificado presentado
   - El documento no ha sido alterado después de la firma

**Opción de confianza manual**: Para eliminar la advertencia en un entorno de pruebas, es posible agregar manualmente el certificado autofirmado a la lista de certificados de confianza de Adobe Reader:
1. Clic derecho en la firma → Mostrar propiedades de la firma
2. Mostrar certificado del firmante
3. Pestaña "Confianza" → Agregar a certificados de confianza
4. Seleccionar "Utilizar este certificado como raíz de confianza"
5. Seleccionar los usos permitidos (firmas de documentos)

Tras este proceso, Adobe Reader reconocería el certificado como confiable y la advertencia desaparecería. Sin embargo, esto solo afecta al sistema local y no resuelve el problema de confianza para otros usuarios que reciban el documento.

---

## 6. Resultados

El laboratorio se completó exitosamente, alcanzando todos los objetivos planteados. Los resultados concretos obtenidos fueron:

1. **Generación exitosa del certificado autofirmado**: Se creó un archivo keystore `mifirma.p12` en formato PKCS#12 conteniendo:
   - Par de claves RSA de 2048 bits
   - Certificado digital X.509 autofirmado con validez de 365 días
   - Algoritmo de firma SHA256withRSA
   - Información del sujeto correctamente configurada

2. **Aplicación Java funcional**: Se desarrolló una aplicación completa en Java capaz de:
   - Cargar keystores PKCS#12
   - Acceder a claves privadas y certificados
   - Aplicar firmas digitales a documentos PDF
   - Configurar firmas visibles con información personalizada
   - Utilizar estándares criptográficos modernos (CMS)

3. **Documento PDF firmado digitalmente**: Se obtuvo el archivo `boleta_matricula_signed.pdf` que contiene:
   - El contenido original del documento intacto
   - Una firma digital criptográficamente válida
   - Un recuadro de firma visible en la primera página
   - Metadatos de firma (razón, ubicación, fecha, firmante)

4. **Verificación exitosa de la firma**: Al abrir el documento firmado en Adobe Acrobat Reader se observó:
   - Validación criptográfica exitosa de la firma
   - Confirmación de que el documento no fue modificado después de la firma
   - Identificación correcta del firmante mediante el certificado
   - Visualización de todos los metadatos de la firma
   - Advertencia esperada sobre certificado autofirmado (no confiable por defecto)

5. **Comprensión de conceptos PKI**: Se logró comprender prácticamente:
   - El flujo completo de generación y uso de certificados digitales
   - La relación entre claves privadas, públicas y certificados
   - El funcionamiento de las firmas digitales basadas en hash y criptografía asimétrica
   - Las diferencias entre certificados autofirmados y emitidos por CA
   - El impacto del periodo de validez en los certificados

El comportamiento del lector de PDF fue el esperado: la firma se validó correctamente desde el punto de vista criptográfico, pero se mostró una advertencia de confianza debido a que el certificado es autofirmado y no está respaldado por una Autoridad Certificadora reconocida. Esta advertencia no invalida la firma, sino que indica que no existe una cadena de confianza verificable hasta una CA raíz confiable.

---

## 7. Análisis y Discusión

### 7.1. Relación entre clave privada, certificado y firma digital

El laboratorio permitió comprender la relación fundamental entre estos tres elementos del ecosistema PKI:

La **clave privada** es el elemento más crítico y sensible del sistema. Es un valor matemático que debe mantenerse en secreto absoluto, ya que su posesión otorga la capacidad de generar firmas digitales válidas. En este laboratorio, la clave privada RSA de 2048 bits se generó aleatoriamente y se almacenó cifrada dentro del keystore PKCS#12, protegida por la contraseña del almacén.

El **certificado digital** actúa como una credencial electrónica que vincula la clave pública con la identidad del titular. Contiene la clave pública (complemento matemático de la clave privada), información identificativa del titular (nombre distinguido), periodo de validez, y la firma del emisor. En un certificado autofirmado, el emisor y el sujeto son la misma entidad, lo que significa que el certificado está firmado con la propia clave privada del titular.

La **firma digital** es el resultado de aplicar la clave privada al hash del documento. Cuando se firma un PDF, el proceso es el siguiente:
1. Se calcula el hash SHA-256 del contenido del documento
2. Este hash se cifra usando la clave privada RSA
3. El hash cifrado, junto con el certificado del firmante, se incrustan en el PDF
4. Cualquier persona puede verificar la firma usando la clave pública del certificado

Esta arquitectura garantiza que solo el poseedor de la clave privada puede generar una firma válida, mientras que cualquiera con acceso a la clave pública (contenida en el certificado) puede verificarla.

### 7.2. Diferencia entre firma digital y simple inserción de imagen

Es fundamental distinguir entre una firma digital criptográfica y la simple inserción de una imagen de firma manuscrita escaneada:

**Imagen de firma escaneada:**
- Es simplemente un elemento gráfico (imagen JPG, PNG, etc.) insertado en el documento
- No tiene protección criptográfica
- Puede ser copiada y reutilizada por cualquier persona
- No garantiza integridad: el documento puede modificarse después de insertar la imagen
- No proporciona no repudio: no hay evidencia técnica de quién insertó la imagen
- No verifica la identidad del firmante

**Firma digital criptográfica:**
- Está matemáticamente vinculada tanto al contenido del documento como a la identidad del firmante
- Solo puede ser generada por quien posee la clave privada
- Cualquier modificación del documento después de firmado invalida la firma inmediatamente
- Proporciona no repudio técnico: el firmante no puede negar haber firmado sin negar la posesión de su clave privada
- Incluye metadatos verificables (fecha, razón, ubicación, algoritmos utilizados)
- Permite verificación automatizada por software

En el laboratorio, la firma aplicada al PDF incluía también un componente visual (el recuadro visible en la página), pero este elemento gráfico está criptográficamente protegido y vinculado a la firma digital subyacente. Si alguien intentara modificar el texto visible de la firma o cualquier parte del documento, la validación criptográfica fallaría inmediatamente.

### 7.3. Seguridad aportada por RSA-2048 y SHA-256

La combinación de RSA con claves de 2048 bits y la función hash SHA-256 proporciona un nivel de seguridad robusto que es apropiado para la mayoría de aplicaciones actuales:

**RSA-2048:**
- Según estimaciones actuales, factorizar un número RSA de 2048 bits requeriría recursos computacionales extraordinarios y tiempo medido en siglos con tecnología actual
- Es el mínimo recomendado por organismos como NIST (National Institute of Standards and Technology) y ENISA (European Union Agency for Cybersecurity) para uso hasta al menos 2030
- Proporciona aproximadamente 112 bits de seguridad simétrica equivalente
- Para mayor seguridad a largo plazo, se recomienda migrar a RSA-3072 o RSA-4096

**SHA-256:**
- Pertenece a la familia SHA-2, diseñada por la NSA y aprobada por NIST
- Produce hashes de 256 bits (64 caracteres hexadecimales)
- No existen ataques de colisión prácticos conocidos contra SHA-256
- Proporciona 128 bits de seguridad contra ataques de colisión y 256 bits contra ataques de preimagen
- Es significativamente más seguro que su predecesor SHA-1, que ya ha sido comprometido

En el contexto de firma digital de PDFs académicos, esta combinación es más que suficiente para garantizar que:
- Es computacionalmente inviable falsificar una firma sin poseer la clave privada
- Es prácticamente imposible encontrar dos documentos diferentes con el mismo hash (ataque de colisión)
- La firma permanecerá segura durante el periodo de validez del certificado y más allá

### 7.4. Impacto del periodo de validez del certificado

El periodo de validez del certificado (en este caso, 365 días) tiene implicaciones importantes:

**Durante el periodo de validez:**
- El certificado puede utilizarse libremente para firmar nuevos documentos
- Los sistemas de validación lo consideran "vigente"
- No se muestran advertencias relacionadas con expiración

**Después de la expiración:**
- El certificado no debe utilizarse para firmar nuevos documentos
- Los validadores mostrarán advertencias indicando que el certificado ha expirado
- Sin embargo, las firmas realizadas ANTES de la expiración siguen siendo técnicamente válidas

**Problemática sin sello de tiempo (timestamp):**

En este laboratorio no se implementó sellado de tiempo (timestamp), lo que significa que:
- La fecha de firma es autoafirmada por el firmante (tomada del reloj del sistema)
- No hay evidencia criptográfica irrefutable de CUÁNDO se realizó la firma
- Si el certificado expira, los verificadores pueden dudar si la firma se realizó cuando el certificado estaba vigente

**Solución con sello de tiempo:**

En entornos de producción, se recomienda incluir un sello de tiempo de una Autoridad de Sellado de Tiempo (TSA) confiable:
- La TSA firma criptográficamente la fecha y hora exactas de la firma
- Esta firma de la TSA es independiente del certificado del firmante
- Incluso si el certificado del firmante expira o es revocado, el timestamp prueba que la firma se realizó cuando el certificado estaba vigente
- Proporciona evidencia legal de la fecha de firma

Para documentos con valor legal a largo plazo (contratos, actas notariales, documentos gubernamentales), el sellado de tiempo es esencial. Para documentos académicos internos de corto plazo, puede ser opcional.

### 7.5. Limitaciones de certificados autofirmados vs. certificados de CA

El laboratorio evidenció claramente la principal limitación de los certificados autofirmados: la falta de cadena de confianza:

**Certificado autofirmado:**
- **Ventajas:**
  - Gratuito y de generación instantánea
  - Control total sobre el certificado
  - Mismas capacidades criptográficas que un certificado de CA
  - Ideal para desarrollo, pruebas, entornos internos cerrados

- **Limitaciones:**
  - No hay verificación de identidad por tercero confiable
  - Los sistemas no confían en él automáticamente
  - Requiere distribución e instalación manual para establecer confianza
  - No es adecuado para documentos que circularán públicamente
  - Vulnerable a ataques de suplantación si no se verifica manualmente

**Certificado emitido por CA reconocida:**
- **Ventajas:**
  - Confianza automática en navegadores y sistemas operativos
  - Verificación de identidad realizada por la CA antes de emisión
  - Cadena de confianza verificable hasta CA raíz
  - Aceptación universal en contextos legales y comerciales
  - Posibilidad de revocación centralizada vía CRL u OCSP

- **Limitaciones:**
  - Costo económico (certificados comerciales)
  - Proceso de validación de identidad puede ser extenso
  - Dependencia de servicios de terceros
  - Renovación periódica necesaria

**Escenarios apropiados:**

- **Usar certificados autofirmados:** Laboratorios educativos, entornos de desarrollo y pruebas, sistemas internos donde todos los usuarios pueden importar manualmente el certificado como confiable, aprendizaje de conceptos PKI.

- **Usar certificados de CA:** Sitios web públicos (HTTPS), firmas de documentos con valor legal, aplicaciones móviles, comunicaciones con clientes externos, cumplimiento normativo (eIDAS, ESIGN Act, etc.).

En el contexto de este laboratorio académico, el certificado autofirmado fue perfectamente apropiado, ya que el objetivo era comprender los mecanismos técnicos subyacentes sin incurrir en costos ni depender de servicios externos. Sin embargo, para un sistema de firmas en producción (por ejemplo, firma de certificados de notas oficiales de una universidad), sería imprescindible adquirir certificados de una CA reconocida.

---

## 8. Conclusiones

Del desarrollo del presente laboratorio se derivan las siguientes conclusiones fundamentales:

1. **Comprensión integral del ciclo de firma digital**: Se logró comprender y ejecutar exitosamente el ciclo completo de firma digital de documentos, que abarca desde la generación del par de claves criptográficas, pasando por la creación del certificado autofirmado, la aplicación de la firma al documento PDF mediante programación, hasta la verificación de la firma en lectores estándar. Este proceso demuestra que la firma digital es un mecanismo técnico sólido que integra múltiples conceptos de criptografía de clave pública, funciones hash y estándares PKI.

2. **Importancia crítica de la gestión de claves y keystores**: El laboratorio evidenció que la seguridad de todo el sistema de firma digital descansa fundamentalmente en la protección de la clave privada. El uso de keystores PKCS#12 protegidos por contraseña robusta es esencial para prevenir accesos no autorizados. La pérdida de la clave privada imposibilita la generación de nuevas firmas con ese certificado, mientras que su compromiso permitiría a un atacante firmar documentos fraudulentamente. Por tanto, las políticas de gestión de claves (generación segura, almacenamiento protegido, backup controlado y destrucción segura al final del ciclo de vida) son tan importantes como los propios algoritmos criptográficos.

3. **Diferenciación clara entre certificados autofirmados y emitidos por CA**: Los certificados autofirmados, si bien proporcionan las mismas garantías criptográficas de integridad, autenticidad y no repudio que los certificados emitidos por Autoridades Certificadoras reconocidas, carecen de la cadena de confianza necesaria para ser aceptados automáticamente por sistemas y aplicaciones. Son herramientas valiosas para entornos de desarrollo, pruebas, aprendizaje académico y sistemas internos cerrados, pero resultan inadecuados para documentos que requieren confianza pública o valor legal en contextos externos. Para entornos de producción que requieren interoperabilidad y confianza universal, es imprescindible utilizar certificados emitidos por CA reconocidas (comerciales o gubernamentales).

4. **Relevancia práctica en múltiples dominios**: La firma digital de documentos PDF tiene aplicaciones concretas y actuales en múltiples ámbitos: en el entorno académico (certificados de notas, títulos profesionales, actas de grado), en el sector empresarial (contratos laborales, facturas electrónicas, reportes financieros), en el ámbito gubernamental (documentos oficiales, resoluciones administrativas, trámites digitales) y en el sector salud (historias clínicas electrónicas, recetas médicas). La transformación digital y las iniciativas de gobierno electrónico han convertido a la firma digital en un habilitador fundamental de la desmaterialización de procesos, reduciendo costos, tiempos y mejorando la trazabilidad documental.

5. **Necesidad de estándares complementarios para firmas de largo plazo**: Si bien la firma digital básica implementada en este laboratorio es suficiente para muchos casos de uso, para documentos que deben mantener su validez legal durante periodos prolongados (años o décadas), es necesario implementar mecanismos adicionales como sellos de tiempo (timestamps) de Autoridades de Sellado de Tiempo confiables, formatos de firma avanzada (PAdES-LTA, XAdES-LTA) que incluyen información de revocación y validación, y archivado seguro de evidencias criptográficas. Estos estándares adicionales garantizan que las firmas puedan ser validadas incluso después de que los certificados hayan expirado o los algoritmos criptográficos hayan sido deprecados.

---

## 9. Recomendaciones

Con base en los resultados y análisis realizados, se formulan las siguientes recomendaciones de buenas prácticas para la implementación de sistemas de firma digital:

1. **Utilizar longitudes de clave robustas y algoritmos modernos**: Se recomienda emplear claves RSA de al menos 2048 bits para aplicaciones actuales, con proyección a migrar hacia 3072 o 4096 bits para sistemas que deban operar más allá de 2030. Alternativamente, considerar algoritmos de curva elíptica (ECDSA con curvas P-256 o superiores) que ofrecen seguridad equivalente con claves más cortas y mejor rendimiento. En cuanto a funciones hash, SHA-256 es el mínimo aceptable; para aplicaciones críticas se recomienda SHA-384 o SHA-512. Es fundamental evitar algoritmos deprecados como MD5, SHA-1 o claves RSA menores a 2048 bits.

2. **Implementar protección robusta de claves privadas**: La clave privada debe protegerse mediante contraseñas de alta entropía (mínimo 12 caracteres, combinando mayúsculas, minúsculas, números y símbolos). Para entornos empresariales críticos, considerar el uso de módulos de seguridad hardware (HSM - Hardware Security Module) que almacenan las claves en dispositivos físicos inviolables. Establecer políticas claras de backup cifrado de claves, procedimientos de recuperación ante pérdida, y destrucción segura al final del ciclo de vida. Nunca compartir claves privadas ni almacenarlas en sistemas no protegidos.

3. **Utilizar certificados de CA reconocida en producción**: Para sistemas que operarán en entornos de producción, especialmente aquellos que involucren partes externas o requieran valor legal, es imprescindible adquirir certificados emitidos por Autoridades Certificadoras reconocidas y confiables. Seleccionar proveedores acreditados (DigiCert, GlobalSign, Sectigo, AC Raíz Nacional en Perú, etc.) y optar por certificados de validación extendida (EV) cuando la criticidad del caso lo justifique. Para firmas con valor legal en contextos gubernamentales, verificar el cumplimiento con regulaciones locales (firma electrónica avanzada según legislación del país).

4. **Incorporar sellado de tiempo (timestamp) para firmas de largo plazo**: Para documentos que deben mantener validez durante periodos prolongados (contratos plurianuales, documentos de archivo permanente, certificaciones académicas), implementar sellado de tiempo mediante Autoridades de Sellado de Tiempo (TSA) confiables. El timestamp criptográfico certifica el momento exacto de la firma, independizando la validez de la firma del periodo de validez del certificado. Esto es especialmente crítico para cumplimiento normativo en firmas electrónicas avanzadas según regulaciones como eIDAS (Europa) o equivalentes.

5. **Establecer políticas de renovación y revocación**: Implementar procedimientos sistemáticos de renovación de certificados antes de su expiración, idealmente con 30-60 días de anticipación. Establecer mecanismos de revocación inmediata en caso de compromiso de clave privada, pérdida de control del dispositivo de firma, o cambio de circunstancias del titular. Mantener listas de revocación de certificados (CRL) actualizadas y considerar el uso de OCSP (Online Certificate Status Protocol) para validación en tiempo real del estado de los certificados.

6. **Validar y auditar firmas periódicamente**: Implementar procesos de validación periódica de documentos firmados, especialmente aquellos con valor legal o contractual. Utilizar herramientas de validación que verifiquen no solo la validez criptográfica, sino también el estado del certificado, la cadena de confianza completa, y la presencia de timestamps. Mantener logs de auditoría de todas las operaciones de firma y validación para trazabilidad y cumplimiento normativo.

7. **Capacitación y concientización de usuarios**: Proporcionar capacitación adecuada a todos los usuarios que utilicen sistemas de firma digital, enfatizando la importancia de la protección de credenciales, el reconocimiento de intentos de phishing o ingeniería social dirigidos a obtener claves privadas, y el uso correcto de las herramientas de firma. Establecer políticas de uso aceptable y consecuencias en caso de mal uso.

8. **Considerar soluciones de firma centralizada para organizaciones**: En entornos empresariales o institucionales donde múltiples usuarios requieren capacidad de firma, evaluar soluciones de firma centralizada o servicios de firma en la nube (cloud signing services) que centralicen la gestión de certificados, implementen controles de acceso granulares, y simplifiquen la operación manteniendo altos estándares de seguridad.

---

## 10. Referencias Bibliográficas

1. **Stallings, W.** (2017). *Cryptography and Network Security: Principles and Practice* (7ª ed.). Pearson Education. ISBN: 978-0134444284.

   Texto fundamental que cubre en profundidad los algoritmos criptográficos (RSA, funciones hash, criptografía de clave pública), protocolos de seguridad y aplicaciones prácticas de la criptografía en redes y sistemas de información.

2. **Housley, R., & Polk, T.** (2001). *Planning for PKI: Best Practices Guide for Deploying Public Key Infrastructure*. John Wiley & Sons. ISBN: 978-0471397024.

   Guía práctica sobre planificación, diseño e implementación de infraestructuras de clave pública (PKI), incluyendo mejores prácticas para gestión de certificados, políticas de certificación y operación de autoridades certificadoras.

3. **Oracle Corporation.** (2023). *keytool - Key and Certificate Management Tool*. Java Platform, Standard Edition Tools Reference. Disponible en: https://docs.oracle.com/en/java/javase/11/tools/keytool.html

   Documentación oficial de Oracle sobre la herramienta keytool, detallando todos los comandos, parámetros y opciones para generación y gestión de claves y certificados en entornos Java.

4. **iText Software.** (2023). *iText 8 API Documentation - Digital Signatures*. Disponible en: https://api.itextpdf.com/iText8/

   Documentación técnica de la biblioteca iText para manipulación de documentos PDF, con especial énfasis en la implementación de firmas digitales conforme a estándares PAdES.

5. **European Telecommunications Standards Institute (ETSI).** (2016). *ETSI EN 319 142-1: PAdES digital signatures - Part 1: Building blocks and PAdES baseline signatures* (v1.1.1).

   Estándar europeo que define los formatos de firma digital avanzada para documentos PDF (PAdES - PDF Advanced Electronic Signatures), incluyendo niveles básicos (B-B, B-T) y de largo plazo (LT, LTA).

6. **Instituto Nacional de Ciberseguridad de España (INCIBE).** (2022). *Certificados Digitales y Firma Electrónica: Guía de Tecnologías y Aplicaciones*. Disponible en: https://www.incibe.es

   Guía práctica en español que explica los conceptos fundamentales de certificados digitales, firma electrónica, tipos de firmas según nivel de seguridad y aplicaciones en diferentes sectores.

---

**FIN DEL INFORME**
