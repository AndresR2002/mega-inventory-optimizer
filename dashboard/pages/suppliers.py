import os
import streamlit as st
import pandas as pd
import plotly.express as px
from dotenv import load_dotenv
from .api import obtener_datos_paginados

load_dotenv()
BASE_URL_PROVEEDORES = os.getenv("API_URL_PROVEEDORES")

def mostrar_proveedores():
    st.header("Dashboard de Proveedores")

    ubicacion_proveedor = st.text_input("Ubicación del proveedor")
    nombre_proveedor = st.text_input("Buscar por nombre del proveedor")
    contacto_proveedor = st.text_input("Buscar por contacto del proveedor")

    limit = st.sidebar.number_input("Límite (limit)", min_value=1, value=1000, step=500)
    offset = st.sidebar.number_input("Desplazamiento (offset)", min_value=0, value=0, step=100)
    obtener_todo = st.sidebar.checkbox("Obtener todos los datos", value=False)

    if st.button("🔍 Buscar Proveedores"):
        params = {"ubicacion": ubicacion_proveedor if ubicacion_proveedor else None}

        if nombre_proveedor:
            datos = obtener_datos_paginados(f"{BASE_URL_PROVEEDORES}/nombre", {"nombre_proveedor": nombre_proveedor}, obtener_todo, limit, offset)
        elif contacto_proveedor:
            datos = obtener_datos_paginados(f"{BASE_URL_PROVEEDORES}/contacto", {"contacto": contacto_proveedor}, obtener_todo, limit, offset)
        else:
            datos = obtener_datos_paginados(BASE_URL_PROVEEDORES, params, obtener_todo, limit, offset)

        if datos:
            df = pd.DataFrame(datos)
            st.dataframe(df)

            st.subheader("📊 Análisis de Proveedores")
            fig_ubicacion_bar = px.bar(
                df.groupby("ubicacion").size().reset_index(name="count"),
                x="ubicacion",
                y="count",
                title="Proveedores por Ubicación",
                labels={"count": "Cantidad", "ubicacion": "Ubicación"}
            )
            st.plotly_chart(fig_ubicacion_bar, use_container_width=True)

        else:
            st.warning("No se encontraron proveedores con los filtros seleccionados.")
