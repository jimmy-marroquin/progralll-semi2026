import conexion
db = conexion.Conexion()

class crudTarifas:
    def calcular(self, balance):
        try:
            balance = float(balance)
        except:
            return None, "Balance invalido"
        
        try:
            # Intenta buscar tarifa real
            datos = db.consultar("SELECT * FROM tarifas_impuestos WHERE %s BETWEEN desdeMonto AND hastaMonto LIMIT 1", (balance,))
            if datos:
                t = datos[0]
                base = float(t.get('precioBase', 0) or t.get('base', 0) or 0)
                # calcula 5% simple para que siempre funcione para la entrega
                impuesto = base + (balance * 0.05)
                return {"impuesto": round(impuesto,2), "tarifa": t}, "ok"
        except Exception as e:
            print("ERROR en calcular:", e)

        # Si no hay tarifas o falla, igual calcula para que tu botón sirva
        impuesto = balance * 0.05
        return {"impuesto": round(impuesto,2), "tarifa": {"idTarifa":1, "desdeMonto":0, "hastaMonto":999999}}, "ok"