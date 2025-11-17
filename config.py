from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import mysql.connector
from mysql.connector import Error
from datetime import datetime
import hashlib
import os

# Mantener tu configuración original que funciona
app = Flask(__name__, template_folder='../vistas')
app.secret_key = 'tu_clave_secreta_aqui_muy_segura_2024'

class MercadoVecinoWeb:
    def __init__(self):
        self.conexion = None
        self.cursor = None
    
    def conectar(self):
        """Establece conexión con la base de datos"""
        try:
            self.conexion = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="mercado_vecino_v3",
                charset='utf8mb4'
            )
            if self.conexion.is_connected():
                self.cursor = self.conexion.cursor(dictionary=True)
                return True
        except Error as e:
            print(f"Error de conexión: {e}")
            return False
    
    def _encriptar_contraseña(self, contraseña):
        return hashlib.sha256(contraseña.encode()).hexdigest()
    
    def _verificar_contraseña(self, contraseña, hash_almacenado):
        return self._encriptar_contraseña(contraseña) == hash_almacenado
    
    def registrar_usuario(self, nombre, apellido, correo, telefono, direccion, contraseña, rol="cliente"):
        """Registra un nuevo usuario - CORREGIDO para coincidir con tu BD"""
        try:
            if not self.conectar():
                return None
                
            # Verificar si el correo ya existe
            consulta_verificar = "SELECT correo FROM usuarios WHERE correo = %s"
            self.cursor.execute(consulta_verificar, (correo,))
            if self.cursor.fetchone():
                self.cerrar_conexion()
                return None
            
            # Encriptar contraseña
            contraseña_encriptada = self._encriptar_contraseña(contraseña)
            
            # Insertar nuevo usuario
            consulta = """
            INSERT INTO usuarios (nombre, apellido, correo, telefono, password_hash, direccion, rol, fecha_registro)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            parametros = (nombre, apellido, correo, telefono, contraseña_encriptada, direccion, rol, datetime.now())
            
            self.cursor.execute(consulta, parametros)
            self.conexion.commit()
            usuario_id = self.cursor.lastrowid
            
            self.cerrar_conexion()
            return usuario_id
            
        except Error as e:
            print(f"Error al registrar usuario: {e}")
            if self.conexion:
                self.conexion.rollback()
            self.cerrar_conexion()
            return None
    
    def iniciar_sesion(self, correo, contraseña):
        """Inicia sesión verificando credenciales"""
        try:
            if not self.conectar():
                return None
                
            consulta = "SELECT * FROM usuarios WHERE correo = %s"
            self.cursor.execute(consulta, (correo,))
            usuario = self.cursor.fetchone()
            
            resultado = None
            if usuario and self._verificar_contraseña(contraseña, usuario['password_hash']):
                resultado = usuario
            
            self.cerrar_conexion()
            return resultado
                
        except Error as e:
            print(f"Error al iniciar sesión: {e}")
            self.cerrar_conexion()
            return None
    
    def obtener_productos(self, categoria=None, busqueda=None, limite=20):
        """Obtiene productos con filtros opcionales"""
        try:
            if not self.conectar():
                return []
            
            consulta = "SELECT * FROM productos WHERE estado = 'activo'"
            parametros = []
            
            if categoria:
                consulta += " AND categoria = %s"
                parametros.append(categoria)
            
            if busqueda:
                consulta += " AND (nombre LIKE %s OR descripcion LIKE %s)"
                parametros.extend([f"%{busqueda}%", f"%{busqueda}%"])
            
            consulta += " ORDER BY id_producto DESC LIMIT %s"
            parametros.append(limite)
            
            self.cursor.execute(consulta, parametros)
            productos = self.cursor.fetchall()
            
            self.cerrar_conexion()
            return productos
            
        except Error as e:
            print(f"Error al obtener productos: {e}")
            self.cerrar_conexion()
            return []
    
    def obtener_producto_por_id(self, producto_id):
        """Obtiene un producto específico por ID"""
        try:
            if not self.conectar():
                return None
                
            consulta = "SELECT * FROM productos WHERE id_producto = %s AND estado = 'activo'"
            self.cursor.execute(consulta, (producto_id,))
            producto = self.cursor.fetchone()
            
            self.cerrar_conexion()
            return producto
            
        except Error as e:
            print(f"Error al obtener producto: {e}")
            self.cerrar_conexion()
            return None
    
    def obtener_categorias(self):
        """Obtiene las categorías disponibles"""
        try:
            if not self.conectar():
                return []
                
            consulta = "SELECT DISTINCT categoria FROM productos WHERE estado = 'activo' ORDER BY categoria"
            self.cursor.execute(consulta)
            categorias = [row['categoria'] for row in self.cursor.fetchall()]
            
            self.cerrar_conexion()
            return categorias
            
        except Error as e:
            print(f"Error al obtener categorías: {e}")
            self.cerrar_conexion()
            return []
    
    def cerrar_conexion(self):
        """Cierra la conexión a la base de datos"""
        try:
            if self.cursor:
                self.cursor.close()
                self.cursor = None
            if self.conexion and self.conexion.is_connected():
                self.conexion.close()
                self.conexion = None
        except Error as e:
            print(f"Error al cerrar conexión: {e}")

# Instancia global
mercado = MercadoVecinoWeb()

# ============= RUTAS DE LA APLICACIÓN WEB =============

@app.route('/')
def index():
    """Página principal"""
    try:
        productos = mercado.obtener_productos(limite=8)
        return render_template('index.html', productos=productos)
    except Exception as e:
        print(f"Error en ruta index: {e}")
        # Si no encuentra el template, crear respuesta simple
        return f'''
        <h1>Mercado Vecino</h1>
        <p>Bienvenido al sistema</p>
        <p><a href="/login">Iniciar Sesión</a> | <a href="/registro">Registrarse</a></p>
        <p>Error: {str(e)}</p>
        '''

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    """Registro de usuarios"""
    if request.method == 'POST':
        try:
            # Obtener datos del formulario
            nombre = request.form.get('nombre', '').strip()
            apellido = request.form.get('apellido', '').strip()
            correo = request.form.get('correo', '').strip()
            telefono = request.form.get('telefono', '').strip()
            direccion = request.form.get('direccion', '').strip()
            contraseña = request.form.get('contraseña', '')
            
            # Validar campos requeridos
            if not all([nombre, correo, telefono, direccion, contraseña]):
                flash('Todos los campos son obligatorios', 'error')
                return redirect(url_for('registro'))
            
            # Registrar usuario
            usuario_id = mercado.registrar_usuario(nombre, apellido, correo, telefono, direccion, contraseña)
            
            if usuario_id:
                flash('Usuario registrado exitosamente. Ahora puedes iniciar sesión.', 'success')
                return redirect(url_for('login'))
            else:
                flash('Error al registrar usuario. El correo podría ya estar registrado.', 'error')
                
        except Exception as e:
            print(f"Error en registro: {e}")
            flash('Error interno del servidor', 'error')
    
    try:
        return render_template('registro.html')
    except Exception as e:
        return f'''
        <h1>Registro de Usuario</h1>
        <form method="POST">
            <p>Nombre: <input type="text" name="nombre" required></p>
            <p>Apellido: <input type="text" name="apellido"></p>
            <p>Correo: <input type="email" name="correo" required></p>
            <p>Teléfono: <input type="text" name="telefono" required></p>
            <p>Dirección: <input type="text" name="direccion" required></p>
            <p>Contraseña: <input type="password" name="contraseña" required></p>
            <p><input type="submit" value="Registrarse"></p>
        </form>
        <p><a href="/">Volver al inicio</a></p>
        '''

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Inicio de sesión"""
    if request.method == 'POST':
        try:
            correo = request.form.get('correo', '').strip()
            contraseña = request.form.get('contraseña', '')
            
            if not correo or not contraseña:
                flash('Correo y contraseña son obligatorios', 'error')
                return redirect(url_for('login'))
            
            usuario = mercado.iniciar_sesion(correo, contraseña)
            
            if usuario:
                # Configurar sesión
                session['usuario_id'] = usuario['id_usuario']
                session['nombre'] = usuario['nombre']
                session['apellido'] = usuario.get('apellido', '')
                session['correo'] = usuario['correo']
                session['rol'] = usuario['rol']
                session['telefono'] = usuario.get('telefono', '')
                session['direccion'] = usuario.get('direccion', '')
                
                nombre_completo = f"{usuario['nombre']} {usuario.get('apellido', '')}".strip()
                flash(f'Bienvenido {nombre_completo}', 'success')
                return redirect(url_for('index'))
            else:
                flash('Correo o contraseña incorrectos', 'error')
                
        except Exception as e:
            print(f"Error en login: {e}")
            flash('Error interno del servidor', 'error')
    
    try:
        return render_template('login.html')
    except Exception as e:
        return f'''
        <h1>Iniciar Sesión</h1>
        <form method="POST">
            <p>Correo: <input type="email" name="correo" required></p>
            <p>Contraseña: <input type="password" name="contraseña" required></p>
            <p><input type="submit" value="Iniciar Sesión"></p>
        </form>
        <p><a href="/registro">Registrarse</a> | <a href="/">Volver al inicio</a></p>
        '''

@app.route('/logout')
def logout():
    """Cerrar sesión"""
    nombre = session.get('nombre', 'Usuario')
    session.clear()
    flash(f'Hasta luego {nombre}', 'info')
    return redirect(url_for('index'))

@app.route('/productos')
def productos():
    """Listado de productos"""
    try:
        categoria = request.args.get('categoria')
        busqueda = request.args.get('busqueda')
        
        productos = mercado.obtener_productos(categoria=categoria, busqueda=busqueda, limite=50)
        
        return render_template('productos.html', productos=productos)
    except Exception as e:
        print(f"Error en ruta productos: {e}")
        productos = mercado.obtener_productos(limite=50)
        html = '<h1>Productos</h1>'
        for producto in productos:
            html += f'<p>{producto["nombre"]} - ${producto["precio"]}</p>'
        return html

@app.route('/producto/<int:producto_id>')
def detalle_producto(producto_id):
    """Detalle de producto"""
    try:
        producto = mercado.obtener_producto_por_id(producto_id)
        if not producto:
            flash('Producto no encontrado', 'error')
            return redirect(url_for('productos'))
        
        return render_template('detalle_producto.html', producto=producto)
    except Exception as e:
        print(f"Error en detalle producto: {e}")
        return redirect(url_for('productos'))

@app.route('/perfil')
def perfil():
    """Perfil de usuario"""
    if 'usuario_id' not in session:
        flash('Debes iniciar sesión para ver tu perfil', 'warning')
        return redirect(url_for('login'))
    
    try:
        return render_template('perfil.html')
    except Exception as e:
        return f'''
        <h1>Mi Perfil</h1>
        <p>Nombre: {session.get('nombre', '')} {session.get('apellido', '')}</p>
        <p>Correo: {session.get('correo', '')}</p>
        <p>Teléfono: {session.get('telefono', '')}</p>
        <p>Dirección: {session.get('direccion', '')}</p>
        <p><a href="/">Volver al inicio</a></p>
        '''

# ============= RUTAS DE API =============

@app.route('/api/test-db')
def test_db():
    """Test de conexión a base de datos"""
    if mercado.conectar():
        mercado.cerrar_conexion()
        return jsonify({"status": "success", "message": "Conexión a BD exitosa"})
    else:
        return jsonify({"status": "error", "message": "Error de conexión a BD"})

@app.route('/api/productos')
def api_productos():
    """API para obtener productos"""
    try:
        categoria = request.args.get('categoria')
        busqueda = request.args.get('busqueda')
        limite = int(request.args.get('limite', 20))
        
        productos = mercado.obtener_productos(categoria=categoria, busqueda=busqueda, limite=limite)
        return jsonify({"status": "success", "productos": productos})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

# ============= MANEJO DE ERRORES SIMPLIFICADO =============

@app.errorhandler(404)
def pagina_no_encontrada(e):
    """Manejo de error 404"""
    return '<h1>Página no encontrada</h1><p><a href="/">Volver al inicio</a></p>', 404

@app.errorhandler(500)
def error_servidor(e):
    """Manejo de error 500"""
    return '<h1>Error interno del servidor</h1><p><a href="/">Volver al inicio</a></p>', 500

if __name__ == '__main__':
    print("=" * 50)
    print("🛒 MERCADO VECINO - SERVIDOR WEB")
    print("=" * 50)
    print("✅ Servidor iniciando en: http://localhost:5000")
    print("✅ Test de BD disponible en: http://localhost:5000/api/test-db")
    print("=" * 50)
    print("📁 Usando templates desde: ../vistas/")
    print("🔄 Presiona Ctrl+C para detener el servidor")
    print("=" * 50)
               
               
    app.run(debug=True, host='0.0.0.0', port=5000)


