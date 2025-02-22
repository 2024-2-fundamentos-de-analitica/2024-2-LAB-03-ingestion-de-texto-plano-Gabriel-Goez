"""
Escriba el codigo que ejecute la accion solicitada en cada pregunta.
"""

# pylint: disable=import-outside-toplevel


import pandas as pd
import re

PATH = 'files/input/clusters_report.txt'

        
def pregunta_01():
    """
    Construya y retorne un dataframe de Pandas a partir del archivo
    'files/input/clusters_report.txt'. Los requierimientos son los siguientes:

    - El dataframe tiene la misma estructura que el archivo original.
    - Los nombres de las columnas deben ser en minusculas, reemplazando los
      espacios por guiones bajos.
    - Las palabras clave deben estar separadas por coma y con un solo
      espacio entre palabra y palabra.


    """

    with open(PATH, 'r') as archivo:
        lineas = archivo.readlines()

    contenido = ''.join(lineas)
    contenido = re.split(r'\-{5,}', contenido)[1].strip()
    filas = contenido.split('\n')

    data = []
    fila_actual = []

    for fila in filas:
      if re.match(r'^\s*\d', fila):
        if fila_actual:

          data.append(fila_actual)
        fila_actual = re.split(r'\s{2,}', fila.strip())

      else:
          fila_actual[-1] += ' ' + fila.strip()
    data.append(fila_actual)
  
    data_limpiada = []

    for row in data:
      if len(row) == 4:
        data_limpiada.append(row)
      else:
        cluster, cantidad, porcentaje, *keywords = row
        keywords = ' '.join(keywords)
        data_limpiada.append([cluster, cantidad, porcentaje, keywords])

    columns = ['cluster', 'cantidad_de_palabras_clave', 'porcentaje_de_palabras_clave', 'principales_palabras_clave']
    df = pd.DataFrame(data_limpiada, columns=columns)
    
    # Limpiar el DataFrame
    df['cluster'] = df['cluster'].astype(int)
    df['cantidad_de_palabras_clave'] = df['cantidad_de_palabras_clave'].astype(int)
    df['porcentaje_de_palabras_clave'] = df['porcentaje_de_palabras_clave'].str.replace('%', '').str.replace(',', '.').astype(float)
    df['principales_palabras_clave'] = df['principales_palabras_clave'].str.replace('\s+', ' ', regex=True).str.replace(' ,', ',', regex=False).str.replace('\s*,\s*', ', ', regex=True)
    
    # Convertir las palabras clave a una cadena separada por comas y quitar el punto final
    df['principales_palabras_clave'] = df['principales_palabras_clave'].apply(lambda x: ', '.join([item.strip() for item in x.split(',')]).rstrip('.'))
    return df



    
df = pregunta_01()

print(df)

