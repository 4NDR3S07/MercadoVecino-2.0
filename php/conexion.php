<?php
// Configuración de la base de datos
define('DB_HOST', 'localhost');
define('DB_NAME', 'mercado_vecino_v3');
define('DB_USER', 'root'); // Cambia por tu usuario de MySQL
define('DB_PASS', ''); // Cambia por tu contraseña de MySQL

try {
    $pdo = new PDO(
        "mysql:host=" . DB_HOST . ";dbname=" . DB_NAME . ";charset=utf8mb4",
        DB_USER,
        DB_PASS,
        [
            PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
            PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
            PDO::ATTR_EMULATE_PREPARES => false,
        ]
    );
} catch (PDOException $e) {
    die("Error de conexión: " . $e->getMessage());
}
?>