from typing import Optional, List
from fastapi import APIRouter, Depends, Query
from sqlmodel import Session, select, func
from sqlalchemy.orm import selectinload
from ..db import get_session
from ..models import Ventas, Clientes, Productos, Tiempo

router = APIRouter()

@router.get("/", summary="Obtener ventas",
            description="Recupera una lista de ventas con opciones de filtrado y paginación.")
def get_ventas(
        limit: int = Query(1000, le=5000, description="Número máximo de registros a devolver (máx. 5000)."),
        offset: int = Query(0, description="Número de registros a omitir en la paginación."),
        fecha_inicio: Optional[str] = Query(None, description="Fecha de inicio en formato YYYY-MM-DD."),
        fecha_fin: Optional[str] = Query(None, description="Fecha de fin en formato YYYY-MM-DD."),
        cliente_id: Optional[str] = Query(None, description="ID del cliente para filtrar."),
        producto_id: Optional[str] = Query(None, description="ID del producto para filtrar."),
        sucursal_id: Optional[int] = Query(None, description="ID de la sucursal para filtrar."),
        include_cliente: bool = Query(False, description="Incluir información del cliente en la respuesta."),
        include_producto: bool = Query(False, description="Incluir información del producto en la respuesta."),
        include_proveedor: bool = Query(False, description="Incluir información del proveedor en la respuesta."),
        session: Session = Depends(get_session)
):
    query = select(Ventas).join(Tiempo, Ventas.tiempo_id == Tiempo.tiempo_id).options(selectinload(Ventas.tiempo))
    load_options = []
    if include_cliente:
        load_options.append(selectinload(Ventas.cliente))
    if include_producto:
        load_options.append(selectinload(Ventas.producto))
    if include_proveedor:
        load_options.append(selectinload(Ventas.proveedor))

    if load_options:
        query = query.options(*load_options)

    if cliente_id:
        query = query.where(Ventas.cliente_id == cliente_id)
    if producto_id:
        query = query.where(Ventas.producto_id == producto_id)
    if fecha_inicio:
        query = query.where(Tiempo.fecha >= fecha_inicio)
    if fecha_fin:
        query = query.where(Tiempo.fecha <= fecha_fin)
    if sucursal_id:
        query = query.where(Ventas.sucursal_id == sucursal_id)

    query = query.offset(offset).limit(limit)
    ventas = session.exec(query).all()

    result = []
    for venta in ventas:
        venta_dict = venta.__dict__.copy()
        venta_dict["tiempo"] = venta.tiempo.__dict__
        if include_cliente and venta.cliente:
            venta_dict['cliente'] = venta.cliente.__dict__
        if include_producto and venta.producto:
            venta_dict['producto'] = venta.producto.__dict__
        if include_proveedor and venta.proveedor:
            venta_dict['proveedor'] = venta.proveedor.__dict__
        result.append(venta_dict)

    return result

@router.get("/categoria/{categoria}", summary="Obtener ventas por categoría",
            description="Recupera las ventas filtradas por categoría del producto.")
def get_ventas_por_categoria(
        categoria: str,
        limit: int = Query(1000, le=5000, description="Número máximo de registros a devolver (máx. 5000)."),
        offset: int = Query(0, description="Número de registros a omitir en la paginación."),
        session: Session = Depends(get_session)
):
    query = select(Ventas).join(Productos).join(Tiempo, Ventas.tiempo_id == Tiempo.tiempo_id).options(selectinload(Ventas.tiempo))
    query = query.where(Productos.categoria == categoria)
    query = query.offset(offset).limit(limit)
    ventas = session.exec(query).all()

    result = []
    for venta in ventas:
        venta_dict = venta.__dict__.copy()
        venta_dict["tiempo"] = venta.tiempo.__dict__
        result.append(venta_dict)

    return result

@router.get("/periodo", summary="Obtener ventas por periodo",
            description="Obtiene la suma de ventas agrupadas por día, mes o año.")
def get_ventas_periodo(
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
        func.sum(Ventas.total).label("total_ventas")
    ).join(Tiempo, Ventas.tiempo_id == Tiempo.tiempo_id)

    if anio:
        query = query.where(Tiempo.anio == anio)
    if mes:
        query = query.where(Tiempo.mes == mes)
    if dia:
        query = query.where(Tiempo.dia == dia)

    query = query.group_by(getattr(Tiempo, periodo))
    query = query.offset(offset).limit(limit)

    return session.exec(query).mappings().all()

@router.get("/genero", summary="Obtener ventas por género",
            description="Filtra las ventas por género y rango de edad de los clientes.")
def get_ventas_por_genero(
        genero: List[str] = Query(["Masculino", "Femenino", "Otro"], description="Lista de géneros a filtrar."),
        edad: Optional[int] = Query(None, description="Edad exacta del cliente."),
        edad_min: Optional[int] = Query(None, description="Edad mínima del cliente."),
        edad_max: Optional[int] = Query(None, description="Edad máxima del cliente."),
        limit: int = Query(1000, le=5000, description="Número máximo de registros a devolver."),
        offset: int = Query(0, description="Número de registros a omitir en la paginación."),
        session: Session = Depends(get_session)
):
    query = select(Ventas).join(Clientes).join(Tiempo, Ventas.tiempo_id == Tiempo.tiempo_id).options(selectinload(Ventas.tiempo))
    query = query.where(Clientes.genero.in_(genero))
    if edad is not None:
        query = query.where(Clientes.edad == edad)
    elif edad_min is not None and edad_max is not None:
        query = query.where(Clientes.edad.between(edad_min, edad_max))
    elif edad_min is not None:
        query = query.where(Clientes.edad >= edad_min)
    elif edad_max is not None:
        query = query.where(Clientes.edad <= edad_max)
    query = query.offset(offset).limit(limit)
    ventas = session.exec(query).all()

    result = []
    for venta in ventas:
        venta_dict = venta.__dict__.copy()
        venta_dict["tiempo"] = venta.tiempo.__dict__
        result.append(venta_dict)

    return result

