from conexion import db
from datetime import datetime

class Usuario:
    @staticmethod
    def crear_usuario(nombre, apellido, correo, telefono, password_hash, rol='COMPRADOR', direccion=None):
        """Crea un nuevo usuario en la base de datos"""
        return db.execute_insert("""
            INSERT INTO usuarios (nombre, apellido, correo, telefono, password_hash, rol, direccion)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (nombre, apellido, correo, telefono, password_hash, rol, direccion))
    
    @staticmethod
    def buscar_por_correo(correo):
        """Busca un usuario por su correo electrónico"""
        usuarios = db.execute_query("SELECT * FROM usuarios WHERE correo = %s", (correo,))
        return usuarios[0] if usuarios else None
    
    @staticmethod
    def buscar_por_id(user_id):
        """Busca un usuario por su ID"""
        usuarios = db.execute_query("SELECT * FROM usuarios WHERE id_usuario = %s", (user_id,))
        return usuarios[0] if usuarios else None
    
    @staticmethod
    def actualizar_usuario(user_id, datos):
        """Actualiza los datos de un usuario"""
        campos = []
        valores = []
        
        for campo, valor in datos.items():
            if valor is not None:
                campos.append(f"{campo} = %s")
                valores.append(valor)
        
        if campos:
            valores.append(user_id)
            query = f"UPDATE usuarios SET {', '.join(campos)} WHERE id_usuario = %s"
            return db.execute_update(query, valores)
        return 0

class Producto:
    @staticmethod
    def obtener_productos(categoria=None, busqueda=None, limit=None):
        """Obtiene productos con filtros opcionales"""
        query = """
            SELECT p.*, u.nombre as vendedor_nombre, u.telefono as vendedor_telefono,
                   COALESCE(AVG(r.calificacion), 0) as rating,
                   COUNT(r.id_resena) as total_resenas
            FROM productos p 
            JOIN usuarios u ON p.id_vendedor = u.id_usuario
            LEFT JOIN resenas r ON p.id_producto = r.id_producto
            WHERE p.estado = 'PUBLICADO' AND p.stock > 0
        """
        params = []
        
        if categoria and categoria != 'TODOS':
            query += " AND p.categoria = %s"
            params.append(categoria)
        
        if busqueda:
            query += " AND (p.nombre LIKE %s OR p.descripcion LIKE %s)"
            params.extend([f"%{busqueda}%", f"%{busqueda}%"])
        
        query += " GROUP BY p.id_producto ORDER BY rating DESC, p.fecha_registro DESC"
        
        if limit:
            query += f" LIMIT {limit}"
        
        return db.execute_query(query, params)
    
    @staticmethod
    def obtener_producto_por_id(producto_id):
        """Obtiene un producto específico por su ID"""
        productos = db.execute_query("""
            SELECT p.*, u.nombre as vendedor_nombre, u.telefono as vendedor_telefono,
                   u.direccion as vendedor_direccion,
                   COALESCE(AVG(r.calificacion), 0) as rating,
                   COUNT(r.id_resena) as total_resenas
            FROM productos p 
            JOIN usuarios u ON p.id_vendedor = u.id_usuario
            LEFT JOIN resenas r ON p.id_producto = r.id_producto
            WHERE p.id_producto = %s
            GROUP BY p.id_producto
        """, (producto_id,))
        return productos[0] if productos else None
    
    @staticmethod
    def crear_producto(vendedor_id, nombre, descripcion, categoria, precio, stock):
        """Crea un nuevo producto"""
        return db.execute_insert("""
            INSERT INTO productos (id_vendedor, nombre, descripcion, categoria, precio, stock)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (vendedor_id, nombre, descripcion, categoria, precio, stock))
    
    @staticmethod
    def obtener_productos_vendedor(vendedor_id):
        """Obtiene todos los productos de un vendedor específico"""
        return db.execute_query("""
            SELECT p.*, COALESCE(AVG(r.calificacion), 0) as rating,
                   COUNT(r.id_resena) as total_resenas
            FROM productos p 
            LEFT JOIN resenas r ON p.id_producto = r.id_producto
            WHERE p.id_vendedor = %s
            GROUP BY p.id_producto
            ORDER BY p.fecha_registro DESC
        """, (vendedor_id,))

class Pedido:
    @staticmethod
    def crear_pedido(comprador_id, vendedor_id, total):
        """Crea un nuevo pedido"""
        return db.execute_insert("""
            INSERT INTO pedidos (id_comprador, id_vendedor, total)
            VALUES (%s, %s, %s)
        """, (comprador_id, vendedor_id, total))
    
    @staticmethod
    def agregar_item_pedido(pedido_id, producto_id, cantidad, precio_unitario):
        """Agrega un item al pedido"""
        return db.execute_insert("""
            INSERT INTO pedido_items (id_pedido, id_producto, cantidad, precio_unitario)
            VALUES (%s, %s, %s, %s)
        """, (pedido_id, producto_id, cantidad, precio_unitario))
    
    @staticmethod
    def obtener_pedidos_comprador(comprador_id, limit=None):
        """Obtiene los pedidos de un comprador"""
        query = """
            SELECT p.*, u.nombre as vendedor_nombre, u.telefono as vendedor_telefono
            FROM pedidos p
            JOIN usuarios u ON p.id_vendedor = u.id_usuario
            WHERE p.id_comprador = %s
            ORDER BY p.fecha_creacion DESC
        """
        if limit:
            query += f" LIMIT {limit}"
        
        return db.execute_query(query, (comprador_id,))
    
    @staticmethod
    def obtener_pedidos_vendedor(vendedor_id, limit=None):
        """Obtiene los pedidos para un vendedor"""
        query = """
            SELECT p.*, u.nombre as comprador_nombre, u.telefono as comprador_telefono
            FROM pedidos p
            JOIN usuarios u ON p.id_comprador = u.id_usuario
            WHERE p.id_vendedor = %s
            ORDER BY p.fecha_creacion DESC
        """
        if limit:
            query += f" LIMIT {limit}"
        
        return db.execute_query(query, (vendedor_id,))

class Favorito:
    @staticmethod
    def agregar_favorito(user_id, producto_id):
        """Agrega un producto a favoritos"""
        return db.execute_insert("""
            INSERT IGNORE INTO favoritos (id_usuario, id_producto) 
            VALUES (%s, %s)
        """, (user_id, producto_id))
    
    @staticmethod
    def quitar_favorito(user_id, producto_id):
        """Quita un producto de favoritos"""
        return db.execute_update("""
            DELETE FROM favoritos 
            WHERE id_usuario = %s AND id_producto = %s
        """, (user_id, producto_id))
    
    @staticmethod
    def obtener_favoritos(user_id):
        """Obtiene los productos favoritos de un usuario"""
        return db.execute_query("""
            SELECT p.*, f.fecha_agregado, u.nombre as vendedor_nombre,
                   COALESCE(AVG(r.calificacion), 0) as rating
            FROM favoritos f
            JOIN productos p ON f.id_producto = p.id_producto
            JOIN usuarios u ON p.id_vendedor = u.id_usuario
            LEFT JOIN resenas r ON p.id_producto = r.id_producto
            WHERE f.id_usuario = %s
            GROUP BY p.id_producto
            ORDER BY f.fecha_agregado DESC
        """, (user_id,))
    
    @staticmethod
    def es_favorito(user_id, producto_id):
        """Verifica si un producto está en favoritos"""
        resultado = db.execute_query("""
            SELECT 1 FROM favoritos 
            WHERE id_usuario = %s AND id_producto = %s
        """, (user_id, producto_id))
        return len(resultado) > 0

class Resena:
    @staticmethod
    def crear_resena(producto_id, comprador_id, calificacion, comentario=None):
        """Crea una nueva reseña"""
        return db.execute_insert("""
            INSERT INTO resenas (id_producto, id_comprador, calificacion, comentario)
            VALUES (%s, %s, %s, %s)
        """, (producto_id, comprador_id, calificacion, comentario))
    
    @staticmethod
    def obtener_resenas_producto(producto_id):
        """Obtiene todas las reseñas de un producto"""
        return db.execute_query("""
            SELECT r.*, u.nombre as comprador_nombre
            FROM resenas r
            JOIN usuarios u ON r.id_comprador = u.id_usuario
            WHERE r.id_producto = %s
            ORDER BY r.fecha_creacion DESC
        """, (producto_id,))