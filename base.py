import streamlit as st
import json
import scrapy
import http.client
import requests

#st.map()
#streamlit run base.py

def obtener_datos_idealista():
    try:
            url = "https://idealista7.p.rapidapi.com/listrooms"

            querystring = {"order":"relevance","locationId":"0-EU-ES-28-07-001-079","locationName":"Madrid","numPage":"1","maxItems":"40","location":"es","locale":"es"}

            headers = {
                    "x-rapidapi-key": "36b815da5cmsh30aed6a96cc841cp173f8fjsn2440373c56a8",
                    "x-rapidapi-host": "idealista7.p.rapidapi.com"
            }

            response = requests.get(url, headers=headers, params=querystring)
            print(response.json())

            # Verificamos que 'elementList' está en el JSON
            if 'elementList' in response:
                pisos = []
                for item in response['elementList']:
                    nombre_piso = item.get('title', 'No disponible')
                    precio = item.get('price', 'No disponible')
                    enlace = item.get('url', 'No disponible')
                    pisos.append({'Nombre': nombre_piso, 'Precio': precio, 'Enlace': enlace})
                return pisos
            else:
                return None
    except requests.exceptions.RequestException as e:
            st.error(f"Hubo un error al hacer la solicitud: {e}")
            return None

    #mercadona ----------------------------------------------------------------------------------------------------------------


# Interfaz de Streamlit
st.title('Scraper de Pisos de Idealista')


st.divider()  # 👈 Draws a horizontal rule

st.write("Dale al botoncuelo para que no funcione por culpa de chat gpt")

st.divider()  # 👈 Another horizontal rule

# Botón para ejecutar la función
if st.button('Obtener Pisos'):
    pisos = obtener_datos_idealista()
    
    if pisos:
        # Mostrar los resultados en una tabla
        st.write("### Resultados de los pisos")
        st.dataframe(pisos)
    else:
        st.warning('No se encontraron pisos o hubo un problema con la respuesta de la API.')





