"""
Ingeniería de Características para el Modelo de Regresión de Cáncer
====================================================================

Este script implementa técnicas avanzadas de ingeniería de características:
1. Creación de interacciones entre variables importantes
2. Transformaciones (log, sqrt, polinomiales) para variables asimétricas
3. Creación de ratios y proporciones entre variables relacionadas

Autor: Análisis Avanzado de Ciencia de Datos
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import PolynomialFeatures
from scipy import stats
import warnings

warnings.filterwarnings('ignore')

print("=" * 80)
print("INGENIERÍA DE CARACTERÍSTICAS - MODELO DE REGRESIÓN DE CÁNCER")
print("=" * 80)

# ==============================================================================
# 1. CARGAR DATOS
# ==============================================================================

print("\n[1] CARGANDO DATASET...")
print("-" * 80)

try:
    df = pd.read_csv('cancer_reg.csv')
    print(f"✓ Dataset cargado: {df.shape[0]} filas × {df.shape[1]} columnas")
except FileNotFoundError:
    print("❌ Error: No se encontró 'cancer_reg.csv'")
    print("   Ejecuta primero 'generate_sample_data.py' o coloca el archivo en la carpeta")
    exit(1)

# Crear copia para trabajar
df_original = df.copy()

# ==============================================================================
# 2. ANÁLISIS DE ASIMETRÍA (SKEWNESS)
# ==============================================================================

print("\n[2] ANÁLISIS DE ASIMETRÍA DE VARIABLES NUMÉRICAS")
print("-" * 80)

# Obtener solo columnas numéricas
numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()

# Calcular skewness para cada variable
skewness_data = []
for col in numeric_cols:
    skew = df[col].skew()
    skewness_data.append({
        'Variable': col,
        'Asimetría (Skewness)': skew,
        'Asimetría Abs': abs(skew)
    })

skewness_df = pd.DataFrame(skewness_data).sort_values('Asimetría Abs', ascending=False)

print("\n📊 Variables con mayor asimetría (|skewness| > 0.5):")
high_skew = skewness_df[skewness_df['Asimetría Abs'] > 0.5]
print(high_skew.to_string(index=False))

# Visualizar asimetría
plt.figure(figsize=(14, 6))
top_skew = skewness_df.head(15)
colors = ['red' if abs(x) > 1 else 'orange' if abs(x) > 0.5 else 'green'
          for x in top_skew['Asimetría (Skewness)'].values]
plt.barh(range(len(top_skew)), top_skew['Asimetría (Skewness)'].values, color=colors)
plt.yticks(range(len(top_skew)), top_skew['Variable'].values)
plt.xlabel('Asimetría (Skewness)', fontsize=12)
plt.title('Top 15 Variables por Asimetría', fontsize=14, fontweight='bold')
plt.axvline(x=0, color='black', linestyle='--', linewidth=1)
plt.axvline(x=1, color='red', linestyle=':', linewidth=1, alpha=0.5, label='|skew| = 1')
plt.axvline(x=-1, color='red', linestyle=':', linewidth=1, alpha=0.5)
plt.legend()
plt.tight_layout()
plt.savefig('analisis_asimetria.png', dpi=300, bbox_inches='tight')
print("\n✓ Gráfico guardado: 'analisis_asimetria.png'")

# ==============================================================================
# 3. APLICAR TRANSFORMACIONES A VARIABLES ASIMÉTRICAS
# ==============================================================================

print("\n[3] APLICANDO TRANSFORMACIONES A VARIABLES ASIMÉTRICAS")
print("-" * 80)

# Variables a transformar (con alta asimetría)
# Excluir la variable objetivo del dataset
vars_to_transform = high_skew['Variable'].tolist()
if 'target_deathrate' in vars_to_transform:
    vars_to_transform.remove('target_deathrate')

transformations_applied = []

for col in vars_to_transform[:10]:  # Transformar las 10 más asimétricas
    if df[col].min() > 0:  # Solo si todos los valores son positivos
        # Aplicar transformación logarítmica
        df[f'{col}_log'] = np.log1p(df[col])  # log1p = log(1 + x)
        transformations_applied.append(f"{col} → {col}_log (logarítmica)")

        # Aplicar transformación de raíz cuadrada
        df[f'{col}_sqrt'] = np.sqrt(df[col])
        transformations_applied.append(f"{col} → {col}_sqrt (raíz cuadrada)")
    elif df[col].min() >= 0:  # Si hay ceros
        # Solo raíz cuadrada
        df[f'{col}_sqrt'] = np.sqrt(df[col])
        transformations_applied.append(f"{col} → {col}_sqrt (raíz cuadrada)")

print(f"\n✓ Transformaciones aplicadas ({len(transformations_applied)}):")
for transform in transformations_applied[:15]:  # Mostrar primeras 15
    print(f"   - {transform}")
if len(transformations_applied) > 15:
    print(f"   ... y {len(transformations_applied) - 15} más")

# Comparar distribuciones antes y después
print("\n📊 Generando comparación de distribuciones...")
fig, axes = plt.subplots(3, 2, figsize=(15, 12))
axes = axes.ravel()

comparison_vars = vars_to_transform[:3]  # Comparar 3 variables
for idx, col in enumerate(comparison_vars):
    # Original
    axes[idx*2].hist(df[col].dropna(), bins=50, edgecolor='black', alpha=0.7)
    axes[idx*2].set_title(f'{col} (Original)\nSkewness: {df[col].skew():.2f}',
                          fontweight='bold')
    axes[idx*2].set_ylabel('Frecuencia')
    axes[idx*2].grid(True, alpha=0.3)

    # Transformada
    if f'{col}_log' in df.columns:
        trans_col = f'{col}_log'
        trans_name = 'Log'
    elif f'{col}_sqrt' in df.columns:
        trans_col = f'{col}_sqrt'
        trans_name = 'Sqrt'
    else:
        continue

    axes[idx*2+1].hist(df[trans_col].dropna(), bins=50, edgecolor='black',
                       alpha=0.7, color='orange')
    axes[idx*2+1].set_title(f'{trans_col} ({trans_name})\nSkewness: {df[trans_col].skew():.2f}',
                           fontweight='bold')
    axes[idx*2+1].set_ylabel('Frecuencia')
    axes[idx*2+1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('transformaciones_comparacion.png', dpi=300, bbox_inches='tight')
print("✓ Gráfico guardado: 'transformaciones_comparacion.png'")

# ==============================================================================
# 4. CREAR RATIOS Y PROPORCIONES
# ==============================================================================

print("\n[4] CREANDO RATIOS Y PROPORCIONES ENTRE VARIABLES RELACIONADAS")
print("-" * 80)

ratios_created = []

# Ratios de salud y cáncer
if 'avgdeathsperyear' in df.columns and 'avganncount' in df.columns:
    df['mortality_rate_ratio'] = df['avgdeathsperyear'] / (df['avganncount'] + 1)
    ratios_created.append('mortality_rate_ratio = avgdeathsperyear / avganncount')

if 'avganncount' in df.columns and 'popest2015' in df.columns:
    df['cancer_cases_per_capita'] = df['avganncount'] / (df['popest2015'] / 100000)
    ratios_created.append('cancer_cases_per_capita = avganncount / (popest2015/100k)')

# Ratios de educación
if 'pctbachdeg25_over' in df.columns and 'pcths25_over' in df.columns:
    df['education_ratio'] = df['pctbachdeg25_over'] / (df['pcths25_over'] + 1)
    ratios_created.append('education_ratio = pctbachdeg25_over / pcths25_over')

# Ratios de empleo
if 'pctemployed16_over' in df.columns and 'pctunemployed16_over' in df.columns:
    df['employment_ratio'] = df['pctemployed16_over'] / (df['pctunemployed16_over'] + 1)
    ratios_created.append('employment_ratio = pctemployed16_over / pctunemployed16_over')

# Ratios de cobertura de seguro
if 'pctprivatecoverage' in df.columns and 'pctpubliccoverage' in df.columns:
    df['insurance_ratio'] = df['pctprivatecoverage'] / (df['pctpubliccoverage'] + 1)
    ratios_created.append('insurance_ratio = pctprivatecoverage / pctpubliccoverage')

# Ratio de pobreza vs ingreso
if 'povertypercent' in df.columns and 'medincome' in df.columns:
    df['poverty_income_ratio'] = df['povertypercent'] * 1000 / (df['medincome'] + 1)
    ratios_created.append('poverty_income_ratio = povertypercent / medincome')

# Índice demográfico
if all(col in df.columns for col in ['medianage', 'birthrate']):
    df['age_birth_ratio'] = df['medianage'] / (df['birthrate'] + 1)
    ratios_created.append('age_birth_ratio = medianage / birthrate')

# Índice de diversidad racial (entropía simplificada)
race_cols = ['pctwhite', 'pctblack', 'pctasian', 'pctotherrace']
if all(col in df.columns for col in race_cols):
    # Normalizar para que sumen 100
    race_sum = df[race_cols].sum(axis=1)
    race_normalized = df[race_cols].div(race_sum, axis=0)
    # Calcular índice de diversidad (1 - suma de cuadrados)
    df['racial_diversity_index'] = 1 - (race_normalized ** 2).sum(axis=1)
    ratios_created.append('racial_diversity_index = diversidad racial (Herfindahl)')

print(f"\n✓ Ratios y proporciones creados ({len(ratios_created)}):")
for ratio in ratios_created:
    print(f"   - {ratio}")

# ==============================================================================
# 5. CREAR INTERACCIONES ENTRE VARIABLES IMPORTANTES
# ==============================================================================

print("\n[5] CREANDO INTERACCIONES ENTRE VARIABLES IMPORTANTES")
print("-" * 80)

# Primero identificar las variables más correlacionadas con target
if 'target_deathrate' in df.columns:
    correlations = df.corr()['target_deathrate'].abs().sort_values(ascending=False)
    top_features = correlations[1:11].index.tolist()  # Top 10 (excluyendo target)

    print(f"\n📊 Top 10 variables más correlacionadas con target_deathrate:")
    for i, feat in enumerate(top_features, 1):
        print(f"   {i}. {feat}: {correlations[feat]:.4f}")

    # Crear interacciones entre pares de las variables más importantes
    interactions_created = []

    # Interacciones específicas basadas en conocimiento del dominio
    interaction_pairs = [
        ('povertypercent', 'medincome', 'poverty_income_interaction'),
        ('medianage', 'incidencerate', 'age_incidence_interaction'),
        ('pctpubliccoverage', 'povertypercent', 'public_insurance_poverty'),
        ('pctbachdeg25_over', 'medincome', 'education_income_interaction'),
        ('pctunemployed16_over', 'povertypercent', 'unemployment_poverty'),
    ]

    for var1, var2, name in interaction_pairs:
        if var1 in df.columns and var2 in df.columns:
            df[name] = df[var1] * df[var2]
            interactions_created.append(f"{name} = {var1} × {var2}")

    # Interacciones cuadráticas para variables muy importantes
    quadratic_vars = top_features[:5]
    for var in quadratic_vars:
        if var in df.columns and df[var].dtype in ['int64', 'float64']:
            df[f'{var}_squared'] = df[var] ** 2
            interactions_created.append(f"{var}_squared = {var}²")

    print(f"\n✓ Interacciones creadas ({len(interactions_created)}):")
    for interaction in interactions_created:
        print(f"   - {interaction}")

# ==============================================================================
# 6. CARACTERÍSTICAS POLINOMIALES (TOP VARIABLES)
# ==============================================================================

print("\n[6] CREANDO CARACTERÍSTICAS POLINOMIALES")
print("-" * 80)

# Seleccionar las 5 variables más importantes para features polinomiales
if 'target_deathrate' in df.columns:
    poly_features = top_features[:5]

    print(f"\n📊 Creando características polinomiales (grado 2) para:")
    for feat in poly_features:
        print(f"   - {feat}")

    # Preparar datos para PolynomialFeatures
    poly_data = df[poly_features].copy()

    # Imputar valores nulos si existen
    poly_data = poly_data.fillna(poly_data.median())

    # Crear características polinomiales
    poly = PolynomialFeatures(degree=2, include_bias=False, interaction_only=False)
    poly_features_array = poly.fit_transform(poly_data)

    # Obtener nombres de las nuevas características
    poly_feature_names = poly.get_feature_names_out(poly_features)

    # Crear DataFrame con las nuevas características
    poly_df = pd.DataFrame(poly_features_array, columns=poly_feature_names, index=df.index)

    # Agregar solo las nuevas características (no las originales)
    original_cols = set(poly_features)
    new_poly_cols = [col for col in poly_df.columns if col not in original_cols]

    for col in new_poly_cols:
        df[f'poly_{col}'] = poly_df[col]

    print(f"\n✓ {len(new_poly_cols)} características polinomiales agregadas")
    print(f"   Ejemplos: {new_poly_cols[:5]}")

# ==============================================================================
# 7. RESUMEN Y EXPORTACIÓN
# ==============================================================================

print("\n[7] RESUMEN DE INGENIERÍA DE CARACTERÍSTICAS")
print("-" * 80)

original_features = df_original.shape[1]
new_features = df.shape[1]
features_added = new_features - original_features

print(f"\n📊 ESTADÍSTICAS:")
print(f"   - Características originales: {original_features}")
print(f"   - Características nuevas: {features_added}")
print(f"   - Total de características: {new_features}")
print(f"   - Incremento: {(features_added/original_features)*100:.1f}%")

print(f"\n📊 DESGLOSE:")
print(f"   - Transformaciones (log, sqrt): {len(transformations_applied)}")
print(f"   - Ratios y proporciones: {len(ratios_created)}")
print(f"   - Interacciones: {len(interactions_created) if 'interactions_created' in locals() else 0}")
print(f"   - Características polinomiales: {len(new_poly_cols) if 'new_poly_cols' in locals() else 0}")

# Guardar dataset con nuevas características
output_file = 'cancer_reg_engineered.csv'
df.to_csv(output_file, index=False)
print(f"\n✓ Dataset con características mejoradas guardado: '{output_file}'")

# Analizar correlación de nuevas características con target
if 'target_deathrate' in df.columns:
    print("\n[8] ANÁLISIS DE CORRELACIÓN DE NUEVAS CARACTERÍSTICAS")
    print("-" * 80)

    # Obtener solo las nuevas características
    new_cols = [col for col in df.columns if col not in df_original.columns]

    if new_cols:
        new_correlations = df[new_cols + ['target_deathrate']].corr()['target_deathrate'].abs()
        new_correlations = new_correlations.drop('target_deathrate').sort_values(ascending=False)

        print(f"\n📊 Top 15 nuevas características por correlación con target:")
        print(new_correlations.head(15))

        # Visualizar
        plt.figure(figsize=(12, 8))
        top_new_corr = new_correlations.head(20)
        plt.barh(range(len(top_new_corr)), top_new_corr.values, color='green', alpha=0.7)
        plt.yticks(range(len(top_new_corr)), top_new_corr.index)
        plt.xlabel('Correlación Absoluta con target_deathrate', fontsize=12)
        plt.title('Top 20 Nuevas Características por Correlación', fontsize=14, fontweight='bold')
        plt.tight_layout()
        plt.savefig('nuevas_caracteristicas_correlacion.png', dpi=300, bbox_inches='tight')
        print("\n✓ Gráfico guardado: 'nuevas_caracteristicas_correlacion.png'")

# ==============================================================================
# 9. RECOMENDACIONES
# ==============================================================================

print("\n" + "=" * 80)
print("RECOMENDACIONES")
print("=" * 80)

print("""
✓ CARACTERÍSTICAS CREADAS EXITOSAMENTE

📊 PRÓXIMOS PASOS:

1. Usar 'cancer_reg_engineered.csv' en lugar del dataset original
2. Aplicar selección de características para eliminar redundancias
3. Entrenar el modelo con las nuevas características
4. Comparar el R² con el modelo base

💡 CONSEJOS:

- No todas las características mejorarán el modelo
- Usa RFE o Lasso para seleccionar las mejores
- Verifica VIF para evitar multicolinealidad extrema
- Considera usar regularización (Ridge/Lasso)

⚠️  PRECAUCIONES:

- Más características ≠ mejor modelo (curse of dimensionality)
- Riesgo de sobreajuste si no se usa regularización
- Aumenta el tiempo de entrenamiento
- Aplica la misma ingeniería a datos nuevos
""")

print("=" * 80)
print("FIN DEL ANÁLISIS DE INGENIERÍA DE CARACTERÍSTICAS")
print("=" * 80)
