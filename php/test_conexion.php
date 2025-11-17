<?php
// Archivo de prueba para verificar la conexión y configuración
header('Content-Type: application/json');

echo "=== PRUEBA DE CONEXIÓN MERCADO VECINO ===\n";

try {
    // Incluir conexión
    require_once 'conexion.php';
    echo "✅ Archivo de conexión incluido correctamente\n";
    
    // Probar conexión PDO
    if (isset($pdo)) {
        echo "✅ Variable PDO existe\n";
        
        // Probar query simple
        $stmt = $pdo->query("SELECT 1 as test");
        $result = $stmt->fetch();
        
        if ($result && $result['test'] == 1) {
            echo "✅ Conexión a base de datos funcional\n";
        }
        
        // Verificar si existe la tabla usuarios
        $stmt = $pdo->query("SHOW TABLES LIKE 'usuarios'");
        if ($stmt->rowCount() > 0) {
            echo "✅ Tabla 'usuarios' existe\n";
            
            // Verificar estructura de la tabla
            $stmt = $pdo->query("DESCRIBE usuarios");
            $columns = $stmt->fetchAll();
            echo "📋 Columnas de la tabla usuarios:\n";
            foreach ($columns as $column) {
                echo "   - {$column['Field']} ({$column['Type']})\n";
            }
            
            // Contar usuarios existentes
            $stmt = $pdo->query("SELECT COUNT(*) as total FROM usuarios");
            $count = $stmt->fetch()['total'];
            echo "👥 Total de usuarios registrados: {$count}\n";
            
        } else {
            echo "❌ Tabla 'usuarios' no existe\n";
            echo "💡 Ejecuta el script SQL para crear las tablas\n";
        }
        
    } else {
        echo "❌ Variable PDO no está definida\n";
    }
    
} catch (PDOException $e) {
    echo "❌ Error de conexión PDO: " . $e->getMessage() . "\n";
    echo "💡 Verifica:\n";
    echo "   - Que MySQL esté ejecutándose\n";
    echo "   - Que la base de datos 'mercado_vecino_v3' existe\n";
    echo "   - Las credenciales en conexion.php\n";
    
} catch (Exception $e) {
    echo "❌ Error general: " . $e->getMessage() . "\n";
}

echo "\n=== CONFIGURACIÓN DEL SISTEMA ===\n";
echo "🐘 Versión PHP: " . phpversion() . "\n";
echo "📁 Directorio actual: " . __DIR__ . "\n";
echo "🌐 Servidor: " . $_SERVER['SERVER_SOFTWARE'] ?? 'No disponible' . "\n";

// Verificar extensiones necesarias
$required_extensions = ['pdo', 'pdo_mysql', 'json', 'mbstring'];
echo "📦 Extensiones PHP requeridas:\n";
foreach ($required_extensions as $ext) {
    $status = extension_loaded($ext) ? '✅' : '❌';
    echo "   {$status} {$ext}\n";
}

echo "\n=== CONFIGURACIÓN DE SESIONES ===\n";
if (session_status() === PHP_SESSION_NONE) {
    session_start();
    echo "✅ Sesión iniciada correctamente\n";
} else {
    echo "ℹ️  Sesión ya estaba activa\n";
}
echo "🔑 Session ID: " . session_id() . "\n";

echo "\n=== PERMISOS DE ARCHIVOS ===\n";
$files_to_check = [
    'conexion.php',
    'registrar.php'
];

foreach ($files_to_check as $file) {
    if (file_exists($file)) {
        $perms = substr(sprintf('%o', fileperms($file)), -4);
        echo "📄 {$file}: {$perms} " . (is_readable($file) ? '✅ Legible' : '❌ No legible') . "\n";
    } else {
        echo "📄 {$file}: ❌ No existe\n";
    }
}

echo "\n=== FIN DE LA PRUEBA ===\n";
?>