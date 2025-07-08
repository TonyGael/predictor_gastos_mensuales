import pandas as pd
import re

class CategorizadorGastos:
    """
    Clase para categorizar automáticamebte las transacciooes/gastos
    """
    def __init__(self):
        self.reglas_categoria = self.reglas_categoria = {
            'Comida': [
                r'MERCADO', r'SUPERMERCADO', r'DIETETICA', r'CARNICERIA',r'VERDULERIA',
                r'RESTAURANT', r'PIZZA', r'HAMBURGUESA', r'DELIVERY', r'CAFE', r'PANADERIA'
                ],
            'Transporte': [
                r'UBER', r'TAXI', r'DIDY', r'CABIFY', r'COMBUSTIBLE', r'ESTACIONAMIENTO',
                r'SUBE', r'PEAJE', r'NAFTA', r'COLECTIVO'
                ],
                'Entretenimiento': [
                r'CINE', r'NETFLIX', r'SPOTIFY', r'TEATRO', r'BAR', r'CONCIERTO',
                r'VIDEOJUEGOS', r'JUEGOS', r'STEAM', r'PLAYSTATION'
                ],
            'Servicios': [
                r'EDENOR', r'TELECOM', r'MOVISTAR', r'PERSONAL', r'INTERNET', r'AGUA',
                r'GAS', r'TELEFONO', r'LUZ', r'EXPENSAS', r'ALQUILER'
                ],
            'Salud': [
                r'FARMACIA', r'MEDICO', r'HOSPITAL', r'DENTISTA', r'LABORATORIO',
                r'CONSULTA', r'OBRA SOCIAL', r'PREPAGA'
                ],
            'Compras': [
                r'AMAZON', r'MERCADOLIBRE', r'TIENDA', r'ROPA', r'ELECTRONICA',
                r'ZAPATERIA', r'LIBRERIA', r'DEPORTE'
                ],
            'Educacion': [
                r'CURSO', r'UDEMY', r'PLATZI', r'COLEGIO', r'UNIVERSIDAD', r'LIBROS'
                ],
            'Otros': [
                r'VARIOS', r'DIVERSOS', r'REGALO', r'DONACION'
                ]
            }
    
    def categorizar(self, df):
        """
        categoriza las transacciones de un datafra,e de gasytos.
        Args:
            df (pd.dataframe): dataframe con al menos una columna e descripcón.
            Returns:
                pd.dataframe: el datafra,e con una nueva columna categoria_auto.
        """
        if 'descripcion' not in df.columns:
            print('Error: el DataFrame debe contener la columna "descripcion".')
            return df
        
        df['categoria_auto'] = 'Desconocido'  # categoría por defecto
        
        # vamos a iterar sobre cada categoría y sus reglas
        for categoria, reglas in self.reglas_categoria.items():
            for regla in reglas:
                df.loc[df['descripcion'].str.contains(regla, na=False, regex=True, case=False), 'categoria_auto'] = categoria
        
        if 'gategoria' in df.columns:
            df.local[df['categoria_auto'] == ]