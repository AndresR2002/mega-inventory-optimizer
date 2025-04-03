from typing import Optional, List
from fastapi import APIRouter, Depends, Query
from sqlmodel import Session, select, func
from sqlalchemy.orm import selectinload
from ..db import get_session
from ..models import Envios, Tiempo

router = APIRouter()

@router.get("/", summary="Obtener envíos",
            description="Recupera una lista de envíos con opciones de filtrado y paginación.")
def get_envios(
        limit: int = Query(1000, le=5000, description="Número máximo de registros a devolver (máx. 5000)."),
        offset: int = Query(0, description="Número de registros a omitir en la paginación."),
        proveedor_id: Optional[str] = Query(None, description="ID del proveedor para filtrar."),
        estado_envio: Optional[str] = Query(None, description="Estado del envío para filtrar."),
        fecha_inicio: Optional[str] = Query(None, description="Fecha de inicio en formato YYYY-MM-DD."),
        fecha_fin: Optional[str] = Query(None, description="Fecha de fin en formato YYYY-MM-DD."),
        include_proveedor: bool = Query(False, description="Incluir información del proveedor en la respuesta."),
        session: Session = Depends(get_session)
):
    query = select(Envios).join(Tiempo, Envios.tiempo_id == Tiempo.tiempo_id).options(selectinload(Envios.tiempo))  # 🔹 Se carga `Tiempo`

    load_options = []
    if include_proveedor:
        load_options.append(selectinload(Envios.proveedor))

    if load_options:
        query = query.options(*load_options)

    if proveedor_id:
        query = query.where(Envios.proveedor_id == proveedor_id)
    if estado_envio:
        query = query.where(Envios.estado_envio == estado_envio)
    if fecha_inicio:
        query = query.where(Tiempo.fecha >= fecha_inicio)
    if fecha_fin:
        query = query.where(Tiempo.fecha <= fecha_fin)

    query = query.offset(offset).limit(limit)
    envios = session.exec(query).all()

    result = []
    for envio in envios:
        envio_dict = envio.__dict__.copy()
        envio_dict["tiempo"] = envio.tiempo.__dict__
        if include_proveedor and envio.proveedor:
            envio_dict['proveedor'] = envio.proveedor.__dict__
        result.append(envio_dict)

    return result

@router.get("/periodo", summary="Obtener envíos por periodo",
            description="Obtiene la cantidad de envíos agrupados por día, mes o año.")
def get_envios_periodo(
        periodo: str = Query("anio", regex="^(dia|mes|anio)$", description="Nivel de agregación de los datos."),
        anio: Optional[int] = Query(None, description="Filtrar por año."),
        mes: Optional[int] = Query(None, description="Filtrar por mes."),
        dia: Optional[int] = Query(None, description="Filtrar por día."),
        limit: int = Query(1000, le=5000, description="Número máximo de registros a devolver."),
        offset: int = Query(0, description="Número de registros a omitir en la paginación."),
        session: Session = Depends(get_session)
):
    query = select(
        getattr(Tiempo, periodo).label(periodo),
        func.count(Envios.envio_id).label("total_envios")
    ).join(Tiempo, Envios.tiempo_id == Tiempo.tiempo_id)

    if anio:
        query = query.where(Tiempo.anio == anio)
    if mes:
        query = query.where(Tiempo.mes == mes)
    if dia:
        query = query.where(Tiempo.dia == dia)

    query = query.group_by(getattr(Tiempo, periodo))
    query = query.offset(offset).limit(limit)

    return session.exec(query).mappings().all()