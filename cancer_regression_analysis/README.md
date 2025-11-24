# Análisis Avanzado de Regresión Lineal - Predicción de Mortalidad por Cáncer

Este proyecto implementa un **sistema completo y profesional** de análisis de regresión lineal para predecir la tasa de mortalidad por cáncer (`target_deathrate`) utilizando técnicas avanzadas de ciencia de datos y machine learning.

## 📋 Descripción

El proyecto analiza datos de diferentes condados/áreas geográficas para predecir la tasa de mortalidad por cáncer utilizando:

- Variables demográficas (edad, población, distribución racial)
- Variables socioeconómicas (ingresos, pobreza, educación, empleo)
- Variables de salud (cobertura de seguros, incidencia de cáncer)
- Técnicas avanzadas de ingeniería y selección de características
- Validación cruzada y optimización de hiperparámetros
- Verificación de supuestos estadísticos

## 🎯 Estructura del Proyecto

```
cancer_regression_analysis/
├── README.md                              # Este archivo
├── requirements.txt                       # Dependencias del proyecto
│
├── generate_sample_data.py                # Generador de datos sintéticos
│
├── cancer_regression_model.py             # Modelo básico de regresión lineal
├── predict_new_data.py                    # Script para hacer predicciones
│
├── feature_engineering.py                 # Ingeniería de características avanzada
├── feature_selection.py                   # Selección de características (RFE, Lasso, VIF)
├── validation_optimization.py             # Validación cruzada y optimización
├── regression_assumptions.py              # Verificación de supuestos estadísticos
│
└── advanced_pipeline_complete.py          # Pipeline completo integrado (⭐ RECOMENDADO)
```

## 🚀 Características Principales

### 🔰 Análisis Básico
- ✅ Exploración de datos (EDA)
- ✅ Preprocesamiento completo
- ✅ Análisis de correlación
- ✅ Entrenamiento de modelo básico
- ✅ Evaluación con métricas estándar (MAE, MSE, RMSE, R²)
- ✅ Visualizaciones profesionales

### 🎓 Análisis Avanzado

#### 1️⃣ **Ingeniería de Características** (`feature_engineering.py`)
- Transformaciones logarítmicas y de raíz cuadrada para variables asimétricas
- Creación de ratios y proporciones entre variables relacionadas
- Generación de interacciones entre variables importantes
- Características polinomiales (grado 2)
- Análisis de asimetría (skewness) de variables

#### 2️⃣ **Selección de Características** (`feature_selection.py`)
- **RFE** (Recursive Feature Elimination)
- **Regularización Lasso** (L1) para selección automática
- **Regularización Ridge** (L2) para reducir overfitting
- **Análisis VIF** (Variance Inflation Factor) para detectar multicolinealidad
- Comparación cuantitativa de métodos

#### 3️⃣ **Validación y Optimización** (`validation_optimization.py`)
- **K-Fold Cross-Validation** (5 folds)
- **GridSearchCV** para búsqueda de hiperparámetros óptimos
- Detección y análisis de outliers (Z-score)
- Comparación de múltiples modelos (Linear, Ridge, Lasso, ElasticNet, Random Forest)
- Evaluación del impacto de outliers en el modelo

#### 4️⃣ **Análisis de Supuestos** (`regression_assumptions.py`)
- ✓ **Linealidad**: Relación lineal entre variables
- ✓ **Homocedasticidad**: Varianza constante (Test de Breusch-Pagan)
- ✓ **Normalidad**: Distribución normal de residuos (Shapiro-Wilk, Jarque-Bera, K-S)
- ✓ **Independencia**: No autocorrelación (Test de Durbin-Watson)
- ✓ **Multicolinealidad**: Análisis VIF completo
- ✓ **Puntos Influyentes**: Cook's Distance, DFFITS, Leverage

#### 5️⃣ **Pipeline Completo** (`advanced_pipeline_complete.py`) ⭐
- **Ejecución automática** de todo el análisis en secuencia
- **Informe ejecutivo** con resultados consolidados
- **Metadatos del modelo** guardados en JSON
- **Visualización comprehensiva** de todo el proceso
- **Modelo final optimizado** listo para producción

## 📦 Requisitos

### Librerías necesarias:
```
pandas>=1.5.0
numpy>=1.23.0
matplotlib>=3.6.0
seaborn>=0.12.0
scikit-learn>=1.2.0
joblib>=1.2.0
scipy>=1.9.0
statsmodels>=0.14.0
```

## 🔧 Instalación

### 1. Navegar al directorio del proyecto

```bash
cd cancer_regression_analysis
```

### 2. Crear un entorno virtual (recomendado)

**En Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**En Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

## 📊 Guía de Uso

### Opción A: Pipeline Completo (⭐ RECOMENDADO)

Para ejecutar **todo el análisis avanzado** de una sola vez:

```bash
# 1. Generar datos de ejemplo (si no tienes cancer_reg.csv)
python generate_sample_data.py

# 2. Ejecutar pipeline completo
python advanced_pipeline_complete.py
```

**Esto ejecutará automáticamente:**
1. Ingeniería de características
2. Selección de características
3. Validación cruzada
4. Optimización de hiperparámetros
5. Verificación de supuestos
6. Generación de informe ejecutivo

**Resultados generados en:** `resultados_analisis_avanzado/`

### Opción B: Análisis Paso a Paso

Para ejecutar cada etapa individualmente:

```bash
# 1. Análisis básico
python cancer_regression_model.py

# 2. Ingeniería de características
python feature_engineering.py

# 3. Selección de características
python feature_selection.py

# 4. Validación y optimización
python validation_optimization.py

# 5. Análisis de supuestos
python regression_assumptions.py
```

### Opción C: Solo Análisis Básico

```bash
# Modelo de regresión lineal básico
python cancer_regression_model.py

# Hacer predicciones con el modelo
python predict_new_data.py
```

## 📈 Salidas Generadas

### 🎨 Visualizaciones

El proyecto genera múltiples visualizaciones profesionales en alta calidad (300 DPI):

**Análisis Básico:**
- `correlaciones_top20.png` - Top 20 variables correlacionadas
- `matriz_correlacion.png` - Heatmap de correlaciones
- `coeficientes_modelo.png` - Importancia de variables
- `evaluacion_modelo.png` - Métricas del modelo
- `residuos_vs_predichos.png` - Análisis de residuos

**Análisis Avanzado:**
- `analisis_asimetria.png` - Skewness de variables
- `transformaciones_comparacion.png` - Antes/después de transformaciones
- `nuevas_caracteristicas_correlacion.png` - Correlación de nuevas features
- `analisis_vif.png` - Multicolinealidad
- `lasso_coeficientes.png` - Features seleccionadas por Lasso
- `comparacion_metodos_seleccion.png` - RFE vs Lasso vs Ridge
- `validacion_cruzada.png` - Resultados de K-Fold CV
- `analisis_outliers.png` - Detección de outliers
- `optimizacion_resultados_finales.png` - Comparación de modelos optimizados
- `supuesto_linealidad.png` - Verificación de linealidad
- `supuesto_homocedasticidad.png` - Test de varianza constante
- `supuesto_normalidad.png` - Q-Q plot y tests de normalidad
- `supuesto_independencia.png` - Autocorrelación
- `analisis_influencia.png` - Cook's Distance y leverage
- `analisis_completo_final.png` - Dashboard comprehensivo

### 💾 Archivos de Datos

- `cancer_reg.csv` - Dataset original
- `cancer_reg_engineered.csv` - Con características mejoradas
- `cancer_reg_selected_features.csv` - Características seleccionadas
- `selected_features.txt` - Lista de features seleccionadas

### 🤖 Modelos Guardados

- `cancer_regression_model.pkl` - Modelo básico
- `scaler.pkl` - Scaler del modelo básico
- `best_model_optimized.pkl` - Mejor modelo tras optimización
- `scaler_optimized.pkl` - Scaler optimizado
- `modelo_final_optimizado.pkl` - Modelo final del pipeline completo
- `scaler_final.pkl` - Scaler final

### 📄 Reportes

- `informe_ejecutivo.txt` - Resumen completo del análisis
- `metadata_modelo.json` - Metadatos del modelo final

## 🎯 Interpretación de Resultados

### Métricas de Evaluación

| Métrica | Rango | Interpretación |
|---------|-------|----------------|
| **R²** | 0-1 | % de varianza explicada. >0.7 bueno, >0.9 excelente |
| **MAE** | ≥0 | Error promedio en unidades de la variable objetivo |
| **RMSE** | ≥0 | Error penalizando grandes desviaciones |
| **MSE** | ≥0 | Error cuadrático medio |

### Tests Estadísticos

| Test | Hipótesis Nula | p-value > 0.05 |
|------|----------------|----------------|
| **Shapiro-Wilk** | Residuos son normales | ✓ No rechazar |
| **Jarque-Bera** | Residuos son normales | ✓ No rechazar |
| **Breusch-Pagan** | Homocedasticidad | ✓ No rechazar |
| **Durbin-Watson** | No autocorrelación | DW ≈ 2 es óptimo |

### Variance Inflation Factor (VIF)

- **VIF < 5**: Multicolinealidad baja ✓
- **VIF 5-10**: Multicolinealidad moderada ⚠️
- **VIF > 10**: Multicolinealidad alta ❌ (eliminar variable)

## 🔮 Usar el Modelo para Predicciones

```python
import joblib
import pandas as pd

# Cargar modelo final optimizado
model = joblib.load('resultados_analisis_avanzado/modelo_final_optimizado.pkl')
scaler = joblib.load('resultados_analisis_avanzado/scaler_final.pkl')

# Preparar nuevos datos (con las mismas características que en entrenamiento)
nuevos_datos = pd.DataFrame([{
    'incidencerate': 450.0,
    'povertypercent': 15.5,
    'medincome': 45000,
    # ... resto de características
}])

# Estandarizar y predecir
datos_scaled = scaler.transform(nuevos_datos)
prediccion = model.predict(datos_scaled)

print(f"Tasa de mortalidad predicha: {prediccion[0]:.2f}")
```

## 🎯 Variables del Dataset

### Variable Objetivo
- **target_deathrate**: Tasa de mortalidad específica por cáncer (muertes por 100,000 habitantes)

### Variables Predictoras (Original)

**Salud:**
- avganncount, avgdeathsperyear, incidencerate

**Demográficas:**
- popest2015, medianage, medianagemale, medianagefemale, birthrate
- pctwhite, pctblack, pctasian, pctotherrace

**Socioeconómicas:**
- medincome, binnedinc, povertypercent

**Educación:**
- studypercap, pctnohs18_24, pcths18_24, pctsomecol18_24, pctbachdeg18_24
- pcths25_over, pctbachdeg25_over

**Empleo:**
- pctemployed16_over, pctunemployed16_over

**Seguro:**
- pctprivatecoverage, pctprivatecoveragealone, pctempprivcoverage
- pctpubliccoverage, pctpubliccoveragealone

**Otros:**
- percentmarried, pctmarriedhouseholds, geography

### Variables Creadas (Ingeniería de Características)

**Transformaciones:**
- `variable_log`: Transformación logarítmica
- `variable_sqrt`: Transformación de raíz cuadrada
- `variable_squared`: Características cuadráticas

**Ratios:**
- `mortality_rate_ratio`: avgdeathsperyear / avganncount
- `cancer_per_capita`: Casos por cada 100,000 habitantes
- `education_ratio`: pctbachdeg25_over / pcths25_over
- `employment_ratio`: pctemployed16_over / pctunemployed16_over
- `insurance_ratio`: pctprivatecoverage / pctpubliccoverage
- `racial_diversity_index`: Índice de diversidad (Herfindahl)

**Interacciones:**
- `poverty_income_int`: povertypercent × medincome
- `age_incidence_int`: medianage × incidencerate
- Y muchas más...

## 💡 Mejores Prácticas

### Para Obtener el Mejor Modelo:

1. **Ejecuta el pipeline completo** primero para obtener una línea base
2. **Revisa el informe ejecutivo** para identificar áreas de mejora
3. **Verifica los supuestos** - si alguno falla, considera:
   - Transformaciones adicionales de variables
   - Modelos robustos a violaciones de supuestos
   - Eliminación de outliers influyentes
4. **Experimenta con diferentes hiperparámetros** usando el código de optimización
5. **Valida con datos nuevos** antes de poner en producción

### Flujo de Trabajo Recomendado:

```
1. generate_sample_data.py (si no tienes datos)
2. advanced_pipeline_complete.py (análisis completo)
3. Revisar resultados_analisis_avanzado/informe_ejecutivo.txt
4. Ajustar según recomendaciones
5. Usar modelo_final_optimizado.pkl para predicciones
```

## 🐛 Solución de Problemas

| Problema | Solución |
|----------|----------|
| No se encuentra cancer_reg.csv | Ejecuta `python generate_sample_data.py` |
| ModuleNotFoundError | `pip install -r requirements.txt` |
| Memoria insuficiente | Reduce número de características o usa muestreo |
| R² muy bajo | Revisa correlaciones, prueba más ingeniería de features |
| Supuestos no cumplen | Considera transformaciones o modelos no-lineales |

## 📚 Referencias y Recursos

### Documentación de Librerías:
- [scikit-learn](https://scikit-learn.org/)
- [pandas](https://pandas.pydata.org/)
- [statsmodels](https://www.statsmodels.org/)

### Conceptos Clave:
- [Regresión Lineal](https://es.wikipedia.org/wiki/Regresi%C3%B3n_lineal)
- [Regularización L1/L2](https://scikit-learn.org/stable/modules/linear_model.html)
- [Validación Cruzada](https://scikit-learn.org/stable/modules/cross_validation.html)
- [VIF y Multicolinealidad](https://en.wikipedia.org/wiki/Variance_inflation_factor)

## 🤝 Contribuciones

Este proyecto es educativo y open-source. Contribuciones bienvenidas:

- 🐛 Reportar bugs
- ✨ Proponer nuevas features
- 📖 Mejorar documentación
- 🎨 Añadir visualizaciones

## 📄 Licencia

Proyecto de código abierto disponible para uso educativo y académico.

---

## 🎓 Créditos

**Desarrollado como proyecto educativo avanzado de Ciencia de Datos**

Técnicas implementadas:
- Feature Engineering Avanzado
- Feature Selection (RFE, Lasso, Ridge)
- Cross-Validation & Hyperparameter Tuning
- Statistical Assumptions Testing
- Influence Analysis (Cook's D, DFFITS, Leverage)

---

**¿Tienes preguntas? Revisa el código - está completamente documentado en español** 🇪🇸
