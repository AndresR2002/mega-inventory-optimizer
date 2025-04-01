DELETE FROM tiempo t
WHERE NOT EXISTS (SELECT 1 FROM ventas v WHERE v.tiempo_id = t.tiempo_id)
AND NOT EXISTS (SELECT 1 FROM envios e WHERE e.tiempo_id = t.tiempo_id);

DELETE FROM ventas
WHERE tiempo_id IN (
    SELECT tiempo_id FROM tiempo
    WHERE fecha::DATE > CURRENT_DATE
);

DELETE FROM envios
WHERE tiempo_id IN (
    SELECT tiempo_id FROM tiempo
    WHERE fecha::DATE > CURRENT_DATE
);
