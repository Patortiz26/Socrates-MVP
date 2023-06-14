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
school = st.text_input("Institución Educativa")
# Grade mapping
course_d = {
    "":0,
    "1° básico": 1,
    "2° básico": 2,
    "3° básico": 3,
    "4° básico": 4,
    "5° básico": 5,
    "6° básico": 6,
    "7° básico": 7,
    "8° básico": 8,
    "1° medio": 9,
    "2° medio": 10,
    "3° medio": 11,
    "4° medio": 12,
}

course_label = st.selectbox("Curso", list(course_d.keys()))
course = course_d[course_label]

subject_d = {
    "":0,
    "Matemáticas": "Math",
    "Fisica": "Physics",
    "Biología": "Biology",
    "Química": "Chemistry",
    "Historia": "History",
    "Lenguaje": "Spanish",
}

subject_label = st.selectbox("Asignatura", list(subject_d.keys()))
subject = subject_d[subject_label]

# Subida de archivo
uploaded_file = st.file_uploader("Subir archivo de Excel", type=["xlsx"])

if uploaded_file:
    # Botón de subida de archivo
    
    if st.button('Generar Guía'):
        generate_guide(uploaded_file, course_label, subject_label, name, school)
        st.markdown("### Descargar Guía Generada")
        with open('guide.docx', 'rb') as docx_file:
            st.download_button('Descargar', data=docx_file, file_name='guide.docx')

        st.balloons()
