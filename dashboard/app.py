import streamlit as st
from pages.customers import mostrar_clientes
from pages.products import mostrar_productos
from pages.suppliers import mostrar_proveedores
from pages.sales import mostrar_ventas
from pages.shipments import mostrar_envios

st.sidebar.title("Navegación")
pagina = st.sidebar.selectbox(
    "Selecciona una sección",
    ["Clientes", "Productos", "Proveedores", "Ventas", "Envíos"]
)
if pagina == "Clientes":
    mostrar_clientes()
elif pagina == "Productos":
    mostrar_productos()
elif pagina == "Proveedores":
    mostrar_proveedores()
elif pagina == "Ventas":
    mostrar_ventas()
elif pagina == "Envíos":
    mostrar_envios()
