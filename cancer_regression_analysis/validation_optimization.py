"""
Validación y Optimización para el Modelo de Regresión de Cáncer
================================================================

Este script implementa:
1. Validación cruzada (K-Fold Cross-Validation)
2. Búsqueda de hiperparámetros con GridSearchCV
3. Análisis de outliers y su impacto
4. Comparación de modelos alternativos

Autor: Análisis Avanzado de Ciencia de Datos
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import (train_test_split, cross_val_score,
                                      KFold, GridSearchCV)
from sklearn.preprocessing import StandardScaler, RobustScaler
from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import (r2_score, mean_absolute_error, mean_squared_error,
                              make_scorer)
from scipy import stats
import warnings

warnings.filterwarnings('ignore')

print("=" * 80)
print("VALIDACIÓN Y OPTIMIZACIÓN - MODELO DE REGRESIÓN DE CÁNCER")
print("=" * 80)

# ==============================================================================
# 1. CARGAR DATOS
# ==============================================================================

print("\n[1] CARGANDO DATASET...")
print("-" * 80)

# Intentar cargar datasets en orden de preferencia
datasets_to_try = [
    ('cancer_reg_selected_features.csv', 'con características seleccionadas'),
    ('cancer_reg_engineered.csv', 'con características mejoradas'),
    ('cancer_reg.csv', 'original')
]

df = None
dataset_used = None

for filename, description in datasets_to_try:
    try:
        df = pd.read_csv(filename)
        dataset_used = description
        print(f"✓ Dataset {description} cargado: '{filename}'")
        break
    except FileNotFoundError:
        continue

if df is None:
    print("❌ Error: No se encontró ningún dataset")
    exit(1)

print(f"   Dimensiones: {df.shape[0]} filas × {df.shape[1]} columnas")

# ==============================================================================
# 2. PREPROCESAMIENTO
# ==============================================================================

print("\n[2] PREPROCESAMIENTO DE DATOS")
print("-" * 80)

# Eliminar columnas categóricas
categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
if categorical_cols:
    print(f"🗑️  Eliminando columnas categóricas: {categorical_cols}")
    df = df.drop(columns=categorical_cols)

# Verificar variable objetivo
if 'target_deathrate' not in df.columns:
    print("❌ Error: No se encontró 'target_deathrate'")
    exit(1)

# Separar X y y
X = df.drop('target_deathrate', axis=1)
y = df['target_deathrate']

# Imputar valores nulos
X = X.fillna(X.median())

print(f"✓ Características: {X.shape[1]}")
print(f"✓ Muestras: {X.shape[0]}")

# ==============================================================================
# 3. DETECCIÓN Y ANÁLISIS DE OUTLIERS
# ==============================================================================

print("\n[3] DETECCIÓN Y ANÁLISIS DE OUTLIERS")
print("-" * 80)

# Detectar outliers usando Z-score
print("\n🔍 Detectando outliers usando Z-score (|z| > 3)...")

z_scores = np.abs(stats.zscore(X, nan_policy='omit'))
outlier_mask = (z_scores > 3).any(axis=1)
n_outliers = outlier_mask.sum()
outlier_percentage = (n_outliers / len(X)) * 100

print(f"\n📊 OUTLIERS DETECTADOS:")
print(f"   - Número de outliers: {n_outliers} ({outlier_percentage:.2f}%)")
print(f"   - Muestras limpias: {len(X) - n_outliers} ({100-outlier_percentage:.2f}%)")

# Analizar impacto de outliers
print("\n📊 Comparando estadísticas con/sin outliers:")
stats_comparison = pd.DataFrame({
    'Con outliers': [y.mean(), y.median(), y.std(), y.min(), y.max()],
    'Sin outliers': [y[~outlier_mask].mean(), y[~outlier_mask].median(),
                     y[~outlier_mask].std(), y[~outlier_mask].min(),
                     y[~outlier_mask].max()]
}, index=['Media', 'Mediana', 'Desv. Est.', 'Mínimo', 'Máximo'])

print(stats_comparison)

# Visualizar outliers
fig, axes = plt.subplots(1, 2, figsize=(15, 5))

# Boxplot de target
axes[0].boxplot([y, y[~outlier_mask]], labels=['Con outliers', 'Sin outliers'])
axes[0].set_ylabel('target_deathrate', fontsize=12)
axes[0].set_title('Distribución de Variable Objetivo', fontsize=14, fontweight='bold')
axes[0].grid(True, alpha=0.3, axis='y')

# Scatter de outliers
axes[1].scatter(range(len(y)), y, c=outlier_mask, cmap='RdYlGn_r',
                alpha=0.6, s=20, edgecolors='k', linewidth=0.3)
axes[1].set_xlabel('Índice de muestra', fontsize=12)
axes[1].set_ylabel('target_deathrate', fontsize=12)
axes[1].set_title(f'Identificación de Outliers ({n_outliers} detectados)',
                  fontsize=14, fontweight='bold')
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('analisis_outliers.png', dpi=300, bbox_inches='tight')
print("\n✓ Gráfico guardado: 'analisis_outliers.png'")

# Crear datasets con y sin outliers
X_no_outliers = X[~outlier_mask]
y_no_outliers = y[~outlier_mask]

# ==============================================================================
# 4. VALIDACIÓN CRUZADA K-FOLD
# ==============================================================================

print("\n[4] VALIDACIÓN CRUZADA K-FOLD")
print("-" * 80)

# Configurar K-Fold
k_folds = 5
kfold = KFold(n_splits=k_folds, shuffle=True, random_state=42)

print(f"\n🎯 Ejecutando validación cruzada con {k_folds} folds...")

# Modelos a evaluar
models = {
    'Linear Regression': LinearRegression(),
    'Ridge': Ridge(alpha=1.0),
    'Lasso': Lasso(alpha=0.1, max_iter=10000),
    'ElasticNet': ElasticNet(alpha=0.1, l1_ratio=0.5, max_iter=10000)
}

# Métricas
scoring = {
    'r2': 'r2',
    'mae': 'neg_mean_absolute_error',
    'rmse': 'neg_root_mean_squared_error'
}

cv_results = []

# Estandarizar datos
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

for model_name, model in models.items():
    print(f"\n   Evaluando {model_name}...")

    # R²
    r2_scores = cross_val_score(model, X_scaled, y, cv=kfold, scoring='r2')
    # MAE (negativo, por eso multiplicamos por -1)
    mae_scores = -cross_val_score(model, X_scaled, y, cv=kfold,
                                   scoring='neg_mean_absolute_error')
    # RMSE
    rmse_scores = -cross_val_score(model, X_scaled, y, cv=kfold,
                                    scoring='neg_root_mean_squared_error')

    cv_results.append({
        'Modelo': model_name,
        'R² Promedio': r2_scores.mean(),
        'R² Std': r2_scores.std(),
        'MAE Promedio': mae_scores.mean(),
        'MAE Std': mae_scores.std(),
        'RMSE Promedio': rmse_scores.mean(),
        'RMSE Std': rmse_scores.std()
    })

    print(f"      R²: {r2_scores.mean():.4f} (+/- {r2_scores.std():.4f})")
    print(f"      MAE: {mae_scores.mean():.4f} (+/- {mae_scores.std():.4f})")

cv_results_df = pd.DataFrame(cv_results)

print("\n📊 RESULTADOS DE VALIDACIÓN CRUZADA:")
print(cv_results_df.to_string(index=False))

# Visualizar resultados de CV
fig, axes = plt.subplots(1, 2, figsize=(15, 5))

# R² comparison
x_pos = np.arange(len(cv_results_df))
axes[0].bar(x_pos, cv_results_df['R² Promedio'], yerr=cv_results_df['R² Std'],
            capsize=5, alpha=0.7, color='steelblue', edgecolor='black')
axes[0].set_xticks(x_pos)
axes[0].set_xticklabels(cv_results_df['Modelo'], rotation=45, ha='right')
axes[0].set_ylabel('R² Score', fontsize=12)
axes[0].set_title(f'Validación Cruzada ({k_folds}-Fold) - R²', fontsize=14, fontweight='bold')
axes[0].grid(True, alpha=0.3, axis='y')

# MAE comparison
axes[1].bar(x_pos, cv_results_df['MAE Promedio'], yerr=cv_results_df['MAE Std'],
            capsize=5, alpha=0.7, color='coral', edgecolor='black')
axes[1].set_xticks(x_pos)
axes[1].set_xticklabels(cv_results_df['Modelo'], rotation=45, ha='right')
axes[1].set_ylabel('MAE', fontsize=12)
axes[1].set_title(f'Validación Cruzada ({k_folds}-Fold) - MAE', fontsize=14, fontweight='bold')
axes[1].grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig('validacion_cruzada.png', dpi=300, bbox_inches='tight')
print("\n✓ Gráfico guardado: 'validacion_cruzada.png'")

# ==============================================================================
# 5. GRID SEARCH - OPTIMIZACIÓN DE HIPERPARÁMETROS
# ==============================================================================

print("\n[5] OPTIMIZACIÓN DE HIPERPARÁMETROS CON GRIDSEARCHCV")
print("-" * 80)

# Dividir datos
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Estandarizar
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# ========== Ridge ==========
print("\n🔍 Optimizando Ridge...")
ridge_params = {
    'alpha': [0.001, 0.01, 0.1, 1, 10, 100, 1000]
}

ridge_grid = GridSearchCV(
    Ridge(random_state=42),
    ridge_params,
    cv=5,
    scoring='r2',
    n_jobs=-1
)
ridge_grid.fit(X_train_scaled, y_train)

print(f"   ✓ Mejor alpha: {ridge_grid.best_params_['alpha']}")
print(f"   ✓ Mejor R² (CV): {ridge_grid.best_score_:.4f}")

# ========== Lasso ==========
print("\n🔍 Optimizando Lasso...")
lasso_params = {
    'alpha': [0.0001, 0.001, 0.01, 0.1, 1, 10]
}

lasso_grid = GridSearchCV(
    Lasso(max_iter=10000, random_state=42),
    lasso_params,
    cv=5,
    scoring='r2',
    n_jobs=-1
)
lasso_grid.fit(X_train_scaled, y_train)

print(f"   ✓ Mejor alpha: {lasso_grid.best_params_['alpha']}")
print(f"   ✓ Mejor R² (CV): {lasso_grid.best_score_:.4f}")

# ========== ElasticNet ==========
print("\n🔍 Optimizando ElasticNet...")
elasticnet_params = {
    'alpha': [0.001, 0.01, 0.1, 1],
    'l1_ratio': [0.1, 0.3, 0.5, 0.7, 0.9]
}

elasticnet_grid = GridSearchCV(
    ElasticNet(max_iter=10000, random_state=42),
    elasticnet_params,
    cv=5,
    scoring='r2',
    n_jobs=-1
)
elasticnet_grid.fit(X_train_scaled, y_train)

print(f"   ✓ Mejor alpha: {elasticnet_grid.best_params_['alpha']}")
print(f"   ✓ Mejor l1_ratio: {elasticnet_grid.best_params_['l1_ratio']}")
print(f"   ✓ Mejor R² (CV): {elasticnet_grid.best_score_:.4f}")

# ========== Random Forest ==========
print("\n🔍 Optimizando Random Forest...")
print("   (Esto puede tardar varios minutos...)")

rf_params = {
    'n_estimators': [50, 100, 200],
    'max_depth': [10, 20, None],
    'min_samples_split': [2, 5],
    'min_samples_leaf': [1, 2]
}

rf_grid = GridSearchCV(
    RandomForestRegressor(random_state=42, n_jobs=-1),
    rf_params,
    cv=3,  # Menos folds para Random Forest (es más lento)
    scoring='r2',
    n_jobs=1  # Solo 1 job porque RF ya usa paralelización
)
rf_grid.fit(X_train_scaled, y_train)

print(f"   ✓ Mejores parámetros: {rf_grid.best_params_}")
print(f"   ✓ Mejor R² (CV): {rf_grid.best_score_:.4f}")

# ==============================================================================
# 6. EVALUAR MODELOS OPTIMIZADOS
# ==============================================================================

print("\n[6] EVALUACIÓN DE MODELOS OPTIMIZADOS EN SET DE PRUEBA")
print("-" * 80)

optimized_models = {
    'Ridge (Optimizado)': ridge_grid.best_estimator_,
    'Lasso (Optimizado)': lasso_grid.best_estimator_,
    'ElasticNet (Optimizado)': elasticnet_grid.best_estimator_,
    'Random Forest (Optimizado)': rf_grid.best_estimator_
}

test_results = []

for model_name, model in optimized_models.items():
    y_pred = model.predict(X_test_scaled)

    r2 = r2_score(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))

    test_results.append({
        'Modelo': model_name,
        'R²': r2,
        'MAE': mae,
        'RMSE': rmse
    })

    print(f"\n{model_name}:")
    print(f"   R²: {r2:.4f}")
    print(f"   MAE: {mae:.4f}")
    print(f"   RMSE: {rmse:.4f}")

test_results_df = pd.DataFrame(test_results)

# Identificar mejor modelo
best_model_idx = test_results_df['R²'].idxmax()
best_model_name = test_results_df.loc[best_model_idx, 'Modelo']
best_r2 = test_results_df.loc[best_model_idx, 'R²']

print(f"\n🏆 MEJOR MODELO: {best_model_name}")
print(f"   R²: {best_r2:.4f}")

# ==============================================================================
# 7. COMPARAR IMPACTO DE OUTLIERS
# ==============================================================================

print("\n[7] IMPACTO DE OUTLIERS EN EL MODELO")
print("-" * 80)

if n_outliers > 0:
    print(f"\n🔍 Entrenando modelo sin outliers ({len(X_no_outliers)} muestras)...")

    # Dividir datos sin outliers
    X_train_no, X_test_no, y_train_no, y_test_no = train_test_split(
        X_no_outliers, y_no_outliers, test_size=0.2, random_state=42
    )

    # Estandarizar
    scaler_no = StandardScaler()
    X_train_no_scaled = scaler_no.fit_transform(X_train_no)
    X_test_no_scaled = scaler_no.transform(X_test_no)

    # Entrenar mejor modelo sin outliers
    if 'Ridge' in best_model_name:
        model_no_outliers = Ridge(alpha=ridge_grid.best_params_['alpha'])
    elif 'Lasso' in best_model_name:
        model_no_outliers = Lasso(alpha=lasso_grid.best_params_['alpha'], max_iter=10000)
    elif 'ElasticNet' in best_model_name:
        model_no_outliers = ElasticNet(**elasticnet_grid.best_params_, max_iter=10000)
    else:  # Random Forest
        model_no_outliers = RandomForestRegressor(**rf_grid.best_params_, random_state=42)

    model_no_outliers.fit(X_train_no_scaled, y_train_no)
    y_pred_no = model_no_outliers.predict(X_test_no_scaled)

    r2_no_outliers = r2_score(y_test_no, y_pred_no)
    mae_no_outliers = mean_absolute_error(y_test_no, y_pred_no)

    print(f"\n📊 COMPARACIÓN CON/SIN OUTLIERS:")
    comparison_outliers = pd.DataFrame({
        'Con outliers': [best_r2, test_results_df.loc[best_model_idx, 'MAE']],
        'Sin outliers': [r2_no_outliers, mae_no_outliers],
        'Diferencia': [r2_no_outliers - best_r2,
                       mae_no_outliers - test_results_df.loc[best_model_idx, 'MAE']]
    }, index=['R²', 'MAE'])

    print(comparison_outliers)

    if r2_no_outliers > best_r2:
        print("\n✓ El modelo mejora SIN outliers")
    else:
        print("\n⚠️  El modelo NO mejora significativamente sin outliers")

# ==============================================================================
# 8. VISUALIZACIÓN FINAL
# ==============================================================================

print("\n[8] GENERANDO VISUALIZACIONES FINALES")
print("-" * 80)

# Comparación de todos los modelos
fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# R² comparison
axes[0, 0].bar(test_results_df['Modelo'], test_results_df['R²'],
               color=['gold' if m == best_model_name else 'steelblue'
                      for m in test_results_df['Modelo']],
               edgecolor='black', alpha=0.8)
axes[0, 0].set_ylabel('R²', fontsize=12)
axes[0, 0].set_title('Comparación de R² en Test', fontsize=14, fontweight='bold')
axes[0, 0].tick_params(axis='x', rotation=45)
axes[0, 0].grid(True, alpha=0.3, axis='y')

for i, v in enumerate(test_results_df['R²']):
    axes[0, 0].text(i, v + 0.005, f'{v:.4f}', ha='center', fontweight='bold')

# MAE comparison
axes[0, 1].bar(test_results_df['Modelo'], test_results_df['MAE'],
               color=['gold' if m == best_model_name else 'coral'
                      for m in test_results_df['Modelo']],
               edgecolor='black', alpha=0.8)
axes[0, 1].set_ylabel('MAE', fontsize=12)
axes[0, 1].set_title('Comparación de MAE en Test', fontsize=14, fontweight='bold')
axes[0, 1].tick_params(axis='x', rotation=45)
axes[0, 1].grid(True, alpha=0.3, axis='y')

for i, v in enumerate(test_results_df['MAE']):
    axes[0, 1].text(i, v + 0.1, f'{v:.2f}', ha='center', fontweight='bold')

# Predicciones del mejor modelo
best_model = optimized_models[best_model_name]
y_pred_best = best_model.predict(X_test_scaled)

axes[1, 0].scatter(y_test, y_pred_best, alpha=0.5, s=30, edgecolors='k', linewidths=0.5)
axes[1, 0].plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()],
                'r--', lw=2, label='Predicción Perfecta')
axes[1, 0].set_xlabel('Valores Reales', fontsize=12)
axes[1, 0].set_ylabel('Valores Predichos', fontsize=12)
axes[1, 0].set_title(f'{best_model_name}\nReales vs Predichos (R²={best_r2:.4f})',
                     fontsize=14, fontweight='bold')
axes[1, 0].legend()
axes[1, 0].grid(True, alpha=0.3)

# Residuos
residuals = y_test - y_pred_best
axes[1, 1].scatter(y_pred_best, residuals, alpha=0.5, s=30, edgecolors='k', linewidths=0.5)
axes[1, 1].axhline(y=0, color='r', linestyle='--', linewidth=2)
axes[1, 1].set_xlabel('Valores Predichos', fontsize=12)
axes[1, 1].set_ylabel('Residuos', fontsize=12)
axes[1, 1].set_title(f'Análisis de Residuos\nMedia: {residuals.mean():.4f}',
                     fontsize=14, fontweight='bold')
axes[1, 1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('optimizacion_resultados_finales.png', dpi=300, bbox_inches='tight')
print("✓ Gráfico guardado: 'optimizacion_resultados_finales.png'")

# ==============================================================================
# 9. GUARDAR MEJOR MODELO
# ==============================================================================

print("\n[9] GUARDANDO MEJOR MODELO")
print("-" * 80)

import joblib

joblib.dump(best_model, 'best_model_optimized.pkl')
joblib.dump(scaler, 'scaler_optimized.pkl')

print(f"✓ Mejor modelo guardado: 'best_model_optimized.pkl'")
print(f"✓ Scaler guardado: 'scaler_optimized.pkl'")
print(f"\nModelo: {best_model_name}")
print(f"R² (Test): {best_r2:.4f}")

# ==============================================================================
# 10. RESUMEN FINAL
# ==============================================================================

print("\n" + "=" * 80)
print("RESUMEN FINAL DE VALIDACIÓN Y OPTIMIZACIÓN")
print("=" * 80)

print(f"""
📊 DATOS UTILIZADOS:
   - Dataset: {dataset_used}
   - Características: {X.shape[1]}
   - Muestras totales: {X.shape[0]}
   - Outliers detectados: {n_outliers} ({outlier_percentage:.2f}%)

🏆 MEJOR MODELO: {best_model_name}
   - R² (Test): {best_r2:.4f}
   - MAE (Test): {test_results_df.loc[best_model_idx, 'MAE']:.4f}
   - RMSE (Test): {test_results_df.loc[best_model_idx, 'RMSE']:.4f}

📈 VALIDACIÓN CRUZADA:
   - Método: {k_folds}-Fold Cross-Validation
   - Modelos evaluados: {len(models)}

🔧 OPTIMIZACIÓN:
   - GridSearchCV aplicado a: Ridge, Lasso, ElasticNet, Random Forest
   - Hiperparámetros optimizados automáticamente

💡 PRÓXIMOS PASOS:
   1. Usar 'best_model_optimized.pkl' para predicciones finales
   2. Analizar supuestos de regresión lineal
   3. Considerar ensemble de modelos
   4. Implementar en producción con validación continua

✓ Todos los resultados guardados en archivos PNG y PKL
""")

print("=" * 80)
print("FIN DEL ANÁLISIS DE VALIDACIÓN Y OPTIMIZACIÓN")
print("=" * 80)
