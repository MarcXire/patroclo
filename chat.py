import streamlit as st
import requests

# Función para obtener los datos de la API
def obtener_datos_idealista():
    try:
        url = "https://idealista7.p.rapidapi.com/listrooms"
        querystring = {
            "order": "relevance",
            "locationId": "0-EU-ES-28-07-001-079",
            "locationName": "Madrid",
            "numPage": "1",
            "maxItems": "40",
            "location": "es",
            "locale": "es"
        }

        headers = {
            "x-rapidapi-key": "36b815da5cmsh30aed6a96cc841cp173f8fjsn2440373c56a8",
            "x-rapidapi-host": "idealista7.p.rapidapi.com"
        }

        response = requests.get(url, headers=headers, params=querystring)

        # Verificamos si la solicitud fue exitosa
        if response.status_code == 200:
            # Imprimimos la respuesta para ver cómo viene estructurada
            st.write("Respuesta completa de la API:")
            st.write(response.json())

            data = response.json()  # Convertimos la respuesta a JSON

            # Verificamos que 'elementList' está en el JSON
            if 'elementList' in data:
                pisos = []
                for item in data['elementList']:
                    nombre_piso = item.get('title', 'No disponible')
                    precio = item.get('price', 'No disponible')
                    enlace = item.get('url', 'No disponible')
                    pisos.append({'Nombre': nombre_piso, 'Precio': precio, 'Enlace': enlace})
                return pisos
            else:
                st.warning("La clave 'elementList' no se encuentra en la respuesta.")
                return None
        else:
            st.error(f"Error en la solicitud: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"Hubo un error al hacer la solicitud: {e}")
        return None

# Interfaz de Streamlit
st.title('Scraper de Pisos de Idealista')

st.divider()  # 👈 Dibuja una línea horizontal

st.write("Haz clic en el botón para obtener los pisos de Idealista.")

st.divider()  # 👈 Otra línea horizontal

# Botón para ejecutar la función
if st.button('Obtener Pisos'):
    pisos = obtener_datos_idealista()

    if pisos:
        # Mostrar los resultados en una tabla
        st.write("### Resultados de los pisos")
        st.dataframe(pisos)
    else:
        st.warning('No se encontraron pisos o hubo un problema con la respuesta de la API.')
