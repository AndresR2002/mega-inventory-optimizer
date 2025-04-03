from typing import Optional, List
from fastapi import APIRouter, Depends, Query
from sqlmodel import Session, select
from ..db import get_session
from ..models import Productos

router = APIRouter()

@router.get("/", response_model=List[Productos], summary="Obtener lista de productos",
            description="Obtiene una lista de productos con paginación y filtros opcionales (por categoría, precio, etc.).")
def get_productos(
        categoria: Optional[str] = Query(None, description="Filtrar por categoría del producto."),
        precio: Optional[float] = Query(None, description="Filtrar por precio exacto del producto."),
        precio_min: Optional[float] = Query(None, description="Filtrar productos con precio mayor o igual a este valor."),
        precio_max: Optional[float] = Query(None, description="Filtrar productos con precio menor o igual a este valor."),
        limit: int = Query(1000, le=5000, description="Número máximo de productos a devolver (máx. 5000)."),
        offset: int = Query(0, description="Número de registros a omitir para la paginación."),
        session: Session = Depends(get_session)
):
    query = select(Productos)

    if categoria:
        query = query.where(Productos.categoria == categoria)
    if precio is not None:
        query = query.where(Productos.precio_base == precio)
    elif precio_min is not None and precio_max is not None:
        query = query.where(Productos.precio_base.between(precio_min, precio_max))
    elif precio_min is not None:
        query = query.where(Productos.precio_base >= precio_min)
    elif precio_max is not None:
        query = query.where(Productos.precio_base <= precio_max)

    query = query.offset(offset).limit(limit)

    return session.exec(query).all()

@router.get("/nombre", response_model=List[Productos], summary="Filtrar productos por nombre",
            description="Obtiene una lista de productos filtrados por nombre.")
def get_productos_por_nombre(
        nombre_producto: str,
        limit: int = Query(1000, le=5000),
        offset: int = 0,
        session: Session = Depends(get_session)
):
    query = select(Productos).where(Productos.nombre_producto.ilike(f"%{nombre_producto}%")).offset(offset).limit(limit)
    return session.exec(query).all()