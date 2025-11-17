document.addEventListener('DOMContentLoaded', async function() {
    const headerActions = document.getElementById('headerActions');
    const userWelcome = document.getElementById('userWelcome');
    
    try {
        // Verificar si hay una sesión activa
        const response = await fetch('../php/verificar_sesion.php');
        const data = await response.json();
        
        if (data.logged_in) {
            // Usuario logueado - mostrar opciones de usuario
            headerActions.innerHTML = `
                <div class="user-info">
                    <span>Hola, ${data.user.name}</span>
                    <button class="button-logout" onclick="logout()">Cerrar Sesión</button>
                </div>
            `;
            
            // Mostrar mensaje de bienvenida
            userWelcome.innerHTML = `
                <div class="welcome-message">
                    <h3>¡Bienvenido/a de vuelta, ${data.user.name}!</h3>
                    <p>Rol: ${data.user.role}</p>
                </div>
            `;
            userWelcome.style.display = 'block';
            
            // Cargar productos o contenido específico para usuarios logueados
            loadUserContent(data.user);
            
        } else {
            // Usuario no logueado - mostrar botones de login/registro
            headerActions.innerHTML = `
                <button class="button-iniciar" onclick="location.href='login.html'">Iniciar Sesión</button>
                <button class="button-registrar" onclick="location.href='registrar.html'">Registrarse</button>
            `;
            
            // Cargar contenido para visitantes
            loadGuestContent();
        }
    } catch (error) {
        console.error('Error al verificar sesión:', error);
        // En caso de error, mostrar botones de login/registro
        headerActions.innerHTML = `
            <button class="button-iniciar" onclick="location.href='login.html'">Iniciar Sesión</button>
            <button class="button-registrar" onclick="location.href='registrar.html'">Registrarse</button>
        `;
    }
});

// Función para cerrar sesión
async function logout() {
    try {
        const response = await fetch('../php/logout.php');
        const data = await response.json();
        
        if (data.success) {
            // Redireccionar al login
            window.location.href = 'login.html';
        }
    } catch (error) {
        console.error('Error al cerrar sesión:', error);
        // Forzar redirección en caso de error
        window.location.href = 'login.html';
    }
}

// Cargar contenido para usuarios logueados
function loadUserContent(user) {
    const productosContainer = document.getElementById('productosContainer');
    
    productosContainer.innerHTML = `
        <div class="user-dashboard">
            <h3>Panel de ${user.role === 'VENDEDOR' ? 'Vendedor' : 'Comprador'}</h3>
            
            ${user.role === 'VENDEDOR' ? `
                <div class="vendor-options">
                    <button class="dashboard-btn" onclick="location.href='#'">Mis Productos</button>
                    <button class="dashboard-btn" onclick="location.href='#'">Agregar Producto</button>
                    <button class="dashboard-btn" onclick="location.href='#'">Ventas</button>
                </div>
            ` : `
                <div class="buyer-options">
                    <button class="dashboard-btn" onclick="location.href='carrito_compras.html'">Mi Carrito</button>
                    <button class="dashboard-btn" onclick="location.href='#'">Mis Compras</button>
                    <button class="dashboard-btn" onclick="location.href='#'">Favoritos</button>
                </div>
            `}
            
            <div class="productos-grid">
                <div class="producto-card">
                    <h4>Producto de Ejemplo</h4>
                    <p>Descripción del producto...</p>
                    <span class="precio">$25.000</span>
                </div>
                <div class="producto-card">
                    <h4>Otro Producto</h4>
                    <p>Descripción del producto...</p>
                    <span class="precio">$15.000</span>
                </div>
            </div>
        </div>
    `;
}

// Cargar contenido para visitantes
function loadGuestContent() {
    const productosContainer = document.getElementById('productosContainer');
    
    productosContainer.innerHTML = `
        <div class="guest-content">
            <h3>¡Descubre MercadoVecino!</h3>
            <p>Inicia sesión o regístrate para acceder a todas las funciones</p>
            
            <div class="productos-grid">
                <div class="producto-card">
                    <h4>Producto de Ejemplo</h4>
                    <p>Descripción del producto...</p>
                    <span class="precio">$25.000</span>
                    <button class="btn-login-required" onclick="location.href='login.html'">
                        Iniciar sesión para comprar
                    </button>
                </div>
                <div class="producto-card">
                    <h4>Otro Producto</h4>
                    <p>Descripción del producto...</p>
                    <span class="precio">$15.000</span>
                    <button class="btn-login-required" onclick="location.href='login.html'">
                        Iniciar sesión para comprar
                    </button>
                </div>
            </div>
        </div>
    `;
}