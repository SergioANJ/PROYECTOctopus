# -*- coding: utf-8 -*-
"""
Created on Mon Jan 13 22:06:21 2025

@author: josel
"""

import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import os
from psd_tools import PSDImage
import time
import pyfiglet
import msvcrt
import numpy as np
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
    
  
# In[ ]:
def generate_image(background_path, imagen_path, logo_path, copy_text, copy_position, image_position, logo_position, legal_text, legal_position, button_path, button_position, output_resolution, output_path):
    ancho, alto = map(int, output_resolution.split('x'))

    background = Image.open(background_path).resize((ancho, alto)).convert("RGBA")

    # Procesar imagen principal
    imagen = Image.open(imagen_path).convert("RGBA")
    imagen = imagen.resize((int(ancho * image_position[2]), int(alto * image_position[3])), Image.LANCZOS)
    imagen_x, imagen_y = int(ancho * image_position[0]), int(alto * image_position[1])
    background.paste(imagen, (imagen_x, imagen_y), imagen)

    # Procesar logo
    logo = Image.open(logo_path).convert("RGBA")
    logo = logo.resize((int(ancho * logo_position[2]), int(alto * logo_position[3])), Image.LANCZOS)
    logo_x, logo_y = int(ancho * logo_position[0]), int(alto * logo_position[1])
    background.paste(logo, (logo_x, logo_y), logo)

    # Procesar botón -> es la imagen 2
    button = Image.open(button_path).convert("RGBA")
    button = button.resize((int(ancho * button_position[2]), int(alto * button_position[3])), Image.LANCZOS)
    button_x, button_y = int(ancho * button_position[0]), int(alto * button_position[1])
    background.paste(button, (button_x, button_y), button)

    # Dibujar o procesar copy_text
    draw = ImageDraw.Draw(background)
    if isinstance(copy_text, str) and copy_text.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".bmp")):
        copy_image = Image.open(copy_text).convert("RGBA")
        copy_image = copy_image.resize((int(ancho * copy_position[2]), int(alto * copy_position[3])), Image.LANCZOS)
        copy_x, copy_y = int(ancho * copy_position[0]), int(alto * copy_position[1])
        background.paste(copy_image, (copy_x, copy_y), copy_image)
    else:
        font_path = r'C:\Windows\Fonts\Arial.ttf'
        font_size = 60
        font = ImageFont.truetype(font_path, font_size)
        text_x, text_y = int(ancho * copy_position[0]), int(alto * copy_position[1])
        for offset in [(0, 0), (1, 0), (0, 1), (1, 1)]:
            draw.text((text_x + offset[0], text_y + offset[1]), copy_text, font=font, fill="White")

    # Dibujar o procesar legal_text
    if isinstance(legal_text, str) and legal_text.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".bmp")):
        legal_image = Image.open(legal_text).convert("RGBA")
        legal_image = legal_image.resize((int(ancho * legal_position[2]), int(alto * legal_position[3])), Image.LANCZOS)
        legal_x, legal_y = int(ancho * legal_position[0]), int(alto * legal_position[1])
        background.paste(legal_image, (legal_x, legal_y), legal_image)
    else:
        font_1 = ImageFont.truetype("arial.ttf", 10)
        legal_x, legal_y = int(ancho * legal_position[0]), int(alto * legal_position[1])
        draw.text((legal_x, legal_y), legal_text, font=font_1, fill="White")

    # Guardar la imagen final
    background.save(output_path)
    print(f"Imagen guardada en {output_path}")

def generate_html(
    copy_text,
    image_src,
    logo_src,
    legal_text,
    legal_position,
    button_src,
#    button_link,
    copy_position,
    image_position,
    logo_position,
    button_position,
):
    html_content = f"""
    <!DOCTYPE html>
    <html>
      <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <title>Email Template</title>
        <style>
          body {{
            margin: 0;
            padding: 0;
            background-color: #ffffff;
          }}
          table {{
            border-collapse: collapse;
            width: 100%;
          }}
          img {{
            display: block;
            max-width: 100%;
            height: auto;
          }}
          .content {{
            max-width: 600px;
            margin: 0 auto;
            text-align: center;
            position: relative;
          }}
          .copy {{
            position: {copy_position};
          }}
          .logo {{
            position: {logo_position};
          }}
          .image {{
            position: {image_position};
          }}
          .legal {{
            position: {legal_position};
            font-size: 11px;
            color: #999;
          }}
          .button {{
            position: {button_position};
          }}
        </style>
      </head>
      <body>
        <div class="content">
          <!-- Logo -->
          <div class="logo">
            <img src="{logo_src}" alt="Logo" />
          </div>

          <!-- Imagen principal -->
          <div class="image">
            <img src="{image_src}" alt="Main Image" />
          </div>

          <!-- Texto -->
          <div class="copy">
            <p>{copy_text}</p>
          </div>

          <!-- Botón -->
          <div class="button">
            <a href="{copy_text}" target="_blank">
              <img src="{button_src}" alt="Button" />
            </a>
          </div>

          <!-- Legal -->
          <div class="legal">
            <p>{legal_text}</p>
          </div>
        </div>
      </body>
    </html>
    """
    return html_content


################ Procesar cada fila del DataFrame
print("Procesando...")
time.sleep(3)  # Espera de 5 segundos
print("Construyendo...")
time.sleep(2)

# In[ ]:

################ Mapeo de columnas desde tablas relacionadas
for index, row in df.iterrows():
    # Obtener IDs desde el dataframe principal (tabla_hechos_random)
    id_mensaje = row['id_mensaje']
    id_back = row['id_back']
    id_imagen_1 = row['id_imagen_1']
    id_logo = row['id_logo']
    id_copy = row['id_copy']
    id_legal = row['id_legal']
    id_imagen_2 = row['id_imagen_2']
    id_plantilla = row['id_plantilla']
    
    background_path = back.loc[back['id_back'] == id_back, 'Background'].values[0]
    imagen_path = imagen1.loc[imagen1['id_imagen_1'] == id_imagen_1, 'Imagen'].values[0]
    logo_path = logo.loc[logo['id_logo'] == id_logo, 'logo'].values[0]
    copy_text = copys.loc[copys['id_copy'] == id_copy, 'copy'].values[0]
    legal_text = legal.loc[legal['id_legal'] == id_legal, 'text'].values[0]
    button_path = imagen2.loc[imagen2['id_imagen_2'] == id_imagen_2, 'Imagen'].values[0]
    
    copy_position = tuple(map(float, plantillas.loc[plantillas['id_plantilla'] == id_plantilla, 'ub_copy'].values[0].split(',')))
    image_position = tuple(map(float, plantillas.loc[plantillas['id_plantilla'] == id_plantilla, 'ub_Imagen_1'].values[0].split(',')))
    logo_position = tuple(map(float, plantillas.loc[plantillas['id_plantilla'] == id_plantilla, 'ub_logo'].values[0].split(',')))
    legal_position = tuple(map(float, plantillas.loc[plantillas['id_plantilla'] == id_plantilla, 'ub_legal'].values[0].split(',')))
    button_position = tuple(map(float, plantillas.loc[plantillas['id_plantilla'] == id_plantilla, 'ub_Imagen_2'].values[0].split(',')))
    output_resolution = plantillas.loc[plantillas['id_plantilla'] == id_plantilla, 'resolucion_output']
    output_resolution = output_resolution.values[0] if not output_resolution.empty else "1080x1920"
    formato = row['formato']
    if formato == "imagen":
        output_path = f'C:\\Users\\sergio.jimenez\\Documents\\octopus\\response\\output_imagen_{index + 1}.png'
        generate_image(
            background_path, imagen_path, logo_path, copy_text, copy_position,
            image_position, logo_position, legal_text, legal_position,
            button_path, button_position, output_resolution, output_path
        )
    elif formato == "html":
        image_src = f'file://{imagen_path}'
        logo_src = f'file://{logo_path}'
        button_src = f'file://{button_path}'
        html_content = generate_html(
            copy_text, image_src, logo_src, legal_text, legal_position,
            button_src,  copy_position, image_position,
            logo_position, button_position
        )
        html_output_path = f'C:\\Users\\sergio.jimenez\\Documents\\octopus\\response\\output_html_{index + 1}.html'
        with open(html_output_path, "w", encoding="utf-8") as html_file:
            html_file.write(html_content)
        print(f"HTML guardado en {html_output_path}")

print("Fin del proceso")

