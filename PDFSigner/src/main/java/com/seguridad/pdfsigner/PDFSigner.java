package com.seguridad.pdfsigner;

import com.itextpdf.kernel.pdf.PdfReader;
import com.itextpdf.kernel.pdf.StampingProperties;
import com.itextpdf.signatures.*;
import org.bouncycastle.jce.provider.BouncyCastleProvider;

import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.security.KeyStore;
import java.security.PrivateKey;
import java.security.Security;
import java.security.cert.Certificate;
import java.util.Scanner;

/**
 * Clase principal para firmar documentos PDF digitalmente usando certificados X.509.
 *
 * Esta aplicación demuestra el uso de criptografía de clave pública para garantizar:
 * - Autenticidad: Verifica la identidad del firmante
 * - Integridad: Asegura que el documento no ha sido modificado
 * - No repudio: El firmante no puede negar haber firmado el documento
 *
 * @author Laboratorio de Seguridad de la Información
 * @version 1.0
 */
public class PDFSigner {

    /**
     * Firma digitalmente un documento PDF utilizando un certificado del keystore.
     *
     * @param src Ruta del archivo PDF de entrada
     * @param dest Ruta del archivo PDF firmado de salida
     * @param keystorePath Ruta del archivo keystore PKCS#12
     * @param keystorePassword Contraseña del keystore
     * @param alias Alias de la clave privada en el keystore
     * @param reason Razón de la firma
     * @param location Ubicación de la firma
     * @throws Exception Si ocurre algún error durante el proceso de firma
     */
    public static void signPDF(String src, String dest, String keystorePath,
                               char[] keystorePassword, String alias,
                               String reason, String location) throws Exception {

        // Añadir el proveedor BouncyCastle para algoritmos criptográficos
        Security.addProvider(new BouncyCastleProvider());

        // Cargar el keystore PKCS#12
        KeyStore keystore = KeyStore.getInstance("PKCS12");
        keystore.load(new FileInputStream(keystorePath), keystorePassword);

        // Obtener la clave privada y la cadena de certificados
        PrivateKey privateKey = (PrivateKey) keystore.getKey(alias, keystorePassword);
        Certificate[] chain = keystore.getCertificateChain(alias);

        if (privateKey == null || chain == null) {
            throw new Exception("No se encontró la clave privada o la cadena de certificados para el alias: " + alias);
        }

        // Crear el lector del PDF de entrada
        PdfReader reader = new PdfReader(src);

        // Crear el firmador del PDF
        PdfSigner signer = new PdfSigner(reader, new FileOutputStream(dest), new StampingProperties());

        // Configurar la apariencia de la firma visible
        PdfSignatureAppearance appearance = signer.getSignatureAppearance();
        appearance.setReason(reason);
        appearance.setLocation(location);
        appearance.setPageRect(new com.itextpdf.kernel.geom.Rectangle(36, 648, 200, 100));
        appearance.setPageNumber(1);
        signer.setFieldName("Firma_Digital");

        // Crear el contenedor de firma externa
        IExternalSignature externalSignature = new PrivateKeySignature(privateKey,
            DigestAlgorithms.SHA256, BouncyCastleProvider.PROVIDER_NAME);
        IExternalDigest digest = new BouncyCastleDigest();

        // Firmar el documento (CAdES equivalent)
        signer.signDetached(digest, externalSignature, chain, null, null, null,
                           0, PdfSigner.CryptoStandard.CMS);

        System.out.println("✓ PDF firmado exitosamente: " + dest);
    }

    /**
     * Muestra información sobre el keystore y el certificado.
     *
     * @param keystorePath Ruta del archivo keystore
     * @param keystorePassword Contraseña del keystore
     * @param alias Alias del certificado
     * @throws Exception Si ocurre algún error
     */
    public static void displayCertificateInfo(String keystorePath, char[] keystorePassword,
                                             String alias) throws Exception {
        KeyStore keystore = KeyStore.getInstance("PKCS12");
        keystore.load(new FileInputStream(keystorePath), keystorePassword);

        Certificate[] chain = keystore.getCertificateChain(alias);
        if (chain != null && chain.length > 0) {
            System.out.println("\n╔══════════════════════════════════════════════════════════════╗");
            System.out.println("║          INFORMACIÓN DEL CERTIFICADO                         ║");
            System.out.println("╚══════════════════════════════════════════════════════════════╝\n");

            for (int i = 0; i < chain.length; i++) {
                System.out.println("Certificado [" + i + "]:");
                System.out.println(chain[i].toString());
                System.out.println("─────────────────────────────────────────────────────────────");
            }
        }
    }

    /**
     * Método principal de la aplicación.
     * Proporciona una interfaz de consola para firmar PDFs.
     *
     * @param args Argumentos de línea de comandos (no utilizados)
     */
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        try {
            System.out.println("╔══════════════════════════════════════════════════════════════╗");
            System.out.println("║        FIRMA DIGITAL DE DOCUMENTOS PDF - PKI LAB            ║");
            System.out.println("╚══════════════════════════════════════════════════════════════╝\n");

            // Solicitar datos al usuario
            System.out.print("Ruta del PDF a firmar: ");
            String pdfInput = scanner.nextLine().trim();

            System.out.print("Ruta del PDF firmado de salida (dejar en blanco para agregar '_signed'): ");
            String pdfOutput = scanner.nextLine().trim();
            if (pdfOutput.isEmpty()) {
                pdfOutput = pdfInput.replace(".pdf", "_signed.pdf");
            }

            System.out.print("Ruta del keystore PKCS#12 (.p12): ");
            String keystorePath = scanner.nextLine().trim();

            System.out.print("Contraseña del keystore: ");
            String password = scanner.nextLine();

            System.out.print("Alias de la clave (dejar en blanco para 'mifirma'): ");
            String alias = scanner.nextLine().trim();
            if (alias.isEmpty()) {
                alias = "mifirma";
            }

            System.out.print("Razón de la firma: ");
            String reason = scanner.nextLine().trim();
            if (reason.isEmpty()) {
                reason = "Firma digital del documento";
            }

            System.out.print("Ubicación: ");
            String location = scanner.nextLine().trim();
            if (location.isEmpty()) {
                location = "Lima, Perú";
            }

            System.out.println("\n⌛ Procesando firma digital...\n");

            // Mostrar información del certificado
            displayCertificateInfo(keystorePath, password.toCharArray(), alias);

            // Firmar el PDF
            signPDF(pdfInput, pdfOutput, keystorePath, password.toCharArray(),
                   alias, reason, location);

            System.out.println("\n╔══════════════════════════════════════════════════════════════╗");
            System.out.println("║                 FIRMA COMPLETADA                             ║");
            System.out.println("╚══════════════════════════════════════════════════════════════╝");
            System.out.println("\nArchivo firmado: " + pdfOutput);
            System.out.println("\nPuede verificar la firma abriendo el PDF en Adobe Acrobat Reader.");

        } catch (Exception e) {
            System.err.println("\n✗ Error durante la firma: " + e.getMessage());
            e.printStackTrace();
        } finally {
            scanner.close();
        }
    }
}
