CREATE INDEX idx_productos_categoria ON productos (categoria);
CREATE INDEX idx_ventas_fecha ON ventas (tiempo_id);
CREATE INDEX idx_ventas_producto ON ventas (producto_id, cliente_id);
CREATE INDEX idx_envios_venta ON envios (venta_id, proveedor_id);
CREATE INDEX idx_envios_fecha ON envios (tiempo_id);
CREATE INDEX idx_envios_estado ON envios (estado_envio);
CREATE INDEX idx_tiempo_fecha ON tiempo (fecha);
