import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt # necesario para usar en combinacion con st.pyplot()
import seaborn as sns
import os # para manejar rutas de archivos

# importamos las clases de tus scripts en src/
from src.procesador_de_datos import ProcesadorDatosGastos
from src.categorizador import CategorizadorGastos
from src.predictor import PredictorGastos
from src.visualizador import VisualizadorGastos

# configuración inicial de la aplicación Streamlit
st.set_page_config(
    page_title='Dashboard de Gastos Mensuales',
    page_icon='📊',
    layout='wide'
)

st.title('📊 Dashboard de Análisis y Predicción de Gastos')
st.write('Bienvenido a tu asistente personal de finanzas. Carga tus gastos y descubre patrones.')

# --- Rutas de archivos ---
RUTA_DATOS_CSV = 'data/gastos_personales.csv'
RUTA_MODELO = 'modelo_gastos.joblib' # El modelo se guardará en la raíz del proyecto

# --- Función para cargar y procesar datos (con cache para eficiencia) ---
@st.cache_data
def cargar_y_procesar_datos():
    """
    Carga, limpia y categoriza los datos de gastos.
    Usa el decorador de caché de Streamlit para no recalcular si los datos no cambian.
    """
    procesador = ProcesadorDatosGastos()
    if not os.path.exists(RUTA_DATOS_CSV):
        st.error(f'Error: El archivo "{RUTA_DATOS_CSV}" no se encontró.')
        st.warning('Asegúrate de ejecutar el script generador_datos_sinteticos.py primero.')
        return None

    if procesador.cargar_datos(RUTA_DATOS_CSV):
        procesador.limpiar_datos()
        
        categorizador = CategorizadorGastos()
        df_final = categorizador.categorizar(procesador.df.copy()) # Trabajar con una copia
        return df_final
    else:
        st.error('No se pudieron cargar o procesar los datos. Revisa el archivo CSV.')
        return None

# --- Cargar y procesar los datos una vez ---
df_gastos = cargar_y_procesar_datos()

if df_gastos is not None:
    st.success(f'Datos cargados y procesados: {len(df_gastos)} transacciones.')

    # --- Sección de KPIs / Estadísticas Resumen ---
    st.header('📈 Estadísticas Clave')
    
    # Podemos usar el procesador para obtener las estadísticas resumen
    # Instanciamos un procesador temporal para usar su método de resumen
    temp_procesador = ProcesadorDatosGastos()
    temp_procesador.df = df_gastos # Asignamos el df ya procesado
    estadisticas = temp_procesador.obtener_estadisticas_resumen()

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric('Total Transacciones', f'{estadisticas["total_transacciones"]:,}')
    with col2:
        st.metric('Gasto Total', f'${estadisticas["gasto_total"]:,.2f}')
    with col3:
        st.metric('Gasto Promedio por Transacción', f'${estadisticas["gasto_promedio"]:,.2f}')
    with col4:
        st.metric('Período de Datos', f'{estadisticas["fecha_inicio"].strftime("%Y-%m-%d")} a {estadisticas["fecha_fin"].strftime("%Y-%m-%d")}')

    # --- Sección de Análisis por Categoría ---
    st.header('📊 Análisis por Categoría')
    visualizador = VisualizadorGastos() # Instanciar visualizador
    
    # reutilizamos el metodo procesasdor para un reumen tabular
    resumen_categoria_df = temp_procesador.obtener_resumen_categoria()
    if resumen_categoria_df is not None:
        st.subheader('Resumen de Gastos por Categoría')
        st.dataframe(resumen_categoria_df)
    else:
        st.warning('No se pudo generar el resumen por categoría.')
    
    # grafico de barras de categorías llamando a visulaizador.py por ejemplo
    st.subheader('Gráfico de Gastos Totales por Categoría')
    fig_barras = visualizador.generar_grafico_barras_categorias(df_gastos, columna_categoria='categoria_auto')
    if fig_barras:
        st.pyplot(fig_barras) # mostramos el gráfico con Streamlit
        plt.close(fig_barras) # Cerramos la figura para liberar memoria
    else:
        st.warning('no se pudo generar el gráfico de barras por categoría')
    
    # sección analsis temporal
    st.header('PAtrones de gastos temporal')
    
    # gráfico de lenea de gastos mensuales
    st.subheader('Gráfico de gastos mensuales a lo largo del Tiempo')
    fig_linea = visualizador.generar_grafico_linea_mensual(df_gastos)
    if fig_linea:
        st.pyplot(fig_linea)
        plt.close(fig_linea)
    else:
        st.warning('No se pudo generar el gráfico de línea mensual.')
    
    # generamos un heatmap de gastos por mes y categoría
    st.subheader('Gráfico tipo Heatmap de Gastos por Mes y Categoría')
    fig_heatmap = visualizador.generar_heatmap_gastos_por_mes_categoria(df_gastos)
    if fig_heatmap:
        st.pyplot(fig_heatmap)
        plt.close(fig_heatmap)
    else:
        st.warning('No se pudo generar el heatmap de gastos por mes y categoría.')
    
    # generemos un histograma de montos
    st.subheader('Gráfico: Distribución de Montos de Gastos')
    fig_histograma = visualizador.generar_histograma_montos(df_gastos)
    if fig_histograma:
        st.pyplot(fig_histograma)
        plt.close(fig_histograma)
    else:
        st.warning('No se pudo generar el histograma de montos.')
    
    # bloque de código para la predicción de Gastos
    st.header('Predicción de Gastos')
    predictor = PredictorGastos()
    
    # preparamos los datos para el predictor
    df_preparado_pred = predictor.preparar_datos(df_gastos.copy())
    
    if df_preparado_pred is not None and not df_preparado_pred.empty:
        # intentamos cargar el modelo si ya existe
        if not predictor.cargar_modelo(RUTA_MODELO):
            st.info('Modelo no encontrado o error al cargarlo. Entrenando nuevo modelo...')
            # si no se pudo cargar, entrenamos y guardamos el modelo
            if predictor.entrenar_modelo(df_preparado_pred):
                predictor.guardar_modelo(RUTA_MODELO)
            else:
                st.warning('No se pudo entrenar el modelo de predicción, verificar datos.')
        else:
            # si se cargó el modelo, necesitamos pasarle los df_preparado para que la predicción sepa el contexto
            predictor.df_preparado = df_preparado_pred
            
        if predictor.modelo is not None:
            prediccion_proximo_mes = predictor.predecir_siguiente_mes()
            if prediccion_proximo_mes is not None:
                st.subheader('Estimación de Gasto para el Próximo Mes:')
                st.write(f'El gasto predicho es de: **${prediccion_proximo_mes:,.2f}**')
            else:
                st.warning('No se pudo realizar la predicción de gasto.')
        else:
            st.warning('El modelo de predicción no está disponible.')
    else:
        st.warning('No hay suficientes datos procesados para entrenar o usar el modelo de predicción.')
        
    # sección de alertas
    st.header('Alertas Personalizadas')
    st.write(' alertas basadas en patrones de gasto.')

    # ejemplo de alerta simple: si el último mes fue un outlier
    if df_gastos is not None and not df_gastos.empty:
        # calculamos el gasto del último mes
        ultimo_mes_gasto = df_gastos[df_gastos['fecha'].dt.to_period('M') == df_gastos['fecha'].dt.to_period('M').max()]['monto'].sum()
        
        # obtenemos el gasto promedio mensual de todos los datos
        gastos_mensuales_promedio = df_gastos.groupby(df_gastos['fecha'].dt.to_period('M'))['monto'].sum().mean()
        
        if ultimo_mes_gasto > (gastos_mensuales_promedio * 1.2): # si por ejemplo gastó 20% más que el promedio mensual
            st.warning(f'¡Atención! Tu gasto total del último mes ({ultimo_mes_gasto:,.2f}) fue un 20% más alto que tu promedio mensual ({gastos_mensuales_promedio:,.2f}).')
        else:
            st.info('Tus gastos recientes están dentro de lo normal. ¡estamos cuidando el dinero!')
    
    st.markdown('---')
    st.write('Desarrollado por Tony Gael Data Master.')

else:
    st.error('No se pudo iniciar el dashboard. Por favor, revisa los mensajes de error anteriores. O corrige absolutamente todo el código.')