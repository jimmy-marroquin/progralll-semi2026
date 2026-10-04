from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib import parse
from urllib.parse import urlparse, parse_qs
import json
import crud_clientes
import crud_tarifas
import crud_periodos

port = 3000
crudClientes = crud_clientes.crud_clientes()
crudTarifas = crud_tarifas.crudTarifas()
crudPeriodos = crud_periodos.crudPeriodos()

class miServidor(SimpleHTTPRequestHandler):
    def do_POST(self):
        longitud = int(self.headers['Content-Length'])
        datos = self.rfile.read(longitud)
        datos = datos.decode("utf-8")
        datos = parse.unquote(datos)
        datos = json.loads(datos)
        urlParse = urlparse(self.path)

    
        if urlParse.path == "/periodo":
            respuesta = {'msg': crudPeriodos.guardar(datos)}
        elif urlParse.path == "/calcular":
            calc, msg = crudTarifas.calcular(datos['balance'])
            if calc:
                respuesta = calc
            else:
                respuesta = {'msg': msg}
        else:
        
            respuesta = {'msg': crudClientes.administrar(datos)}

        self.send_response(200)
        self.send_header("Content-type","application/json")
        self.end_headers()
        self.wfile.write(json.dumps(respuesta).encode("utf-8"))

    def do_GET(self):
        urlParse = urlparse(self.path)
        qs = parse_qs(urlParse.query)

        if urlParse.path == "/clientes":
            buscar = qs.get('buscar', [''])[0]
            print(buscar)
            datos = crudClientes.consultar(buscar)
            self.send_response(200)
            self.send_header("Content-type","text/json")
            self.end_headers()
            self.wfile.write(json.dumps(datos).encode("utf-8"))

        # ESTO ES LO NUEVO QUE AGREGAS
        elif urlParse.path == "/periodos":
            datos = crudPeriodos.consultar()
            self.send_response(200)
            self.send_header("Content-type","text/json")
            self.end_headers()
            self.wfile.write(json.dumps(datos, default=str).encode("utf-8"))

        elif self.path == "/":
            self.path = "/index.html"
            return SimpleHTTPRequestHandler.do_GET(self)

        else:
            return SimpleHTTPRequestHandler.do_GET(self)

print(f"Servidor corriendo en el puerto {port}")
HTTPServer(("localhost", port), miServidor).serve_forever()