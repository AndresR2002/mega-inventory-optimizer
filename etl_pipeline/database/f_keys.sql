ALTER TABLE "ventas" ADD CONSTRAINT "fk_ventas_tiempo" FOREIGN KEY ("tiempo_id") REFERENCES "tiempo" ("tiempo_id");
ALTER TABLE "ventas" ADD CONSTRAINT "fk_ventas_producto" FOREIGN KEY ("producto_id") REFERENCES "productos" ("producto_id");
ALTER TABLE "ventas" ADD CONSTRAINT "fk_ventas_cliente" FOREIGN KEY ("cliente_id") REFERENCES "clientes" ("cliente_id");

ALTER TABLE "envios" ADD CONSTRAINT "fk_envios_venta" FOREIGN KEY ("venta_id") REFERENCES "ventas" ("venta_id");
ALTER TABLE "envios" ADD CONSTRAINT "fk_envios_tiempo" FOREIGN KEY ("tiempo_id") REFERENCES "tiempo" ("tiempo_id");
ALTER TABLE "envios" ADD CONSTRAINT "fk_envios_proveedor" FOREIGN KEY ("proveedor_id") REFERENCES "proveedores" ("proveedor_id");
