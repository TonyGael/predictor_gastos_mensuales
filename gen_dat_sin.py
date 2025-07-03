import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import random
from datetime import datetime, timedelta

# configuramos una semilla de reproducibilidad
np.random.seed(42)
random.seed(42)

def generador_datos_gastos(fecha_inicio='2023-01-01', fecha_fin='2024-12-31', num_transacciones=1000):
    """
    Generamos datos sintéticos (ficticios) de gastos personales.
    """

    # Categorías de gastos típicas:
    categorias = {
        'Comida': {
            'keywords': ['MERCADO', 'SUPERMERCADO', 'RESTAURANT', 'DELIVERY', 'CAFE', 'PANADERIA'],
            'rango_gasto': (500, 15000),
            'frecuencia_gasto': 0.35  # 35% de las transacciones
        },
        'Transporte': {
            'keywords': ['UBER', 'TAXI', 'COMBUSTIBLE', 'ESTACIONAMIENTO', 'SUBE', 'PEAJE'],
            'rango_gasto': (200, 8000),
            'frecuencia_gasto': 0.20
        },
        'Entretenimiento': {
            'keywords': ['CINE', 'NETFLIX', 'SPOTIFY', 'TEATRO', 'BAR', 'CONCIERTO'],
            'rango_gasto': (1000, 12000),
            'frecuencia_gasto': 0.15
        },
        'Servicios': {
            'keywords': ['EDENOR', 'TELECOM', 'INTERNET', 'AGUA', 'GAS', 'TELEFONO'],
            'rango_gasto': (3000, 25000),
            'frecuencia_gasto': 0.10
        },
        'Salud': {
            'keywords': ['FARMACIA', 'MEDICO', 'HOSPITAL', 'DENTISTA', 'LABORATORIO'],
            'rango_gasto': (1500, 30000),
            'frecuencia_gasto': 0.08
        },
        'Compras': {
            'keywords': ['AMAZON', 'MERCADOLIBRE', 'TIENDA', 'ROPA', 'ELECTRONICA'],
            'rango_gasto': (2000, 50000),
            'frecuencia_gasto': 0.12
        }
    }
    
    # Generamos unas fechas aleatorias entre fecha_inicio y fecha_fin
    inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d')
    fin = datetime.strptime(fecha_fin, '%Y-%m-%d')

    transacciones = []

    for i in range(num_transacciones):
        # fecha aleatoria
        fecha_aleatoria = inicio + timedelta(days=random.randint(0, (fin - inicio).days))
        
        # seleccionamos una categoría basandoos en la frecuencia de gasto
        categoria = np.random.choice(
            list(categorias.keys()),
            p=[cat['frecuencia_gasto'] for cat in categorias.values()]  # CORREGIDO: frecuencia_gasto
        )

        # generamos una desripción
        keyword = random.choice(categorias[categoria]['keywords'])
        descripcion = f'{keyword} {random.randint(1000, 9999)}'

        # generamos un monto aleatorio basado en el rango de gasto
        monto_min, monto_max = categorias[categoria]['rango_gasto']
        cantidad = np.random.uniform(monto_min, monto_max)

        # agregamos un mes con mas gastos
        if fecha_aleatoria.month == 12:
            cantidad *= 1.3
        elif fecha_aleatoria.month in [6, 7]:  # CORREGIDO: espaciado en la lista
            cantidad *= 1.2
        
        transacciones.append({
            'fecha': fecha_aleatoria.strftime('%Y-%m-%d'),
            'descripcion': descripcion,
            'monto': round(cantidad, 2),
            'categoria': categoria
        })

    # CORREGIDO: Movido fuera del bucle for
    # creamos el dataframe
    df = pd.DataFrame(transacciones)
    df = df.sort_values('fecha').reset_index(drop=True)
    
    return df

# generamos los datos
print('Generando datos sintéticos...')
df_gastos = generador_datos_gastos(num_transacciones=1200)

# mostramos las primeras 10 filas
print('\nPrimeras 10 transacciones:')
print(df_gastos.head(10))

# algunas estadísticas básicas
print(f'\nTotal de transacciones: {len(df_gastos)}')
print(f'Rango de fechas: {df_gastos["fecha"].min()} - {df_gastos["fecha"].max()}')
print(f'Gasto total: ${df_gastos["monto"].sum():,.2f}')
print(f'Gasto promedio por transacción: ${df_gastos["monto"].mean():.2f}')

# Distribución por categoría
print('\nDistribución por categoría:')
resumen_categorias = df_gastos.groupby('categoria').agg({
    'monto': ['count', 'sum', 'mean']
}).round(2)
resumen_categorias.columns = ['Cantidad', 'Total', 'Promedio']
print(resumen_categorias)

# Guardar datos
df_gastos.to_csv('gastos_personales.csv', index=False)
print("\nDatos guardados en 'gastos_personales.csv'")

# Visualización rápida
plt.figure(figsize=(12, 8))

# Gráfico 1: Gastos por categoría
plt.subplot(2, 2, 1)
total_categorias = df_gastos.groupby('categoria')['monto'].sum().sort_values(ascending=False)
plt.bar(total_categorias.index, total_categorias.values)
plt.title('Gastos Totales por Categoría')
plt.xticks(rotation=45)
plt.ylabel('Monto ($)')

# Gráfico 2: Gastos mensuales
plt.subplot(2, 2, 2)
df_gastos['fecha'] = pd.to_datetime(df_gastos['fecha'])
gastos_mensuales = df_gastos.groupby(df_gastos['fecha'].dt.to_period('M'))['monto'].sum()
plt.plot(gastos_mensuales.index.astype(str), gastos_mensuales.values, marker='o')
plt.title('Gastos Mensuales')
plt.xticks(rotation=45)
plt.ylabel('Monto ($)')

# Gráfico 3: Distribución de montos
plt.subplot(2, 2, 3)
plt.hist(df_gastos['monto'], bins=30, alpha=0.7)
plt.title('Distribución de Montos')
plt.xlabel('Monto ($)')
plt.ylabel('Frecuencia')

# Gráfico 4: Heatmap gastos por mes y categoría
plt.subplot(2, 2, 4)
df_gastos['mes'] = df_gastos['fecha'].dt.month
pivot_data = df_gastos.pivot_table(values='monto', index='categoria', columns='mes', aggfunc='sum', fill_value=0)
sns.heatmap(pivot_data, annot=True, fmt='.0f', cmap='YlOrRd')
plt.title('Gastos por Mes y Categoría')

plt.tight_layout()
plt.show()

print("\n¡Datos generados exitosamente!")