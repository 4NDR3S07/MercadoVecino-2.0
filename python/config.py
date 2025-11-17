import os

class Config:
    # Configuración de la base de datos
    DB_HOST = os.environ.get('DB_HOST', 'localhost')
    DB_USER = os.environ.get('DB_USER', 'root')
    DB_PASSWORD = os.environ.get('DB_PASSWORD', '')
    DB_NAME = os.environ.get('DB_NAME', 'mercado_vecino')
    
    # Configuración de Flask
    SECRET_KEY = os.environ.get('SECRET_KEY', 'mercado_vecino_secret_key_2024')
    
    # Configuración de archivos
    UPLOAD_FOLDER = 'static/imagenes/productos'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB máximo para archivos
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
    
    # Configuración de paginación
    PRODUCTOS_POR_PAGINA = 12
    
    # Configuración de correo (para futuras funcionalidades)
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

def allowed_file(filename):
    """Verifica si el archivo tiene una extensión permitida"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS