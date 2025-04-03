import os
import streamlit as st
import pandas as pd
import plotly.express as px
from dotenv import load_dotenv
from .api import  obtener_datos_paginados

load_dotenv()
BASE_URL_CLIENTES = os.getenv("API_URL_CLIENTES")

def mostrar_clientes():
    st.header("Dashboard de Clientes")

    genero = st.multiselect("Género", ["Masculino", "Femenino", "Otro"])
    edad_min = st.number_input("Edad mínima", min_value=0, max_value=120, value=18)
    edad_max = st.number_input("Edad máxima", min_value=0, max_value=120, value=100)
    ubicacion = st.text_input("Ubicación")
    nombre = st.text_input("Buscar por nombre")

    limit = st.sidebar.number_input("Límite (limit)", min_value=1, value=1000, step=500)
    offset = st.sidebar.number_input("Desplazamiento (offset)", min_value=0, value=0, step=100)
    obtener_todo = st.sidebar.checkbox("Obtener todos los datos", value=False)

    if st.button("🔍 Buscar Clientes"):
        params = {"genero": genero if genero else None, "edad_min": edad_min, "edad_max": edad_max, "ubicacion": ubicacion if ubicacion else None}

        if nombre:
            datos = obtener_datos_paginados(f"{BASE_URL_CLIENTES}/nombre", {"nombre_cliente": nombre}, obtener_todo, limit, offset)
        else:
            datos = obtener_datos_paginados(BASE_URL_CLIENTES, params, obtener_todo, limit, offset)

        if datos:
            df = pd.DataFrame(datos)
            st.dataframe(df)

            st.subheader("📊 Análisis de Clientes")
            fig_genero_bar = px.bar(df.groupby("genero").size().reset_index(name="count"), x="genero", y="count", title="Clientes por Género", labels={"count": "Cantidad", "genero": "Género"})
            st.plotly_chart(fig_genero_bar, use_container_width=True)

            fig_edad_pie = px.pie(df, names="edad", title="Distribución de Clientes por Edad")
            st.plotly_chart(fig_edad_pie, use_container_width=True)

            fig_ubicacion_pie = px.pie(df, names="ubicacion", title="Distribución de Clientes por Ubicación")
            st.plotly_chart(fig_ubicacion_pie, use_container_width=True)
        else:
            st.warning("No se encontraron clientes con los filtros seleccionados.")
