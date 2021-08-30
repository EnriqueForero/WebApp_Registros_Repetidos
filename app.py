# Main library to make the Web application.
import streamlit as st
import streamlit.components as stc
from streamlit_lottie import st_lottie
# Library to manipulate data.
import pandas as pd
import numpy as np
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go 
import matplotlib.pyplot as plt
import missingno as msno
# Utils
import base64 
import time
import requests
timestr = time.strftime("%Y%m%d-%H%M%S")

pd.options.plotting.backend = "plotly"

##################################################################################
# Let's give our app a title
st.title("Aplicación Web para identificar registros repetidos y únicos")
# Let's create a sidebar
st.sidebar.header("Comparación de nombres")

from PIL import Image # We put an image
img = Image.open("ProColombia.png") # Open the saved image.
st.sidebar.image(img, width=200) # It is indicated that it goes on the side.


##################################################################################

# Interactivity with the user
opciones_analisis = ['Introducción', "Análisis de nombres", 'VEIN - Analítica'] # And a drop-down list with the analyzes to show.


analisis_seleccionado = st.sidebar.selectbox('Por favor, seleccione una de las opciones de la lista:', opciones_analisis) # The list of drop down options is placed in this part.

# The first thing is to create the introduction section.
if analisis_seleccionado == 'Introducción': # Logic to assign what to display.
    st.header("Introducción")
    
    st.header("Autores: Coordinación De Analítica")
    st.markdown("Vicepresidencia de Estrategia Internacional e Innovación [ProColombia](https://procolombia.co)")
    st.subheader("Bienvenidos")

    text = """
    Con este aplicativo podrá subir un archivo ".CSV" para encontrar los registros que estén repetidos.
    
    Para iniciar, por favor, `Seleccione` en la barra lateral izquierda la opción "Análisis de nombres" de la lista desplegable.    
    
    """
    st.markdown(text) 

##################################################################################    

elif analisis_seleccionado == "Análisis de nombres": # Un mapa en Dash
    st.subheader("Sección para subir archivo")
    
    
    def load_lottieurl(url: str):
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()

    lottie_airplane = load_lottieurl('https://assets4.lottiefiles.com/packages/lf20_jhu1lqdz.json')
    st_lottie(lottie_airplane, speed=1, height=200, key="initial")


    import Algoritmo # Here is all the code to compare the names
    
    
    #----------------------------------------------------------------------------------------
    #st.subheader("Aquí puede ver algunas gráficas")   

 
    #st.markdown("Miremos cómo está la información.")
    
            
    
    #Mostrando el DataFrame 
    #st.dataframe(df_A)    
   
    
    # Security can be added as a password for access.  
    
##################################################################################
elif analisis_seleccionado == "VEIN - Analítica": 
    st.header("Coordinación de Analítica - VEIN")
    
    text = """
    La Coordinación de Analítica formula, ejecuta y hace seguimiento a proyectos de impacto y alta complejidad, liderando ejercicios de ciencia de datos, con el fin de generar valor a los diferentes clientes a través del aprovechamiento de la información, la generación de insights y orientando la toma de decisiones estratégicas.
"   
    
    """
    st.markdown(text) 
