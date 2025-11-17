import mysql.connector
from mysql.connector import Error
import os

class DatabaseConnection:
    def __init__(self):
        self.host = 'localhost'
        self.database = 'mercadovecino'
        self.user = 'root'  # Cambia según tu configuración
        self.password = ''  # Cambia según tu configuración
        self.connection = None
        
    def connect(self):
        """Establece la conexión con la base de datos"""
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password,
                charset='utf8mb4',
                collation='utf8mb4_unicode_ci'
            )
            
            if self.connection.is_connected():
                print("✅ Conexión exitosa a la base de datos MySQL")
                return True
                
        except Error as e:
            print(f"❌ Error al conectar a MySQL: {e}")
            return False
    
    def disconnect(self):
        """Cierra la conexión con la base de datos"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("🔌 Conexión cerrada")
    
    def get_connection(self):
        """Retorna la conexión activa"""
        if not self.connection or not self.connection.is_connected():
            self.connect()
        return self.connection
    
    def execute_query(self, query, params=None):
        """Ejecuta una consulta SELECT y retorna los resultados"""
        try:
            cursor = self.get_connection().cursor(dictionary=True)
            cursor.execute(query, params or ())
            result = cursor.fetchall()
            cursor.close()
            return result
        except Error as e:
            print(f"❌ Error ejecutando consulta: {e}")
            return []
    
    def execute_insert(self, query, params=None):
        """Ejecuta una consulta INSERT y retorna el ID insertado"""
        try:
            cursor = self.get_connection().cursor()
            cursor.execute(query, params or ())
            self.connection.commit()
            last_id = cursor.lastrowid
            cursor.close()
            return last_id
        except Error as e:
            print(f"❌ Error en INSERT: {e}")
            self.connection.rollback()
            return None
    
    def execute_update(self, query, params=None):
        """Ejecuta una consulta UPDATE/DELETE y retorna filas afectadas"""
        try:
            cursor = self.get_connection().cursor()
            cursor.execute(query, params or ())
            self.connection.commit()
            affected_rows = cursor.rowcount
            cursor.close()
            return affected_rows
        except Error as e:
            print(f"❌ Error en UPDATE/DELETE: {e}")
            self.connection.rollback()
            return 0

# Instancia global de la conexión
db = DatabaseConnection()