"""
Pipeline Completo de Análisis Avanzado de Regresión
===================================================

Este script ejecuta TODOS los análisis avanzados en secuencia:
1. Ingeniería de características
2. Selección de características
3. Validación y optimización
4. Análisis de supuestos de regresión
5. Modelo final optimizado

Autor: Análisis Avanzado de Ciencia de Datos
Fecha: 2024
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import os
import warnings

warnings.filterwarnings('ignore')

# ==============================================================================
# CONFIGURACIÓN
# ==============================================================================

print("=" * 80)
print("PIPELINE COMPLETO DE ANÁLISIS AVANZADO")
print("Predicción de Mortalidad por Cáncer")
print("=" * 80)
print(f"\nIniciado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# Crear carpeta para resultados
results_dir = 'resultados_analisis_avanzado'
if not os.path.exists(results_dir):
    os.makedirs(results_dir)
    print(f"\n✓ Carpeta de resultados creada: '{results_dir}/'")

# ==============================================================================
# ETAPA 1: INGENIERÍA DE CARACTERÍSTICAS
# ==============================================================================

print("\n" + "=" * 80)
print("ETAPA 1: INGENIERÍA DE CARACTERÍSTICAS")
print("=" * 80)

from sklearn.preprocessing import PolynomialFeatures, StandardScaler, LabelEncoder
from scipy import stats

try:
    df = pd.read_csv('cancer_reg.csv')
    print(f"✓ Dataset cargado: {df.shape}")
except FileNotFoundError:
    print("❌ Error: Ejecuta 'generate_sample_data.py' primero")
    exit(1)

df_original = df.copy()

# Eliminar categóricas no procesables
categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
if 'geography' in categorical_cols:
    df = df.drop(columns=['geography'])
    categorical_cols.remove('geography')

# Codificar binnedinc si existe
if 'binnedinc' in df.columns:
    le = LabelEncoder()
    df['binnedinc_encoded'] = le.fit_transform(df['binnedinc'].fillna('unknown'))
    df = df.drop('binnedinc', axis=1)

print("\n[1.1] Creando transformaciones logarítmicas y de raíz cuadrada...")
numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
if 'target_deathrate' in numeric_cols:
    numeric_cols.remove('target_deathrate')

transformations_count = 0
for col in numeric_cols[:15]:  # Top 15 para evitar explosión de características
    if df[col].min() > 0 and df[col].skew() > 1:
        df[f'{col}_log'] = np.log1p(df[col])
        transformations_count += 1
    if df[col].min() >= 0 and df[col].skew() > 0.5:
        df[f'{col}_sqrt'] = np.sqrt(df[col])
        transformations_count += 1

print(f"   ✓ {transformations_count} transformaciones creadas")

print("\n[1.2] Creando ratios y proporciones...")
ratios_count = 0

# Ratios de salud
if 'avgdeathsperyear' in df.columns and 'avganncount' in df.columns:
    df['mortality_rate_ratio'] = df['avgdeathsperyear'] / (df['avganncount'] + 1)
    ratios_count += 1

if 'avganncount' in df.columns and 'popest2015' in df.columns:
    df['cancer_per_capita'] = df['avganncount'] / (df['popest2015'] / 100000)
    ratios_count += 1

# Ratios socioeconómicos
if 'pctbachdeg25_over' in df.columns and 'pcths25_over' in df.columns:
    df['education_ratio'] = df['pctbachdeg25_over'] / (df['pcths25_over'] + 1)
    ratios_count += 1

if 'pctemployed16_over' in df.columns and 'pctunemployed16_over' in df.columns:
    df['employment_ratio'] = df['pctemployed16_over'] / (df['pctunemployed16_over'] + 1)
    ratios_count += 1

if 'pctprivatecoverage' in df.columns and 'pctpubliccoverage' in df.columns:
    df['insurance_ratio'] = df['pctprivatecoverage'] / (df['pctpubliccoverage'] + 1)
    ratios_count += 1

print(f"   ✓ {ratios_count} ratios creados")

print("\n[1.3] Creando interacciones entre variables clave...")
interactions_count = 0

if all(col in df.columns for col in ['povertypercent', 'medincome']):
    df['poverty_income_int'] = df['povertypercent'] * df['medincome'] / 10000
    interactions_count += 1

if all(col in df.columns for col in ['medianage', 'incidencerate']):
    df['age_incidence_int'] = df['medianage'] * df['incidencerate'] / 100
    interactions_count += 1

print(f"   ✓ {interactions_count} interacciones creadas")

# Imputar valores nulos
df = df.fillna(df.median())

print(f"\n✓ Ingeniería de características completada:")
print(f"   - Características originales: {df_original.shape[1]}")
print(f"   - Características finales: {df.shape[1]}")
print(f"   - Nuevas características: {df.shape[1] - df_original.shape[1]}")

# Guardar dataset con características mejoradas
df.to_csv(f'{results_dir}/dataset_engineered.csv', index=False)

# ==============================================================================
# ETAPA 2: SELECCIÓN DE CARACTERÍSTICAS
# ==============================================================================

print("\n" + "=" * 80)
print("ETAPA 2: SELECCIÓN DE CARACTERÍSTICAS")
print("=" * 80)

from sklearn.model_selection import train_test_split
from sklearn.feature_selection import RFE
from sklearn.linear_model import LinearRegression, Lasso, LassoCV
from sklearn.metrics import r2_score, mean_absolute_error

# Preparar datos
X = df.drop('target_deathrate', axis=1)
y = df['target_deathrate']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Estandarizar
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

print(f"\n[2.1] Modelo base con todas las características...")
model_base = LinearRegression()
model_base.fit(X_train_scaled, y_train)
r2_base = r2_score(y_test, model_base.predict(X_test_scaled))
print(f"   ✓ R² base: {r2_base:.4f} con {X.shape[1]} características")

print(f"\n[2.2] Selección con Lasso (L1 regularization)...")
lasso_cv = LassoCV(alphas=np.logspace(-4, 1, 50), cv=5, random_state=42, max_iter=10000)
lasso_cv.fit(X_train_scaled, y_train)

selected_features_lasso = X.columns[lasso_cv.coef_ != 0].tolist()
r2_lasso = r2_score(y_test, lasso_cv.predict(X_test_scaled))

print(f"   ✓ Alpha óptimo: {lasso_cv.alpha_:.6f}")
print(f"   ✓ Características seleccionadas: {len(selected_features_lasso)}/{X.shape[1]}")
print(f"   ✓ R² con Lasso: {r2_lasso:.4f}")

print(f"\n[2.3] Selección con RFE...")
n_features_rfe = min(40, X.shape[1] // 2)
rfe = RFE(LinearRegression(), n_features_to_select=n_features_rfe)
rfe.fit(X_train_scaled, y_train)

selected_features_rfe = X.columns[rfe.support_].tolist()

X_train_rfe = X_train[selected_features_rfe]
X_test_rfe = X_test[selected_features_rfe]
scaler_rfe = StandardScaler()
X_train_rfe_scaled = scaler_rfe.fit_transform(X_train_rfe)
X_test_rfe_scaled = scaler_rfe.transform(X_test_rfe)

model_rfe = LinearRegression()
model_rfe.fit(X_train_rfe_scaled, y_train)
r2_rfe = r2_score(y_test, model_rfe.predict(X_test_rfe_scaled))

print(f"   ✓ Características seleccionadas: {len(selected_features_rfe)}")
print(f"   ✓ R² con RFE: {r2_rfe:.4f}")

# Usar el mejor método
if r2_lasso > r2_rfe:
    selected_features = selected_features_lasso
    best_selection_method = 'Lasso'
    best_r2_selection = r2_lasso
else:
    selected_features = selected_features_rfe
    best_selection_method = 'RFE'
    best_r2_selection = r2_rfe

print(f"\n✓ Mejor método: {best_selection_method}")
print(f"   - Características finales: {len(selected_features)}")
print(f"   - R²: {best_r2_selection:.4f}")
print(f"   - Mejora sobre base: {best_r2_selection - r2_base:+.4f}")

# Guardar características seleccionadas
df_selected = df[selected_features + ['target_deathrate']]
df_selected.to_csv(f'{results_dir}/dataset_selected_features.csv', index=False)

# ==============================================================================
# ETAPA 3: VALIDACIÓN Y OPTIMIZACIÓN
# ==============================================================================

print("\n" + "=" * 80)
print("ETAPA 3: VALIDACIÓN Y OPTIMIZACIÓN")
print("=" * 80)

from sklearn.model_selection import cross_val_score, GridSearchCV, KFold
from sklearn.linear_model import Ridge, ElasticNet
from sklearn.ensemble import RandomForestRegressor

# Preparar datos con características seleccionadas
X_selected = df[selected_features]
y_selected = df['target_deathrate']

X_train_sel, X_test_sel, y_train_sel, y_test_sel = train_test_split(
    X_selected, y_selected, test_size=0.2, random_state=42
)

scaler_sel = StandardScaler()
X_train_sel_scaled = scaler_sel.fit_transform(X_train_sel)
X_test_sel_scaled = scaler_sel.transform(X_test_sel)

print("\n[3.1] Validación cruzada 5-fold...")
kfold = KFold(n_splits=5, shuffle=True, random_state=42)

models_cv = {
    'Linear Regression': LinearRegression(),
    'Ridge': Ridge(),
    'Lasso': Lasso(max_iter=10000),
    'ElasticNet': ElasticNet(max_iter=10000)
}

cv_results = {}
for name, model in models_cv.items():
    scores = cross_val_score(model, X_train_sel_scaled, y_train_sel,
                             cv=kfold, scoring='r2')
    cv_results[name] = {
        'mean': scores.mean(),
        'std': scores.std()
    }
    print(f"   {name}: R² = {scores.mean():.4f} (+/- {scores.std():.4f})")

print("\n[3.2] Optimización de hiperparámetros con GridSearchCV...")

# Ridge
print("   Optimizando Ridge...")
ridge_params = {'alpha': [0.01, 0.1, 1, 10, 100]}
ridge_grid = GridSearchCV(Ridge(), ridge_params, cv=5, scoring='r2', n_jobs=-1)
ridge_grid.fit(X_train_sel_scaled, y_train_sel)
print(f"      Mejor alpha: {ridge_grid.best_params_['alpha']}")

# Lasso
print("   Optimizando Lasso...")
lasso_params = {'alpha': [0.001, 0.01, 0.1, 1]}
lasso_grid = GridSearchCV(Lasso(max_iter=10000), lasso_params, cv=5, scoring='r2', n_jobs=-1)
lasso_grid.fit(X_train_sel_scaled, y_train_sel)
print(f"      Mejor alpha: {lasso_grid.best_params_['alpha']}")

# ElasticNet
print("   Optimizando ElasticNet...")
elastic_params = {'alpha': [0.01, 0.1, 1], 'l1_ratio': [0.3, 0.5, 0.7]}
elastic_grid = GridSearchCV(ElasticNet(max_iter=10000), elastic_params, cv=5, scoring='r2', n_jobs=-1)
elastic_grid.fit(X_train_sel_scaled, y_train_sel)
print(f"      Mejor alpha: {elastic_grid.best_params_['alpha']}, l1_ratio: {elastic_grid.best_params_['l1_ratio']}")

# Evaluar modelos optimizados
optimized_models = {
    'Ridge (opt)': ridge_grid.best_estimator_,
    'Lasso (opt)': lasso_grid.best_estimator_,
    'ElasticNet (opt)': elastic_grid.best_estimator_
}

print("\n[3.3] Evaluación en conjunto de prueba...")
test_results = {}
for name, model in optimized_models.items():
    y_pred = model.predict(X_test_sel_scaled)
    r2 = r2_score(y_test_sel, y_pred)
    mae = mean_absolute_error(y_test_sel, y_pred)
    test_results[name] = {'R2': r2, 'MAE': mae}
    print(f"   {name}: R² = {r2:.4f}, MAE = {mae:.4f}")

# Seleccionar mejor modelo
best_model_name = max(test_results, key=lambda x: test_results[x]['R2'])
best_model = optimized_models[best_model_name]
best_r2 = test_results[best_model_name]['R2']
best_mae = test_results[best_model_name]['MAE']

print(f"\n✓ Mejor modelo: {best_model_name}")
print(f"   - R²: {best_r2:.4f}")
print(f"   - MAE: {best_mae:.4f}")

# ==============================================================================
# ETAPA 4: ANÁLISIS DE SUPUESTOS
# ==============================================================================

print("\n" + "=" * 80)
print("ETAPA 4: ANÁLISIS DE SUPUESTOS DE REGRESIÓN")
print("=" * 80)

# Predicciones y residuos
y_train_pred_final = best_model.predict(X_train_sel_scaled)
residuals_final = y_train_sel - y_train_pred_final

print("\n[4.1] Verificando normalidad de residuos...")
from scipy.stats import shapiro, jarque_bera

if len(residuals_final) < 5000:
    _, shapiro_p = shapiro(residuals_final)
    print(f"   Shapiro-Wilk p-value: {shapiro_p:.6f}")
    normality_ok = shapiro_p >= 0.05
else:
    _, jb_p = jarque_bera(residuals_final)
    print(f"   Jarque-Bera p-value: {jb_p:.6f}")
    normality_ok = jb_p >= 0.05

if normality_ok:
    print("   ✓ Residuos siguen distribución normal")
else:
    print("   ⚠️  Residuos NO siguen distribución normal")

print("\n[4.2] Verificando homocedasticidad...")
import statsmodels.api as sm
from statsmodels.stats.diagnostic import het_breuschpagan

X_train_const = sm.add_constant(X_train_sel_scaled)
ols_model = sm.OLS(y_train_sel, X_train_const).fit()
_, bp_pvalue, _, _ = het_breuschpagan(ols_model.resid, X_train_const)

print(f"   Breusch-Pagan p-value: {bp_pvalue:.6f}")
if bp_pvalue >= 0.05:
    print("   ✓ Homocedasticidad confirmada")
else:
    print("   ⚠️  Heterocedasticidad presente")

print("\n[4.3] Verificando independencia...")
from statsmodels.stats.stattools import durbin_watson

dw_stat = durbin_watson(residuals_final)
print(f"   Durbin-Watson: {dw_stat:.4f}")
if 1.5 <= dw_stat <= 2.5:
    print("   ✓ No autocorrelación detectada")
else:
    print("   ⚠️  Posible autocorrelación")

# ==============================================================================
# ETAPA 5: VISUALIZACIONES FINALES
# ==============================================================================

print("\n" + "=" * 80)
print("ETAPA 5: GENERANDO VISUALIZACIONES FINALES")
print("=" * 80)

# Crear visualización comprehensiva
fig = plt.figure(figsize=(18, 12))
gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)

# 1. Evolución de características
ax1 = fig.add_subplot(gs[0, 0])
stages = ['Original', 'Engineered', 'Selected']
n_features = [df_original.shape[1], df.shape[1], len(selected_features)]
colors_stages = ['lightblue', 'orange', 'green']
ax1.bar(stages, n_features, color=colors_stages, edgecolor='black', alpha=0.8)
ax1.set_ylabel('Número de Características', fontsize=11)
ax1.set_title('Evolución de Características', fontsize=12, fontweight='bold')
ax1.grid(True, alpha=0.3, axis='y')
for i, v in enumerate(n_features):
    ax1.text(i, v + 2, str(v), ha='center', fontweight='bold')

# 2. Comparación de R²
ax2 = fig.add_subplot(gs[0, 1])
r2_comparison = [r2_base, best_r2_selection, best_r2]
stages_r2 = ['Base', best_selection_method, 'Optimizado']
colors_r2 = ['gray', 'steelblue', 'gold']
ax2.bar(stages_r2, r2_comparison, color=colors_r2, edgecolor='black', alpha=0.8)
ax2.set_ylabel('R² Score', fontsize=11)
ax2.set_title('Mejora del Modelo', fontsize=12, fontweight='bold')
ax2.grid(True, alpha=0.3, axis='y')
for i, v in enumerate(r2_comparison):
    ax2.text(i, v + 0.01, f'{v:.4f}', ha='center', fontweight='bold')

# 3. Comparación de modelos optimizados
ax3 = fig.add_subplot(gs[0, 2])
model_names = list(test_results.keys())
model_r2s = [test_results[m]['R2'] for m in model_names]
colors_models = ['gold' if m == best_model_name else 'steelblue' for m in model_names]
ax3.bar(range(len(model_names)), model_r2s, color=colors_models, edgecolor='black', alpha=0.8)
ax3.set_xticks(range(len(model_names)))
ax3.set_xticklabels(model_names, rotation=45, ha='right')
ax3.set_ylabel('R² Score', fontsize=11)
ax3.set_title('Modelos Optimizados', fontsize=12, fontweight='bold')
ax3.grid(True, alpha=0.3, axis='y')

# 4. Predichos vs Reales
ax4 = fig.add_subplot(gs[1, :2])
y_test_pred_final = best_model.predict(X_test_sel_scaled)
ax4.scatter(y_test_sel, y_test_pred_final, alpha=0.5, s=30, edgecolors='k', linewidths=0.5)
ax4.plot([y_test_sel.min(), y_test_sel.max()], [y_test_sel.min(), y_test_sel.max()],
         'r--', lw=2, label='Predicción Perfecta')
ax4.set_xlabel('Valores Reales', fontsize=11)
ax4.set_ylabel('Valores Predichos', fontsize=11)
ax4.set_title(f'Predicciones Finales (R²={best_r2:.4f})', fontsize=12, fontweight='bold')
ax4.legend()
ax4.grid(True, alpha=0.3)

# 5. Distribución de residuos
ax5 = fig.add_subplot(gs[1, 2])
ax5.hist(residuals_final, bins=50, density=True, alpha=0.7, edgecolor='black', color='steelblue')
mu, sigma = residuals_final.mean(), residuals_final.std()
x = np.linspace(residuals_final.min(), residuals_final.max(), 100)
ax5.plot(x, stats.norm.pdf(x, mu, sigma), 'r-', linewidth=2, label='Normal')
ax5.set_xlabel('Residuos', fontsize=11)
ax5.set_ylabel('Densidad', fontsize=11)
ax5.set_title('Distribución de Residuos', fontsize=12, fontweight='bold')
ax5.legend()
ax5.grid(True, alpha=0.3)

# 6. Residuos vs Predichos
ax6 = fig.add_subplot(gs[2, :2])
ax6.scatter(y_train_pred_final, residuals_final, alpha=0.5, s=20, edgecolors='k', linewidths=0.3)
ax6.axhline(y=0, color='red', linestyle='--', linewidth=2)
ax6.set_xlabel('Valores Predichos', fontsize=11)
ax6.set_ylabel('Residuos', fontsize=11)
ax6.set_title('Análisis de Residuos', fontsize=12, fontweight='bold')
ax6.grid(True, alpha=0.3)

# 7. Q-Q Plot
ax7 = fig.add_subplot(gs[2, 2])
stats.probplot(residuals_final, dist="norm", plot=ax7)
ax7.set_title('Q-Q Plot', fontsize=12, fontweight='bold')
ax7.grid(True, alpha=0.3)

plt.suptitle('Análisis Completo del Modelo de Regresión Lineal',
             fontsize=16, fontweight='bold', y=0.995)

plt.savefig(f'{results_dir}/analisis_completo_final.png', dpi=300, bbox_inches='tight')
print(f"✓ Visualización final guardada")

# ==============================================================================
# GUARDAR MODELO FINAL
# ==============================================================================

print("\n" + "=" * 80)
print("GUARDANDO MODELO FINAL Y METADATOS")
print("=" * 80)

import joblib

# Guardar modelo y scaler
joblib.dump(best_model, f'{results_dir}/modelo_final_optimizado.pkl')
joblib.dump(scaler_sel, f'{results_dir}/scaler_final.pkl')

# Guardar metadatos
metadata = {
    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    'modelo': best_model_name,
    'caracteristicas_originales': df_original.shape[1],
    'caracteristicas_engineered': df.shape[1],
    'caracteristicas_seleccionadas': len(selected_features),
    'metodo_seleccion': best_selection_method,
    'r2_base': r2_base,
    'r2_seleccion': best_r2_selection,
    'r2_final': best_r2,
    'mae_final': best_mae,
    'caracteristicas_usadas': selected_features,
    'supuestos': {
        'normalidad': 'OK' if normality_ok else 'Advertencia',
        'homocedasticidad': 'OK' if bp_pvalue >= 0.05 else 'Advertencia',
        'independencia': 'OK' if 1.5 <= dw_stat <= 2.5 else 'Advertencia'
    }
}

import json
with open(f'{results_dir}/metadata_modelo.json', 'w') as f:
    json.dump(metadata, f, indent=4)

print(f"✓ Modelo guardado: modelo_final_optimizado.pkl")
print(f"✓ Scaler guardado: scaler_final.pkl")
print(f"✓ Metadatos guardados: metadata_modelo.json")

# ==============================================================================
# RESUMEN EJECUTIVO
# ==============================================================================

print("\n" + "=" * 80)
print("RESUMEN EJECUTIVO DEL ANÁLISIS COMPLETO")
print("=" * 80)

report = f"""
📊 DATOS PROCESADOS:
   • Muestras totales: {df.shape[0]}
   • Características originales: {df_original.shape[1]}
   • Características después de ingeniería: {df.shape[1]} (+{df.shape[1] - df_original.shape[1]})
   • Características finales seleccionadas: {len(selected_features)}

🔧 PROCESO DE OPTIMIZACIÓN:
   1. Ingeniería de Características:
      - Transformaciones: {transformations_count}
      - Ratios: {ratios_count}
      - Interacciones: {interactions_count}

   2. Selección de Características:
      - Método utilizado: {best_selection_method}
      - Reducción: {df.shape[1]} → {len(selected_features)} (-{df.shape[1] - len(selected_features)})

   3. Optimización de Modelo:
      - Mejor modelo: {best_model_name}
      - Método: GridSearchCV con validación cruzada 5-fold

📈 RENDIMIENTO DEL MODELO:
   • R² (Base): {r2_base:.4f}
   • R² (Selección): {best_r2_selection:.4f} ({best_r2_selection - r2_base:+.4f})
   • R² (Final): {best_r2:.4f} ({best_r2 - r2_base:+.4f})
   • MAE (Final): {best_mae:.4f}
   • Mejora total: {((best_r2 - r2_base) / r2_base * 100):.2f}%

✅ VALIDACIÓN DE SUPUESTOS:
   • Normalidad: {'✓ Cumple' if normality_ok else '⚠️  No cumple'}
   • Homocedasticidad: {'✓ Cumple' if bp_pvalue >= 0.05 else '⚠️  No cumple'}
   • Independencia: {'✓ Cumple' if 1.5 <= dw_stat <= 2.5 else '⚠️  No cumple'}

📁 ARCHIVOS GENERADOS:
   → {results_dir}/
      • dataset_engineered.csv
      • dataset_selected_features.csv
      • modelo_final_optimizado.pkl
      • scaler_final.pkl
      • metadata_modelo.json
      • analisis_completo_final.png

💡 CONCLUSIONES:
   {'✓ El modelo cumple todos los supuestos y está listo para producción' if all([normality_ok, bp_pvalue >= 0.05, 1.5 <= dw_stat <= 2.5]) else '⚠️  El modelo tiene algunas advertencias en supuestos. Revisar antes de producción.'}

   El modelo explica el {best_r2*100:.2f}% de la varianza en la tasa de mortalidad
   por cáncer, con un error absoluto medio de {best_mae:.2f} puntos.

🎯 PRÓXIMOS PASOS:
   1. Validar el modelo con datos nuevos
   2. Implementar monitoreo de desempeño
   3. Considerar ensembles para mejorar predicciones
   4. Documentar casos de uso y limitaciones
"""

print(report)

# Guardar informe
with open(f'{results_dir}/informe_ejecutivo.txt', 'w') as f:
    f.write("INFORME EJECUTIVO - ANÁLISIS DE REGRESIÓN LINEAL\n")
    f.write("=" * 80 + "\n")
    f.write(report)

print(f"\n✓ Informe ejecutivo guardado: informe_ejecutivo.txt")

print("\n" + "=" * 80)
print("PIPELINE COMPLETADO EXITOSAMENTE")
print("=" * 80)
print(f"Finalizado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"\nTodos los resultados en: {results_dir}/")
print("=" * 80)
