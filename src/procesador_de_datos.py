import pandas as pd
import numpy as np
import re
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

class ProcesadorDatosGastos:
    """
    Clase para procesar y limpiar datos de gastos personales
    """
    
    def __init__(self):
        self.df = None
        self.df_original = None
        
    def cargar_datos(self, ruta_archivo):
        """
        Carga datos desde archivo CSV
        """
        try:
            self.df = pd.read_csv(ruta_archivo)
            self.df_original = self.df.copy()
            print(f"Datos cargados exitosamente: {len(self.df)} transacciones")
            return True
        except Exception as e:
            print(f"Error al cargar datos: {e}")
            return False
    
    def limpiar_datos(self):
        """
        Limpia y prepara los datos
        """
        print("Limpiando datos...")
        
        # Convertir fecha a datetime
        self.df['fecha'] = pd.to_datetime(self.df['fecha'], errors='coerce')
        
        # Eliminar filas con fechas inválidas
        cantidad_antes = len(self.df)
        self.df = self.df.dropna(subset=['fecha'])
        if len(self.df) < cantidad_antes:
            print(f"Eliminadas {cantidad_antes - len(self.df)} filas con fechas inválidas")
        
        # Limpiar montos (remover signos negativos, convertir a float)
        self.df['monto'] = self.df['monto'].abs()  # Todos los gastos son positivos
        self.df['monto'] = pd.to_numeric(self.df['monto'], errors='coerce')
        
        # Eliminar transacciones con montos inválidos o cero
        self.df = self.df[(self.df['monto'] > 0) & (self.df['monto'].notna())]
        
        # Limpiar descripciones
        self.df['descripcion'] = self.df['descripcion'].str.strip().str.upper()
        
        # Detectar y marcar outliers (gastos extremadamente altos)
        q1 = self.df['monto'].quantile(0.25)
        q3 = self.df['monto'].quantile(0.75)
        rango_intercuartil = q3 - q1
        umbral_outlier = q3 + 1.5 * rango_intercuartil
        
        self.df['es_outlier'] = self.df['monto'] > umbral_outlier
        cantidad_outliers = self.df['es_outlier'].sum()
        
        if cantidad_outliers > 0:
            print(f"Detectados {cantidad_outliers} outliers (gastos > ${umbral_outlier:,.2f})")
        
        # Agregar columnas de fecha útiles
        self.df['año'] = self.df['fecha'].dt.year
        self.df['mes'] = self.df['fecha'].dt.month
        self.df['dia_semana'] = self.df['fecha'].dt.dayofweek
        self.df['es_fin_semana'] = self.df['dia_semana'].isin([5, 6])
        
        # Crear período mensual para análisis
        self.df['periodo'] = self.df['fecha'].dt.to_period('M')
        
        print(f"Datos limpios: {len(self.df)} transacciones válidas")
        
    def obtener_estadisticas_resumen(self):
        """
        Obtiene estadísticas resumidas de los datos
        """
        estadisticas = {
            'total_transacciones': len(self.df),
            'gasto_total': self.df['monto'].sum(),
            'gasto_promedio': self.df['monto'].mean(),
            'gasto_mediana': self.df['monto'].median(),
            'fecha_inicio': self.df['fecha'].min(),
            'fecha_fin': self.df['fecha'].max(),
            'categorias_unicas': self.df['categoria'].nunique() if 'categoria' in self.df.columns else 0,
            'outliers': self.df['es_outlier'].sum(),
            'gastos_fin_semana': self.df[self.df['es_fin_semana']]['monto'].sum()
        }
        return estadisticas
    
    def obtener_resumen_mensual(self):
        """
        Obtiene resumen mensual de gastos
        """
        resumen_mensual = self.df.groupby('periodo').agg({
            'monto': ['sum', 'mean', 'count'],
            'categoria': 'nunique'
        }).round(2)
        
        resumen_mensual.columns = ['Total', 'Promedio', 'Transacciones', 'Categorías']
        resumen_mensual = resumen_mensual.sort_index()
        
        return resumen_mensual
    
    def obtener_resumen_categoria(self):
        """
        Obtiene resumen por categoría
        """
        if 'categoria' not in self.df.columns:
            return None
            
        resumen_categoria = self.df.groupby('categoria').agg({
            'monto': ['sum', 'mean', 'count'],
            'fecha': ['min', 'max']
        }).round(2)
        
        resumen_categoria.columns = ['Total', 'Promedio', 'Transacciones', 'Primera', 'Última']
        
        # Calcular porcentaje del total
        total_gastos = self.df['monto'].sum()
        resumen_categoria['Porcentaje'] = (resumen_categoria['Total'] / total_gastos * 100).round(1)
        
        return resumen_categoria.sort_values('Total', ascending=False)
    
    def detectar_patrones(self):
        """
        Detecta patrones en los gastos
        """
        patrones = {}
        
        # Patrones por día de la semana
        patrones_dia = self.df.groupby('dia_semana')['monto'].agg(['sum', 'mean', 'count'])
        nombres_dias = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
        patrones_dia.index = nombres_dias
        patrones['por_dia'] = patrones_dia
        
        # Patrones por mes
        patrones_mes = self.df.groupby('mes')['monto'].agg(['sum', 'mean', 'count'])
        nombres_meses = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun',
                        'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']
        patrones_mes.index = [nombres_meses[i-1] for i in patrones_mes.index]
        patrones['por_mes'] = patrones_mes
        
        # Fin de semana vs días laborables
        comparacion_fin_semana = self.df.groupby('es_fin_semana')['monto'].agg(['sum', 'mean', 'count'])
        comparacion_fin_semana.index = ['Días laborables', 'Fin de semana']
        patrones['fin_semana'] = comparacion_fin_semana
        
        return patrones
    
    def exportar_datos_limpios(self, ruta_salida='gastos_limpios.csv'):
        """
        Exporta los datos limpios
        """
        self.df.to_csv(ruta_salida, index=False)
        print(f"Datos limpios exportados a: {ruta_salida}")

# Ejemplo de uso
if __name__ == "__main__":
    # Crear instancia del procesador
    procesador = ProcesadorDatosGastos()
    
    # Cargar datos (asume que ya tienes el archivo del generador anterior)
    if procesador.cargar_datos('gastos_personales.csv'):
        # Limpiar datos
        procesador.limpiar_datos()
        
        # Mostrar estadísticas
        estadisticas = procesador.obtener_estadisticas_resumen()
        print("\nESTADÍSTICAS GENERALES:")
        print(f"Total de transacciones: {estadisticas['total_transacciones']}")
        print(f"Gasto total: ${estadisticas['gasto_total']:,.2f}")
        print(f"Gasto promedio: ${estadisticas['gasto_promedio']:,.2f}")
        print(f"Gasto mediana: ${estadisticas['gasto_mediana']:,.2f}")
        print(f"Período: {estadisticas['fecha_inicio'].strftime('%Y-%m-%d')} a {estadisticas['fecha_fin'].strftime('%Y-%m-%d')}")
        print(f"Outliers detectados: {estadisticas['outliers']}")
        
        # Resumen mensual
        print("\nRESUMEN MENSUAL:")
        resumen_mensual = procesador.obtener_resumen_mensual()
        print(resumen_mensual.tail())  # Últimos 5 meses
        
        # Resumen por categoría
        print("\nRESUMEN POR CATEGORÍA:")
        resumen_categoria = procesador.obtener_resumen_categoria()
        if resumen_categoria is not None:
            print(resumen_categoria)
        
        # Patrones detectados
        print("\nPATRONES DETECTADOS:")
        patrones = procesador.detectar_patrones()
        
        print("\nGastos promedio por día de la semana:")
        print(patrones['por_dia']['mean'].sort_values(ascending=False))
        
        print("\nComparación fin de semana vs días laborables:")
        print(patrones['fin_semana']['mean'])
        
        # Exportar datos limpios
        procesador.exportar_datos_limpios()