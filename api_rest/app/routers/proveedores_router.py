from typing import Optional, List
from fastapi import APIRouter, Depends, Query
from sqlmodel import Session, select
from ..db import get_session
from ..models import Proveedores

router = APIRouter()

@router.get("/", response_model=List[Proveedores], summary="Obtener lista de proveedores con filtros opcionales",
            description="Obtiene una lista de proveedores con paginación y filtros opcionales por ubicación y estado del envío.")
def get_proveedores(
        ubicacion: Optional[str] = Query(None, description="Ubicación del proveedor para filtrar."),
        estado_envio: Optional[str] = Query(None, descaaaaaription="Estado del envío para filtrar."),
        limit: int = Query(1000, le=5000, description="Número máximo de proveedores a devolver (máx. 5000)."),
        offset: int = Query(0, description="Número de registros a omitir para la paginación."),
        session: Session = Depends(get_session)
):
    query = select(Proveedores)

    if ubicacion:
        query = query.where(Proveedores.ubicacion.ilike(f"%{ubicacion}%"))
    if estado_envio:
        query = query.where(Proveedores.envios.any(estado_envio=estado_envio))

    query = query.offset(offset).limit(limit)

    return session.exec(query).all()

@router.get("/nombre", response_model=List[Proveedores], summary="Filtrar proveedores por nombre",
            description="Obtiene una lista de proveedores filtrados por nombre.")
def get_proveedores_por_nombre(
        nombre_proveedor: str,
        limit: int = Query(1000, le=5000),
        offset: int = 0,
        session: Session = Depends(get_session)
):
    query = select(Proveedores).where(Proveedores.nombre_proveedor.ilike(f"%{nombre_proveedor}%")).offset(offset).limit(limit)
    return session.exec(query).all()

@router.get("/contacto", response_model=List[Proveedores], summary="Filtrar proveedores por contacto",
            description="Obtiene una lista de proveedores filtrados por contacto.")
def get_proveedores_por_contacto(
        contacto: str,
        limit: int = Query(1000, le=5000),
        offset: int = 0,
        session: Session = Depends(get_session)
):
    query = select(Proveedores).where(Proveedores.contacto.ilike(f"%{contacto}%")).offset(offset).limit(limit)
    return session.exec(query).all()
