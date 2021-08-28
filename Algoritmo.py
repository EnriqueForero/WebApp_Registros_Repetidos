"""2021-08-22 Limpieza y Comparación de nombres 
*Enrique Forero*
*Date: 2021-08-19*
"""
"""### ✅ Cargando librerias necesarias"""
import streamlit as st
import pandas as pd
import recordlinkage as rl
import missingno as msno

"""# ⏯ Programación

### ✅ 0.1. Instalar paquete necesario:
"""

"""### ✅ I.1 Cargar archivos - Excel"""

df_A = pd.read_csv("Base_a_analizar.csv", encoding= 'unicode_escape') 

df_A['Orden'] = df_A.index


"""# ⏯ **I. Limpiar Nombres**

### ✅ I.2 CLEANCO - Limpiar nombres corporativos

#### 🟡 I.2.a Librerias necesarias
"""

from cleanco import prepare_terms, basename
from cleanco import cleanco
from cleanco import prepare_terms, basename

"""#### 🟡 I.2.e Creando la columna - Nombre Ajustado"""

# Volviendo a ajustar los nombres con el proceso más básico. 
df_A['Nombre ajustado'] = df_A['NAME'].apply(lambda x: cleanco(x).clean_name() if type(x)==str else x)

"""# 🆕 Utilizando la librería de deduplicación - Datos reales

## Cargar paquetes necesarios y base de datos
"""

dfA = df_A.copy()

dfA.shape

"""## Make record pairs"""

"""One of the most well known indexing methods is named blocking. This method includes only record pairs that are identical on one or more stored attributes of the person (or entity in general). The blocking method can be used in the recordlinkage module."""

# Como no tenemos una variable para hacer un bloque, creemos una
dfA["bloque"] = "Grupo único"

# Para no generar tantos emparejamientos, utilizamos una variable por la cual agrupar y en la que las observaciones deben ser idénticas. En este caso la variable es "Grupo único"
import recordlinkage 
indexer = recordlinkage.Index()
indexer.block('bloque') # The argument ‘given_name’ is the blocking variable.
candidate_links = indexer.index(dfA)

# Revisando la cantidad de enlaces que se crearon
st.markdown("Cantidad de filas del archivo subido " + str(len(df_A)) + ". Se harán " 
            + str(len(candidate_links)) + " comparaciones" )
# (1000*1000-1000)/2 = 499500

"""The last step is to decide which records belong to the same person. In this example, we keep it simple:"""

compare_cl = recordlinkage.Compare()

compare_cl.exact('LASTNAME', 'LASTNAME', label='LASTNAME')
compare_cl.string('Nombre ajustado', 'Nombre ajustado', method='levenshtein', threshold=0.85, label='Nombre ajustado')
compare_cl.string('FIRSTNAME', 'FIRSTNAME', method='jarowinkler', threshold=0.85, label='FIRSTNAME')
compare_cl.string('NAME', 'NAME', method='levenshtein', threshold=0.85, label='NAME')
compare_cl.string('EMAIL', 'EMAIL', method='damerau_levenshtein', threshold=0.85, label='EMAIL')
compare_cl.exact('CIUDAD__C', 'CIUDAD__C', label='CIUDAD__C')

features = compare_cl.compute(candidate_links, dfA)

# Vamos a tomar las observaciones que tengan más de 3 criterios que pasaron la validación. 
matches = features[features.sum(axis=1) > 2]

# Sumar columnas
matches['Total'] = matches.apply(lambda x: x.sum(), axis=1)

# Convertir los índices en variables para poder hacer el empalme. 
reset_df = matches.reset_index()

# Renombrar las columnas
reset_df = reset_df.rename({'level_0': 'Orden_A', 'level_1': 'Orden_B'}, axis=1)

# Copia de seguridad
df_merge = df_A.copy()
df_merge.shape

# Hacer un merge para entender con cuál hay emparejamiento. 
df_merge = pd.merge( df_A , reset_df[['Orden_A', 'Orden_B', 'Total' ]] , how = 'left' , 
              left_on = [ 'Orden' ] , right_on = [ 'Orden_A' ])

st.markdown("Cantidad de coincidencias entre los registros " + str(df_merge.shape[0]))

# Conteo de Registros únicos
df_merge["Total"].isna().sum()

df_valores_unidos = df_merge[df_merge['Total'].isnull()]
#st.markdown("df_valores_unidos.shape " + str(df_valores_unidos.shape))

# Utils
import base64 
import time
timestr = time.strftime("%Y%m%d-%H%M%S")

# Esta es la función para descargar los archivos a CSV. 
def csv_downloader(data, mensaje):
    csvfile = data.to_csv()
    b64 = base64.b64encode(csvfile.encode()).decode()
    new_filename = "new_text_file_{}_.csv".format(timestr)
    st.markdown(mensaje)
    href = f'<a href="data:file/csv;base64,{b64}" download="{new_filename}">¡Hacer clic aquí!</a>'
    st.markdown(href,unsafe_allow_html=True)

# Revisando la cantidad de enlaces que se crearon
st.markdown("La cantidad de registros únicos son " + str(len(df_valores_unidos)) 
            + ", esto representa el  " + str(len(df_valores_unidos)/len(df_A)) + " del total analizado.")
# (1000*1000-1000)/2 = 499500

csv_downloader(df_valores_unidos, "#### Descargar registros únicos ###") # Aquí se llama la función para descargar los datos. 

st.markdown("")
st.markdown("Tabla con los registros")
#st.dataframe(df_merge) # Mostrar el DataFrame. # Aquí debo referenciar el DataFrame con los resultados. 
csv_downloader(df_merge, "#### Descargar las coincidencias entre los registros ###") # Aquí se llama la función para descargar los datos. 

