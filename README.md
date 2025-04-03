# Mega Inventory Optimizer

**MegaMercado** es una cadena de supermercados que busca optimizar sus inventarios y reducir costos operativos mediante la integración y análisis de datos. Este proyecto implementa una solución integral que incluye:
- Un pipeline de datos (ETL)
- Análisis exploratorio de datos (EDA)
- Un modelo predictivo de demanda
- Una API REST para consulta y visualización
- Un dashboard interactivo

---
## 📁 Estructura del Proyecto

### 1. ETL Pipeline (`etl_pipeline/`)
Encargado de la extracción, transformación y carga de datos desde diferentes fuentes a una base de datos centralizada.
- `extract/` → Extracción de datos.
- `transform/` → Procesamiento y limpieza de datos.
- `load/` → Carga de datos en la base de datos.
- `database/` → Configuración de la base de datos.
- `output/` → Almacenamiento de datos transformados.
- `config.py` → Configuración de la conexión a la base de datos.
- `main.py` → Script principal del pipeline ETL.

### 2. Análisis Exploratorio de Datos (EDA) (`eda/`)
Contiene notebooks con exploraciones iniciales de los datos, análisis de patrones y generación de reportes.
- `01_database_exploration.ipynb` → Exploración de la base de datos.
- `02_dimension_exploration.ipynb` → Análisis de dimensiones.
- `03_dates_exploration.ipynb` → Análisis de fechas.
- `04_measure_exploration.ipynb` → Exploración de métricas relevantes.

### 3. Modelo Predictivo (`ml_model/`)
Desarrollo y entrenamiento de un modelo de aprendizaje automático para la predicción de demanda de productos.
- `model_training.ipynb` → Entrenamiento y evaluación del modelo.
- `model.json` → Modelo entrenado.

### 4. API REST (`api_rest/`)
Permite acceder a los datos procesados y al modelo predictivo a través de endpoints.
- `app/` → Implementación de la API con FastAPI.
- `main.py` → Archivo principal para la ejecución de la API.
- `requirements.txt` → Dependencias necesarias.

Ejecutar localmente:
```sh
uvicorn main:app --host 0.0.0.0 --port $PORT
```

La API está disponible públicamente para pruebas en: [Mega Inventory Optimizer API](https://mega-inventory-optimizer.onrender.com/docs)

### 5. Dashboard (`dashboard/`)
Aplicación interactiva para la visualización de datos y reportes mediante Streamlit.
- `pages/` → Secciones del dashboard.
- `app.py` → Archivo principal del dashboard.
- `requirements.txt` → Dependencias necesarias.

Ejecutar localmente:
```sh
streamlit run app.py
```

---
## 🚀 Instalación y Configuración

Para ejecutar este proyecto, clona el repositorio y accede a su directorio:
```sh
git clone https://github.com/AndresR2002/mega-inventory-optimizer.git
cd mega-inventory-optimizer
```

Cada módulo contiene su propio archivo `requirements.txt`. Para instalar las dependencias:
```sh
pip install -r requirements.txt
```

---
## 🔧 Variables de Entorno
Cada módulo maneja su propio archivo de entorno (`.env`). Una configuración típica incluye:
```ini
DATABASE_URL=postgresql://<usuario>:<password>@<host>:<puerto>/<base_de_datos>
API_URL_CLIENTES=base_url/clientes
API_URL_PRODUCTOS=base_url/productos
API_URL_PROVEEDORES=base_url/proveedores
API_URL_VENTAS=base_url/ventas/
API_URL_ENVIOS=base_url/envios/
AZURE_STORAGE_ACCOUNT=<tu_cuenta>
AZURE_STORAGE_KEY=<tu_clave>
AZURE_CONTAINER_NAME=<tu_contenedor>
```
Cada usuario puede configurar estas variables según su necesidad.

---
### 🎯 ¡Listo para optimizar el inventario de MegaMercado! 🚀

