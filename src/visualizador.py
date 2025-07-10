import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

class VisualizadorGastos:
    def __init__(self):
        pass

    def generar_grafico_barras_categorias(self, df, columna_categoria='categoria_auto', titulo='Gastos Totales por Categoría'):
        pass

    def generar_grafico_linea_mensual(self, df, columna_fecha='fecha', columna_monto='monto', titulo='Gastos Mensuales a lo largo del Tiempo'):
        pass

    def generar_heatmap_gastos_por_mes_categoria(self, df, columna_fecha='fecha', columna_categoria='categoria_auto', columna_monto='monto', titulo='Gastos por Mes y Categoría'):
        pass

    def generar_histograma_montos(self, df, columna_monto='monto', bins=30, titulo='Distribución de Montos de Gastos'):
        pass
