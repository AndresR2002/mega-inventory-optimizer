CREATE TABLE "tiempo" (
    "tiempo_id" VARCHAR(10) PRIMARY KEY ,
    "fecha" DATE,
    "hora" TIME,
    "anio" INT,
    "mes" INT,
    "mes_nombre" VARCHAR(15),
    "dia" INT,
    "dia_nombre" VARCHAR(15)
);

CREATE TABLE "ventas" (
    "venta_id" VARCHAR(10) PRIMARY KEY,
    "producto_id" VARCHAR(10),
    "cantidad" INT,
    "precio_unitario" DECIMAL(10,2),
    "cliente_id" VARCHAR(10),
    "sucursal_id" INT,
    "total" DECIMAL(10,2),
    "tiempo_id" VARCHAR(10)
);

CREATE TABLE "clientes" (
    "cliente_id" VARCHAR(10) PRIMARY KEY,
    "nombre" VARCHAR(255),
    "edad" INT,
    "genero" VARCHAR(50) CHECK ("genero" IN ('Masculino', 'Femenino', 'Otro')),
    "ubicacion" VARCHAR(255)
);

CREATE TABLE "productos" (
    "producto_id" VARCHAR(10) PRIMARY KEY,
    "nombre_producto" VARCHAR(255),
    "categoria" VARCHAR(100) CHECK ("categoria" IN ('Abarrotes', 'Electrónica', 'Ropa', 'Hogar', 'Salud')),
    "precio_base" DECIMAL(10,2)
);

CREATE TABLE "proveedores" (
    "proveedor_id" VARCHAR(10) PRIMARY KEY,
    "nombre_proveedor" VARCHAR(255),
    "contacto" VARCHAR(255),
    "ubicacion" VARCHAR(255)
);

CREATE TABLE "envios" (
    "envio_id" VARCHAR(10) PRIMARY KEY,
    "venta_id" VARCHAR(10),
    "proveedor_id" VARCHAR(10),
    "estado_envio" VARCHAR(50) CHECK ("estado_envio" IN ('Retrasado', 'Entregado', 'En tránsito', 'Cancelado')),
    "tiempo_id" VARCHAR(10)
);


ALTER TABLE "ventas" ADD FOREIGN KEY ("tiempo_id") REFERENCES "tiempo" ("tiempo_id");

ALTER TABLE "ventas" ADD FOREIGN KEY ("producto_id") REFERENCES "productos" ("producto_id");

ALTER TABLE "ventas" ADD FOREIGN KEY ("cliente_id") REFERENCES "clientes" ("cliente_id");

ALTER TABLE "envios" ADD FOREIGN KEY ("venta_id") REFERENCES "ventas" ("venta_id");

ALTER TABLE "envios" ADD FOREIGN KEY ("tiempo_id") REFERENCES "tiempo" ("tiempo_id");

ALTER TABLE "envios" ADD FOREIGN KEY ("proveedor_id") REFERENCES "proveedores" ("proveedor_id");

CREATE INDEX idx_productos_categoria ON productos (categoria);

CREATE INDEX idx_ventas_fecha ON ventas (tiempo_id);
CREATE INDEX idx_ventas_producto ON ventas (producto_id, cliente_id);

CREATE INDEX idx_envios_venta ON envios (venta_id, proveedor_id);
CREATE INDEX idx_envios_fecha ON envios (tiempo_id);
CREATE INDEX idx_envios_estado ON envios (estado_envio);

CREATE INDEX idx_tiempo_fecha ON tiempo (fecha)

