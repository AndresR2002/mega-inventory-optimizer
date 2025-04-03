from fastapi import FastAPI
from app.db import create_db_and_tables
from app.routers.clientes_router import router as clientes_router
from app.routers.productos_router import router as productos_router
from app.routers.proveedores_router import router as proveedores_router
from app.routers.ventas_router import router as ventas_router
from app.routers.envios_router import router as envios_router

app = FastAPI()

app.include_router(clientes_router, prefix="/clientes", tags=["Clientes"])
app.include_router(productos_router, prefix="/productos", tags=["Productos"])
app.include_router(proveedores_router, prefix="/proveedores", tags=["Proveedores"])
app.include_router(ventas_router, prefix="/ventas", tags=["Ventas"])
app.include_router(envios_router, prefix="/envios", tags=["Envíos"])

@app.on_event("startup")
def on_startup():
    create_db_and_tables()
