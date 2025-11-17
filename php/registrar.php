<?php
session_start();
require_once 'conexion.php';

// Configurar headers para JSON
header('Content-Type: application/json; charset=utf-8');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: POST');
header('Access-Control-Allow-Headers: Content-Type');

// Log de debugging (opcional - remover en producción)
error_log("Método: " . $_SERVER['REQUEST_METHOD']);
error_log("POST data: " . print_r($_POST, true));

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
    $required_fields = ['nombre', 'correo', 'password'];
    $missing_fields = [];
    
    foreach ($required_fields as $field) {
        if (!isset($_POST[$field]) || trim($_POST[$field]) === '') {
            $missing_fields[] = $field;
        }
    }
    
    if (!empty($missing_fields)) {
        throw new Exception("Campos obligatorios faltantes: " . implode(', ', $missing_fields));
    }

    // Sanitizar y obtener datos
    $nombre = trim($_POST['nombre']);
    $correo = trim(strtolower($_POST['correo'])); // Normalizar email
    $password = $_POST['password'];
    $telefono = isset($_POST['telefono']) && trim($_POST['telefono']) !== '' ? trim($_POST['telefono']) : null;
    $direccion = isset($_POST['direccion']) && trim($_POST['direccion']) !== '' ? trim($_POST['direccion']) : null;
    $rol = isset($_POST['rol']) ? strtoupper(trim($_POST['rol'])) : 'COMPRADOR';

    // Validaciones mejoradas
    if (strlen($nombre) < 2) {
        throw new Exception("El nombre debe tener al menos 2 caracteres");
    }
    
    if (strlen($nombre) > 60) {
        throw new Exception("El nombre no puede exceder 60 caracteres");
    }
    
    // Validar que el nombre no contenga solo números o caracteres especiales
    if (!preg_match("/^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$/u", $nombre)) {
        throw new Exception("El nombre solo puede contener letras y espacios");
    }

    if (!filter_var($correo, FILTER_VALIDATE_EMAIL)) {
        throw new Exception("El formato del correo electrónico no es válido");
    }
    
    if (strlen($correo) > 120) {
        throw new Exception("El correo electrónico es demasiado largo");
    }

    if (strlen($password) < 6) {
        throw new Exception("La contraseña debe tener al menos 6 caracteres");
    }
    
    if (strlen($password) > 255) {
        throw new Exception("La contraseña es demasiado larga");
    }

    // Validar teléfono si se proporciona
    if ($telefono !== null) {
        if (strlen($telefono) < 7 || strlen($telefono) > 20) {
            throw new Exception("El teléfono debe tener entre 7 y 20 caracteres");
        }
        
        // Validar formato básico de teléfono
        if (!preg_match("/^[\+]?[\d\s\-\(\)]{7,20}$/", $telefono)) {
            throw new Exception("El formato del teléfono no es válido");
        }
    }

    // Validar dirección si se proporciona
    if ($direccion !== null && strlen($direccion) > 255) {
        throw new Exception("La dirección no puede exceder 255 caracteres");
    }

    // Validar rol
    $roles_validos = ['COMPRADOR', 'VENDEDOR', 'ADMIN'];
    if (!in_array($rol, $roles_validos)) {
        $rol = 'COMPRADOR';
    }

    // Verificar si el correo ya existe
    $stmt = $pdo->prepare("SELECT id_usuario, nombre FROM usuarios WHERE correo = ?");
    $stmt->execute([$correo]);
    
    if ($stmt->rowCount() > 0) {
        throw new Exception("Ya existe una cuenta registrada con este correo electrónico");
    }

    // Hash de la contraseña
    $password_hash = password_hash($password, PASSWORD_DEFAULT);
    
    if (!$password_hash) {
        throw new Exception("Error al procesar la contraseña");
    }

    // Insertar usuario en la base de datos
    $sql = "INSERT INTO usuarios (rol, nombre, correo, telefono, password_hash, direccion) 
            VALUES (?, ?, ?, ?, ?, ?)";
            
    $stmt = $pdo->prepare($sql);
    $result = $stmt->execute([$rol, $nombre, $correo, $telefono, $password_hash, $direccion]);
    
    if (!$result) {
        throw new Exception("Error al crear la cuenta en la base de datos");
    }

    $user_id = $pdo->lastInsertId();
    
    if (!$user_id) {
        throw new Exception("Error al obtener el ID del usuario creado");
    }

    // Crear sesión para el usuario recién registrado
    $_SESSION['user_id'] = $user_id;
    $_SESSION['user_name'] = $nombre;
    $_SESSION['user_email'] = $correo;
    $_SESSION['user_role'] = $rol;
    $_SESSION['logged_in'] = true;

    // Log de éxito
    error_log("Usuario creado exitosamente: ID {$user_id}, Email: {$correo}");

    // Respuesta exitosa
    echo json_encode([
        'success' => true,
        'message' => 'Usuario registrado exitosamente',
        'user_id' => intval($user_id),
        'user_name' => $nombre,
        'user_role' => $rol,
        'redirect' => 'index.html'
    ]);

} catch (Exception $e) {
    // Log del error específico
    error_log("Error de validación: " . $e->getMessage());
    
    http_response_code(400);
    echo json_encode([
        'success' => false,
        'message' => $e->getMessage()
    ]);

} catch (PDOException $e) {
    // Log del error de base de datos
    error_log("Error de base de datos en registro: " . $e->getMessage());
    
    http_response_code(500);
    echo json_encode([
        'success' => false,
        'message' => 'Error interno del servidor. Intente nuevamente.'
    ]);

} catch (Throwable $e) {
    // Catch para cualquier otro error inesperado
    error_log("Error inesperado en registro: " . $e->getMessage());
    
    http_response_code(500);
    echo json_encode([
        'success' => false,
        'message' => 'Error interno del servidor'
    ]);
}
?>