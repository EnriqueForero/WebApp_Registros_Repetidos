# Libreria principal para hacer la aplicación Web. 
import streamlit as st
import streamlit.components as stc
from streamlit_lottie import st_lottie
# Libreria para manipular datos. 
import pandas as pd
# Libreria para hacer cálculos numéricos
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

# La siguiente línea invoca un módulo de pandas. Cambia Default para que quede plotly. 
pd.options.plotting.backend = "plotly"

##################################################################################
# Démosle un título a nuestra aplicación
st.title("Aplicación Web para identificar registros repetidos y únicos")
# Creemos una barra lateral
st.sidebar.header("Comparación de nombres")

from PIL import Image # Le ponemos una imagen
img = Image.open("ProColombia.png") # Abre la imagen guardada. 
st.sidebar.image(img, width=200) #Se le indica que va en la parte lateral. 


##################################################################################

#Interactividad con el usuario
opciones_analisis = ['Introducción', "Análisis de nombres", 'VEIN - Analítica'] # Y una lista desplegable con los análisis a mostrar. 


analisis_seleccionado = st.sidebar.selectbox('Por favor, seleccione una de las opciones de la lista:', opciones_analisis) # La lista de opciones desplegables se coloca en esta parte. 

# Lo primero es crear el análisis de bienvenida. 
if analisis_seleccionado == 'Introducción': #Lógica para asignar lo que se va a mostrar. 
    st.header("Introducción")
    
    st.header("Autores: Coordinación De Analítica")
    st.markdown("Vicepresidencia de Estrategia Internacional e Innovación [ProColombia](https://procolombia.co)")
    st.subheader("Bienvenidos")

    text = """
    Con este aplicativo podrá subir un archivo de formato ".CSV" para encontrar los registros que estén repetidos.
    Por favor, `Seleccione` el archivo sobre el que va a trabajar.
    
    Para iniciar, por favor, seleccione en la barra lateral izquierda la opción "Análisis de nombres" de la lista desplegable.    
    
    """
    st.markdown(text) #Para mostrar el texto   

##################################################################################    
    #Sección número dos.  
elif analisis_seleccionado == "Análisis de nombres": # Un mapa en Dash
    st.subheader("Sección para subir archivo")
    
    
    def load_lottieurl(url: str):
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()

    lottie_airplane = load_lottieurl('https://assets4.lottiefiles.com/packages/lf20_jhu1lqdz.json')
    st_lottie(lottie_airplane, speed=1, height=200, key="initial")

    
    
    file = st.file_uploader('Por favor, suba su archivo de Excel en formato “.CSV” ', type="csv") 
    if file is not None: 
        df_A = pd.read_csv(file, encoding= 'unicode_escape') 
    else: 
        st.stop()

    text = """
    La siguiente Tabla muestra los primeros cinco (5) registros de la información que acaba de subir.
    """
    st.markdown(text) #Para mostrar el texto      
    st.write(df_A.head()) # Imprimir las primeras 5 filas del archivo. 
    
    df_A.to_csv( "Base_a_analizar.csv", encoding='unicode_escape') 
    

    #----------------------------------------------------------------------------------------
    
    st.subheader("Aquí encontrará los registros únicos")
    
    text = """
    En esta sección encuentra los registros no repetidos
    """
    st.markdown(text) #Para mostrar el texto    
  
    text = """
    Archivo con registros no repetidos
    """
    st.markdown(text) #Para mostrar el texto   
        
    import Algoritmo # Aquí está toda la programación para comparar los nombres
    
    
    #----------------------------------------------------------------------------------------
    #st.subheader("Aquí puede ver algunas gráficas")   

 
    #st.markdown("Miremos cómo está la información.")
    
            
    
    #Mostrando el DataFrame 
    #st.dataframe(df_A)    
   
    
    # Se puede añadir seguridad como clave para acceso.   
    
##################################################################################
elif analisis_seleccionado == "VEIN - Analítica": 
    st.header("Coordinación de Analítica - VEIN")
    
    text = """
    La Coordinación de Analítica formula, ejecuta y hace seguimiento a proyectos de impacto y alta complejidad, liderando ejercicios de ciencia de datos, con el fin de generar valor a los diferentes clientes a través del aprovechamiento de la información, la generación de insights y orientando la toma de decisiones estratégicas.
"   
    
    """
    st.markdown(text) #Para mostrar el texto   
    
    