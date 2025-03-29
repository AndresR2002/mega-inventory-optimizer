ALTER TABLE "tiempo" ADD CONSTRAINT "pk_tiempo" PRIMARY KEY ("tiempo_id");
ALTER TABLE "ventas" ADD CONSTRAINT "pk_ventas" PRIMARY KEY ("venta_id");
ALTER TABLE "clientes" ADD CONSTRAINT "pk_clientes" PRIMARY KEY ("cliente_id");
ALTER TABLE "productos" ADD CONSTRAINT "pk_productos" PRIMARY KEY ("producto_id");
ALTER TABLE "proveedores" ADD CONSTRAINT "pk_proveedores" PRIMARY KEY ("proveedor_id");
ALTER TABLE "envios" ADD CONSTRAINT "pk_envios" PRIMARY KEY ("envio_id");
