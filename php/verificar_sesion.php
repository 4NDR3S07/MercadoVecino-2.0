<?php
session_start();
header('Content-Type: application/json');

// Verificar si hay una sesión activa
if (isset($_SESSION['logged_in']) && $_SESSION['logged_in'] === true && isset($_SESSION['user_id'])) {
    echo json_encode([
        'logged_in' => true,
        'user' => [
            'id' => $_SESSION['user_id'],
            'name' => $_SESSION['user_name'],
            'email' => $_SESSION['user_email'],
            'role' => $_SESSION['user_role']
        ]
    ]);
} else {
    echo json_encode([
        'logged_in' => false
    ]);
}
?>