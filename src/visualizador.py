import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

class VisualizadorGastos:
    def __init__(self):
        # pass
        # configraciones básicas para los gráficos
        plt.style.use('seaborn-v0_8-drakgrid') # es un estilo visual de seaborn
        # rcParams: Run-Time Configurations Parameters. Parámetros de configuración en tiempo de ejecución
        plt.rcParams['figure.figsize'] = (12, 8) # serrá el tamaño por defecto de las figuras
        plt.rcParams['font.size'] = 10
        plt.rcParams['axes.labelsize'] = 12
        plt.rcParams['axes.titlesize'] = 14
        plt.rcParams['xstick.labelsize'] = 10
        plt.rcParams['ystick.labelsize'] = 10
        plt.rcParams['legend.fontsize'] = 10
        plt.rcParams['figure.titlesize'] = 16
        
    def generar_grafico_barras_categorias(self, df, columna_categoria='categoria_auto', titulo='Gastos Totales por Categoría'):
        # pass
        """
        aqui generamos u gráfico de barras de los gastos totales
        """
        if df is None or df.empty or 'mmonto' not in df.columns or columna_categoria not in df.columns:
            print(f'Error: el DataFRame para el gráfico "{titulo}" es inválido o faltan columnas.')
            return None
        
        fig, ax = plt.subplots() # creamos na figura nueva con sus respectivos ejes x e y ( ax-> axes)
        gastos_por_categoria = df.groupby(columna_categoria)['monto'].sum().sort_values(ascending=False)
        sns.barplot(x=gastos_por_categoria.index, y=gastos_por_categoria.values, palette='viridis', ax=ax)
        ax.set_title(titulo)
        ax.set_xlabel('Categoría')
        ax.set_ylabel('Monto Tolatl ($)')
        plt.xticks(rotation=45, ha='right') # rotamos las etiquetas para mejor lectura
        # aca iría plt.show() normalmente pero no mostraremos el gráfico
        # ya que retornaremos el objeto figura
        print(f'Gráfico "{titulo}" generado con éxito.')
        return fig

    def generar_grafico_linea_mensual(self, df, columna_fecha='fecha', columna_monto='monto', titulo='Gastos Mensuales a lo largo del Tiempo'):
        # pass
        """
        Genera un gráfico lineal de lso gastos mensuales
        """
        if df is None or df.empty or columna_fecha not in df.columns or columna_monto not in df.columns:
            return None
        
        df_temp = df.copy()
        df_temp[columna_fecha] = pd.to_datetime(df[columna_fecha], errors='corce')
        df_temp.dropna(subset=[columna_fecha], inplace=True)
        
        gastos_mensuales = df_temp.groupby(df_temp[columna_fecha].dt.to_period('M'))[columna_monto].sum()
        
        if gastos_mensuales.empty:
            print(f'Advertencia: no hay datos suficientes oara generar el gráfico "{titulo}".')
            return None
        
        fig, ax = plt.subplots()
        sns.lineplot(x=gastos_mensuales.index.astype(str), y = gastos_mensuales.values, marker='o', color='darkblue', ax=ax)
        ax.set_title(titulo)
        ax.set_xlabel('Mes')
        ax.set_ylabel('Monto total ($)')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        # plt.show()
        print(f'Gráfico "{titulo} preparado.')
        return fig

    def generar_heatmap_gastos_por_mes_categoria(self, df, columna_fecha='fecha', columna_categoria='categoria_auto', columna_monto='monto', titulo='Gastos por Mes y Categoría'):
        # pass
        """
        Genera un heatmap de los gastos totales por mes y categoría.
        """
        if df is None or df.empty or columna_fecha not in df.columns or columna_categoria not in df.columns or columna_monto not in df.columns:
            print(f'Errir, el DataFRame para el grñafico "{titulo}" es inválido o faltan columnas.')
            return None
        
        df_temp = df.copy()
        df_temp[columna_fecha] = pd.to_datetime(df_temp[columna_fecha], errors='coerce')
        df_temp.dropna(subset=[columna_fecha], inplace = True)
        df_temp['mes_numero'] = df_temp[columna_fecha].dt.month
        
        pivot_data = df_temp.pivot_table(
            values=columna_monto,
            index=columna_categoria,
            columns='mes_numero',
            aggfunc='sum',
            fill_value=0
        )
        
        if pivot_data.empty:
            print(f'Advertencia: No hay datos suficientes para generar el gráfico "{titulo}".')
            return None
        
        nombres_meses = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']
        columnas_actuales = pivot_data.columns.tolist()
        nuevas_columnas = [nombres_meses[i-1] for i in columnas_actuales if i-1 < len(nombres_meses)]
        
        if len(nuevas_columnas) == len(columnas_actuales):
            pivot_data.columns = nuevas_columnas
        else:
            print("Advertencia: No se pudieron asignar nombres de meses a todas las columnas del heatmap.")
        
        fig, ax = plt.subplots()
        sns.heatmap(pivot_data, annot=True, fmt='.0f', cmap='YlGnBu', linewidths=.5, ax=ax)
        ax.set_title(titulo)
        ax.set_xlabel('Mes')
        ax.set_ylabel('Categoría')
        plt.tight_layout()
        # plt.show()
        print(f'Gráfico "{titulo}" preparado.')
        return fig

    def generar_histograma_montos(self, df, columna_monto='monto', bins=30, titulo='Distribución de Montos de Gastos'):
        # pass
        """
        Genera un histograma de la distribución de los montos de gastos.
        """
        if df is None or df.empty or columna_monto not in df.columns:
            print(f'Error: El DAtaFrame para el gráfico "{titulo}" es inválido o falta la columna de monto.')
            return None
                
        if df[columna_monto].isnull().all():
            print(f'Advertencia: La columna "{columna_monto}" está vacía o contiene solo valores nulos para el gráfico "{titulo}".')
            return None

        fig, ax = plt.subplots()
        sns.histplot(df[columna_monto], bins=bins, kde=True, color='skyblue', ax=ax)
        ax.set_title(titulo)
        ax.set_xlabel('Monto ($)')
        ax.set_ylabel('Frecuencia')
        plt.tight_layout()
        # plt.show()
        print(f'Gráfico "{titulo}" preparado.')
        return fig
