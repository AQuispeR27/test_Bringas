# Análisis de Regresión Lineal - Predicción de Mortalidad por Cáncer

Este proyecto implementa un modelo de regresión lineal completo para predecir la tasa de mortalidad por cáncer (`target_deathrate`) utilizando diversas variables socioeconómicas y demográficas.

## 📋 Descripción

El modelo analiza datos de diferentes condados/áreas geográficas para predecir la tasa de mortalidad por cáncer basándose en:

- Variables demográficas (edad, población, distribución racial)
- Variables socioeconómicas (ingresos, pobreza, educación, empleo)
- Variables de salud (cobertura de seguros, incidencia de cáncer)
- Otras variables relevantes (tasa de natalidad, estado civil, etc.)

## 🚀 Características

El script incluye:

✅ **Análisis Exploratorio de Datos (EDA)**
- Estadísticas descriptivas
- Detección de valores nulos
- Distribución de variables

✅ **Preprocesamiento de Datos**
- Imputación de valores nulos
- Codificación de variables categóricas
- Estandarización de características

✅ **Análisis de Correlación**
- Identificación de variables más correlacionadas
- Detección de multicolinealidad
- Visualizaciones de correlaciones

✅ **Entrenamiento del Modelo**
- Regresión lineal con scikit-learn
- División train/test (80/20)
- Estandarización de datos

✅ **Evaluación Exhaustiva**
- MAE (Error Absoluto Medio)
- MSE (Error Cuadrático Medio)
- RMSE (Raíz del Error Cuadrático Medio)
- R² (Coeficiente de Determinación)

✅ **Visualizaciones**
- Gráficos de correlaciones
- Valores reales vs predichos
- Distribución de residuos
- Importancia de variables

✅ **Recomendaciones**
- Análisis de resultados
- Sugerencias de mejora
- Próximos pasos

## 📦 Requisitos

### Librerías necesarias:
```
pandas
numpy
matplotlib
seaborn
scikit-learn
joblib
```

## 🔧 Instalación

### 1. Clonar o descargar este proyecto

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

## 📊 Uso

### 1. Preparar el dataset

Asegúrate de tener el archivo `cancer_reg.csv` en la misma carpeta que el script.

### 2. Ejecutar el análisis

```bash
python cancer_regression_model.py
```

### 3. Resultados generados

El script generará:

**Archivos de salida:**
- `correlaciones_top20.png` - Top 20 variables más correlacionadas
- `matriz_correlacion.png` - Matriz de correlación de variables principales
- `coeficientes_modelo.png` - Importancia de variables según coeficientes
- `evaluacion_modelo.png` - Gráficos de evaluación del modelo
- `residuos_vs_predichos.png` - Análisis de residuos
- `cancer_regression_model.pkl` - Modelo entrenado guardado
- `scaler.pkl` - Scaler guardado para nuevas predicciones

**Salida en consola:**
- Estadísticas del dataset
- Proceso de preprocesamiento
- Análisis de correlaciones
- Métricas de evaluación
- Conclusiones y recomendaciones

## 📈 Interpretación de Resultados

### Métricas principales:

**R² (Coeficiente de Determinación)**
- Rango: 0 a 1 (donde 1 es perfecto)
- Indica qué porcentaje de la varianza explica el modelo
- > 0.7: Modelo bueno
- > 0.9: Modelo excelente

**MAE (Error Absoluto Medio)**
- Error promedio en las mismas unidades que la variable objetivo
- Más bajo = mejor
- Ejemplo: MAE = 5.2 significa que en promedio el error es de ±5.2 en la tasa de mortalidad

**RMSE (Raíz del Error Cuadrático Medio)**
- Penaliza más los errores grandes
- Más bajo = mejor
- Útil para identificar predicciones muy desviadas

## 🔮 Usar el modelo para nuevas predicciones

Una vez entrenado el modelo, puedes usarlo para hacer predicciones:

```python
import joblib
import pandas as pd
import numpy as np

# Cargar el modelo y el scaler
model = joblib.load('cancer_regression_model.pkl')
scaler = joblib.load('scaler.pkl')

# Preparar nuevos datos (debe tener las mismas columnas que X_train)
# nuevos_datos = pd.DataFrame([...])

# Estandarizar
nuevos_datos_scaled = scaler.transform(nuevos_datos)

# Predecir
predicciones = model.predict(nuevos_datos_scaled)
print(f"Tasa de mortalidad predicha: {predicciones[0]:.2f}")
```

## 🎯 Variables del Dataset

### Variable Objetivo:
- **target_deathrate**: Tasa de mortalidad específica por cáncer

### Variables Predictoras:

**Cáncer y Salud:**
- avganncount: Promedio anual de diagnósticos
- avgdeathsperyear: Promedio anual de muertes
- incidencerate: Tasa de incidencia por 100,000 habitantes

**Demográficas:**
- popest2015: Población estimada en 2015
- medianage: Edad mediana
- medianagemale/female: Edad mediana por género
- birthrate: Tasa de natalidad
- pctwhite, pctblack, pctasian, pctotherrace: Distribución racial

**Socioeconómicas:**
- medincome: Ingreso medio
- binnedinc: Rango de ingreso (categórico)
- povertypercent: Porcentaje en pobreza

**Educación:**
- studypercap: Estudios per cápita
- pctnohs18_24: % sin secundaria (18-24)
- pcths18_24: % con secundaria (18-24)
- pctsomecol18_24: % con universidad incompleta (18-24)
- pctbachdeg18_24: % con título universitario (18-24)
- pcths25_over: % con secundaria (25+)
- pctbachdeg25_over: % con título universitario (25+)

**Empleo:**
- pctemployed16_over: % empleados (16+)
- pctunemployed16_over: % desempleados (16+)

**Seguro de Salud:**
- pctprivatecoverage: % con seguro privado
- pctprivatecoveragealone: % con solo seguro privado
- pctempprivcoverage: % empleados con seguro privado
- pctpubliccoverage: % con seguro público
- pctpubliccoveragealone: % con solo seguro público

**Otros:**
- percentmarried: % población casada
- pctmarriedhouseholds: % hogares matrimoniales

## 💡 Sugerencias de Mejora

El script incluye recomendaciones para mejorar el modelo:

1. **Ingeniería de características**: Crear interacciones entre variables
2. **Selección de características**: RFE, Lasso, análisis de VIF
3. **Modelos alternativos**: Ridge, Random Forest, XGBoost, etc.
4. **Validación cruzada**: K-fold cross-validation
5. **Optimización de hiperparámetros**: GridSearchCV

## 🐛 Solución de Problemas

### Error: "No se encontró el archivo 'cancer_reg.csv'"
**Solución:** Asegúrate de que el archivo CSV está en la misma carpeta que el script.

### Error: "ModuleNotFoundError"
**Solución:** Instala las dependencias con `pip install -r requirements.txt`

### Warning: "DeprecationWarning"
**Solución:** Actualiza las librerías a las versiones más recientes.

## 📝 Notas

- El script maneja automáticamente valores nulos
- Las variables categóricas se codifican automáticamente
- Se genera estandarización para mejor rendimiento
- Todos los gráficos se guardan en formato PNG de alta calidad (300 DPI)

## 🤝 Contribuciones

Este es un proyecto educativo. Siéntete libre de:
- Modificar el código según tus necesidades
- Experimentar con diferentes modelos
- Agregar nuevas visualizaciones
- Mejorar el preprocesamiento

## 📄 Licencia

Este proyecto es de código abierto y está disponible para uso educativo y académico.

---

**Desarrollado con ❤️ para análisis de datos de salud pública**
