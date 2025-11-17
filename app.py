from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import os
from conexion import db  # Importar la conexión MySQL

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta_aqui'  # Cambia esto por una clave secreta segura

UPLOAD_FOLDER = 'static/imagenes/perfiles'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def init_db():
    """Función para inicializar la base de datos si es necesario"""
    if db.connect():
        print("Conexión a MySQL establecida correctamente")
    else:
        print("Error al conectar con MySQL")


# ----------------- Rutas principales -----------------

@app.route('/')
def index():
    """Página principal"""
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Página de inicio de sesión"""
    if request.method == 'POST':
        correo = request.form.get('correo')
        contraseña = request.form.get('contraseña')

        if not correo or not contraseña:
            flash('Por favor completa todos los campos', 'error')
            return render_template('login.html')

        query = 'SELECT * FROM usuarios WHERE correo = %s'
        users = db.execute_query(query, (correo,))

        if users and len(users) > 0:
            user = users[0]
            if check_password_hash(user['password_hash'], contraseña):
                # Guardamos en sesión los datos
                session['user_id'] = user['id_usuario']
                session['user_name'] = user['nombre']
                session['user_email'] = user['correo']
                session['user_phone'] = user['telefono']
                session['user_address'] = user['direccion']
                session['user_role'] = user['rol']

                flash('Inicio de sesión exitoso', 'success')
                return redirect(url_for('perfil_comprador'))

        flash('Credenciales incorrectas', 'error')

    return render_template('login.html')


@app.route('/registrar', methods=['GET', 'POST'])
def registrar():
    """Página de registro"""
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        apellido = request.form.get('apellido')
        correo = request.form.get('correo')
        telefono = request.form.get('telefono')
        contraseña = request.form.get('contraseña')
        confirm_password = request.form.get('confirm_password')
        rol = request.form.get('rol', 'COMPRADOR')
        direccion = request.form.get('direccion')

        if not all([nombre, apellido, correo, contraseña]):
            flash('Por favor completa todos los campos obligatorios', 'error')
            return render_template('registrar.html')

        if contraseña != confirm_password:
            flash('Las contraseñas no coinciden', 'error')
            return render_template('registrar.html')

        if len(contraseña) < 6:
            flash('La contraseña debe tener al menos 6 caracteres', 'error')
            return render_template('registrar.html')

        check_query = 'SELECT id_usuario FROM usuarios WHERE correo = %s'
        existing_users = db.execute_query(check_query, (correo,))

        if existing_users and len(existing_users) > 0:
            flash('Ya existe una cuenta con este correo electrónico', 'error')
            return render_template('registrar.html')

        hashed_password = generate_password_hash(contraseña)

        rol_mapping = {
            'cliente': 'COMPRADOR',
            'vendedor': 'VENDEDOR'
        }
        rol_bd = rol_mapping.get(rol, 'COMPRADOR')

        insert_query = '''
            INSERT INTO usuarios (nombre, apellido, correo, telefono, password_hash, rol, direccion)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        '''

        user_id = db.execute_insert(insert_query,
            (nombre, apellido, correo, telefono, hashed_password, rol_bd, direccion))

        if user_id:
            flash('Cuenta creada exitosamente', 'success')
            return redirect(url_for('login'))
        else:
            flash('Error al crear la cuenta. Inténtalo de nuevo.', 'error')
            return render_template('registrar.html')

    return render_template('registrar.html')


@app.route('/logout')
def logout():
    """Cerrar sesión"""
    session.clear()
    flash('Sesión cerrada exitosamente', 'success')
    return redirect(url_for('index'))


# ----------------- Perfil comprador -----------------

from werkzeug.utils import secure_filename

@app.route('/editar_perfil', methods=['POST'])
def editar_perfil():
    """Actualizar datos del perfil del comprador"""
    if 'user_id' not in session:
        flash('Debes iniciar sesión para editar tu perfil', 'error')
        return redirect(url_for('login'))

    user_id = session['user_id']
    nombre = request.form.get('nombre')
    apellido = request.form.get('apellido')
    correo = request.form.get('correo')
    telefono = request.form.get('telefono')
    direccion = request.form.get('direccion')

    # Si subió nueva foto
    foto = request.files.get('foto')
    foto_filename = None
    if foto and foto.filename != '':
        filename = secure_filename(foto.filename)
        foto_filename = f"user_{user_id}_{filename}"
        foto.save(os.path.join(app.config['UPLOAD_FOLDER'], foto_filename))

    # Construir query dinámico
    update_fields = []
    params = []

    if nombre:
        update_fields.append("nombre = %s")
        params.append(nombre)
    if apellido:
        update_fields.append("apellido = %s")
        params.append(apellido)
    if correo:
        update_fields.append("correo = %s")
        params.append(correo)
    if telefono:
        update_fields.append("telefono = %s")
        params.append(telefono)
    if direccion:
        update_fields.append("direccion = %s")
        params.append(direccion)
    if foto_filename:
        update_fields.append("foto = %s")
        params.append(f"imagenes/perfiles/{foto_filename}")

    params.append(user_id)

    if update_fields:
        query = f"UPDATE usuarios SET {', '.join(update_fields)} WHERE id_usuario = %s"
        db.execute_update(query, tuple(params))

        # Actualizar sesión
        if nombre: session['user_name'] = nombre
        if apellido: session['user_lastname'] = apellido
        if correo: session['user_email'] = correo
        if telefono: session['user_phone'] = telefono
        if direccion: session['user_address'] = direccion
        if foto_filename: session['user_foto'] = f"imagenes/perfiles/{foto_filename}"

        flash("Perfil actualizado correctamente", "success")

    return redirect(url_for('perfil_comprador'))

@app.route('/perfil_comprador')
def perfil_comprador():
    """Página de perfil del comprador"""
    if 'user_id' not in session:
        flash('Debes iniciar sesión para acceder a esta página', 'error')
        return redirect(url_for('login'))

    return render_template('perfil_comprador.html')


# ----------------- Otras rutas -----------------

@app.route('/carrito_compras')
def carrito_compras():
    """Página del carrito de compras"""
    if 'user_id' not in session:
        flash('Debes iniciar sesión para acceder a esta página', 'error')
        return redirect(url_for('login'))
    return render_template('carrito_compras.html')


@app.route('/productos')
def productos():
    """Página de productos"""
    query = '''
        SELECT p.*, u.nombre as vendedor_nombre 
        FROM productos p 
        JOIN usuarios u ON p.id_vendedor = u.id_usuario 
        WHERE p.estado = 'PUBLICADO'
        ORDER BY p.id_producto DESC
    '''
    productos = db.execute_query(query)
    return render_template('productos.html', productos=productos)


@app.route('/api/productos')
def api_productos():
    """API para obtener productos"""
    query = '''
        SELECT p.*, u.nombre as vendedor_nombre 
        FROM productos p 
        JOIN usuarios u ON p.id_vendedor = u.id_usuario 
        WHERE p.estado = 'PUBLICADO'
        ORDER BY p.id_producto DESC
    '''
    productos = db.execute_query(query)

    productos_list = []
    for producto in productos:
        productos_list.append({
            'id': producto['id_producto'],
            'nombre': producto['nombre'],
            'descripcion': producto['descripcion'],
            'precio': float(producto['precio']) if producto['precio'] else 0,
            'categoria': producto['categoria'],
            'vendedor': producto['vendedor_nombre']
        })

    return jsonify(productos_list)


# ----------------- Inicialización -----------------

if __name__ == '__main__':
    os.makedirs('static/css', exist_ok=True)
    os.makedirs('static/js', exist_ok=True)
    os.makedirs('static/imagenes', exist_ok=True)
    os.makedirs('templates', exist_ok=True)

    init_db()
    app.run(debug=True)
