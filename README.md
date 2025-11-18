# Generador de Firma Virtual

Script en Python para generar firmas virtuales con formato estructurado y código único.

## Características

- ✅ Solicita datos al usuario (nombre, motivo, credenciales)
- ✅ Genera automáticamente un código de firma único de 10 caracteres alfanuméricos
- ✅ Añade automáticamente la fecha actual en formato YYYY-MM-DD
- ✅ Muestra la firma en formato estructurado
- ✅ Opción para guardar la firma en archivo

## Requisitos

- Python 3.6 o superior

## Uso

Ejecuta el script:

```bash
python3 virtual_signature.py
```

O si tiene permisos de ejecución:

```bash
./virtual_signature.py
```

## Formato de la Firma

```
Nombre completo: [nombre ingresado]
Código de firma: [código generado automáticamente]
Motivo: [motivo ingresado]
Fecha: [fecha automática YYYY-MM-DD]
Credenciales: [credenciales ingresadas]
```

## Ejemplo de Ejecución

```
=== GENERADOR DE FIRMA VIRTUAL ===

Ingrese su nombre completo: Juan Pérez García
Ingrese el motivo de la firma: Aprobación de documento
Ingrese sus credenciales profesionales: PhD en Ingeniería

╔══════════════════════════════════════════════════════════════╗
║                    FIRMA VIRTUAL                             ║
╚══════════════════════════════════════════════════════════════╝

Nombre completo: Juan Pérez García
Código de firma: aB3xK9mP2L
Motivo: Aprobación de documento
Fecha: 2025-11-18
Credenciales: PhD en Ingeniería
```

## Seguridad

El código de firma se genera utilizando el módulo `secrets` de Python, que es criptográficamente seguro y apropiado para generar tokens únicos.
