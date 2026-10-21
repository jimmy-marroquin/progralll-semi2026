from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import pymysql

app = Flask(__name__)
app.secret_key = 'clave_secreta_parcial'

def obtener_conexion():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='',
        database='db_academica',
        cursorclass=pymysql.cursors.DictCursor
    )

# 1. Login
@app.route('/', methods=['GET', 'POST'])
def login():
    mensaje = ""
    if request.method == 'POST':
        usuario = request.form['usuario']
        clave = request.form['clave']
        
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            query = "SELECT * FROM usuarios_usss092825 WHERE usuario = %s AND clave = %s"
            cursor.execute(query, (usuario, clave))
            user = cursor.fetchone()
        conexion.close()
        
        if user:
            session['usuario'] = user['usuario']
            return redirect(url_for('panel_usuarios'))
        else:
            mensaje = "Usuario o clave incorrectos, o no está registrado."
            
    return render_template('login.html', mensaje=mensaje)

# 2. Panel de gestión de usuarios
@app.route('/usuarios')
def panel_usuarios():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    return render_template('usuarios.html')

# 3. Método requerido: crud_usuarios_usss092825
@app.route('/crud_usuarios_usss092825', methods=['POST'])
def crud_usuarios_usss092825():
    data = request.json
    accion = data.get('accion')
    
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            if accion == 'registrar':
                query = """INSERT INTO usuarios_usss092825 (usuario, clave, nombre, dirección, teléfono) 
                           VALUES (%s, %s, %s, %s, %s)"""
                cursor.execute(query, (
                    data['usuario'], data['clave'], data['nombre'], 
                    data['direccion'], data['telefono']
                ))
                conexion.commit()
                return jsonify({'status': 'success', 'message': 'Usuario registrado correctamente'})
            
            elif accion == 'editar':
                query = """UPDATE usuarios_usss092825 SET usuario=%s, clave=%s, nombre=%s, dirección=%s, teléfono=%s 
                           WHERE idUsuario=%s"""
                cursor.execute(query, (
                    data['usuario'], data['clave'], data['nombre'], 
                    data['direccion'], data['telefono'], data['idUsuario']
                ))
                conexion.commit()
                return jsonify({'status': 'success', 'message': 'Usuario actualizado correctamente'})
            
            elif accion == 'eliminar':
                query = "DELETE FROM usuarios_usss092825 WHERE idUsuario=%s"
                cursor.execute(query, (data['idUsuario'],))
                conexion.commit()
                return jsonify({'status': 'success', 'message': 'Usuario eliminado correctamente'})
                
        return jsonify({'status': 'error', 'message': 'Acción no válida'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})
    finally:
        conexion.close()

# 4. Búsqueda de usuarios
@app.route('/buscar_usuarios', methods=['GET'])
def buscar_usuarios():
    termino = request.args.get('q', '')
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        query = "SELECT * FROM usuarios_usss092825 WHERE nombre LIKE %s OR usuario LIKE %s"
        cursor.execute(query, (f"%{termino}%", f"%{termino}%"))
        resultados = cursor.fetchall()
    conexion.close()
    return jsonify(resultados)

@app.route('/logout')
def logout():
    session.pop('usuario', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)