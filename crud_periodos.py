import conexion
from crud_tarifas import crudTarifas
db = conexion.Conexion()
ct = crudTarifas()

class crudPeriodos:
    def consultar(self):
        try:
            return db.consultar("SELECT p.*, c.nombre as cliente_nombre FROM periodos_impuestos p LEFT JOIN clientes c ON p.idCliente=c.idCliente ORDER BY p.idPeriodo DESC")
        except:
            return db.consultar("SELECT * FROM periodos_impuestos ORDER BY idPeriodo DESC")

    def guardar(self, datos):
        try:
            print("Datos que llegan a guardar:", datos)
            calc, msg = ct.calcular(datos.get('balance',0))
            if not calc:
                return msg
            sql = "INSERT INTO periodos_impuestos(idCliente, idImpuesto, fechaDesde, fechaHasta, balance, precioCalculado) VALUES(%s,%s,%s,%s,%s,%s)"
            res = db.ejecutar(sql, (datos['idCliente'], 1, datos['fechaDesde'], datos['fechaHasta'], datos['balance'], calc['impuesto']))
            print("Resultado insert:", res)
            return "ok"
        except Exception as e:
            print("ERROR en guardar:", e)
            return str(e)