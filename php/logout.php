<?php
session_start();

// Limpiar todas las variables de sesión
$_SESSION = array();

// Si se está usando cookies de sesión, eliminar la cookie
if (ini_get("session.use_cookies")) {
    $params = session_get_cookie_params();
    setcookie(session_name(), '', time() - 42000,
        $params["path"], $params["domain"],
        $params["secure"], $params["httponly"]
    );
}

// Destruir la sesión
session_destroy();

header('Content-Type: application/json');
echo json_encode([
    'success' => true,
    'message' => 'Sesión cerrada exitosamente',
    'redirect' => '../vistas/login.html'
]);
?>