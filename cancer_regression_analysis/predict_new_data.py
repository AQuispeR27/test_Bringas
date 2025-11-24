"""
Script para hacer predicciones con el modelo de regresión lineal entrenado
==========================================================================

Este script demuestra cómo usar el modelo entrenado para hacer predicciones
sobre nuevos datos.
"""

import joblib
import pandas as pd
import numpy as np
import os

print("=" * 80)
print("PREDICCIÓN CON MODELO DE REGRESIÓN LINEAL - MORTALIDAD POR CÁNCER")
print("=" * 80)

# Verificar que los archivos del modelo existen
if not os.path.exists('cancer_regression_model.pkl'):
    print("\n❌ Error: No se encontró 'cancer_regression_model.pkl'")
    print("   Primero ejecuta 'cancer_regression_model.py' para entrenar el modelo")
    exit(1)

if not os.path.exists('scaler.pkl'):
    print("\n❌ Error: No se encontró 'scaler.pkl'")
    print("   Primero ejecuta 'cancer_regression_model.py' para entrenar el modelo")
    exit(1)

# Cargar el modelo y el scaler
print("\n[1] Cargando modelo entrenado...")
model = joblib.load('cancer_regression_model.pkl')
scaler = joblib.load('scaler.pkl')
print("✓ Modelo y scaler cargados exitosamente")

# Ejemplo: Crear datos ficticios para demostración
# En un caso real, estos datos vendrían de un CSV o base de datos
print("\n[2] Preparando datos para predicción...")
print("    (Este es un ejemplo con datos ficticios)")

# IMPORTANTE: Los datos nuevos deben tener exactamente las mismas columnas
# que se usaron para entrenar el modelo, en el mismo orden.
#
# Para usar tus propios datos:
# 1. Carga tu dataset con pd.read_csv() o similar
# 2. Asegúrate de que tenga las mismas columnas que X_train
# 3. Aplica el mismo preprocesamiento (codificación, etc.)

# Ejemplo de datos nuevos (un solo condado/área)
# Estos valores son ilustrativos - reemplázalos con datos reales
ejemplo_datos = {
    'avganncount': [450.5],
    'avgdeathsperyear': [150.2],
    'incidencerate': [450.8],
    'medincome': [45000],
    'popest2015': [100000],
    'povertypercent': [15.5],
    'studypercap': [300.0],
    'binnedinc_encoded': [2],  # Si usaste Label Encoding
    'medianage': [38.5],
    'medianagemale': [37.2],
    'medianagefemale': [39.8],
    'percentmarried': [55.0],
    'pctnohs18_24': [12.5],
    'pcths18_24': [30.0],
    'pctsomecol18_24': [25.0],
    'pctbachdeg18_24': [10.0],
    'pcths25_over': [85.0],
    'pctbachdeg25_over': [22.0],
    'pctemployed16_over': [60.0],
    'pctunemployed16_over': [5.5],
    'pctprivatecoverage': [65.0],
    'pctprivatecoveragealone': [40.0],
    'pctempprivcoverage': [55.0],
    'pctpubliccoverage': [35.0],
    'pctpubliccoveragealone': [15.0],
    'pctwhite': [70.0],
    'pctblack': [15.0],
    'pctasian': [5.0],
    'pctotherrace': [10.0],
    'pctmarriedhouseholds': [50.0],
    'birthrate': [12.5]
}

# Crear DataFrame
nuevos_datos = pd.DataFrame(ejemplo_datos)

print(f"✓ Datos preparados: {nuevos_datos.shape[0]} muestra(s), {nuevos_datos.shape[1]} variables")

# NOTA IMPORTANTE:
# Si tu modelo fue entrenado con más o menos variables (por ejemplo, si se
# crearon columnas adicionales por One-Hot Encoding), debes ajustar esto.
# Puedes verificar las columnas necesarias con:
# print(scaler.feature_names_in_) si usaste scikit-learn >= 1.0

print("\n[3] Estandarizando datos...")
try:
    nuevos_datos_scaled = scaler.transform(nuevos_datos)
    print("✓ Datos estandarizados")
except ValueError as e:
    print(f"❌ Error al estandarizar: {e}")
    print("\n⚠️  Los datos nuevos deben tener exactamente las mismas columnas que el modelo entrenado")
    print("   Verifica que hayas aplicado el mismo preprocesamiento")
    exit(1)

# Hacer predicción
print("\n[4] Realizando predicción...")
prediccion = model.predict(nuevos_datos_scaled)
print("✓ Predicción completada")

# Mostrar resultados
print("\n" + "=" * 80)
print("RESULTADOS DE LA PREDICCIÓN")
print("=" * 80)

print(f"\n📊 Tasa de mortalidad predicha: {prediccion[0]:.2f}")
print("\nInterpretación:")
print(f"   El modelo predice una tasa de mortalidad de {prediccion[0]:.2f} muertes")
print("   por cada 100,000 habitantes para este condado/área.")

# Rangos de referencia (ajusta según tu dataset)
print("\n📈 Contexto (valores aproximados):")
print("   - Tasa baja: < 150")
print("   - Tasa media: 150-180")
print("   - Tasa alta: > 180")

if prediccion[0] < 150:
    nivel = "BAJA"
    emoji = "✓"
elif prediccion[0] < 180:
    nivel = "MEDIA"
    emoji = "⚠️"
else:
    nivel = "ALTA"
    emoji = "❌"

print(f"\n{emoji} La predicción indica una tasa de mortalidad {nivel}")

# Mostrar los datos de entrada
print("\n" + "=" * 80)
print("DATOS DE ENTRADA UTILIZADOS")
print("=" * 80)
print(nuevos_datos.T)

print("\n" + "=" * 80)
print("CÓMO USAR CON TUS PROPIOS DATOS")
print("=" * 80)
print("""
1. Prepara un CSV con las mismas columnas que el dataset de entrenamiento
2. Carga el CSV: datos = pd.read_csv('mis_datos.csv')
3. Aplica el mismo preprocesamiento que en el entrenamiento
4. Estandariza: datos_scaled = scaler.transform(datos)
5. Predice: predicciones = model.predict(datos_scaled)

Ejemplo de código:

    import pandas as pd
    import joblib

    # Cargar modelo
    model = joblib.load('cancer_regression_model.pkl')
    scaler = joblib.load('scaler.pkl')

    # Cargar tus datos
    mis_datos = pd.read_csv('datos_nuevos.csv')

    # Preprocesar (aplicar mismas transformaciones que en entrenamiento)
    # ... tu código de preprocesamiento aquí ...

    # Estandarizar
    mis_datos_scaled = scaler.transform(mis_datos)

    # Predecir
    predicciones = model.predict(mis_datos_scaled)

    # Guardar resultados
    mis_datos['prediccion_mortalidad'] = predicciones
    mis_datos.to_csv('predicciones.csv', index=False)
""")

print("=" * 80)
print("FIN")
print("=" * 80)
