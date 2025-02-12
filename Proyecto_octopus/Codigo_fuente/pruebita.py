# -*- coding: utf-8 -*-
"""
Created on Mon Jan 13 22:06:21 2025

@author: josel
"""

import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import textwrap
import os
from psd_tools import PSDImage
import time
import pyfiglet
import msvcrt
import numpy as np
import random
ascii_art = pyfiglet.figlet_format("BIENVENIDO A OCTOPUS v0.1")
print(ascii_art)

time.sleep(2)

###################Data_octopus
data = pd.read_excel(r"C:\Users\sergio.jimenez\Documents\octopus\Data_octopus.xlsx", sheet_name="Tabla_octopus")
plantillas = pd.read_excel(r"C:\Users\sergio.jimenez\Documents\octopus\Data_octopus.xlsx", sheet_name="Tabla_plantillas")
back = pd.read_excel(r"C:\Users\sergio.jimenez\Documents\octopus\Data_octopus.xlsx", sheet_name="Dim_back")
imagen1 = pd.read_excel(r"C:\Users\sergio.jimenez\Documents\octopus\Data_octopus.xlsx", sheet_name="Dim_imagen1")
imagen2 = pd.read_excel(r"C:\Users\sergio.jimenez\Documents\octopus\Data_octopus.xlsx", sheet_name="Dim_imagen2")
copys = pd.read_excel(r"C:\Users\sergio.jimenez\Documents\octopus\Data_octopus.xlsx", sheet_name="Dim_copys")
legal = pd.read_excel(r"C:\Users\sergio.jimenez\Documents\octopus\Data_octopus.xlsx", sheet_name="Dim_legal")
logo = pd.read_excel(r"C:\Users\sergio.jimenez\Documents\octopus\Data_octopus.xlsx", sheet_name="Dim_logo")

##################Data_claro
mensaje_claro = pd.read_excel(r"C:\Users\sergio.jimenez\Documents\octopus\Data_octopus.xlsx", sheet_name="Tabla_mensaje")
audiencia_claro = pd.read_excel(r"C:\Users\sergio.jimenez\Documents\octopus\Data_octopus.xlsx", sheet_name="Tabla_audiencia")
variacion_claro = pd.read_excel(r"C:\Users\sergio.jimenez\Documents\octopus\Data_octopus.xlsx", sheet_name="Dim_variacion")
canal_claro = pd.read_excel(r"C:\Users\sergio.jimenez\Documents\octopus\Data_octopus.xlsx", sheet_name="Dim_canal")
oferta_claro = pd.read_excel(r"C:\Users\sergio.jimenez\Documents\octopus\Data_octopus.xlsx", sheet_name="Dim_oferta")

#################Tabla_mensajes_SOLODEMO_SOLODEMO
num_filas = 10 #cantidad de piezas 

################## Generar IDs aleatorios para todas las dimensiones
id_plantilla_random = np.random.choice(plantillas['id_plantilla'], size=num_filas, replace=True) #False si no queremos que se repitan las Img
id_back_random = np.random.choice(back['id_back'], size=num_filas, replace=True)
id_imagen1_random = np.random.choice(imagen1['id_imagen_1'], size=num_filas, replace=True)
id_imagen2_random = np.random.choice(imagen2['id_imagen_2'], size=num_filas, replace=True)
id_copys_random = np.random.choice(copys['id_copy'], size=num_filas, replace=True)
id_legal_random = np.random.choice(legal['id_legal'], size=num_filas, replace=True)
id_logo_random = np.random.choice(logo['id_logo'], size=num_filas, replace=True)


tabla_hechos_random = pd.DataFrame({
    'id_plantilla':id_plantilla_random,
    'id_back': id_back_random,
    'id_imagen_1': id_imagen1_random,
    'id_imagen_2': id_imagen2_random,
    'id_copy': id_copys_random,
    'id_legal': id_legal_random,
    'id_logo': id_logo_random,
})

print(tabla_hechos_random)
tabla_hechos_random['id_mensaje'] = np.arange(1, num_filas + 1)
################# Verificar claves foráneas para cada dimensión
missing_keys = {}

dimensiones = {
    'id_plantilla':plantillas['id_plantilla'],
    'id_back': back['id_back'],
    'id_imagen_1': imagen1['id_imagen_1'],
    'id_imagen_2': imagen2['id_imagen_2'],
    'id_copy': copys['id_copy'],
    'id_legal': legal['id_legal'],
    'id_logo': logo['id_logo']
}

for clave, dimension in dimensiones.items():
    missing_keys[clave] = tabla_hechos_random[~tabla_hechos_random[clave].isin(dimension)]

errores = False
for clave, df_missing in missing_keys.items():
    if not df_missing.empty:
        print(f"Hay claves foráneas en '{clave}' que no coinciden con las dimensiones:")
        print(df_missing)
        errores = True

if not errores:
    print("Todos los valores de las claves coinciden correctamente.")
df = tabla_hechos_random

# In[ ]:

mensaje_claro = pd.merge(mensaje_claro, canal_claro[['id_canal','formato']],how = 'left', on = 'id_canal')
mensaje_claro = pd.merge(mensaje_claro, audiencia_claro[['id_audiencia','AUDIENCIA']],how = 'left', on = 'id_audiencia')

df = pd.merge(df, mensaje_claro[['id_mensaje','id_canal','formato','id_oferta', 'AUDIENCIA','id_var']],how = 'left', on = 'id_mensaje')

print(f"tabla data frame con los valores aleatorios: \n {df}") #Se imprime tod el dataframe
print(df.columns) # Se imprime la lista de columnas del dataframe
#print(df['id_back'])
#df.to_csv('mi_dataframe.csv', index=False)

# Nueva fila como una Serie
# Nueva fila como un DataFrame
new_row = pd.DataFrame({
    'id_plantilla': [13], 'id_back': [4], 'id_imagen_1': [4], 'id_imagen_2': [5], 'id_copy': [4],
    'id_legal': [2], 'id_logo': [4], 'id_mensaje': [6], 'id_canal': [4], 'formato': ["imagen"],
    'id_oferta': [4], 'AUDIENCIA': ["MATCH"], 'id_var': ["A"] 
    })

# Agregar al DataFrame usando pd.concat
df = pd.concat([df, new_row], ignore_index=True)

print(f"tabla data frame con los valores aleatorios: \n {df}") # Se imprime todo el dataframe