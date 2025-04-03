from typing import Optional, List
from fastapi import APIRouter, Depends, Query
from sqlmodel import Session, select
from ..db import get_session
from ..models import Clientes

router = APIRouter()

@router.get("/", response_model=List[Clientes], summary="Obtener lista de clientes con filtros opcionales",
            description="Obtiene una lista de clientes con paginación y filtros opcionales por género, edad, y ubicación.")
def get_clientes(
        genero: Optional[List[str]] = Query(None,
                                            description="Lista de géneros a filtrar (ej. Masculino, Femenino, Otro)."),
        edad: Optional[int] = Query(None, description="Edad exacta del cliente."),
        edad_min: Optional[int] = Query(None, description="Edad mínima del rango."),
        edad_max: Optional[int] = Query(None, description="Edad máxima del rango."),
        ubicacion: Optional[str] = Query(None, description="Ubicación del cliente."),
        limit: int = Query(1000, le=5000, description="Número máximo de clientes a devolver (máx. 5000)."),
        offset: int = Query(0, description="Número de registros a omitir para la paginación."),
        session: Session = Depends(get_session)
):
    query = select(Clientes)

    if genero:
        query = query.where(Clientes.genero.in_(genero))
    if edad is not None:
        query = query.where(Clientes.edad == edad)
    elif edad_min is not None and edad_max is not None:
        query = query.where(Clientes.edad.between(edad_min, edad_max))
    elif edad_min is not None:
        query = query.where(Clientes.edad >= edad_min)
    elif edad_max is not None:
        query = query.where(Clientes.edad <= edad_max)
    if ubicacion:
        query = query.where(Clientes.ubicacion == ubicacion)

    query = query.offset(offset).limit(limit)

    return session.exec(query).all()

@router.get("/nombre", response_model=List[Clientes], summary="Filtrar clientes por nombre",
            description="Obtiene una lista de clientes filtrados por nombre.")
def get_clientes_por_nombre(
        nombre_cliente: str,
        limit: int = Query(1000, le=5000),
        offset: int = 0,
        session: Session = Depends(get_session)
):
    query = select(Clientes).where(Clientes.nombre.ilike(f"%{nombre_cliente}%")).offset(offset).limit(limit)
    return session.exec(query).all()
