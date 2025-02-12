from fastapi import FastAPI, UploadFile, HTTPException
import pandas as pd
import json
from openpyxl import load_workbook
from io import BytesIO

app = FastAPI()

# Ruta al archivo Excel
archivo_excel = "C:/Users/sergio.jimenez/Documents/octopus/Data_octopus.xlsx"

@app.post("/update-excel/")
async def update_excel(file: UploadFile):
    # Verificar que sea un archivo JSON
    if not file.filename.endswith('.json'):
        raise HTTPException(status_code=400, detail="El archivo debe ser un JSON.")

    # Leer y cargar el contenido del archivo JSON
    try:
        nuevas_coordenadas = json.load(BytesIO(await file.read()))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al procesar el JSON: {str(e)}")

    # Leer el archivo Excel existente
    try:
        df_existente = pd.read_excel(archivo_excel, sheet_name="Tabla_plantillas")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"No se pudo leer el archivo Excel: {str(e)}")

    # Obtener el valor máximo de id_plantilla
    max_id_plantilla = df_existente['id_plantilla'].max() if not df_existente.empty else 0

    # Crear un diccionario para las nuevas coordenadas
    plantilla = {
        'id_plantilla': max_id_plantilla + 1,
        'ub_Imagen_1': [],
        'ub_Imagen_2': [],
        'ub_copy': [],
        'ub_legal': [],
        'ub_logo': [],
        'resolucion_output': '1080x608'
    }

    # Procesar las coordenadas
    for rect in nuevas_coordenadas:
        coords = f"{rect['x']:.3f}, {rect['y']:.3f}, {rect['width']:.3f}, {rect['height']:.3f}"
        if rect['type'] == "Imagen 1":
            plantilla['ub_Imagen_1'].append(coords)
        elif rect['type'] == "Imagen 2":
            plantilla['ub_Imagen_2'].append(coords)
        elif rect['type'] == "Titulo":
            plantilla['ub_copy'].append(coords)
        elif rect['type'] == "Legal":
            plantilla['ub_legal'].append(coords)
        elif rect['type'] == "Logo":
            plantilla['ub_logo'].append(coords)

    # Convertir listas a cadenas separadas por ' | '
    for key in ['ub_Imagen_1', 'ub_Imagen_2', 'ub_copy', 'ub_legal', 'ub_logo']:
        plantilla[key] = ' | '.join(plantilla[key])

    # Convertir a DataFrame
    df_nuevas = pd.DataFrame([plantilla])

    # Combinar los DataFrames
    df_combined = pd.concat([df_existente, df_nuevas], ignore_index=True)

    # Guardar el archivo actualizado
    try:
        with pd.ExcelWriter(archivo_excel, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
            df_combined.to_excel(writer, sheet_name="Tabla_plantillas", index=False)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"No se pudo actualizar el archivo Excel: {str(e)}")

    return {"message": "Excel actualizado exitosamente."}

#para iniciar el servidor: uvicorn Pagina_web.app:app --reload
