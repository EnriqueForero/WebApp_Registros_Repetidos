"""2021-08-22 Clean and compare names 
*AUthor: Enrique Forero*
*Date: 2021-08-19*
"""
"""### ✅ Main libraries """
import streamlit as st
import pandas as pd
import recordlinkage as rl
import missingno as msno

"""# ⏯ Main Code

### ✅ 0.1. Install all required libraries:
"""

"""### ✅ I.1 Upload files - Excel"""

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

st.subheader("Aquí encontrará los registros únicos")

text = """
En esta sección encuentra los registros no repetidos
"""
st.markdown(text)   

text = """
Archivo con registros no repetidos
"""
st.markdown(text)   


df_A['Orden'] = df_A.index


"""# ⏯ **I. Clean names**

#### 🟡 I.2.a Libraries
"""

from cleanco import prepare_terms, basename
from cleanco import cleanco
from cleanco import prepare_terms, basename

"""#### 🟡 I.2.e Creating the column "Nombre Ajustado" """

# Creating a new variables named "Nombre Ajustado" using the basic process to clean "NAME".
df_A['Nombre ajustado'] = df_A['NAME'].apply(lambda x: cleanco(x).clean_name() if type(x)==str else x)

"""# 🆕 Deduplication

## 
"""

dfA = df_A.copy()

dfA.shape

"""## Make record pairs"""

"""One of the most well known indexing methods is named blocking. This method includes only record pairs that are identical on one or more stored attributes of the person (or entity in general). The blocking method can be used in the recordlinkage module."""

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

"""The last step is to decide which records belong to the same person. In this example, we keep it simple:"""

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
df_merge.shape

# Make a merge to understand which one there is a match with.
df_merge = pd.merge( df_A , reset_df[['Orden_A', 'Orden_B', 'Total' ]] , how = 'left' , 
              left_on = [ 'Orden' ] , right_on = [ 'Orden_A' ])

st.subheader("Resultados") 

st.markdown("Se encontraron " + str(df_merge.shape[0]) + " coincidencias entre los registros." )

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

csv_downloader(df_valores_unidos, "#### Descargar registros únicos ###") # Using the function to download the data. 

st.markdown("")
st.markdown("Tabla con los registros")
#st.dataframe(df_merge) # Show the DataFrame. # Here I must reference the DataFrame with the results.
csv_downloader(df_merge, "#### Descargar las coincidencias entre los registros ###") #  
st.markdown("Las coincidencias entres los registros se da entre pares con las variables `Orden_A` y `Orden_B` las cuales indican la ubicación de las observaciones, siendo cero la primera.")


st.balloons()
