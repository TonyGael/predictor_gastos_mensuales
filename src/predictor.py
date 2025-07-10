import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error
import joblib
class PredictorGastos:
    def __init__(self):
        # pass
        def __init__(self):
            self.modelo = None # aquí se almacenará el modelo entrenado
            self.df_preparado = None # DataFrame con datos preparados para el modelo

    def preparar_datos(self, df):
        # pass
        if df is None or df.empty:
            print('Error: DataFrame vacío o nulo para preparar los datos.')
            return None
        if 'fecha' not in df.columns or 'monto' not in df.columns:
            print('Error: el DataFra,e debe contener las columnas "fecha" y "monto"')
            return None
        
        # 2fecha2 debe ser del tipo datetimw y se agrega un 'período' mensual
        df['fecha'] = pd.to_datetime(df['fecha'], errors='coerce')
        df = df.dropna(subset=['fecha'])
        df['periodo'] = df['fecha'].dt.to_period('M')
        
        # agregamos gastos por mes
        gastos_mensuales = df.groupby('peridodo')['monto'].sum().reset_index()
        gastos_mensuales.columns = ['periodo', 'gasto_total_mensual']
        
        # conertimos el período a una representación numérica
        # lo que es útil y neecsario para la regresión lineal temporal
        gastos_mensuales['mes_numerico'] = (gastos_mensuales['periodo'] - gastos_mensuales['periodo'].min()).apply(lambda x: x.n)
        
        self.df_preparado = gastos_mensuales
        print(f'Datos preparados para la predicción. Hay {len(self.df_preparado)} meses de datos.')

    def entrenar_modelo(self, df_preparado=None):
        # pass
        if df_preparado is None:
            df_preparado = self.df_preparado
        
        if df_preparado is None or df_preparado.empty:
            print('Error: no hay datos preparados para entrenarel modelo.')
            return False
        
        # características variables independientes (X) y la variable objetivo o variable predicha (y)
        X = df_preparado[['mes_numerico']]
        y = df_preparado['gasto_total_mensual']
        
        # entrenamos el modelo con los datos disponibles
        self.modelo = LinearRegression()
        self.modelo.fit(X, y)
        
        print('Modelo de regresión lineal entrenado con exito')
        
        y_pred = self.modelo.predict(X)
        mean_abs_error = mean_absolute_error(y, y_pred)
        rmse = np.sqrt(mean_squared_error(y, y_pred)) # RMSE o Error Cuadrático Medio (Root Mean Square Error en inglés)
        print(f'MAE ( Error Absoluto Medio) en datos de entrenamiento: ${mean_abs_error:,.2f}')
        print(f'RMSE ( Raíz del Error Cuadrático Medio) en datos de entrenamiento: ${rmse:,.2f}')
        
        return True

    def predecir_siguiente_mes(self):
        # pass
        if self.modelo is None:
            print('Error: El modelo no ha sido entrenado')
            return None
        if self.df_preparado is None or self.df_preparado.empty:
            print('Error: no hay datos preparados paar realizar la predicción.')
            return None
        
        # calculamos el 'mes_numerico' del mes entrante
        ultimo_mes_numerico = self.df_preparado['mes_numerico'].max()
        siguiente_mes_numerico = ultimo_mes_numerico + 1
        
        # realizamos la predicción
        prediccion = self.modelo.predict([[siguiente_mes_numerico]])[0]
        
        # obtenemos el período del siguiente mes para mostrarlo
        periodo_base = self.df_preparado['periodo'].min()
        siguiente_periodo = periodo_base + siguiente_mes_numerico
        
        print(f'Gasto predicho para el perídodo {siguiente_periodo}: ${prediccion:,.2f}')
        
        return prediccion

    def guardar_modelo(self, ruta='data/modelo_gastos.joblib'):
        # pass
        if self.modelo:
            joblib.dump(self.modelo, ruta)
            print(f'Modelo guardado en "{ruta}"')
        else:
            print('No existe un modelo para guardar.')

    def cargar_modelo(self, ruta='modelo_gastos.joblib'):
        # pass
        try:
            self.modelo = joblib.load(ruta)
            print(f'Modelo cargado desde "{ruta}".')
            return True
        except FileNotFoundError:
            print(f'Error: archivi de modelo no encontradi en "{ruta}"')
            return False
        except Exception as e:
            print(f'Error al cargar el modelo: {e}')
            return False
