"""
Selección de Características para el Modelo de Regresión de Cáncer
===================================================================

Este script implementa técnicas avanzadas de selección de características:
1. RFE (Recursive Feature Elimination)
2. Regularización L1 (Lasso) y L2 (Ridge)
3. Análisis de VIF (Variance Inflation Factor) para multicolinealidad
4. Selección basada en importancia de correlación

Autor: Análisis Avanzado de Ciencia de Datos
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.feature_selection import RFE, SelectKBest, f_regression
from sklearn.linear_model import LinearRegression, Lasso, Ridge, LassoCV, RidgeCV
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
from statsmodels.stats.outliers_influence import variance_inflation_factor
import warnings

warnings.filterwarnings('ignore')

print("=" * 80)
print("SELECCIÓN DE CARACTERÍSTICAS - MODELO DE REGRESIÓN DE CÁNCER")
print("=" * 80)

# ==============================================================================
# 1. CARGAR DATOS
# ==============================================================================

print("\n[1] CARGANDO DATASET...")
print("-" * 80)

# Intentar cargar el dataset con características mejoradas primero
try:
    df = pd.read_csv('cancer_reg_engineered.csv')
    print(f"✓ Dataset con características mejoradas cargado")
    using_engineered = True
except FileNotFoundError:
    try:
        df = pd.read_csv('cancer_reg.csv')
        print(f"✓ Dataset original cargado")
        using_engineered = False
    except FileNotFoundError:
        print("❌ Error: No se encontró ningún dataset")
        exit(1)

print(f"   Dimensiones: {df.shape[0]} filas × {df.shape[1]} columnas")

# ==============================================================================
# 2. PREPROCESAMIENTO
# ==============================================================================

print("\n[2] PREPROCESAMIENTO DE DATOS")
print("-" * 80)

# Eliminar columnas categóricas no procesadas
categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
if categorical_cols:
    print(f"\n🗑️  Eliminando columnas categóricas: {categorical_cols}")
    df = df.drop(columns=categorical_cols)

# Verificar variable objetivo
if 'target_deathrate' not in df.columns:
    print("❌ Error: No se encontró la variable objetivo 'target_deathrate'")
    exit(1)

# Separar X y y
X = df.drop('target_deathrate', axis=1)
y = df['target_deathrate']

# Imputar valores nulos con la mediana
print(f"\n🔧 Imputando valores nulos...")
null_count_before = X.isnull().sum().sum()
X = X.fillna(X.median())
print(f"   - Valores nulos imputados: {null_count_before}")

print(f"\n✓ Dataset preprocesado:")
print(f"   - Características: {X.shape[1]}")
print(f"   - Muestras: {X.shape[0]}")
print(f"   - Variable objetivo: target_deathrate")

# Dividir en train/test
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Estandarizar
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

print(f"\n✓ División y estandarización completada")

# ==============================================================================
# 3. MODELO BASE (Sin selección de características)
# ==============================================================================

print("\n[3] ENTRENANDO MODELO BASE (TODAS LAS CARACTERÍSTICAS)")
print("-" * 80)

base_model = LinearRegression()
base_model.fit(X_train_scaled, y_train)

y_train_pred_base = base_model.predict(X_train_scaled)
y_test_pred_base = base_model.predict(X_test_scaled)

r2_train_base = r2_score(y_train, y_train_pred_base)
r2_test_base = r2_score(y_test, y_test_pred_base)
mae_test_base = mean_absolute_error(y_test, y_test_pred_base)

print(f"\n📊 RESULTADOS DEL MODELO BASE:")
print(f"   - Características utilizadas: {X.shape[1]}")
print(f"   - R² (entrenamiento): {r2_train_base:.4f}")
print(f"   - R² (prueba): {r2_test_base:.4f}")
print(f"   - MAE (prueba): {mae_test_base:.4f}")

# ==============================================================================
# 4. ANÁLISIS DE VIF (MULTICOLINEALIDAD)
# ==============================================================================

print("\n[4] ANÁLISIS DE MULTICOLINEALIDAD (VIF)")
print("-" * 80)

print("\n🔍 Calculando VIF para todas las características...")
print("   (Esto puede tardar unos momentos...)")

# Para dataset grande, calcular VIF en una muestra
if X.shape[1] > 50:
    print(f"   ⚠️  Dataset tiene {X.shape[1]} características. Calculando VIF para las top 50.")
    # Seleccionar top 50 por correlación con target
    correlations = df.corr()['target_deathrate'].abs().sort_values(ascending=False)
    top_50_features = correlations[1:51].index.tolist()
    X_vif = X[top_50_features].copy()
else:
    X_vif = X.copy()

# Calcular VIF
vif_data = []
for i, col in enumerate(X_vif.columns):
    try:
        vif = variance_inflation_factor(X_vif.values, i)
        vif_data.append({'Variable': col, 'VIF': vif})
    except:
        vif_data.append({'Variable': col, 'VIF': np.nan})

vif_df = pd.DataFrame(vif_data).sort_values('VIF', ascending=False)

print("\n📊 Variables con VIF > 10 (alta multicolinealidad):")
high_vif = vif_df[vif_df['VIF'] > 10]
if len(high_vif) > 0:
    print(high_vif.head(20).to_string(index=False))
else:
    print("   ✓ No se encontraron variables con VIF > 10")

print("\n📊 Top 15 variables por VIF:")
print(vif_df.head(15).to_string(index=False))

# Visualizar VIF
plt.figure(figsize=(12, 8))
top_vif = vif_df.head(20)
colors = ['red' if x > 10 else 'orange' if x > 5 else 'green' for x in top_vif['VIF'].values]
plt.barh(range(len(top_vif)), top_vif['VIF'].values, color=colors)
plt.yticks(range(len(top_vif)), top_vif['Variable'].values)
plt.xlabel('VIF (Variance Inflation Factor)', fontsize=12)
plt.title('Top 20 Variables por VIF', fontsize=14, fontweight='bold')
plt.axvline(x=5, color='orange', linestyle='--', linewidth=1, label='VIF = 5 (moderado)')
plt.axvline(x=10, color='red', linestyle='--', linewidth=1, label='VIF = 10 (alto)')
plt.legend()
plt.tight_layout()
plt.savefig('analisis_vif.png', dpi=300, bbox_inches='tight')
print("\n✓ Gráfico guardado: 'analisis_vif.png'")

# Identificar variables a eliminar por VIF alto
vars_to_remove_vif = vif_df[vif_df['VIF'] > 10]['Variable'].tolist()
print(f"\n⚠️  Variables candidatas a eliminar por VIF alto: {len(vars_to_remove_vif)}")

# ==============================================================================
# 5. SELECCIÓN CON RFE (RECURSIVE FEATURE ELIMINATION)
# ==============================================================================

print("\n[5] SELECCIÓN DE CARACTERÍSTICAS CON RFE")
print("-" * 80)

# Probar diferentes números de características
n_features_to_select = min(30, X.shape[1] // 2)  # Seleccionar hasta 30 o la mitad

print(f"\n🎯 Ejecutando RFE para seleccionar {n_features_to_select} características...")

rfe = RFE(estimator=LinearRegression(), n_features_to_select=n_features_to_select)
rfe.fit(X_train_scaled, y_train)

# Obtener características seleccionadas
selected_features_rfe = X.columns[rfe.support_].tolist()
rejected_features_rfe = X.columns[~rfe.support_].tolist()

print(f"\n✓ RFE completado:")
print(f"   - Características seleccionadas: {len(selected_features_rfe)}")
print(f"   - Características rechazadas: {len(rejected_features_rfe)}")

# Ranking de características
feature_ranking = pd.DataFrame({
    'Variable': X.columns,
    'Ranking RFE': rfe.ranking_,
    'Seleccionada': rfe.support_
}).sort_values('Ranking RFE')

print(f"\n📊 Top 20 características según RFE:")
print(feature_ranking.head(20).to_string(index=False))

# Entrenar modelo con características seleccionadas por RFE
X_train_rfe = X_train[selected_features_rfe]
X_test_rfe = X_test[selected_features_rfe]

scaler_rfe = StandardScaler()
X_train_rfe_scaled = scaler_rfe.fit_transform(X_train_rfe)
X_test_rfe_scaled = scaler_rfe.transform(X_test_rfe)

model_rfe = LinearRegression()
model_rfe.fit(X_train_rfe_scaled, y_train)

y_test_pred_rfe = model_rfe.predict(X_test_rfe_scaled)
r2_test_rfe = r2_score(y_test, y_test_pred_rfe)
mae_test_rfe = mean_absolute_error(y_test, y_test_pred_rfe)

print(f"\n📊 RESULTADOS CON RFE:")
print(f"   - R² (prueba): {r2_test_rfe:.4f}")
print(f"   - MAE (prueba): {mae_test_rfe:.4f}")
print(f"   - Mejora en R²: {r2_test_rfe - r2_test_base:+.4f}")

# ==============================================================================
# 6. REGULARIZACIÓN L1 (LASSO)
# ==============================================================================

print("\n[6] SELECCIÓN CON REGULARIZACIÓN LASSO (L1)")
print("-" * 80)

print("\n🎯 Buscando mejor alpha para Lasso con validación cruzada...")

# Usar LassoCV para encontrar el mejor alpha
alphas = np.logspace(-4, 1, 100)
lasso_cv = LassoCV(alphas=alphas, cv=5, random_state=42, max_iter=10000)
lasso_cv.fit(X_train_scaled, y_train)

best_alpha_lasso = lasso_cv.alpha_
print(f"✓ Mejor alpha encontrado: {best_alpha_lasso:.6f}")

# Entrenar Lasso con el mejor alpha
lasso = Lasso(alpha=best_alpha_lasso, max_iter=10000, random_state=42)
lasso.fit(X_train_scaled, y_train)

y_test_pred_lasso = lasso.predict(X_test_scaled)
r2_test_lasso = r2_score(y_test, y_test_pred_lasso)
mae_test_lasso = mean_absolute_error(y_test, y_test_pred_lasso)

# Características seleccionadas (coeficiente != 0)
non_zero_coefs = np.sum(lasso.coef_ != 0)
selected_features_lasso = X.columns[lasso.coef_ != 0].tolist()

print(f"\n📊 RESULTADOS CON LASSO:")
print(f"   - Características con coeficiente no-cero: {non_zero_coefs}/{X.shape[1]}")
print(f"   - R² (prueba): {r2_test_lasso:.4f}")
print(f"   - MAE (prueba): {mae_test_lasso:.4f}")
print(f"   - Mejora en R²: {r2_test_lasso - r2_test_base:+.4f}")

# Visualizar coeficientes Lasso
lasso_coefs = pd.DataFrame({
    'Variable': X.columns,
    'Coeficiente': lasso.coef_,
    'Abs_Coeficiente': np.abs(lasso.coef_)
}).sort_values('Abs_Coeficiente', ascending=False)

print(f"\n📊 Top 20 variables según Lasso:")
print(lasso_coefs.head(20).to_string(index=False))

# Gráfico de coeficientes Lasso
plt.figure(figsize=(12, 8))
top_lasso_coefs = lasso_coefs[lasso_coefs['Coeficiente'] != 0].head(20)
if len(top_lasso_coefs) > 0:
    colors = ['green' if x > 0 else 'red' for x in top_lasso_coefs['Coeficiente'].values]
    plt.barh(range(len(top_lasso_coefs)), top_lasso_coefs['Coeficiente'].values, color=colors)
    plt.yticks(range(len(top_lasso_coefs)), top_lasso_coefs['Variable'].values)
    plt.xlabel('Coeficiente Lasso', fontsize=12)
    plt.title(f'Top 20 Características Seleccionadas por Lasso (α={best_alpha_lasso:.4f})',
              fontsize=14, fontweight='bold')
    plt.axvline(x=0, color='black', linestyle='--', linewidth=1)
    plt.tight_layout()
    plt.savefig('lasso_coeficientes.png', dpi=300, bbox_inches='tight')
    print("\n✓ Gráfico guardado: 'lasso_coeficientes.png'")

# ==============================================================================
# 7. REGULARIZACIÓN L2 (RIDGE)
# ==============================================================================

print("\n[7] REGULARIZACIÓN RIDGE (L2)")
print("-" * 80)

print("\n🎯 Buscando mejor alpha para Ridge con validación cruzada...")

# Usar RidgeCV para encontrar el mejor alpha
alphas_ridge = np.logspace(-2, 3, 100)
ridge_cv = RidgeCV(alphas=alphas_ridge, cv=5)
ridge_cv.fit(X_train_scaled, y_train)

best_alpha_ridge = ridge_cv.alpha_
print(f"✓ Mejor alpha encontrado: {best_alpha_ridge:.6f}")

# Entrenar Ridge con el mejor alpha
ridge = Ridge(alpha=best_alpha_ridge, random_state=42)
ridge.fit(X_train_scaled, y_train)

y_test_pred_ridge = ridge.predict(X_test_scaled)
r2_test_ridge = r2_score(y_test, y_test_pred_ridge)
mae_test_ridge = mean_absolute_error(y_test, y_test_pred_ridge)

print(f"\n📊 RESULTADOS CON RIDGE:")
print(f"   - R² (prueba): {r2_test_ridge:.4f}")
print(f"   - MAE (prueba): {mae_test_ridge:.4f}")
print(f"   - Mejora en R²: {r2_test_ridge - r2_test_base:+.4f}")

# ==============================================================================
# 8. COMPARACIÓN DE MÉTODOS
# ==============================================================================

print("\n[8] COMPARACIÓN DE MÉTODOS DE SELECCIÓN")
print("-" * 80)

# Crear DataFrame comparativo
comparison_df = pd.DataFrame({
    'Método': ['Base (Sin selección)', 'RFE', 'Lasso', 'Ridge'],
    'Características': [X.shape[1], len(selected_features_rfe), non_zero_coefs, X.shape[1]],
    'R² (Prueba)': [r2_test_base, r2_test_rfe, r2_test_lasso, r2_test_ridge],
    'MAE (Prueba)': [mae_test_base, mae_test_rfe, mae_test_lasso, mae_test_ridge]
})

comparison_df['Mejora R²'] = comparison_df['R² (Prueba)'] - r2_test_base

print("\n📊 TABLA COMPARATIVA:")
print(comparison_df.to_string(index=False))

# Identificar el mejor método
best_method_idx = comparison_df['R² (Prueba)'].idxmax()
best_method = comparison_df.loc[best_method_idx, 'Método']
best_r2 = comparison_df.loc[best_method_idx, 'R² (Prueba)']

print(f"\n🏆 MEJOR MÉTODO: {best_method}")
print(f"   - R² (Prueba): {best_r2:.4f}")
print(f"   - Características: {int(comparison_df.loc[best_method_idx, 'Características'])}")

# Visualizar comparación
fig, axes = plt.subplots(1, 2, figsize=(15, 6))

# R² comparison
axes[0].bar(comparison_df['Método'], comparison_df['R² (Prueba)'],
            color=['gray', 'blue', 'green', 'orange'])
axes[0].set_ylabel('R² (Prueba)', fontsize=12)
axes[0].set_title('Comparación de R² por Método', fontsize=14, fontweight='bold')
axes[0].tick_params(axis='x', rotation=45)
axes[0].grid(True, alpha=0.3, axis='y')

for i, v in enumerate(comparison_df['R² (Prueba)']):
    axes[0].text(i, v + 0.01, f'{v:.4f}', ha='center', fontweight='bold')

# Características comparison
axes[1].bar(comparison_df['Método'], comparison_df['Características'],
            color=['gray', 'blue', 'green', 'orange'])
axes[1].set_ylabel('Número de Características', fontsize=12)
axes[1].set_title('Número de Características por Método', fontsize=14, fontweight='bold')
axes[1].tick_params(axis='x', rotation=45)
axes[1].grid(True, alpha=0.3, axis='y')

for i, v in enumerate(comparison_df['Características']):
    axes[1].text(i, v + 1, f'{int(v)}', ha='center', fontweight='bold')

plt.tight_layout()
plt.savefig('comparacion_metodos_seleccion.png', dpi=300, bbox_inches='tight')
print("\n✓ Gráfico guardado: 'comparacion_metodos_seleccion.png'")

# ==============================================================================
# 9. EXPORTAR CARACTERÍSTICAS SELECCIONADAS
# ==============================================================================

print("\n[9] EXPORTANDO CARACTERÍSTICAS SELECCIONADAS")
print("-" * 80)

# Guardar características seleccionadas por cada método
results = {
    'rfe_features': selected_features_rfe,
    'lasso_features': selected_features_lasso,
    'vif_high_multicollinearity': vars_to_remove_vif
}

# Guardar en archivo de texto
with open('selected_features.txt', 'w') as f:
    f.write("CARACTERÍSTICAS SELECCIONADAS POR DIFERENTES MÉTODOS\n")
    f.write("=" * 80 + "\n\n")

    f.write(f"RFE - {len(selected_features_rfe)} características seleccionadas:\n")
    f.write("-" * 80 + "\n")
    for feat in selected_features_rfe:
        f.write(f"  - {feat}\n")

    f.write(f"\n\nLASSO - {len(selected_features_lasso)} características con coef != 0:\n")
    f.write("-" * 80 + "\n")
    for feat in selected_features_lasso:
        f.write(f"  - {feat}\n")

    f.write(f"\n\nVARIABLES CON VIF ALTO - {len(vars_to_remove_vif)} para considerar eliminar:\n")
    f.write("-" * 80 + "\n")
    for feat in vars_to_remove_vif:
        f.write(f"  - {feat}\n")

print("✓ Archivo guardado: 'selected_features.txt'")

# Crear dataset con características seleccionadas por el mejor método
if best_method == 'RFE':
    best_features = selected_features_rfe
elif best_method == 'Lasso':
    best_features = selected_features_lasso
else:
    best_features = X.columns.tolist()

df_selected = df[best_features + ['target_deathrate']]
df_selected.to_csv('cancer_reg_selected_features.csv', index=False)
print(f"✓ Dataset con mejores características guardado: 'cancer_reg_selected_features.csv'")
print(f"   - Método: {best_method}")
print(f"   - Características: {len(best_features)}")

# ==============================================================================
# 10. RECOMENDACIONES
# ==============================================================================

print("\n" + "=" * 80)
print("RECOMENDACIONES FINALES")
print("=" * 80)

print(f"""
✓ ANÁLISIS DE SELECCIÓN COMPLETADO

📊 RESULTADOS PRINCIPALES:

- Mejor método: {best_method}
- R² alcanzado: {best_r2:.4f}
- Mejora sobre base: {best_r2 - r2_test_base:+.4f}
- Características finales: {len(best_features)} (reducción de {X.shape[1] - len(best_features)})

💡 PRÓXIMOS PASOS:

1. Usar 'cancer_reg_selected_features.csv' para entrenar modelos finales
2. Considerar combinar métodos (intersección de RFE y Lasso)
3. Aplicar validación cruzada para confirmar resultados
4. Probar modelos más complejos (Random Forest, XGBoost)

⚠️  CONSIDERACIONES:

- VIF alto indica multicolinealidad - considera eliminar esas variables
- Lasso puede ser muy agresivo - prueba alphas más pequeños si elimina demasiado
- RFE es computacionalmente costoso para muchas características
- Ridge no elimina características, solo reduce coeficientes

🎯 RECOMENDACIÓN ESPECÍFICA:

Variables con VIF > 10: {len(vars_to_remove_vif)}
→ Considera eliminarlas y volver a entrenar para reducir multicolinealidad
""")

print("=" * 80)
print("FIN DEL ANÁLISIS DE SELECCIÓN DE CARACTERÍSTICAS")
print("=" * 80)
