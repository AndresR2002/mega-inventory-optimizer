from azure.storage.blob import BlobServiceClient
from config import AZURE_STORAGE_ACCOUNT, AZURE_STORAGE_KEY, AZURE_CONTAINER_NAME
import os


def download_csv(blob_name, local_path):
    """
    Descarga un archivo CSV desde Azure Blob Storage.

    :param blob_name: Nombre del archivo en el contenedor de Azure Blob Storage
    :param local_path: Ruta local donde se guardará el archivo descargado
    """
    connection_string = f"DefaultEndpointsProtocol=https;AccountName={AZURE_STORAGE_ACCOUNT};AccountKey={AZURE_STORAGE_KEY};EndpointSuffix=core.windows.net"

    blob_service_client = BlobServiceClient.from_connection_string(connection_string)

    blob_client = blob_service_client.get_blob_client(container=AZURE_CONTAINER_NAME, blob=blob_name)

    os.makedirs(os.path.dirname(local_path), exist_ok=True)

    with open(local_path, "wb") as file:
        file.write(blob_client.download_blob().readall())

    print(f"✅ Descargado: {blob_name} → {local_path}")


def download_all_csv():
    """
    Descarga todos los archivos necesarios para la ETL.

    Llama a la función download_csv para cada archivo necesario en el proceso de ETL.
    """
    files = ["clientes.csv", "productos.csv", "proveedores.csv", "ventas.csv", "logistica.csv"]

    for file in files:
        download_csv(file, f"data/{file}")

    print("✅ Descarga de archivos completada.")
