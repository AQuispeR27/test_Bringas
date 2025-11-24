"""
Análisis de Supuestos de Regresión Lineal
==========================================

Este script verifica los supuestos fundamentales de regresión lineal:
1. Linealidad: Relación lineal entre variables independientes y dependiente
2. Homocedasticidad: Varianza constante de los residuos
3. Normalidad: Distribución normal de los residuos
4. Independencia: No autocorrelación de residuos
5. Multicolinealidad: VIF (Variance Inflation Factor)
6. Análisis de influencia: Cook's Distance, DFFITS, Leverage

Autor: Análisis Avanzado de Ciencia de Datos
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from scipy import stats
from statsmodels.stats.stattools import durbin_watson
from statsmodels.stats.outliers_influence import variance_inflation_factor, OLSInfluence
from statsmodels.formula.api import ols
import statsmodels.api as sm
import warnings

warnings.filterwarnings('ignore')

print("=" * 80)
print("ANÁLISIS DE SUPUESTOS DE REGRESIÓN LINEAL")
print("=" * 80)

# ==============================================================================
# 1. CARGAR DATOS Y PREPARAR MODELO
# ==============================================================================

print("\n[1] CARGANDO DATASET Y PREPARANDO MODELO")
print("-" * 80)

# Intentar cargar datasets
datasets_to_try = [
    ('cancer_reg_selected_features.csv', 'seleccionadas'),
    ('cancer_reg.csv', 'original')
]

df = None
for filename, desc in datasets_to_try:
    try:
        df = pd.read_csv(filename)
        print(f"✓ Dataset con características {desc} cargado")
        break
    except FileNotFoundError:
        continue

if df is None:
    print("❌ Error: No se encontró ningún dataset")
    exit(1)

# Preprocesamiento
categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
if categorical_cols:
    df = df.drop(columns=categorical_cols)

if 'target_deathrate' not in df.columns:
    print("❌ Error: Variable objetivo no encontrada")
    exit(1)

# Separar X y y
X = df.drop('target_deathrate', axis=1)
y = df['target_deathrate']
X = X.fillna(X.median())

# Limitar características si hay demasiadas (para eficiencia)
if X.shape[1] > 30:
    print(f"\n⚠️  Dataset tiene {X.shape[1]} características. Seleccionando top 30 por correlación...")
    correlations = df.corr()['target_deathrate'].abs().sort_values(ascending=False)
    top_features = correlations[1:31].index.tolist()
    X = X[top_features]
    print(f"✓ Usando {X.shape[1]} características principales")

print(f"\n📊 Datos:")
print(f"   - Muestras: {X.shape[0]}")
print(f"   - Características: {X.shape[1]}")

# Dividir datos
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Estandarizar
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Entrenar modelo
print("\n🎯 Entrenando modelo de regresión lineal...")
model = LinearRegression()
model.fit(X_train_scaled, y_train)

# Predicciones
y_train_pred = model.predict(X_train_scaled)
y_test_pred = model.predict(X_test_scaled)

# Residuos
residuals_train = y_train - y_train_pred
residuals_test = y_test - y_test_pred

r2_train = r2_score(y_train, y_train_pred)
r2_test = r2_score(y_test, y_test_pred)

print(f"✓ Modelo entrenado:")
print(f"   R² (train): {r2_train:.4f}")
print(f"   R² (test): {r2_test:.4f}")

# ==============================================================================
# 2. SUPUESTO 1: LINEALIDAD
# ==============================================================================

print("\n[2] VERIFICANDO SUPUESTO DE LINEALIDAD")
print("-" * 80)

print("\n📊 Analizando relación lineal entre variables predictoras y objetivo...")

# Calcular correlaciones
correlations = []
for col in X.columns:
    corr = X[col].corr(y)
    correlations.append({
        'Variable': col,
        'Correlación': corr,
        'Correlación Abs': abs(corr)
    })

corr_df = pd.DataFrame(correlations).sort_values('Correlación Abs', ascending=False)

print("\nTop 10 variables con mayor correlación lineal:")
print(corr_df.head(10).to_string(index=False))

# Test visual: Residuos vs Valores Predichos
print("\n🔍 Análisis visual de residuos vs predichos:")
print("   - Si hay patrón → problema de linealidad")
print("   - Si dispersión aleatoria → linealidad OK")

# Crear gráficos de linealidad
fig, axes = plt.subplots(2, 3, figsize=(18, 12))

# 1. Residuos vs Predichos (entrenamiento)
axes[0, 0].scatter(y_train_pred, residuals_train, alpha=0.5, s=20,
                   edgecolors='k', linewidths=0.3)
axes[0, 0].axhline(y=0, color='red', linestyle='--', linewidth=2)
axes[0, 0].set_xlabel('Valores Predichos', fontsize=11)
axes[0, 0].set_ylabel('Residuos', fontsize=11)
axes[0, 0].set_title('Residuos vs Predichos (Train)', fontsize=12, fontweight='bold')
axes[0, 0].grid(True, alpha=0.3)

# Añadir línea de tendencia LOWESS
from scipy.signal import savgol_filter
sorted_indices = np.argsort(y_train_pred)
y_smooth = savgol_filter(residuals_train.values[sorted_indices], 51, 3)
axes[0, 0].plot(y_train_pred.values[sorted_indices], y_smooth,
                color='blue', linewidth=2, label='Tendencia')
axes[0, 0].legend()

# 2. Residuos vs Predichos (prueba)
axes[0, 1].scatter(y_test_pred, residuals_test, alpha=0.5, s=20,
                   color='orange', edgecolors='k', linewidths=0.3)
axes[0, 1].axhline(y=0, color='red', linestyle='--', linewidth=2)
axes[0, 1].set_xlabel('Valores Predichos', fontsize=11)
axes[0, 1].set_ylabel('Residuos', fontsize=11)
axes[0, 1].set_title('Residuos vs Predichos (Test)', fontsize=12, fontweight='bold')
axes[0, 1].grid(True, alpha=0.3)

# 3. Scale-Location plot (√|residuos| vs predichos)
standardized_residuals_train = residuals_train / residuals_train.std()
axes[0, 2].scatter(y_train_pred, np.sqrt(np.abs(standardized_residuals_train)),
                   alpha=0.5, s=20, edgecolors='k', linewidths=0.3)
axes[0, 2].set_xlabel('Valores Predichos', fontsize=11)
axes[0, 2].set_ylabel('√|Residuos Estandarizados|', fontsize=11)
axes[0, 2].set_title('Scale-Location Plot', fontsize=12, fontweight='bold')
axes[0, 2].grid(True, alpha=0.3)

# 4-6. Scatter plots de top 3 variables vs target
top_vars = corr_df.head(3)['Variable'].tolist()
for idx, var in enumerate(top_vars):
    axes[1, idx].scatter(X[var], y, alpha=0.4, s=20, edgecolors='k', linewidths=0.3)
    # Línea de regresión
    z = np.polyfit(X[var].fillna(X[var].median()), y, 1)
    p = np.poly1d(z)
    x_line = np.linspace(X[var].min(), X[var].max(), 100)
    axes[1, idx].plot(x_line, p(x_line), "r--", linewidth=2)
    axes[1, idx].set_xlabel(var, fontsize=11)
    axes[1, idx].set_ylabel('target_deathrate', fontsize=11)
    axes[1, idx].set_title(f'{var} vs Target (r={corr_df[corr_df["Variable"]==var]["Correlación"].values[0]:.3f})',
                           fontsize=12, fontweight='bold')
    axes[1, idx].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('supuesto_linealidad.png', dpi=300, bbox_inches='tight')
print("\n✓ Gráfico guardado: 'supuesto_linealidad.png'")

# ==============================================================================
# 3. SUPUESTO 2: HOMOCEDASTICIDAD (VARIANZA CONSTANTE)
# ==============================================================================

print("\n[3] VERIFICANDO SUPUESTO DE HOMOCEDASTICIDAD")
print("-" * 80)

# Test de Breusch-Pagan
print("\n🔍 Test de Breusch-Pagan para homocedasticidad...")

# Preparar datos para statsmodels
X_train_with_const = sm.add_constant(X_train_scaled)
ols_model = sm.OLS(y_train, X_train_with_const).fit()

from statsmodels.compat import lzip
from statsmodels.stats.diagnostic import het_breuschpagan

bp_test = het_breuschpagan(ols_model.resid, X_train_with_const)
labels = ['LM Statistic', 'LM-Test p-value', 'F-Statistic', 'F-Test p-value']
bp_results = dict(lzip(labels, bp_test))

print(f"\n📊 Resultados del Test de Breusch-Pagan:")
for key, value in bp_results.items():
    print(f"   - {key}: {value:.6f}")

if bp_results['LM-Test p-value'] < 0.05:
    print("\n⚠️  p-value < 0.05: RECHAZAR homocedasticidad (hay heterocedasticidad)")
else:
    print("\n✓ p-value ≥ 0.05: NO se rechaza homocedasticidad")

# Visualización
fig, axes = plt.subplots(1, 2, figsize=(15, 5))

# Residuos vs Predichos (para homocedasticidad)
axes[0].scatter(y_train_pred, residuals_train, alpha=0.5, s=20,
                edgecolors='k', linewidths=0.3)
axes[0].axhline(y=0, color='red', linestyle='--', linewidth=2)
axes[0].set_xlabel('Valores Predichos', fontsize=12)
axes[0].set_ylabel('Residuos', fontsize=12)
axes[0].set_title('Homocedasticidad: Residuos vs Predichos', fontsize=14, fontweight='bold')
axes[0].grid(True, alpha=0.3)

# Añadir bandas de dispersión
y_pred_sorted = np.sort(y_train_pred)
residuals_sorted = residuals_train[np.argsort(y_train_pred)]
window = len(y_pred_sorted) // 10
rolling_std = pd.Series(residuals_sorted.values).rolling(window=window, center=True).std()
axes[0].plot(y_pred_sorted, rolling_std * 2, 'b--', label='Desv. Estándar Móvil', linewidth=2)
axes[0].plot(y_pred_sorted, -rolling_std * 2, 'b--', linewidth=2)
axes[0].legend()

# Scale-Location (√|residuos estandarizados| vs predichos)
axes[1].scatter(y_train_pred, np.sqrt(np.abs(standardized_residuals_train)),
                alpha=0.5, s=20, edgecolors='k', linewidths=0.3)
axes[1].set_xlabel('Valores Predichos', fontsize=12)
axes[1].set_ylabel('√|Residuos Estandarizados|', fontsize=12)
axes[1].set_title('Scale-Location Plot', fontsize=14, fontweight='bold')
axes[1].grid(True, alpha=0.3)

# Línea de tendencia
sorted_idx = np.argsort(y_train_pred)
y_smooth_scale = savgol_filter(np.sqrt(np.abs(standardized_residuals_train.values[sorted_idx])), 51, 3)
axes[1].plot(y_train_pred.values[sorted_idx], y_smooth_scale,
             color='red', linewidth=2, label='Tendencia')
axes[1].legend()

plt.tight_layout()
plt.savefig('supuesto_homocedasticidad.png', dpi=300, bbox_inches='tight')
print("✓ Gráfico guardado: 'supuesto_homocedasticidad.png'")

# ==============================================================================
# 4. SUPUESTO 3: NORMALIDAD DE RESIDUOS
# ==============================================================================

print("\n[4] VERIFICANDO SUPUESTO DE NORMALIDAD DE RESIDUOS")
print("-" * 80)

# Test de Shapiro-Wilk (para muestras < 5000)
# Test de Kolmogorov-Smirnov (para muestras grandes)

print("\n🔍 Tests de normalidad:")

if len(residuals_train) < 5000:
    shapiro_stat, shapiro_p = stats.shapiro(residuals_train)
    print(f"\nTest de Shapiro-Wilk:")
    print(f"   - Estadístico: {shapiro_stat:.6f}")
    print(f"   - p-value: {shapiro_p:.6f}")

    if shapiro_p < 0.05:
        print("   ⚠️  p-value < 0.05: RECHAZAR normalidad")
    else:
        print("   ✓ p-value ≥ 0.05: NO se rechaza normalidad")

# Test de Kolmogorov-Smirnov
ks_stat, ks_p = stats.kstest(residuals_train, 'norm',
                              args=(residuals_train.mean(), residuals_train.std()))
print(f"\nTest de Kolmogorov-Smirnov:")
print(f"   - Estadístico: {ks_stat:.6f}")
print(f"   - p-value: {ks_p:.6f}")

if ks_p < 0.05:
    print("   ⚠️  p-value < 0.05: RECHAZAR normalidad")
else:
    print("   ✓ p-value ≥ 0.05: NO se rechaza normalidad")

# Jarque-Bera test
jb_stat, jb_p = stats.jarque_bera(residuals_train)
print(f"\nTest de Jarque-Bera:")
print(f"   - Estadístico: {jb_stat:.6f}")
print(f"   - p-value: {jb_p:.6f}")

if jb_p < 0.05:
    print("   ⚠️  p-value < 0.05: RECHAZAR normalidad")
else:
    print("   ✓ p-value ≥ 0.05: NO se rechaza normalidad")

# Visualizaciones de normalidad
fig, axes = plt.subplots(2, 2, figsize=(15, 12))

# 1. Histograma de residuos
axes[0, 0].hist(residuals_train, bins=50, density=True, alpha=0.7,
                edgecolor='black', color='steelblue')
# Curva normal teórica
mu, sigma = residuals_train.mean(), residuals_train.std()
x = np.linspace(residuals_train.min(), residuals_train.max(), 100)
axes[0, 0].plot(x, stats.norm.pdf(x, mu, sigma), 'r-', linewidth=2,
                label=f'Normal(μ={mu:.2f}, σ={sigma:.2f})')
axes[0, 0].set_xlabel('Residuos', fontsize=11)
axes[0, 0].set_ylabel('Densidad', fontsize=11)
axes[0, 0].set_title('Distribución de Residuos', fontsize=12, fontweight='bold')
axes[0, 0].legend()
axes[0, 0].grid(True, alpha=0.3)

# 2. Q-Q Plot
stats.probplot(residuals_train, dist="norm", plot=axes[0, 1])
axes[0, 1].set_title('Q-Q Plot (Normalidad)', fontsize=12, fontweight='bold')
axes[0, 1].grid(True, alpha=0.3)

# 3. Residuos estandarizados
axes[1, 0].scatter(range(len(standardized_residuals_train)),
                   standardized_residuals_train, alpha=0.5, s=20,
                   edgecolors='k', linewidths=0.3)
axes[1, 0].axhline(y=0, color='red', linestyle='--', linewidth=2)
axes[1, 0].axhline(y=2, color='orange', linestyle=':', linewidth=1, alpha=0.7)
axes[1, 0].axhline(y=-2, color='orange', linestyle=':', linewidth=1, alpha=0.7)
axes[1, 0].axhline(y=3, color='red', linestyle=':', linewidth=1, alpha=0.7)
axes[1, 0].axhline(y=-3, color='red', linestyle=':', linewidth=1, alpha=0.7)
axes[1, 0].set_xlabel('Índice', fontsize=11)
axes[1, 0].set_ylabel('Residuos Estandarizados', fontsize=11)
axes[1, 0].set_title('Residuos Estandarizados', fontsize=12, fontweight='bold')
axes[1, 0].grid(True, alpha=0.3)

# 4. Box plot de residuos
axes[1, 1].boxplot([residuals_train], labels=['Residuos'])
axes[1, 1].set_ylabel('Valor', fontsize=11)
axes[1, 1].set_title('Box Plot de Residuos', fontsize=12, fontweight='bold')
axes[1, 1].grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig('supuesto_normalidad.png', dpi=300, bbox_inches='tight')
print("\n✓ Gráfico guardado: 'supuesto_normalidad.png'")

# Estadísticas de residuos
print(f"\n📊 Estadísticas de residuos:")
print(f"   - Media: {residuals_train.mean():.6f}")
print(f"   - Mediana: {residuals_train.median():.6f}")
print(f"   - Desv. Estándar: {residuals_train.std():.6f}")
print(f"   - Asimetría (Skewness): {residuals_train.skew():.6f}")
print(f"   - Curtosis: {residuals_train.kurtosis():.6f}")

# ==============================================================================
# 5. SUPUESTO 4: INDEPENDENCIA (NO AUTOCORRELACIÓN)
# ==============================================================================

print("\n[5] VERIFICANDO SUPUESTO DE INDEPENDENCIA")
print("-" * 80)

# Test de Durbin-Watson
dw_statistic = durbin_watson(residuals_train)

print(f"\n🔍 Test de Durbin-Watson:")
print(f"   - Estadístico: {dw_statistic:.4f}")
print(f"\n   Interpretación:")
print(f"   - DW ≈ 2: No autocorrelación")
print(f"   - DW < 2: Autocorrelación positiva")
print(f"   - DW > 2: Autocorrelación negativa")

if 1.5 <= dw_statistic <= 2.5:
    print(f"   ✓ DW = {dw_statistic:.4f}: NO hay autocorrelación significativa")
elif dw_statistic < 1.5:
    print(f"   ⚠️  DW = {dw_statistic:.4f}: Posible autocorrelación POSITIVA")
else:
    print(f"   ⚠️  DW = {dw_statistic:.4f}: Posible autocorrelación NEGATIVA")

# Gráfico de autocorrelación
fig, axes = plt.subplots(1, 2, figsize=(15, 5))

# Residuos consecutivos
axes[0].scatter(residuals_train[:-1], residuals_train[1:], alpha=0.5, s=20,
                edgecolors='k', linewidths=0.3)
axes[0].axhline(y=0, color='red', linestyle='--', linewidth=1)
axes[0].axvline(x=0, color='red', linestyle='--', linewidth=1)
axes[0].set_xlabel('Residuo(t)', fontsize=12)
axes[0].set_ylabel('Residuo(t+1)', fontsize=12)
axes[0].set_title(f'Autocorrelación de Residuos (DW={dw_statistic:.4f})',
                  fontsize=14, fontweight='bold')
axes[0].grid(True, alpha=0.3)

# ACF Plot
from statsmodels.graphics.tsaplots import plot_acf
plot_acf(residuals_train, lags=40, ax=axes[1], alpha=0.05)
axes[1].set_title('Autocorrelation Function (ACF)', fontsize=14, fontweight='bold')

plt.tight_layout()
plt.savefig('supuesto_independencia.png', dpi=300, bbox_inches='tight')
print("✓ Gráfico guardado: 'supuesto_independencia.png'")

# ==============================================================================
# 6. MULTICOLINEALIDAD (VIF)
# ==============================================================================

print("\n[6] ANÁLISIS DE MULTICOLINEALIDAD (VIF)")
print("-" * 80)

print("\n🔍 Calculando Variance Inflation Factor (VIF)...")

# Calcular VIF para todas las variables
vif_data = []
for i, col in enumerate(X_train.columns):
    try:
        vif = variance_inflation_factor(X_train.values, i)
        vif_data.append({'Variable': col, 'VIF': vif})
    except:
        vif_data.append({'Variable': col, 'VIF': np.nan})

vif_df = pd.DataFrame(vif_data).sort_values('VIF', ascending=False)

print("\n📊 Variables con VIF alto (potencial multicolinealidad):")
print(vif_df.head(15).to_string(index=False))

print(f"\n📊 Resumen VIF:")
high_vif = vif_df[vif_df['VIF'] > 10]
moderate_vif = vif_df[(vif_df['VIF'] > 5) & (vif_df['VIF'] <= 10)]
low_vif = vif_df[vif_df['VIF'] <= 5]

print(f"   - VIF > 10 (alto): {len(high_vif)} variables")
print(f"   - VIF 5-10 (moderado): {len(moderate_vif)} variables")
print(f"   - VIF ≤ 5 (bajo): {len(low_vif)} variables")

if len(high_vif) > 0:
    print("\n⚠️  Variables con VIF > 10 (considerar eliminar):")
    for var in high_vif.head(10)['Variable']:
        print(f"     - {var}")

# ==============================================================================
# 7. ANÁLISIS DE INFLUENCIA (COOK'S DISTANCE)
# ==============================================================================

print("\n[7] ANÁLISIS DE PUNTOS INFLUYENTES (COOK'S DISTANCE)")
print("-" * 80)

print("\n🔍 Calculando Cook's Distance y métricas de influencia...")

# Usar statsmodels para cálculos detallados
influence = OLSInfluence(ols_model)

# Cook's Distance
cooks_d = influence.cooks_distance[0]

# DFFITS
dffits = influence.dffits[0]

# Leverage (hat values)
leverage = influence.hat_matrix_diag

# Umbral para Cook's Distance: 4/n
threshold_cooks = 4 / len(X_train)

influential_points = np.where(cooks_d > threshold_cooks)[0]
n_influential = len(influential_points)

print(f"\n📊 Puntos influyentes detectados:")
print(f"   - Umbral Cook's D: {threshold_cooks:.6f}")
print(f"   - Puntos sobre umbral: {n_influential} ({n_influential/len(X_train)*100:.2f}%)")
print(f"   - Cook's D máximo: {cooks_d.max():.6f}")
print(f"   - Cook's D mediano: {np.median(cooks_d):.6f}")

# Visualizaciones de influencia
fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# 1. Cook's Distance
axes[0, 0].stem(range(len(cooks_d)), cooks_d, markerfmt=',',
                basefmt=' ', linefmt='steelblue')
axes[0, 0].axhline(y=threshold_cooks, color='red', linestyle='--',
                   linewidth=2, label=f'Umbral = {threshold_cooks:.4f}')
axes[0, 0].set_xlabel('Índice de observación', fontsize=11)
axes[0, 0].set_ylabel("Cook's Distance", fontsize=11)
axes[0, 0].set_title("Cook's Distance por Observación", fontsize=12, fontweight='bold')
axes[0, 0].legend()
axes[0, 0].grid(True, alpha=0.3)

# 2. Leverage vs Residuos Estandarizados
axes[0, 1].scatter(leverage, standardized_residuals_train, alpha=0.5, s=20,
                   edgecolors='k', linewidths=0.3)
# Marcar puntos influyentes
if n_influential > 0:
    axes[0, 1].scatter(leverage[influential_points],
                       standardized_residuals_train.values[influential_points],
                       color='red', s=100, alpha=0.7, marker='o',
                       edgecolors='darkred', linewidths=2,
                       label='Influyentes')
axes[0, 1].axhline(y=0, color='gray', linestyle='--', linewidth=1)
axes[0, 1].axhline(y=2, color='orange', linestyle=':', linewidth=1)
axes[0, 1].axhline(y=-2, color='orange', linestyle=':', linewidth=1)
axes[0, 1].set_xlabel('Leverage', fontsize=11)
axes[0, 1].set_ylabel('Residuos Estandarizados', fontsize=11)
axes[0, 1].set_title('Leverage vs Residuos Estandarizados', fontsize=12, fontweight='bold')
axes[0, 1].legend()
axes[0, 1].grid(True, alpha=0.3)

# 3. DFFITS
axes[1, 0].scatter(range(len(dffits)), dffits, alpha=0.5, s=20,
                   edgecolors='k', linewidths=0.3)
threshold_dffits = 2 * np.sqrt(X_train.shape[1] / X_train.shape[0])
axes[1, 0].axhline(y=threshold_dffits, color='red', linestyle='--',
                   linewidth=2, label=f'Umbral = ±{threshold_dffits:.4f}')
axes[1, 0].axhline(y=-threshold_dffits, color='red', linestyle='--', linewidth=2)
axes[1, 0].set_xlabel('Índice de observación', fontsize=11)
axes[1, 0].set_ylabel('DFFITS', fontsize=11)
axes[1, 0].set_title('DFFITS por Observación', fontsize=12, fontweight='bold')
axes[1, 0].legend()
axes[1, 0].grid(True, alpha=0.3)

# 4. Residuos vs Leverage con contornos de Cook's D
axes[1, 1].scatter(leverage, residuals_train, alpha=0.5, s=20,
                   c=cooks_d, cmap='YlOrRd', edgecolors='k', linewidths=0.3)
cbar = plt.colorbar(axes[1, 1].collections[0], ax=axes[1, 1])
cbar.set_label("Cook's Distance", fontsize=10)
axes[1, 1].axhline(y=0, color='blue', linestyle='--', linewidth=1)
axes[1, 1].set_xlabel('Leverage', fontsize=11)
axes[1, 1].set_ylabel('Residuos', fontsize=11)
axes[1, 1].set_title("Residuos vs Leverage (color = Cook's D)", fontsize=12, fontweight='bold')
axes[1, 1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('analisis_influencia.png', dpi=300, bbox_inches='tight')
print("✓ Gráfico guardado: 'analisis_influencia.png'")

# ==============================================================================
# 8. RESUMEN FINAL
# ==============================================================================

print("\n" + "=" * 80)
print("RESUMEN DE VERIFICACIÓN DE SUPUESTOS")
print("=" * 80)

print(f"""
📊 MODELO EVALUADO:
   - R² (Train): {r2_train:.4f}
   - R² (Test): {r2_test:.4f}
   - Características: {X.shape[1]}
   - Muestras (Train): {len(X_train)}

1️⃣ LINEALIDAD:
   - Verificar gráficos de residuos vs predichos
   - Buscar patrones no aleatorios
   - Top correlación: {corr_df.iloc[0]['Correlación']:.4f}

2️⃣ HOMOCEDASTICIDAD:
   - Breusch-Pagan p-value: {bp_results['LM-Test p-value']:.6f}
   {'✓ Homocedasticidad OK' if bp_results['LM-Test p-value'] >= 0.05 else '⚠️  Heterocedasticidad presente'}

3️⃣ NORMALIDAD DE RESIDUOS:
   - Shapiro-Wilk p-value: {shapiro_p if len(residuals_train) < 5000 else 'N/A (muestra grande)'}
   - Kolmogorov-Smirnov p-value: {ks_p:.6f}
   - Jarque-Bera p-value: {jb_p:.6f}
   - Asimetría: {residuals_train.skew():.4f}
   - Curtosis: {residuals_train.kurtosis():.4f}

4️⃣ INDEPENDENCIA:
   - Durbin-Watson: {dw_statistic:.4f}
   {'✓ No autocorrelación' if 1.5 <= dw_statistic <= 2.5 else '⚠️  Posible autocorrelación'}

5️⃣ MULTICOLINEALIDAD:
   - Variables con VIF > 10: {len(high_vif)}
   - Variables con VIF 5-10: {len(moderate_vif)}
   {'✓ Multicolinealidad baja' if len(high_vif) == 0 else '⚠️  Revisar variables con VIF alto'}

6️⃣ PUNTOS INFLUYENTES:
   - Cook's D umbral: {threshold_cooks:.6f}
   - Puntos influyentes: {n_influential} ({n_influential/len(X_train)*100:.2f}%)
   {'✓ Pocos puntos influyentes' if n_influential < len(X_train) * 0.05 else '⚠️  Muchos puntos influyentes'}

💡 RECOMENDACIONES:

""")

recommendations = []

if bp_results['LM-Test p-value'] < 0.05:
    recommendations.append("- Heterocedasticidad detectada → Usar errores estándar robustos o transformar Y")

if jb_p < 0.05:
    recommendations.append("- Residuos no normales → Considerar transformaciones o modelos robustos")

if not (1.5 <= dw_statistic <= 2.5):
    recommendations.append("- Autocorrelación detectada → Verificar orden temporal de los datos")

if len(high_vif) > 0:
    recommendations.append(f"- Eliminar o combinar {len(high_vif)} variables con VIF > 10")

if n_influential > len(X_train) * 0.05:
    recommendations.append("- Revisar puntos influyentes → Considerar eliminarlos o usar modelos robustos")

if recommendations:
    for rec in recommendations:
        print(rec)
else:
    print("✓ El modelo cumple razonablemente bien todos los supuestos")

print("""
📁 ARCHIVOS GENERADOS:
   - supuesto_linealidad.png
   - supuesto_homocedasticidad.png
   - supuesto_normalidad.png
   - supuesto_independencia.png
   - analisis_influencia.png
""")

print("=" * 80)
print("FIN DEL ANÁLISIS DE SUPUESTOS DE REGRESIÓN")
print("=" * 80)
