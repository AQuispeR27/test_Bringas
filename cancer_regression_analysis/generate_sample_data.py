"""
Generador de Datos de Ejemplo para el Modelo de Regresión de Cáncer
====================================================================

Este script genera un dataset sintético similar a cancer_reg.csv para propósitos
de prueba y demostración. Los datos NO son reales, pero mantienen correlaciones
y distribuciones realistas para probar el modelo.

⚠️  IMPORTANTE: Esto es solo para propósitos de prueba. Para análisis real,
    utiliza el dataset original cancer_reg.csv con datos reales.
"""

import pandas as pd
import numpy as np

print("=" * 80)
print("GENERADOR DE DATOS DE EJEMPLO - CANCER_REG.CSV")
print("=" * 80)

# Configurar semilla para reproducibilidad
np.random.seed(42)

# Número de muestras (condados/áreas)
n_samples = 3000
print(f"\n[1] Generando {n_samples} muestras sintéticas...")

# ==============================================================================
# Generar variables base
# ==============================================================================

# Población
popest2015 = np.random.lognormal(mean=10, sigma=1.5, size=n_samples).astype(int)
popest2015 = np.clip(popest2015, 10000, 10000000)

# Edad mediana (influye en mortalidad)
medianage = np.random.normal(38, 5, n_samples)
medianage = np.clip(medianage, 25, 65)
medianagemale = medianage - np.random.uniform(0.5, 2, n_samples)
medianagefemale = medianage + np.random.uniform(0.5, 2, n_samples)

# Ingresos (correlacionado negativamente con mortalidad)
medincome = np.random.lognormal(mean=10.5, sigma=0.4, size=n_samples).astype(int)
medincome = np.clip(medincome, 20000, 150000)

# Pobreza (correlacionado con mortalidad)
povertypercent = 30 - (medincome - 20000) / 4000 + np.random.normal(0, 3, n_samples)
povertypercent = np.clip(povertypercent, 3, 45)

# Binned income (categórico basado en medincome)
binnedinc_bins = ['[20000, 35000)', '[35000, 45000)', '[45000, 60000)',
                   '[60000, 75000)', '[75000, 100000)', '[100000, 150000)']
binnedinc = pd.cut(medincome, bins=[20000, 35000, 45000, 60000, 75000, 100000, 150000],
                    labels=binnedinc_bins, include_lowest=True)

# Educación (correlacionada con ingresos y mortalidad)
education_factor = (medincome - 20000) / 130000

pctnohs18_24 = 30 - 25 * education_factor + np.random.normal(0, 3, n_samples)
pctnohs18_24 = np.clip(pctnohs18_24, 2, 50)

pcths18_24 = 35 + 15 * education_factor + np.random.normal(0, 3, n_samples)
pcths18_24 = np.clip(pcths18_24, 20, 60)

pctsomecol18_24 = 20 + 10 * education_factor + np.random.normal(0, 2, n_samples)
pctsomecol18_24 = np.clip(pctsomecol18_24, 10, 40)

pctbachdeg18_24 = 10 * education_factor + np.random.normal(0, 2, n_samples)
pctbachdeg18_24 = np.clip(pctbachdeg18_24, 1, 30)

pcths25_over = 75 + 15 * education_factor + np.random.normal(0, 3, n_samples)
pcths25_over = np.clip(pcths25_over, 60, 95)

pctbachdeg25_over = 15 + 20 * education_factor + np.random.normal(0, 3, n_samples)
pctbachdeg25_over = np.clip(pctbachdeg25_over, 5, 50)

studypercap = 100 + 500 * education_factor + np.random.normal(0, 50, n_samples)
studypercap = np.clip(studypercap, 50, 800)

# Empleo (correlacionado con economía)
pctemployed16_over = 50 + 15 * education_factor + np.random.normal(0, 3, n_samples)
pctemployed16_over = np.clip(pctemployed16_over, 40, 75)

pctunemployed16_over = 12 - 8 * education_factor + np.random.normal(0, 1.5, n_samples)
pctunemployed16_over = np.clip(pctunemployed16_over, 2, 20)

# Seguro de salud
pctprivatecoverage = 50 + 30 * education_factor + np.random.normal(0, 5, n_samples)
pctprivatecoverage = np.clip(pctprivatecoverage, 30, 85)

pctprivatecoveragealone = pctprivatecoverage * 0.6 + np.random.normal(0, 3, n_samples)
pctprivatecoveragealone = np.clip(pctprivatecoveragealone, 20, 60)

pctempprivcoverage = pctprivatecoverage * 0.8 + np.random.normal(0, 3, n_samples)
pctempprivcoverage = np.clip(pctempprivcoverage, 25, 75)

pctpubliccoverage = 45 - 20 * education_factor + np.random.normal(0, 5, n_samples)
pctpubliccoverage = np.clip(pctpubliccoverage, 15, 70)

pctpubliccoveragealone = pctpubliccoverage * 0.5 + np.random.normal(0, 3, n_samples)
pctpubliccoveragealone = np.clip(pctpubliccoveragealone, 5, 40)

# Demografía racial
pctwhite = np.random.beta(6, 2, n_samples) * 100
pctblack = np.random.beta(2, 6, n_samples) * 100
pctasian = np.random.beta(1.5, 10, n_samples) * 100
pctotherrace = 100 - pctwhite - pctblack - pctasian
pctotherrace = np.clip(pctotherrace, 0, 30)

# Estado civil
percentmarried = 45 + 15 * education_factor + np.random.normal(0, 5, n_samples)
percentmarried = np.clip(percentmarried, 30, 70)

pctmarriedhouseholds = percentmarried * 0.9 + np.random.normal(0, 3, n_samples)
pctmarriedhouseholds = np.clip(pctmarriedhouseholds, 25, 65)

# Tasa de natalidad
birthrate = 14 - 4 * education_factor + 0.1 * (medianage - 38) + np.random.normal(0, 1.5, n_samples)
birthrate = np.clip(birthrate, 5, 20)

# ==============================================================================
# Variables relacionadas con cáncer
# ==============================================================================

# Tasa de incidencia (casos nuevos por 100,000)
# Correlacionada con edad y otros factores
incidencerate = 400 + 5 * (medianage - 38) + np.random.normal(0, 30, n_samples)
incidencerate = np.clip(incidencerate, 300, 600)

# Promedio anual de casos (basado en población e incidencia)
avganncount = (popest2015 / 100000) * incidencerate + np.random.normal(0, 50, n_samples)
avganncount = np.clip(avganncount, 10, 5000)

# ==============================================================================
# VARIABLE OBJETIVO: target_deathrate
# ==============================================================================

# Tasa de mortalidad (lo que queremos predecir)
# Influenciada por múltiples factores:
# - Edad (+): Mayor edad, mayor mortalidad
# - Pobreza (+): Mayor pobreza, mayor mortalidad
# - Educación (-): Mayor educación, menor mortalidad
# - Seguro privado (-): Más seguro privado, menor mortalidad
# - Incidencia (+): Mayor incidencia, mayor mortalidad

target_deathrate = (
    120 +  # Base
    2 * (medianage - 38) +  # Efecto de edad
    0.8 * povertypercent +  # Efecto de pobreza
    -0.015 * (medincome - 50000) +  # Efecto de ingresos
    -0.5 * pctbachdeg25_over +  # Efecto de educación
    -0.3 * pctprivatecoverage +  # Efecto de seguro privado
    0.15 * incidencerate +  # Efecto de incidencia
    np.random.normal(0, 10, n_samples)  # Ruido
)
target_deathrate = np.clip(target_deathrate, 50, 300)

# Promedio anual de muertes (basado en población y tasa de mortalidad)
avgdeathsperyear = (popest2015 / 100000) * target_deathrate + np.random.normal(0, 20, n_samples)
avgdeathsperyear = np.clip(avgdeathsperyear, 5, 2000)

# ==============================================================================
# Crear geografías ficticias
# ==============================================================================

states = ['California', 'Texas', 'Florida', 'New York', 'Pennsylvania',
          'Illinois', 'Ohio', 'Georgia', 'North Carolina', 'Michigan']
counties = ['County ' + str(i) for i in range(1, 301)]

geography = []
for i in range(n_samples):
    state = np.random.choice(states)
    county = np.random.choice(counties)
    geography.append(f"{county}, {state}")

# ==============================================================================
# Crear DataFrame
# ==============================================================================

print("\n[2] Creando DataFrame...")

df = pd.DataFrame({
    'avganncount': avganncount,
    'avgdeathsperyear': avgdeathsperyear,
    'target_deathrate': target_deathrate,
    'incidencerate': incidencerate,
    'medincome': medincome,
    'popest2015': popest2015,
    'povertypercent': povertypercent,
    'studypercap': studypercap,
    'binnedinc': binnedinc,
    'medianage': medianage,
    'medianagemale': medianagemale,
    'medianagefemale': medianagefemale,
    'geography': geography,
    'percentmarried': percentmarried,
    'pctnohs18_24': pctnohs18_24,
    'pcths18_24': pcths18_24,
    'pctsomecol18_24': pctsomecol18_24,
    'pctbachdeg18_24': pctbachdeg18_24,
    'pcths25_over': pcths25_over,
    'pctbachdeg25_over': pctbachdeg25_over,
    'pctemployed16_over': pctemployed16_over,
    'pctunemployed16_over': pctunemployed16_over,
    'pctprivatecoverage': pctprivatecoverage,
    'pctprivatecoveragealone': pctprivatecoveragealone,
    'pctempprivcoverage': pctempprivcoverage,
    'pctpubliccoverage': pctpubliccoverage,
    'pctpubliccoveragealone': pctpubliccoveragealone,
    'pctwhite': pctwhite,
    'pctblack': pctblack,
    'pctasian': pctasian,
    'pctotherrace': pctotherrace,
    'pctmarriedhouseholds': pctmarriedhouseholds,
    'birthrate': birthrate
})

# Introducir algunos valores nulos aleatoriamente (5% de los datos)
print("\n[3] Introduciendo valores nulos aleatorios (para simular datos reales)...")
null_columns = ['povertypercent', 'pctprivatecoverage', 'pctemployed16_over',
                'pcths25_over', 'pctbachdeg25_over']
for col in null_columns:
    null_indices = np.random.choice(df.index, size=int(len(df) * 0.05), replace=False)
    df.loc[null_indices, col] = np.nan

print(f"✓ Valores nulos introducidos en {len(null_columns)} columnas")

# ==============================================================================
# Guardar CSV
# ==============================================================================

print("\n[4] Guardando archivo CSV...")
df.to_csv('cancer_reg.csv', index=False)
print("✓ Archivo guardado: 'cancer_reg.csv'")

# ==============================================================================
# Resumen
# ==============================================================================

print("\n" + "=" * 80)
print("RESUMEN DEL DATASET GENERADO")
print("=" * 80)

print(f"\n📊 Dimensiones: {df.shape[0]} filas × {df.shape[1]} columnas")
print(f"\n📊 Estadísticas de la variable objetivo (target_deathrate):")
print(f"   - Media: {df['target_deathrate'].mean():.2f}")
print(f"   - Mediana: {df['target_deathrate'].median():.2f}")
print(f"   - Desviación estándar: {df['target_deathrate'].std():.2f}")
print(f"   - Mínimo: {df['target_deathrate'].min():.2f}")
print(f"   - Máximo: {df['target_deathrate'].max():.2f}")

print(f"\n📊 Valores nulos totales: {df.isnull().sum().sum()}")

print("\n📊 Primeras 5 filas:")
print(df.head())

print("\n" + "=" * 80)
print("⚠️  RECORDATORIO")
print("=" * 80)
print("""
Este es un dataset SINTÉTICO generado para propósitos de PRUEBA y DEMOSTRACIÓN.
Los datos NO son reales y NO deben usarse para análisis médico o investigación real.

Para análisis real de mortalidad por cáncer, utiliza el dataset original
cancer_reg.csv con datos reales de fuentes oficiales.

Ahora puedes ejecutar el análisis con:
    python cancer_regression_model.py
""")

print("=" * 80)
print("✓ GENERACIÓN COMPLETADA")
print("=" * 80)
