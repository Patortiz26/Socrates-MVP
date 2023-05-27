import streamlit as st
import pandas as pd
from functions import *

# Título
st.title("Generador de Material Educativo con IA")

# Descripción
st.write("¡Bienvenido! Este asistente de IA te ayuda a generar guías y pruebas para tus alumnos. \n\nPara que el modulo funcione correctamente recuerde que debe configurar el documento excel de ejemplo tal como se le fue indicado.")
st.write("Esta herramienta está en desarrollo, por lo que las funcionalidades son limitadas. En caso de tener algún problema o sugerencia, favor contactar al autor.")
st.write("Autor : Patricio Ortiz - \nEmail de contacto: [patricio.ortiz.v@ug.uchile.cl](mailto:patricio.ortiz.v@ug.uchile.cl)")

# Entrada del usuario
st.subheader("Información del Usuario")
name = st.text_input("Nombre del Profesor")
school = st.text_input("Institución educativa")
course = st.selectbox("Curso \n\n Modulo en desarrollo, favor sólo elegir una de las opciones indicadas", ['', 'primaria', 'secundaria'])
subject = st.text_input("Asignatura \n\nModulo en desarrollo, favor escribir asignatura en inglés.")

# Subida de archivo
uploaded_file = st.file_uploader("Subir archivo de Excel", type=["xlsx"])

if uploaded_file:
    # Botón de subida de archivo
    
    if st.button('Generar Guía'):
        generate_guide(uploaded_file, course, subject, name, school)
        st.markdown("### Descargar Guía Generada")
        with open('guide.docx', 'rb') as docx_file:
            st.download_button('Descargar', data=docx_file, file_name='guide.docx')

        st.balloons()
