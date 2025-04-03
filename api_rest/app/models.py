from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, List

class Tiempo(SQLModel, table=True):
    tiempo_id: str = Field(primary_key=True, max_length=10)
    fecha: Optional[str] = None
    hora: Optional[str] = None
    anio: Optional[int] = None
    mes: Optional[int] = None
    mes_nombre: Optional[str] = None
    dia: Optional[int] = None
    dia_nombre: Optional[str] = None

    ventas: List["Ventas"] = Relationship(back_populates="tiempo")
    envios: List["Envios"] = Relationship(back_populates="tiempo")

class Clientes(SQLModel, table=True):
    cliente_id: str = Field(primary_key=True, max_length=10)
    nombre: str
    edad: Optional[int] = None
    genero: str = Field(max_length=50)
    ubicacion: Optional[str] = None

    ventas: List["Ventas"] = Relationship(back_populates="cliente")

class Productos(SQLModel, table=True):
    producto_id: str = Field(primary_key=True, max_length=10)
    nombre_producto: str
    categoria: str
    precio_base: float

    ventas: List["Ventas"] = Relationship(back_populates="producto")

class Proveedores(SQLModel, table=True):
    proveedor_id: str = Field(primary_key=True, max_length=10)
    nombre_proveedor: str
    contacto: Optional[str] = None
    ubicacion: Optional[str] = None

    envios: List["Envios"] = Relationship(back_populates="proveedor")

class Ventas(SQLModel, table=True):
    venta_id: str = Field(primary_key=True, max_length=10)
    producto_id: str = Field(foreign_key="productos.producto_id")
    cantidad: int
    precio_unitario: float
    cliente_id: str = Field(foreign_key="clientes.cliente_id")
    sucursal_id: Optional[int] = None
    total: float
    tiempo_id: str = Field(foreign_key="tiempo.tiempo_id")

    tiempo: Optional[Tiempo] = Relationship(back_populates="ventas")
    producto: Optional[Productos] = Relationship(back_populates="ventas")
    cliente: Optional[Clientes] = Relationship(back_populates="ventas")

class Envios(SQLModel, table=True):
    envio_id: str = Field(primary_key=True, max_length=10)
    venta_id: str = Field(foreign_key="ventas.venta_id")
    proveedor_id: str = Field(foreign_key="proveedores.proveedor_id")
    estado_envio: str
    tiempo_id: str = Field(foreign_key="tiempo.tiempo_id")

    tiempo: Optional[Tiempo] = Relationship(back_populates="envios")
    proveedor: Optional[Proveedores] = Relationship(back_populates="envios")
