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


    import streamlit as st
    import pandas as pd
    import recordlinkage as rl
    import missingno as msno

    st.markdown("El archivo a analizar debe contener al menos las siguientes variables con esos mismos nombres")
    st.write(pd.DataFrame({'Nombres de las variables': ['NAME','FIRSTNAME','LASTNAME','EMAIL','CITY']}))

    file = st.file_uploader('Por favor, suba su archivo de Excel guardado en formato “.CSV” ', type="csv") 
    if file is not None: 
        df_A = pd.read_csv(file, encoding= 'unicode_escape') 
    else: 
        st.stop()

    text = """
    La siguiente Tabla muestra los primeros cinco (5) registros de la información que acaba de subir.
    """
    st.markdown(text) # Display text    
    st.write(df_A.head()) # Print the first five observations 

    df_A.to_csv( "Base_a_analizar.csv", encoding='unicode_escape') 


    #----------------------------------------------------------------------------------------

    df_A['Orden'] = df_A.index

    from cleanco import prepare_terms, basename
    from cleanco import cleanco
    from cleanco import prepare_terms, basename

    # Creating a new variables named "Nombre Ajustado" using the basic process to clean "NAME".
    df_A['Nombre ajustado'] = df_A['NAME'].apply(lambda x: cleanco(x).clean_name() if type(x)==str else x)

    dfA = df_A.copy()


    # Since we don't have a variable to make a block, let's create one
    dfA["bloque"] = "Grupo único"

    # In order not to generate so many matches, we use a variable by which to group and in which the observations must be identical. In this case the variable is "Unique group"
    import recordlinkage 
    indexer = recordlinkage.Index()
    indexer.block('bloque') # The argument ‘given_name’ is the blocking variable.
    candidate_links = indexer.index(dfA)

    # Checking out the number of links that were created
    st.markdown("Cantidad de filas del archivo subido " + str(len(df_A)) + ". Se harán " 
                + str(len(candidate_links)) + " comparaciones" )
    # (1000*1000-1000)/2 = 499500

    st.markdown(" #### Por favor, espere unos segundos mientras se muestran los resultados #### " )
    st.markdown("")
    
    st.subheader("Aquí encontrará los registros únicos y las coincidencias")

    compare_cl = recordlinkage.Compare()

    compare_cl.exact('LASTNAME', 'LASTNAME', label='LASTNAME')
    compare_cl.string('Nombre ajustado', 'Nombre ajustado', method='levenshtein', threshold=0.85, label='Nombre ajustado')
    compare_cl.string('FIRSTNAME', 'FIRSTNAME', method='jarowinkler', threshold=0.85, label='FIRSTNAME')
    compare_cl.string('NAME', 'NAME', method='levenshtein', threshold=0.85, label='NAME')
    compare_cl.string('EMAIL', 'EMAIL', method='damerau_levenshtein', threshold=0.85, label='EMAIL')
    compare_cl.exact('CITY', 'CITY', label='CITY')

    features = compare_cl.compute(candidate_links, dfA)

    # We are going to take the observations that have more than 3 criteria that passed the validation. 
    matches = features[features.sum(axis=1) > 2]

    # Sum columns
    matches['Total'] = matches.apply(lambda x: x.sum(), axis=1)

    # Convert the indexes into variables to be able to do the match.
    reset_df = matches.reset_index()

    # Rename columns
    reset_df = reset_df.rename({'level_0': 'Orden_A', 'level_1': 'Orden_B'}, axis=1)

    # Copy
    df_merge = df_A.copy()
    #df_merge.shape

    # Make a merge to understand which one there is a match with.
    df_merge = pd.merge( df_A , reset_df[['Orden_A', 'Orden_B', 'Total' ]] , how = 'left' , 
                  left_on = [ 'Orden' ] , right_on = [ 'Orden_A' ])

    # Unique Record Count
    df_merge["Total"].isna().sum()

    df_valores_unidos = df_merge[df_merge['Total'].isnull()]
    #st.markdown("df_valores_unidos.shape " + str(df_valores_unidos.shape))

    # Utils
    import base64 
    import time
    timestr = time.strftime("%Y%m%d-%H%M%S")

    # This is the function to download the files to CSV.
    def csv_downloader(data, mensaje):
        csvfile = data.to_csv()
        b64 = base64.b64encode(csvfile.encode()).decode()
        new_filename = "new_text_file_{}_.csv".format(timestr)
        st.markdown(mensaje)
        href = f'<a href="data:file/csv;base64,{b64}" download="{new_filename}">¡Hacer clic aquí!</a>'
        st.markdown(href,unsafe_allow_html=True)

    # Checking the number of links that were created
    st.markdown("La cantidad de registros únicos son " + str(len(df_valores_unidos)) 
                + ", esto representa el  " + str(len(df_valores_unidos)/len(df_A)) + " del total analizado.")
    
    st.markdown("Se encontraron " + str(df_merge.shape[0]) + " coincidencias entre los registros." )
    st.markdown("")
    
    csv_downloader(df_valores_unidos, "#### Descargar registros únicos ###") # Using the function to download the data. 

    st.markdown("")
    #st.markdown("Tabla con los registros")
    #st.dataframe(df_merge) # Show the DataFrame. # Here I must reference the DataFrame with the results.
    csv_downloader(df_merge, "#### Descargar las coincidencias entre los registros ###") #  
    st.markdown("Las coincidencias entres los registros se da entre pares con las variables `Orden_A` y `Orden_B` las cuales indican la ubicación de las observaciones, siendo cero la primera.")


    st.balloons()
    
    
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
    st.markdown(text) #Para mostrar el texto   
    
    
