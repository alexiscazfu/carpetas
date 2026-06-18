import streamlit as st
import pandas as pd
import os
import zipfile
import tempfile

st.title("Generador de Carpetas de Universidades")

archivo = st.file_uploader(
    "Cuñis, selecciona el archivo Excel",
    type=["xlsx"]
)

if archivo:

    if st.button("Generar carpetas"):

        with tempfile.TemporaryDirectory() as temp_dir:

            df = pd.read_excel(archivo, header=None)

            for i in range(2, len(df)):

                numero = df.iloc[i, 0]
                universidad = df.iloc[i, 3]

                if pd.isna(numero) or pd.isna(universidad):
                    continue

                nombre = f"{int(numero)}. {str(universidad).strip()}"

                for c in '<>:"/\\|?*':
                    nombre = nombre.replace(c, '')

                os.makedirs(
                    os.path.join(temp_dir, nombre),
                    exist_ok=True
                )

            zip_path = os.path.join(temp_dir, "universidades.zip")

            with zipfile.ZipFile(zip_path, "w") as zipf:
                for carpeta in os.listdir(temp_dir):

                    ruta = os.path.join(temp_dir, carpeta)

                    if os.path.isdir(ruta):
                        zipf.write(ruta, arcname=carpeta + "/")

            with open(zip_path, "rb") as f:

                st.download_button(
                    "Descargar ZIP",
                    data=f,
                    file_name="universidades.zip",
                    mime="application/zip"
                )
