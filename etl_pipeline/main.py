import time
import os
from extract.download_data import download_all_csv
from transform.clean_customers import clean_customers_data
from transform.clean_products import clean_products_data
from transform.clean_suppliers import clean_suppliers_data
from transform.clean_sales import clean_sales_data
from transform.clean_logistic import clean_logistics_data
from transform.utils import format_ids_in_csv
from transform.clean_time import generate_time_dimension
from load.load_to_postgresql import load_csv_to_postgresql, execute_sql_from_file

def wait_for_file(file_path, timeout=30):
    """Espera hasta que un archivo esté disponible antes de continuar."""
    start_time = time.time()
    while not os.path.exists(file_path):
        if time.time() - start_time > timeout:
            raise TimeoutError(f"⛔ Error: El archivo {file_path} no se generó en el tiempo esperado.")
        time.sleep(1)

print("🚀 Descargando datos...")
download_all_csv()

print("🧹 Limpiando clientes...")
clean_customers_data("data/clientes.csv", "output/clientes_cleaned.csv")
wait_for_file("output/clientes_cleaned.csv")

print("🧹 Limpiando productos...")
clean_products_data("data/productos.csv", "output/productos_cleaned.csv")
wait_for_file("output/productos_cleaned.csv")

print("🧹 Limpiando proveedores...")
clean_suppliers_data("data/proveedores.csv", "output/proveedores_cleaned.csv")
wait_for_file("output/proveedores_cleaned.csv")

print("📆 Generando dimensión de tiempo...")
generate_time_dimension("data/ventas.csv", "data/logistica.csv", "output/dim_tiempo.csv")
wait_for_file("output/dim_tiempo.csv")

print("🧹 Limpiando ventas...")
clean_sales_data("data/ventas.csv", "output/productos_cleaned.csv", "output/clientes_cleaned.csv", "output/dim_tiempo.csv", "output/ventas_cleaned.csv")
wait_for_file("output/ventas_cleaned.csv")

print("🧹 Limpiando logística...")
clean_logistics_data("data/logistica.csv", "output/ventas_cleaned.csv", "output/proveedores_cleaned.csv", "output/dim_tiempo.csv", "output/logistica_cleaned.csv")
wait_for_file("output/logistica_cleaned.csv")

files_to_format = [
    ("output/clientes_cleaned.csv", ["cliente_id"]),
    ("output/productos_cleaned.csv", ["producto_id"]),
    ("output/proveedores_cleaned.csv", ["proveedor_id"]),
    ("output/dim_tiempo.csv", ["tiempo_id"]),
    ("output/ventas_cleaned.csv", ["venta_id", "producto_id", "cliente_id", "tiempo_id"]),
    ("output/logistica_cleaned.csv", ["envio_id", "venta_id", "proveedor_id", "tiempo_id"])
]

print("🔍 Formateando IDs...")
for file_path, id_columns in files_to_format:
    format_ids_in_csv(file_path, file_path, id_columns)
    wait_for_file(file_path)


print("💾 Cargando datos en PostgreSQL...")

load_csv_to_postgresql("output/clientes_cleaned.csv", "clientes", id_columns=["cliente_id"])
load_csv_to_postgresql("output/productos_cleaned.csv", "productos", id_columns=["producto_id"])
load_csv_to_postgresql("output/proveedores_cleaned.csv", "proveedores", id_columns=["proveedor_id"])
load_csv_to_postgresql("output/dim_tiempo.csv", "tiempo", id_columns=["tiempo_id"])
load_csv_to_postgresql("output/ventas_cleaned.csv", "ventas", id_columns=["venta_id", "producto_id", "cliente_id", "tiempo_id"])
load_csv_to_postgresql("output/logistica_cleaned.csv", "envios", id_columns=["envio_id", "venta_id", "proveedor_id", "tiempo_id"])
execute_sql_from_file("database/p_keys.sql")
execute_sql_from_file("database/f_keys.sql")
execute_sql_from_file("database/indexes.sql")
print("✅ ¡Proceso de ETL completado!")

