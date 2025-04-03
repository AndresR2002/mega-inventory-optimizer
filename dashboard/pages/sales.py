import os
import streamlit as st
import pandas as pd
import plotly.express as px
from dotenv import load_dotenv
from .api import obtener_datos_paginados

load_dotenv()
BASE_URL_VENTAS = os.getenv("API_URL_VENTAS")

def mostrar_ventas():
    st.header("Dashboard de Ventas")

    fecha_inicio = st.date_input("Fecha inicio")
    fecha_fin = st.date_input("Fecha fin")
    cliente_id = st.text_input("ID Cliente")
    producto_id = st.text_input("ID Producto")
    sucursal_id = st.text_input("ID Sucursal")

    limit = st.sidebar.number_input("Límite (limit)", min_value=1, value=1000, step=500)
    offset = st.sidebar.number_input("Desplazamiento (offset)", min_value=0, value=0, step=100)
    obtener_todo = st.sidebar.checkbox("Obtener todos los datos", value=False)

    if st.button("🔍 Buscar Ventas"):
        params = {
            "fecha_inicio": fecha_inicio if fecha_inicio else None,
            "fecha_fin": fecha_fin if fecha_fin else None,
            "cliente_id": cliente_id if cliente_id else None,
            "producto_id": producto_id if producto_id else None,
            "sucursal_id": sucursal_id if sucursal_id else None,
        }

        datos = obtener_datos_paginados(BASE_URL_VENTAS, params, obtener_todo, limit, offset)

        if datos:
            df = pd.DataFrame(datos)
            st.dataframe(df)

            df["fecha"] = pd.to_datetime(df["tiempo"].apply(lambda x: x["fecha"]))

            top_productos = df.groupby("producto_id")["total"].sum().reset_index()
            top_productos = top_productos.sort_values(by="total", ascending=False).head(10)
            top_productos["producto_id"] = top_productos["producto_id"].astype(int)

            top_productos["total_formateado"] = top_productos["total"].apply(lambda x: f"${x:,.2f}")

            fig_productos = px.bar(
                top_productos,
                x="producto_id",
                y="total",
                title="🛒 Productos que más generaron ingresos",
                labels={"total": "Ingresos", "producto_id": "ID Producto"},
                text="total_formateado"
            )
            fig_productos.update_layout(xaxis_type="category")
            st.plotly_chart(fig_productos, use_container_width=True)

            top_sucursales = df.groupby("sucursal_id")["total"].sum().reset_index()
            top_sucursales = top_sucursales.sort_values(by="total", ascending=False).head(10)
            top_sucursales["sucursal_id"] = top_sucursales["sucursal_id"].astype(int)

            top_sucursales["total_formateado"] = top_sucursales["total"].apply(lambda x: f"${x:,.2f}")

            fig_sucursales = px.bar(
                top_sucursales,
                x="sucursal_id",
                y="total",
                title="🏬 Sucursales con más ventas",
                labels={"total": "Ingresos", "sucursal_id": "ID Sucursal"},
                text="total_formateado"
            )
            fig_sucursales.update_layout(xaxis_type="category")
            st.plotly_chart(fig_sucursales, use_container_width=True)

            top_clientes = df.groupby("cliente_id")["total"].sum().reset_index()
            top_clientes = top_clientes.sort_values(by="total", ascending=False).head(10)
            top_clientes["cliente_id"] = top_clientes["cliente_id"].astype(int)

            top_clientes["total_formateado"] = top_clientes["total"].apply(lambda x: f"${x:,.2f}")

            fig_clientes = px.bar(
                top_clientes,
                x="cliente_id",
                y="total",
                title="👤 Clientes con más ventas",
                labels={"total": "Ingresos", "cliente_id": "ID Cliente"},
                text="total_formateado"
            )
            fig_clientes.update_layout(xaxis_type="category")
            st.plotly_chart(fig_clientes, use_container_width=True)

        else:
            st.warning("No se encontraron ventas con los filtros seleccionados.")