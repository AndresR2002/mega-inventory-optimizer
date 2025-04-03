import requests
import streamlit as st

def obtener_datos_paginados(url, params, obtener_todo, limit, offset):
    datos_totales = []

    if obtener_todo:
        temp_offset = 0
        while True:
            params.update({"limit": limit, "offset": temp_offset})
            response = requests.get(url, params=params)

            if response.status_code == 200:
                datos = response.json()
                if not datos:
                    break
                datos_totales.extend(datos)
                temp_offset += limit
            else:
                st.error(f"Error al obtener datos de la API: {response.status_code}")
                return []
    else:
        params.update({"limit": limit, "offset": offset})
        response = requests.get(url, params=params)
        if response.status_code == 200:
            datos_totales = response.json()
        else:
            st.error(f"Error al obtener datos de la API: {response.status_code}")
            return []

    return datos_totales
