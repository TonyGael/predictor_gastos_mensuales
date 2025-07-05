# predictor_gastos_mensuales
Proyecto: Predictor de Gastos Mensuales. Para práctica de Data Science con daos sintéticos.

Proyecto: Predictor de Gastos Mensuales
Funcionalidades principales:

Cargar datos desde CSV de extractos bancarios
Categorización automática de gastos (comida, transporte, entretenimiento)
Visualizaciones de patrones de gasto por mes/categoría
Predicción simple del gasto del próximo mes
Alertas cuando gastas más de lo normal

Stack tecnológico:

Pandas: manipulación de datos
Matplotlib/Seaborn: gráficos
Scikit-learn: regresión lineal para predicciones
Streamlit: interfaz web simple
Regex: para categorizar transacciones automáticamente

Tareas específicas:

Limpiar datos de transacciones (fechas, montos, descripciones)
Crear reglas para categorizar gastos automáticamente
Calcular estadísticas mensuales (promedio, mediana, desviación)
Implementar regresión lineal para predecir gasto siguiente mes
Crear gráficos de barras, líneas de tiempo y heatmaps

Datos de ejemplo:
Puedes usar datos ficticios o crear un generador de transacciones bancarias simuladas.
Entregables:

Script de limpieza de datos
Función de categorización automática
Dashboard con 4-5 gráficos principales
Modelo predictivo simple
Reporte mensual automatizado

Estructura del proyecto:
expense_analyzer/
├── data/
│   └── gastos_personales.csv
├── src/
│   ├── data_processor.py
│   ├── categorizer.py
│   ├── predictor.py
│   └── visualizer.py
├── app.py (Streamlit dashboard)
├── requirements.txt
└── README.md