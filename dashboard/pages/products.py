import os
import streamlit as st
import pandas as pd
import plotly.express as px
from dotenv import load_dotenv
from .api import obtener_datos_paginados

load_dotenv()
BASE_URL_PRODUCTOS = os.getenv("API_URL_PRODUCTOS")

def mostrar_productos():
    st.header("Dashboard de Productos")

    categoria = st.multiselect("Categoría", ["Abarrotes", "Salud", "Ropa", "Electrónica", "Hogar"])
    precio_min = st.number_input("Precio mínimo", min_value=0.0, value=0.0)
    precio_max = st.number_input("Precio máximo", min_value=0.0, value=10000.0)
    nombre_producto = st.text_input("Buscar por nombre de producto")

    limit = st.sidebar.number_input("Límite (limit)", min_value=1, value=1000, step=500)
    offset = st.sidebar.number_input("Desplazamiento (offset)", min_value=0, value=0, step=100)
    obtener_todo = st.sidebar.checkbox("Obtener todos los datos", value=False)

    if st.button("🔍 Buscar Productos"):
        params = {"categoria": categoria if categoria else None, "precio_min": precio_min, "precio_max": precio_max}

        if nombre_producto:
            datos = obtener_datos_paginados(f"{BASE_URL_PRODUCTOS}/nombre", {"nombre_producto": nombre_producto}, obtener_todo, limit, offset)
        else:
            datos = obtener_datos_paginados(BASE_URL_PRODUCTOS, params, obtener_todo, limit, offset)

        if datos:
            df = pd.DataFrame(datos)
            st.dataframe(df)

            st.subheader("📊 Análisis de Productos")
            fig_categoria_pie = px.pie(df, names="categoria", title="Distribución de Productos por Categoría")
            st.plotly_chart(fig_categoria_pie, use_container_width=True)
        else:
            st.warning("No se encontraron productos con los filtros seleccionados.")
