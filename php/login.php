<?php
session_start();
require_once 'conexion.php';

// Configurar headers para JSON
header('Content-Type: application/json; charset=utf-8');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: POST');
header('Access-Control-Allow-Headers: Content-Type');

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode([
        'success' => false, 
        'message' => 'Método no permitido. Use POST.'
    ]);
    exit;
}

try {
    // Validar que todos los campos requeridos estén presentes
    $required_fields = ['correo', 'password'];
    $missing_fields = [];
    
    foreach ($required_fields as $field) {
        if (!isset($_POST[$field]) || trim($_POST[$field]) === '') {
            $missing_fields[] = $field;
        }
    }
    
    if (!empty($missing_fields)) {
        throw new Exception("Campos obligatorios faltantes: " . implode(', ', $missing_fields));
    }

    // Sanitizar datos
    $correo = trim(strtolower($_POST['correo']));
    $password = $_POST['password'];

    // Validaciones básicas
    if (!filter_var($correo, FILTER_VALIDATE_EMAIL)) {
        throw new Exception("El formato del correo electrónico no es válido");
    }

    if (strlen($password) < 6) {
        throw new Exception("La contraseña debe tener al menos 6 caracteres");
    }

    // Buscar usuario en la base de datos
    $stmt = $pdo->prepare("SELECT id_usuario, nombre, correo, password_hash, rol FROM usuarios WHERE correo = ?");
    $stmt->execute([$correo]);
    
    $usuario = $stmt->fetch();
    
    if (!$usuario) {
        throw new Exception("Correo electrónico o contraseña incorrectos");
    }

    // Verificar contraseña
    if (!password_verify($password, $usuario['password_hash'])) {
        throw new Exception("Correo electrónico o contraseña incorrectos");
    }

    // Crear sesión
    $_SESSION['user_id'] = $usuario['id_usuario'];
    $_SESSION['user_name'] = $usuario['nombre'];
    $_SESSION['user_email'] = $usuario['correo'];
    $_SESSION['user_role'] = $usuario['rol'];
    $_SESSION['logged_in'] = true;

    // Log de éxito
    error_log("Usuario logueado exitosamente: ID {$usuario['id_usuario']}, Email: {$correo}");

    // Respuesta exitosa
    echo json_encode([
        'success' => true,
        'message' => 'Inicio de sesión exitoso',
        'user' => [
            'id' => intval($usuario['id_usuario']),
            'name' => $usuario['nombre'],
            'email' => $usuario['correo'],
            'role' => $usuario['rol']
        ],
        'redirect' => '../vistas/index.html'
    ]);

} catch (Exception $e) {
    error_log("Error de login: " . $e->getMessage());
    
    http_response_code(400);
    echo json_encode([
        'success' => false,
        'message' => $e->getMessage()
    ]);

} catch (PDOException $e) {
    error_log("Error de base de datos en login: " . $e->getMessage());
    
    http_response_code(500);
    echo json_encode([
        'success' => false,
        'message' => 'Error interno del servidor. Intente nuevamente.'
    ]);

} catch (Throwable $e) {
    error_log("Error inesperado en login: " . $e->getMessage());
    
    http_response_code(500);
    echo json_encode([
        'success' => false,
        'message' => 'Error interno del servidor'
    ]);
}
?>