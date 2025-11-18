#!/usr/bin/env python3
"""
Script para generar firmas virtuales con formato estructurado.
"""

import secrets
import string
from datetime import datetime


def generar_codigo_firma():
    """
    Genera un código de firma único alfanumérico de 10 caracteres.

    Returns:
        str: Código alfanumérico único de 10 caracteres
    """
    caracteres = string.ascii_letters + string.digits
    codigo = ''.join(secrets.choice(caracteres) for _ in range(10))
    return codigo


def obtener_fecha_actual():
    """
    Obtiene la fecha actual en formato YYYY-MM-DD.

    Returns:
        str: Fecha en formato YYYY-MM-DD
    """
    return datetime.now().strftime('%Y-%m-%d')


def solicitar_datos():
    """
    Solicita al usuario los datos necesarios para la firma.

    Returns:
        tuple: (nombre_completo, motivo, credenciales)
    """
    print("=== GENERADOR DE FIRMA VIRTUAL ===\n")

    nombre_completo = input("Ingrese su nombre completo: ").strip()
    while not nombre_completo:
        print("El nombre no puede estar vacío.")
        nombre_completo = input("Ingrese su nombre completo: ").strip()

    motivo = input("Ingrese el motivo de la firma: ").strip()
    while not motivo:
        print("El motivo no puede estar vacío.")
        motivo = input("Ingrese el motivo de la firma: ").strip()

    credenciales = input("Ingrese sus credenciales profesionales: ").strip()
    while not credenciales:
        print("Las credenciales no pueden estar vacías.")
        credenciales = input("Ingrese sus credenciales profesionales: ").strip()

    return nombre_completo, motivo, credenciales


def generar_firma(nombre_completo, motivo, credenciales):
    """
    Genera la firma virtual con todos los componentes.

    Args:
        nombre_completo (str): Nombre completo del autor
        motivo (str): Motivo de la firma
        credenciales (str): Credenciales profesionales

    Returns:
        str: Firma virtual formateada
    """
    codigo_firma = generar_codigo_firma()
    fecha = obtener_fecha_actual()

    firma = f"""
╔══════════════════════════════════════════════════════════════╗
║                    FIRMA VIRTUAL                             ║
╚══════════════════════════════════════════════════════════════╝

Nombre completo: {nombre_completo}
Código de firma: {codigo_firma}
Motivo: {motivo}
Fecha: {fecha}
Credenciales: {credenciales}

══════════════════════════════════════════════════════════════
"""
    return firma


def main():
    """Función principal del programa."""
    try:
        # Solicitar datos al usuario
        nombre_completo, motivo, credenciales = solicitar_datos()

        # Generar y mostrar la firma
        firma = generar_firma(nombre_completo, motivo, credenciales)
        print(firma)

        # Preguntar si desea guardar la firma
        guardar = input("¿Desea guardar la firma en un archivo? (s/n): ").strip().lower()
        if guardar == 's':
            nombre_archivo = f"firma_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            with open(nombre_archivo, 'w', encoding='utf-8') as f:
                f.write(firma)
            print(f"\n✓ Firma guardada en: {nombre_archivo}")

    except KeyboardInterrupt:
        print("\n\nOperación cancelada por el usuario.")
    except Exception as e:
        print(f"\n✗ Error: {e}")


if __name__ == "__main__":
    main()
