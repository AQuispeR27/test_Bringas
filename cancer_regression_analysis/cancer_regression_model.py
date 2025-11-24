"""
Análisis de Regresión Lineal para Predicción de Tasa de Mortalidad por Cáncer
=============================================================================

Este script implementa un análisis completo de regresión lineal para predecir
la tasa de mortalidad por cáncer (target_deathrate) utilizando diversas
variables socioeconómicas y demográficas.

Autor: Análisis de Ciencia de Datos
Dataset: cancer_reg.csv
"""

# ==============================================================================
# 1. IMPORTACIÓN DE LIBRERÍAS
# ==============================================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import warnings

# Configuración
warnings.filterwarnings('ignore')
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

print("=" * 80)
print("ANÁLISIS DE REGRESIÓN LINEAL - MORTALIDAD POR CÁNCER")
print("=" * 80)

# ==============================================================================
# 2. CARGA DEL DATASET
# ==============================================================================

print("\n[1] CARGANDO DATASET...")
print("-" * 80)

try:
    df = pd.read_csv('cancer_reg.csv')
    print(f"✓ Dataset cargado exitosamente")
    print(f"  - Dimensiones: {df.shape[0]} filas × {df.shape[1]} columnas")
except FileNotFoundError:
    print("✗ ERROR: No se encontró el archivo 'cancer_reg.csv'")
    print("  Por favor, coloca el archivo en la misma carpeta que este script.")
    exit(1)

# ==============================================================================
# 3. EXPLORACIÓN INICIAL DEL DATASET
# ==============================================================================

print("\n[2] EXPLORACIÓN INICIAL DEL DATASET")
print("-" * 80)

# Vista previa de los datos
print("\n📊 Primeras 5 filas del dataset:")
print(df.head())

# Información general del dataset
print("\n📋 Información del dataset:")
print(df.info())

# Estadísticas descriptivas
print("\n📈 Estadísticas descriptivas:")
print(df.describe())

# Verificar valores nulos
print("\n🔍 Valores nulos por columna:")
null_counts = df.isnull().sum()
null_percentages = (null_counts / len(df)) * 100
null_info = pd.DataFrame({
    'Valores Nulos': null_counts,
    'Porcentaje (%)': null_percentages
})
print(null_info[null_info['Valores Nulos'] > 0])

# Verificar si existe la variable objetivo
if 'target_deathrate' not in df.columns:
    print("\n✗ ERROR: La columna 'target_deathrate' no existe en el dataset")
    exit(1)

print(f"\n✓ Variable objetivo 'target_deathrate' encontrada")
print(f"  - Rango: [{df['target_deathrate'].min():.2f}, {df['target_deathrate'].max():.2f}]")
print(f"  - Media: {df['target_deathrate'].mean():.2f}")
print(f"  - Mediana: {df['target_deathrate'].median():.2f}")

# ==============================================================================
# 4. LIMPIEZA Y PREPROCESAMIENTO DE DATOS
# ==============================================================================

print("\n[3] LIMPIEZA Y PREPROCESAMIENTO DE DATOS")
print("-" * 80)

# Crear una copia para no modificar el dataset original
df_processed = df.copy()

# Identificar columnas categóricas y numéricas
categorical_columns = df_processed.select_dtypes(include=['object']).columns.tolist()
numerical_columns = df_processed.select_dtypes(include=['int64', 'float64']).columns.tolist()

print(f"\n📊 Columnas categóricas encontradas: {len(categorical_columns)}")
if categorical_columns:
    print(f"   {categorical_columns}")

print(f"\n📊 Columnas numéricas encontradas: {len(numerical_columns)}")

# Eliminar columnas que no aportan al modelo (identificadores geográficos únicos)
# La columna 'geography' contiene demasiados valores únicos y es un identificador
columns_to_drop = []
if 'geography' in df_processed.columns:
    unique_count = df_processed['geography'].nunique()
    print(f"\n🗑️  Eliminando columna 'geography' ({unique_count} valores únicos - identificador)")
    columns_to_drop.append('geography')

if columns_to_drop:
    df_processed = df_processed.drop(columns=columns_to_drop)

# Actualizar lista de columnas categóricas
categorical_columns = [col for col in categorical_columns if col not in columns_to_drop]

# Tratamiento de valores nulos
print(f"\n🔧 Tratamiento de valores nulos:")
for column in df_processed.columns:
    null_count = df_processed[column].isnull().sum()
    if null_count > 0:
        if column in categorical_columns:
            # Para categóricas: imputar con la moda (valor más frecuente)
            mode_value = df_processed[column].mode()[0]
            df_processed[column].fillna(mode_value, inplace=True)
            print(f"   - {column}: {null_count} nulos → imputados con moda ('{mode_value}')")
        else:
            # Para numéricas: imputar con la mediana
            median_value = df_processed[column].median()
            df_processed[column].fillna(median_value, inplace=True)
            print(f"   - {column}: {null_count} nulos → imputados con mediana ({median_value:.2f})")

# Codificación de variables categóricas
if categorical_columns:
    print(f"\n🔄 Codificando variables categóricas:")
    # Para 'binnedinc' usamos Label Encoding ya que tiene orden implícito
    if 'binnedinc' in categorical_columns:
        le = LabelEncoder()
        df_processed['binnedinc_encoded'] = le.fit_transform(df_processed['binnedinc'])
        print(f"   - binnedinc → binnedinc_encoded (Label Encoding)")
        print(f"     Clases: {list(le.classes_)}")
        df_processed = df_processed.drop('binnedinc', axis=1)
        categorical_columns.remove('binnedinc')

    # Para otras categóricas, usar One-Hot Encoding
    if categorical_columns:
        df_processed = pd.get_dummies(df_processed, columns=categorical_columns, drop_first=True)
        print(f"   - Otras categóricas: One-Hot Encoding aplicado")

print(f"\n✓ Dataset preprocesado: {df_processed.shape[0]} filas × {df_processed.shape[1]} columnas")

# Verificar que no quedan valores nulos
remaining_nulls = df_processed.isnull().sum().sum()
if remaining_nulls == 0:
    print("✓ No quedan valores nulos en el dataset")
else:
    print(f"⚠️  Advertencia: Aún quedan {remaining_nulls} valores nulos")

# ==============================================================================
# 5. ANÁLISIS DE CORRELACIÓN Y SELECCIÓN DE VARIABLES
# ==============================================================================

print("\n[4] ANÁLISIS DE CORRELACIÓN Y SELECCIÓN DE VARIABLES")
print("-" * 80)

# Matriz de correlación con la variable objetivo
correlations = df_processed.corr()['target_deathrate'].sort_values(ascending=False)

print("\n📊 Top 15 variables más correlacionadas con 'target_deathrate':")
print(correlations.head(15))

print("\n📊 Top 10 variables menos correlacionadas (negativas) con 'target_deathrate':")
print(correlations.tail(10))

# Visualizar las correlaciones más importantes
plt.figure(figsize=(12, 8))
top_corr = correlations[1:21]  # Excluir la correlación consigo misma
colors = ['green' if x > 0 else 'red' for x in top_corr.values]
plt.barh(range(len(top_corr)), top_corr.values, color=colors)
plt.yticks(range(len(top_corr)), top_corr.index)
plt.xlabel('Correlación con target_deathrate')
plt.title('Top 20 Variables con Mayor Correlación Absoluta', fontsize=14, fontweight='bold')
plt.axvline(x=0, color='black', linestyle='--', linewidth=0.8)
plt.tight_layout()
plt.savefig('correlaciones_top20.png', dpi=300, bbox_inches='tight')
print("\n✓ Gráfico de correlaciones guardado: 'correlaciones_top20.png'")

# Matriz de correlación entre las variables más importantes
plt.figure(figsize=(14, 10))
top_features = correlations.abs().sort_values(ascending=False)[1:16].index.tolist()
top_features.append('target_deathrate')
correlation_matrix = df_processed[top_features].corr()

sns.heatmap(correlation_matrix, annot=True, fmt='.2f', cmap='coolwarm',
            center=0, square=True, linewidths=1, cbar_kws={"shrink": 0.8})
plt.title('Matriz de Correlación - Top 15 Variables', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('matriz_correlacion.png', dpi=300, bbox_inches='tight')
print("✓ Matriz de correlación guardada: 'matriz_correlacion.png'")

# Identificar variables con alta multicolinealidad (correlación > 0.9 entre sí)
print("\n⚠️  Pares de variables con alta multicolinealidad (|r| > 0.9):")
high_corr_pairs = []
for i in range(len(correlation_matrix.columns)):
    for j in range(i+1, len(correlation_matrix.columns)):
        if abs(correlation_matrix.iloc[i, j]) > 0.9:
            high_corr_pairs.append({
                'Variable 1': correlation_matrix.columns[i],
                'Variable 2': correlation_matrix.columns[j],
                'Correlación': correlation_matrix.iloc[i, j]
            })

if high_corr_pairs:
    for pair in high_corr_pairs:
        print(f"   - {pair['Variable 1']} ↔ {pair['Variable 2']}: {pair['Correlación']:.3f}")
else:
    print("   ✓ No se encontraron pares con multicolinealidad extrema")

# ==============================================================================
# 6. DIVISIÓN EN DATOS DE ENTRENAMIENTO Y PRUEBA
# ==============================================================================

print("\n[5] DIVISIÓN EN DATOS DE ENTRENAMIENTO Y PRUEBA")
print("-" * 80)

# Separar características (X) y variable objetivo (y)
X = df_processed.drop('target_deathrate', axis=1)
y = df_processed['target_deathrate']

print(f"\n📊 Características (X): {X.shape[1]} variables")
print(f"📊 Variable objetivo (y): target_deathrate")

# División 80% entrenamiento, 20% prueba
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print(f"\n✓ División completada:")
print(f"   - Conjunto de entrenamiento: {X_train.shape[0]} muestras ({X_train.shape[0]/len(df_processed)*100:.1f}%)")
print(f"   - Conjunto de prueba: {X_test.shape[0]} muestras ({X_test.shape[0]/len(df_processed)*100:.1f}%)")

# Estandarización de características (importante para regresión lineal)
print(f"\n🔧 Estandarizando características (StandardScaler)...")
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)
print("✓ Características estandarizadas (media=0, desviación estándar=1)")

# ==============================================================================
# 7. ENTRENAMIENTO DEL MODELO DE REGRESIÓN LINEAL
# ==============================================================================

print("\n[6] ENTRENAMIENTO DEL MODELO DE REGRESIÓN LINEAL")
print("-" * 80)

# Crear y entrenar el modelo
model = LinearRegression()
print("\n🎯 Entrenando modelo de Regresión Lineal...")
model.fit(X_train_scaled, y_train)
print("✓ Modelo entrenado exitosamente")

# Información del modelo
print(f"\n📊 Información del modelo:")
print(f"   - Intercepto: {model.intercept_:.4f}")
print(f"   - Número de coeficientes: {len(model.coef_)}")

# Variables más importantes (coeficientes más grandes en valor absoluto)
feature_importance = pd.DataFrame({
    'Variable': X.columns,
    'Coeficiente': model.coef_,
    'Importancia Absoluta': np.abs(model.coef_)
}).sort_values('Importancia Absoluta', ascending=False)

print(f"\n📊 Top 15 variables más importantes según coeficientes:")
print(feature_importance.head(15).to_string(index=False))

# Visualizar coeficientes
plt.figure(figsize=(12, 8))
top_15_features = feature_importance.head(15)
colors = ['green' if x > 0 else 'red' for x in top_15_features['Coeficiente'].values]
plt.barh(range(len(top_15_features)), top_15_features['Coeficiente'].values, color=colors)
plt.yticks(range(len(top_15_features)), top_15_features['Variable'].values)
plt.xlabel('Valor del Coeficiente')
plt.title('Top 15 Variables Más Importantes del Modelo', fontsize=14, fontweight='bold')
plt.axvline(x=0, color='black', linestyle='--', linewidth=0.8)
plt.tight_layout()
plt.savefig('coeficientes_modelo.png', dpi=300, bbox_inches='tight')
print("\n✓ Gráfico de coeficientes guardado: 'coeficientes_modelo.png'")

# ==============================================================================
# 8. EVALUACIÓN DEL MODELO
# ==============================================================================

print("\n[7] EVALUACIÓN DEL MODELO")
print("-" * 80)

# Predicciones
y_train_pred = model.predict(X_train_scaled)
y_test_pred = model.predict(X_test_scaled)

# Métricas de evaluación
print("\n📊 MÉTRICAS EN CONJUNTO DE ENTRENAMIENTO:")
train_mae = mean_absolute_error(y_train, y_train_pred)
train_mse = mean_squared_error(y_train, y_train_pred)
train_rmse = np.sqrt(train_mse)
train_r2 = r2_score(y_train, y_train_pred)

print(f"   - MAE (Error Absoluto Medio): {train_mae:.4f}")
print(f"   - MSE (Error Cuadrático Medio): {train_mse:.4f}")
print(f"   - RMSE (Raíz del Error Cuadrático Medio): {train_rmse:.4f}")
print(f"   - R² (Coeficiente de Determinación): {train_r2:.4f}")

print("\n📊 MÉTRICAS EN CONJUNTO DE PRUEBA:")
test_mae = mean_absolute_error(y_test, y_test_pred)
test_mse = mean_squared_error(y_test, y_test_pred)
test_rmse = np.sqrt(test_mse)
test_r2 = r2_score(y_test, y_test_pred)

print(f"   - MAE (Error Absoluto Medio): {test_mae:.4f}")
print(f"   - MSE (Error Cuadrático Medio): {test_mse:.4f}")
print(f"   - RMSE (Raíz del Error Cuadrático Medio): {test_rmse:.4f}")
print(f"   - R² (Coeficiente de Determinación): {test_r2:.4f}")

# Comparación
print("\n📊 COMPARACIÓN ENTRENAMIENTO vs PRUEBA:")
print(f"   - Diferencia en R²: {abs(train_r2 - test_r2):.4f}")
if abs(train_r2 - test_r2) < 0.05:
    print("   ✓ Modelo bien generalizado (diferencia < 0.05)")
elif abs(train_r2 - test_r2) < 0.10:
    print("   ⚠️  Modelo con ligero sobreajuste (diferencia < 0.10)")
else:
    print("   ⚠️  Modelo con sobreajuste significativo (diferencia ≥ 0.10)")

# ==============================================================================
# 9. VISUALIZACIÓN DE RESULTADOS
# ==============================================================================

print("\n[8] VISUALIZACIÓN DE RESULTADOS")
print("-" * 80)

# Crear figura con múltiples subgráficos
fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# 1. Valores reales vs predichos (Entrenamiento)
axes[0, 0].scatter(y_train, y_train_pred, alpha=0.5, s=20, edgecolors='k', linewidths=0.5)
axes[0, 0].plot([y_train.min(), y_train.max()], [y_train.min(), y_train.max()],
                'r--', lw=2, label='Predicción Perfecta')
axes[0, 0].set_xlabel('Valores Reales', fontsize=11)
axes[0, 0].set_ylabel('Valores Predichos', fontsize=11)
axes[0, 0].set_title(f'Entrenamiento: Reales vs Predichos (R² = {train_r2:.4f})',
                     fontsize=12, fontweight='bold')
axes[0, 0].legend()
axes[0, 0].grid(True, alpha=0.3)

# 2. Valores reales vs predichos (Prueba)
axes[0, 1].scatter(y_test, y_test_pred, alpha=0.5, s=20, color='orange',
                   edgecolors='k', linewidths=0.5)
axes[0, 1].plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()],
                'r--', lw=2, label='Predicción Perfecta')
axes[0, 1].set_xlabel('Valores Reales', fontsize=11)
axes[0, 1].set_ylabel('Valores Predichos', fontsize=11)
axes[0, 1].set_title(f'Prueba: Reales vs Predichos (R² = {test_r2:.4f})',
                     fontsize=12, fontweight='bold')
axes[0, 1].legend()
axes[0, 1].grid(True, alpha=0.3)

# 3. Distribución de residuos (Entrenamiento)
residuals_train = y_train - y_train_pred
axes[1, 0].hist(residuals_train, bins=50, edgecolor='black', alpha=0.7)
axes[1, 0].axvline(x=0, color='red', linestyle='--', linewidth=2)
axes[1, 0].set_xlabel('Residuos', fontsize=11)
axes[1, 0].set_ylabel('Frecuencia', fontsize=11)
axes[1, 0].set_title(f'Distribución de Residuos - Entrenamiento (Media: {residuals_train.mean():.4f})',
                     fontsize=12, fontweight='bold')
axes[1, 0].grid(True, alpha=0.3)

# 4. Distribución de residuos (Prueba)
residuals_test = y_test - y_test_pred
axes[1, 1].hist(residuals_test, bins=50, edgecolor='black', alpha=0.7, color='orange')
axes[1, 1].axvline(x=0, color='red', linestyle='--', linewidth=2)
axes[1, 1].set_xlabel('Residuos', fontsize=11)
axes[1, 1].set_ylabel('Frecuencia', fontsize=11)
axes[1, 1].set_title(f'Distribución de Residuos - Prueba (Media: {residuals_test.mean():.4f})',
                     fontsize=12, fontweight='bold')
axes[1, 1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('evaluacion_modelo.png', dpi=300, bbox_inches='tight')
print("✓ Gráficos de evaluación guardados: 'evaluacion_modelo.png'")

# Gráfico adicional: Residuos vs Valores Predichos
plt.figure(figsize=(14, 6))

plt.subplot(1, 2, 1)
plt.scatter(y_train_pred, residuals_train, alpha=0.5, s=20, edgecolors='k', linewidths=0.5)
plt.axhline(y=0, color='red', linestyle='--', linewidth=2)
plt.xlabel('Valores Predichos', fontsize=11)
plt.ylabel('Residuos', fontsize=11)
plt.title('Residuos vs Predichos - Entrenamiento', fontsize=12, fontweight='bold')
plt.grid(True, alpha=0.3)

plt.subplot(1, 2, 2)
plt.scatter(y_test_pred, residuals_test, alpha=0.5, s=20, color='orange',
            edgecolors='k', linewidths=0.5)
plt.axhline(y=0, color='red', linestyle='--', linewidth=2)
plt.xlabel('Valores Predichos', fontsize=11)
plt.ylabel('Residuos', fontsize=11)
plt.title('Residuos vs Predichos - Prueba', fontsize=12, fontweight='bold')
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('residuos_vs_predichos.png', dpi=300, bbox_inches='tight')
print("✓ Gráficos de residuos guardados: 'residuos_vs_predichos.png'")

# ==============================================================================
# 10. CONCLUSIONES Y SUGERENCIAS
# ==============================================================================

print("\n" + "=" * 80)
print("CONCLUSIONES Y RECOMENDACIONES")
print("=" * 80)

# Análisis de R²
print("\n📊 INTERPRETACIÓN DEL R²:")
if test_r2 >= 0.9:
    print(f"   ✓ EXCELENTE: El modelo explica el {test_r2*100:.2f}% de la varianza en los datos")
elif test_r2 >= 0.7:
    print(f"   ✓ BUENO: El modelo explica el {test_r2*100:.2f}% de la varianza en los datos")
elif test_r2 >= 0.5:
    print(f"   ⚠️  MODERADO: El modelo explica el {test_r2*100:.2f}% de la varianza en los datos")
else:
    print(f"   ⚠️  BAJO: El modelo solo explica el {test_r2*100:.2f}% de la varianza en los datos")

# Análisis de errores
print(f"\n📊 INTERPRETACIÓN DEL ERROR:")
mean_target = y_test.mean()
error_percentage = (test_mae / mean_target) * 100
print(f"   - Error absoluto medio (MAE): {test_mae:.4f}")
print(f"   - Media de target_deathrate: {mean_target:.4f}")
print(f"   - Error relativo: {error_percentage:.2f}%")

if error_percentage < 5:
    print("   ✓ Error muy bajo - predicciones muy precisas")
elif error_percentage < 10:
    print("   ✓ Error aceptable - predicciones razonablemente precisas")
else:
    print("   ⚠️  Error considerable - hay margen de mejora")

# Análisis de residuos
print(f"\n📊 ANÁLISIS DE RESIDUOS:")
print(f"   - Media de residuos (entrenamiento): {residuals_train.mean():.6f}")
print(f"   - Media de residuos (prueba): {residuals_test.mean():.6f}")
print(f"   - Desviación estándar (entrenamiento): {residuals_train.std():.4f}")
print(f"   - Desviación estándar (prueba): {residuals_test.std():.4f}")

if abs(residuals_test.mean()) < 1:
    print("   ✓ Los residuos están bien centrados en cero")
else:
    print("   ⚠️  Los residuos muestran sesgo")

# Sugerencias de mejora
print(f"\n💡 SUGERENCIAS PARA MEJORAR EL MODELO:")
print("\n1. INGENIERÍA DE CARACTERÍSTICAS:")
print("   - Crear interacciones entre variables importantes")
print("   - Aplicar transformaciones (log, sqrt, polinomiales) a variables asimétricas")
print("   - Crear ratios o proporciones entre variables relacionadas")

print("\n2. SELECCIÓN DE CARACTERÍSTICAS:")
print("   - Aplicar técnicas como RFE (Recursive Feature Elimination)")
print("   - Usar regularización (Ridge, Lasso) para reducir sobreajuste")
print("   - Eliminar características con alta multicolinealidad")

print("\n3. MODELOS ALTERNATIVOS:")
print("   - Regresión Ridge o Lasso (regularización)")
print("   - Regresión Polinomial")
print("   - Random Forest Regressor")
print("   - Gradient Boosting (XGBoost, LightGBM)")
print("   - Support Vector Regression (SVR)")

print("\n4. VALIDACIÓN Y OPTIMIZACIÓN:")
print("   - Implementar validación cruzada (k-fold cross-validation)")
print("   - Búsqueda de hiperparámetros con GridSearchCV")
print("   - Análisis de outliers y su impacto en el modelo")

print("\n5. ANÁLISIS ADICIONAL:")
print("   - Verificar supuestos de regresión lineal (linealidad, homocedasticidad, normalidad)")
print("   - Calcular VIF (Variance Inflation Factor) para detectar multicolinealidad")
print("   - Realizar análisis de influencia (Cook's distance)")

# Variables más importantes
print(f"\n🎯 TOP 5 VARIABLES MÁS INFLUYENTES EN EL MODELO:")
for i, row in feature_importance.head(5).iterrows():
    direction = "aumenta" if row['Coeficiente'] > 0 else "disminuye"
    print(f"   {i+1}. {row['Variable']}: Coef = {row['Coeficiente']:.4f} "
          f"({direction} la tasa de mortalidad)")

# Resumen final
print("\n" + "=" * 80)
print("RESUMEN FINAL")
print("=" * 80)
print(f"""
📊 Modelo: Regresión Lineal
📈 R² (Prueba): {test_r2:.4f}
📉 MAE (Prueba): {test_mae:.4f}
📉 RMSE (Prueba): {test_rmse:.4f}
🎯 Variables en el modelo: {X.shape[1]}
📦 Muestras de entrenamiento: {X_train.shape[0]}
📦 Muestras de prueba: {X_test.shape[0]}

✓ Análisis completado exitosamente
✓ Gráficos generados y guardados
✓ El modelo está listo para hacer predicciones
""")

print("=" * 80)
print("FIN DEL ANÁLISIS")
print("=" * 80)

# Guardar el modelo para uso futuro (opcional)
import joblib
joblib.dump(model, 'cancer_regression_model.pkl')
joblib.dump(scaler, 'scaler.pkl')
print("\n✓ Modelo guardado en: 'cancer_regression_model.pkl'")
print("✓ Scaler guardado en: 'scaler.pkl'")
print("\nPara cargar el modelo más tarde:")
print("   model = joblib.load('cancer_regression_model.pkl')")
print("   scaler = joblib.load('scaler.pkl')")
