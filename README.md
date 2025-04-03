# mega-inventory-optimizer
Mega Inventory Optimizer

MegaMercado es una cadena de supermercados que busca optimizar sus inventarios y reducir costos operativos mediante la integración y análisis de datos. Este proyecto implementa una solución integral que incluye un pipeline de datos, un análisis exploratorio, un modelo predictivo y una API REST para la consulta y visualización de información relevante.

Estructura del Proyecto

El proyecto está dividido en los siguientes módulos:

1. ETL Pipeline (etl_pipeline/)

Encargado de la extracción, transformación y carga de datos desde diferentes fuentes a una base de datos centralizada.

extract/: Extracción de datos.

transform/: Procesamiento y limpieza de datos.

load/: Carga de datos en la base de datos.

database/: Configuración de la base de datos.

output/: Almacenamiento de datos transformados.

config.py: Configuración de la conexión a la base de datos.

main.py: Script principal del pipeline ETL.

2. Análisis Exploratorio de Datos (EDA) (eda/)

Contiene notebooks con exploraciones iniciales de los datos, análisis de patrones y generación de reportes.

01_database_exploration.ipynb: Exploración de la base de datos.

02_dimension_exploration.ipynb: Análisis de dimensiones.

03_dates_exploration.ipynb: Análisis de fechas.

04_measure_exploration.ipynb: Exploración de métricas relevantes.

3. Modelo Predictivo (ml_model/)

Desarrollo y entrenamiento de un modelo de aprendizaje automático para la predicción de demanda de productos.

model_training.ipynb: Entrenamiento y evaluación del modelo.

model.json: Modelo entrenado.

4. API REST (api_rest/)

Permite acceder a los datos procesados y al modelo predictivo a través de endpoints.

app/: Contiene la implementación de la API con FastAPI.

main.py: Archivo principal para la ejecución de la API.

requirements.txt: Dependencias necesarias.

Se puede ejecutar localmente con:

uvicorn main:app --host 0.0.0.0 --port $PORT

También está desplegada en: Mega Inventory Optimizer API

5. Dashboard (dashboard/)

Aplicación interactiva para la visualización de datos y reportes mediante Streamlit.

pages/: Contiene las diferentes secciones del dashboard.

app.py: Archivo principal del dashboard.

requirements.txt: Dependencias necesarias.

Instalación y Configuración

Para ejecutar este proyecto, puedes clonar el repositorio y ejecutar cada módulo de manera independiente.

git clone https://github.com/AndresR2002/mega-inventory-optimizer.git
cd mega-inventory-optimizer

Cada carpeta contiene su propio archivo requirements.txt. Para instalar las dependencias en cada módulo, ejecuta:

pip install -r requirements.txt

Variables de Entorno

Cada módulo puede manejar su propio archivo de entorno (.env), pero una configuración típica incluiría:

DATABASE_URL=postgresql://<usuario>:<password>@<host>:<puerto>/<base_de_datos>
API_URL_CLIENTES=base_url/clientes
API_URL_PRODUCTOS=base_url/productos
API_URL_PROVEEDORES=base_url/proveedores
API_URL_VENTAS=http:base_url/ventas/
API_URL_ENVIOS=base_url/envios/
AZURE_STORAGE_ACCOUNT=<tu_cuenta>
AZURE_STORAGE_KEY=<tu_clave>
AZURE_CONTAINER_NAME=<tu_contenedor>

Cada usuario puede configurar las variables de entorno según su necesidad.