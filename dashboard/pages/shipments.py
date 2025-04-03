import os
import streamlit as st
import pandas as pd
import plotly.express as px
from dotenv import load_dotenv
from .api import obtener_datos_paginados

load_dotenv()
BASE_URL_ENVIOS = os.getenv("API_URL_ENVIOS")

def mostrar_envios():
    st.header("Dashboard de Envíos")

    fecha_inicio = st.date_input("Fecha inicio")
    fecha_fin = st.date_input("Fecha fin")
    proveedor_id = st.text_input("ID Proveedor")
    estado_envio = st.multiselect("Estado del Envío", ["En tránsito", "Retrasado", "Entregado", "Cancelado"])

    limit = st.sidebar.number_input("Límite (limit)", min_value=1, value=1000, step=500)
    offset = st.sidebar.number_input("Desplazamiento (offset)", min_value=0, value=0, step=100)
    obtener_todo = st.sidebar.checkbox("Obtener todos los datos", value=False)

    if st.button("🔍 Buscar Envíos"):
        params = {
            "fecha_inicio": fecha_inicio if fecha_inicio else None,
            "fecha_fin": fecha_fin if fecha_fin else None,
            "proveedor_id": proveedor_id if proveedor_id else None,
            "estado_envio": estado_envio if estado_envio else None,
        }

        datos = obtener_datos_paginados(BASE_URL_ENVIOS, params, obtener_todo, limit, offset)

        if datos:
            df = pd.DataFrame(datos)
            st.dataframe(df)

            df["fecha"] = pd.to_datetime(df["tiempo"].apply(lambda x: x["fecha"]))

            # 📌 1. **Envíos por Estado**
            estado_envios = df.groupby("estado_envio")["proveedor_id"].count().reset_index(name="cantidad_envios")
            estado_envios["cantidad_envios"] = estado_envios["cantidad_envios"].astype(int)  # Convertir a int

            fig_estado = px.bar(
                estado_envios,
                x="estado_envio",
                y="cantidad_envios",
                title="📦 Envíos por Estado",
                labels={"cantidad_envios": "Cantidad de Envíos", "estado_envio": "Estado del Envío"},
                text_auto=True
            )
            fig_estado.update_layout(xaxis_type="category")
            st.plotly_chart(fig_estado, use_container_width=True)

            top_proveedores = df.groupby("proveedor_id")["proveedor_id"].count().reset_index(name="cantidad_envios")
            top_proveedores = top_proveedores.sort_values(by="cantidad_envios", ascending=False).head(10)
            top_proveedores["proveedor_id"] = top_proveedores["proveedor_id"].astype(int)

            fig_proveedores = px.bar(
                top_proveedores,
                x="proveedor_id",
                y="cantidad_envios",
                title="🏢 Proveedores con más Envíos",
                labels={"cantidad_envios": "Cantidad de Envíos", "proveedor_id": "ID Proveedor"},
                text_auto=True
            )
            fig_proveedores.update_layout(xaxis_type="category")
            st.plotly_chart(fig_proveedores, use_container_width=True)

        else:
            st.warning("No se encontraron envíos con los filtros seleccionados.")