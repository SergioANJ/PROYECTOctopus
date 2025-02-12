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
import random
import sys


ascii_art = pyfiglet.figlet_format("BIENVENIDO A OCTOPUS V0.1")
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
num_filas = 30 #cantidad de piezas 

################## Generar IDs aleatorios para todas las dimensiones
# Excluir el id_plantilla 13
plantillas_excluidas = plantillas[~plantillas['id_plantilla'].isin([13,15])]
id_plantilla_random = np.random.choice(plantillas_excluidas['id_plantilla'], size=num_filas, replace=True) #False si no queremos que se repitan las Img
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

print(f"tabla data frame con los valores aleatorios: \n {df}")
print(df.columns)

#Agregamos una fila con los valores fijos para crear, se puede eliminar lo que es new_row hastaa el print que dice, 
#se imprime todo el dataframe
"""
new_row_1 = pd.DataFrame({
    'id_plantilla': [13], 'id_back': [4], 'id_imagen_1': [4], 'id_imagen_2': [5], 'id_copy': [4],
    'id_legal': [2], 'id_logo': [4], 'id_mensaje': [6], 'id_canal': [4], 'formato': ["imagen"],
    'id_oferta': [4], 'AUDIENCIA': ["MATCH"], 'id_var': ["A"] 
    })
  
new_row_2 = pd.DataFrame({
    'id_plantilla': [10], 'id_back': [2], 'id_imagen_1': [2], 'id_imagen_2': [2], 'id_copy': [2],
    'id_legal': [1], 'id_logo': [2], 'id_mensaje': [6], 'id_canal': [4], 'formato': ["imagen"],
    'id_oferta': [4], 'AUDIENCIA': ["MATCH"], 'id_var': ["A"] 
    })

new_row_3 = pd.DataFrame({
    'id_plantilla': [15], 'id_back': [5], 'id_imagen_1': [6], 'id_imagen_2': [6], 'id_copy': [5],
    'id_legal': [3], 'id_logo': [6], 'id_mensaje': [6], 'id_canal': [4], 'formato': ["imagen"],
    'id_oferta': [4], 'AUDIENCIA': ["MATCH"], 'id_var': ["A"] 
    })

# Agregar al DataFrame usando pd.concat
df = pd.concat([df, new_row_1, new_row_2, new_row_3], ignore_index=True)
"""
print(f"tabla data frame con los valores aleatorios: \n {df}") # Se imprime todo el dataframe

def check_overlap(new_coords, existing_coords):
    new_x1, new_y1, new_x2, new_y2 = new_coords
    for (x1, y1, x2, y2) in existing_coords:
        if (new_x1 < x2 and new_x2 > x1 and new_y1 < y2 and new_y2 > y1):
            return True
    return False

def resize_and_crop(image_path, target_size):
    # Abre la imagen
    img = Image.open(image_path)
    
    # Calcula la relación de aspecto
    img_ratio = img.width / img.height
    target_ratio = target_size[0] / target_size[1]

    # Redimensiona la imagen manteniendo la proporción
    if img_ratio > target_ratio:
        new_height = target_size[1]
        new_width = int(new_height * img_ratio)
    else:
        new_width = target_size[0]
        new_height = int(new_width / img_ratio)

    # Redimensiona la imagen
    img = img.resize((new_width, new_height), Image.LANCZOS)

    # Recorta la imagen al tamaño objetivo
    left = (new_width - target_size[0]) / 2
    top = (new_height - target_size[1]) / 2
    right = (new_width + target_size[0]) / 2
    bottom = (new_height + target_size[1]) / 2

    img = img.crop((left, top, right, bottom))

    return img

def round_corners(image, min_radius=1, max_radius=1):
    """
    Redondea las esquinas de una imagen.
    :param image: La imagen a la que se le aplicará el redondeo.
    :param radius: El radio de redondeo.
    :return: La imagen con esquinas redondeadas.
    """
    radius =  random.randint(min_radius, max_radius)
    # Crea una máscara con las esquinas redondeadas
    rounded_mask = Image.new('L', image.size, 0)
    draw = ImageDraw.Draw(rounded_mask)
    draw.rounded_rectangle((0, 0, image.size[0], image.size[1]), radius, fill=255)
    
    # Aplica la máscara a la imagen
    rounded_image = Image.new('RGBA', image.size)
    rounded_image.paste(image, (0, 0), rounded_mask)
    
    return rounded_image

def resize_and_pad(image_path, target_size, background_color=(255, 255, 255, 0)):
    # Esta función se usará para las otras imágenes
    img = Image.open(image_path)
    
    # Calcula la relación de aspecto
    img_ratio = img.width / img.height
    target_ratio = target_size[0] / target_size[1]

    # Redimensiona la imagen manteniendo la proporción
    if img_ratio > target_ratio:
        new_width = target_size[0]
        new_height = int(new_width / img_ratio)
    else:
        new_height = target_size[1]
        new_width = int(new_height * img_ratio)

    # Redimensiona la imagen
    img = img.resize((new_width, new_height), Image.LANCZOS)

    # Crea una nueva imagen con el color de fondo
    new_image = Image.new("RGBA", target_size, background_color)
    
    # Calcula la posición para centrar la imagen
    left = (target_size[0] - new_width) // 2
    top = (target_size[1] - new_height) // 2

    # Pega la imagen redimensionada en la nueva imagen
    new_image.paste(img, (left, top))

    return new_image

from PIL import Image, ImageDraw, ImageFont

def generate_image(background_path, imagen_path, logo_path, copy_text, copy_position, image_position, logo_position, legal_text, legal_position, button_path, button_position, output_resolution, output_path):
    from PIL import Image, ImageDraw, ImageFont
    ancho, alto = map(int, output_resolution.split('x'))

    # Cargar y redimensionar el fondo
    background = Image.open(background_path).resize((ancho, alto)).convert("RGBA")

    # Lista para almacenar las coordenadas de las imágenes ya dibujadas
    existing_image_coords = []

    # Procesar imagen principal
    imagen = resize_and_crop(imagen_path, (int(ancho * image_position[2]), int(alto * image_position[3])))
    imagen = round_corners(imagen)  # Aplicar redondeo de esquinas
    imagen_x = int(ancho * image_position[0])
    imagen_y = int(alto * image_position[1])
    new_coords = (imagen_x, imagen_y, imagen_x + imagen.width, imagen_y + imagen.height)

    # Verificar superposición
    if not check_overlap(new_coords, existing_image_coords):
        background.paste(imagen, (imagen_x, imagen_y), imagen)
        existing_image_coords.append(new_coords)  # Agregar coordenadas a la lista
    else:
        print(f"Superposición detectada para la imagen principal en {new_coords}. Ajustando posición...")

    # Procesar botón
    button = resize_and_pad(button_path, (int(ancho * button_position[2]), int(alto * button_position[3])))
    button = button.convert("RGBA")  # Asegúrate de que la imagen tenga un canal alfa
    button_x, button_y = int(ancho * button_position[0]), int(alto * button_position[1])
    background.paste(button, (button_x, button_y), button)

    # Procesar logo
    logo = resize_and_pad(logo_path, (int(ancho * logo_position[2]), int(alto * logo_position[3])))
    logo = logo.convert("RGBA")  # Asegúrate de que la imagen tenga un canal alfa
    logo_x, logo_y = int(ancho * logo_position[0]), int(alto * logo_position[1])
    background.paste(logo, (logo_x, logo_y), logo)


    # Resto del código para dibujar el texto y guardar la imagen...
    draw = ImageDraw.Draw(background)
    if isinstance(copy_text, str) and copy_text.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".bmp")):
        copy_image = resize_and_pad(copy_text, (int(ancho * copy_position[2]), int(alto * copy_position[3])))
        copy_x, copy_y = int(ancho * copy_position[0]), int(alto * copy_position[1])
        background.paste(copy_image, (copy_x, copy_y), copy_image)
    else:
        # Ajustar texto para que encaje dentro del cuadro
        #font_path = r'C:\Windows\Fonts\Arialbd.ttf'
        font_path = r'C:\USERS\SERGIO.JIMENEZ\APPDATA\LOCAL\MICROSOFT\WINDOWS\Fonts\AMX-BOLD.TTF'
        x1 = int(ancho * copy_position[0])
        y1 = int(alto * copy_position[1])
        x2 = x1 + int(ancho * copy_position[2])
        y2 = y1 + int(alto * copy_position[3])
        box_coords = (x1, y1, x2, y2)

        def draw_text_within_box(draw, text, font_path, box_coords, fill="White"):
            x1, y1, x2, y2 = box_coords
            box_width = x2 - x1
            box_height = y2 - y1

            # Tamaño inicial de la fuente
            font_size = 60
            min_font_size = 40  # Tamaño mínimo permitido de la fuente
            font = ImageFont.truetype(font_path, font_size)

            # Ajustar el tamaño de la fuente para que quepa en el ancho del cuadro
            while font.getbbox(text)[2] > box_width and font_size > min_font_size:
                font_size -= 1
                font = ImageFont.truetype(font_path, font_size)

            # Dividir el texto en líneas para que encaje en el alto del cuadro
            lines = []
            words = text.split()
            current_line = ""
            for word in words:
                test_line = f"{current_line} {word}".strip()
                if font.getbbox(test_line)[2] <= box_width:
                    current_line = test_line
                else:
                    lines.append(current_line)
                    current_line = word
            if current_line:
                lines.append(current_line)

            # Reducir aún más el tamaño de la fuente si el texto no encaja en la altura
            while len(lines) * font.getbbox("A")[3] > box_height and font_size > min_font_size:
                font_size -= 1
                font = ImageFont.truetype(font_path, font_size)
                # Recalcular líneas con el nuevo tamaño de fuente
                lines = []
                current_line = ""
                for word in words:
                    test_line = f"{current_line} {word}".strip()
                    if font.getbbox(test_line)[2] <= box_width:
                        current_line = test_line
                    else:
                        lines.append(current_line)
                        current_line = word
                if current_line:
                    lines.append(current_line)

            # Dibujar las líneas centradas dentro del cuadro
            line_height = font.getbbox("A")[3]
            total_text_height = len(lines) * line_height
            y_offset = y1 + (box_height - total_text_height) // 2

            for line in lines:
                text_width = font.getbbox(line)[2]
                x_offset = x1 + (box_width - text_width) // 2
                draw.text((x_offset, y_offset), line, font=font, fill=fill)
                y_offset += line_height

        draw_text_within_box(draw, copy_text, font_path, box_coords, fill="White")

    

    # Dibujar o procesar legal_text
    if isinstance(legal_text, str) and legal_text.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".bmp")):
        legal_image = resize_and_pad(legal_text, (int(ancho * legal_position[2]), int(alto * legal_position[3])))
        legal_x, legal_y = int(ancho * legal_position[0]), int(alto * legal_position[1])
        background.paste(legal_image, (legal_x, legal_y), legal_image)
    else:
        font_1 = ImageFont.truetype("arial.ttf", 10)
        legal_x, legal_y = int(ancho * legal_position[0]), int(alto * legal_position[1])
        draw.text((legal_x, legal_y), legal_text, font=font_1, fill="White")

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
