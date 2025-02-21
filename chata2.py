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
            data = response.json()  # Convertimos la respuesta a JSON

            # Verificamos si 'elementList' está en el JSON
            if 'elementList' in data:
                pisos = []
                for i, item in enumerate(data['elementList'], start=1):
                    # Asignamos un número incremental al nombre del piso
                    nombre_piso = i  # Número de piso

                    # Extraemos los datos (si están disponibles)
                    precio = item.get('price', 'No disponible')
                    enlace = item.get('url', 'No disponible')

                    # Obtenemos la dirección directamente de 'address' (calle)
                    address = item.get('address', 'No disponible')
                    
                    # Barrio sigue siendo 'neighborhood'
                    barrio = item.get('neighborhood', 'No disponible')

                    habitaciones = item.get('rooms', 'No disponible')  # Habitaciones
                    baños = item.get('bathrooms', 'No disponible')  # Baños

                    # Añadimos el piso a la lista
                    pisos.append({
                        'Piso': nombre_piso,
                        'Precio': precio,
                        'Enlace': enlace,
                        'Calle': address,  # Calle directamente desde 'address'
                        'Habitaciones': habitaciones,
                        'Baños': baños,
                        'Barrio': barrio
                    })

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
