// index.js - JavaScript para la página principal
document.addEventListener('DOMContentLoaded', function() {
    // Cargar productos al cargar la página
    cargarProductos();
    
    // Configurar el buscador
    configurarBuscador();
    
    // Configurar filtros
    configurarFiltros();
});

function cargarProductos() {
    const productosContainer = document.getElementById('productosContainer');
    
    // Mostrar indicador de carga
    productosContainer.innerHTML = '<p>Cargando productos...</p>';
    
    // Simular carga de productos (reemplazar con llamada real a API)
    setTimeout(() => {
        const productosHTML = generarProductosHTML();
        productosContainer.innerHTML = productosHTML;
    }, 1000);
}

function generarProductosHTML() {
    // Productos de ejemplo - en producción estos vendrían de la API
    const productos = [
        {
            id: 1,
            nombre: 'Tomates frescos',
            descripcion: 'Tomates orgánicos cultivados localmente',
            precio: 5000,
            categoria: 'Verduras',
            vendedor: 'María González'
        },
        {
            id: 2,
            nombre: 'Pan casero',
            descripcion: 'Pan artesanal horneado diariamente',
            precio: 3000,
            categoria: 'Panadería',
            vendedor: 'Panadería El Horno'
        },
        {
            id: 3,
            nombre: 'Miel pura',
            descripcion: 'Miel 100% natural sin aditivos',
            precio: 15000,
            categoria: 'Endulzantes',
            vendedor: 'Apiario San José'
        }
    ];
    
    let html = '<div class="productos-grid">';
    
    productos.forEach(producto => {
        html += `
            <div class="producto-card">
                <h4>${producto.nombre}</h4>
                <p>${producto.descripcion}</p>
                <span class="precio">$${producto.precio.toLocaleString()}</span>
                <p><small>Vendedor: ${producto.vendedor}</small></p>
                <button class="btn-login-required" onclick="requireLogin()">
                    Agregar al carrito
                </button>
            </div>
        `;
    });
    
    html += '</div>';
    return html;
}

function configurarBuscador() {
    const buscador = document.querySelector('.buscador');
    
    if (buscador) {
        buscador.addEventListener('input', function(e) {
            const termino = e.target.value.toLowerCase();
            filtrarProductos(termino);
        });
    }
}

function configurarFiltros() {
    const filtro = document.getElementById('filtro');
    
    if (filtro) {
        filtro.addEventListener('change', function(e) {
            const tipoFiltro = e.target.value;
            aplicarFiltro(tipoFiltro);
        });
    }
}

function filtrarProductos(termino) {
    const productos = document.querySelectorAll('.producto-card');
    
    productos.forEach(producto => {
        const nombre = producto.querySelector('h4').textContent.toLowerCase();
        const descripcion = producto.querySelector('p').textContent.toLowerCase();
        
        if (nombre.includes(termino) || descripcion.includes(termino)) {
            producto.style.display = 'block';
        } else {
            producto.style.display = 'none';
        }
    });
}

function aplicarFiltro(tipoFiltro) {
    const productos = document.querySelectorAll('.producto-card');
    const productosArray = Array.from(productos);
    
    switch (tipoFiltro) {
        case 'precio':
            productosArray.sort((a, b) => {
                const precioA = parseInt(a.querySelector('.precio').textContent.replace(/[^\d]/g, ''));
                const precioB = parseInt(b.querySelector('.precio').textContent.replace(/[^\d]/g, ''));
                return precioA - precioB;
            });
            break;
        case 'categoria':
            // Implementar ordenamiento por categoría
            break;
        case 'fecha':
            // Productos más recientes primero (orden por defecto)
            break;
        case 'disponibilidad':
            // Mostrar solo productos disponibles
            break;
    }
    
    // Reordenar elementos en el DOM
    const container = document.querySelector('.productos-grid');
    if (container) {
        productosArray.forEach(producto => {
            container.appendChild(producto);
        });
    }
}

// FUNCIÓN QUE VERIFICA SI ESTÁ LOGUEADO
function requireLogin() {
    // Verificar si el usuario está logueado buscando el mensaje de bienvenida
    const userWelcome = document.getElementById('userWelcome');
    
    if (!userWelcome) {
        // Usuario NO logueado - mostrar mensaje y redirigir
        alert('Debes iniciar sesión para agregar productos al carrito');
        window.location.href = '/login';
    } else {
        // Usuario SÍ logueado - no hacer nada (función carrito no existe aún)
        console.log('Usuario logueado - función carrito pendiente de implementar');
        // Aquí irá tu función de carrito cuando la tengas lista
    }
}

// Función para cargar productos desde la API (para uso futuro)
async function cargarProductosDesdeAPI() {
    try {
        const response = await fetch('/api/productos');
        const productos = await response.json();
        
        const productosContainer = document.getElementById('productosContainer');
        let html = '<div class="productos-grid">';
        
        productos.forEach(producto => {
            html += `
                <div class="producto-card">
                    <h4>${producto.nombre}</h4>
                    <p>${producto.descripcion}</p>
                    <span class="precio">$${producto.precio.toLocaleString()}</span>
                    <p><small>Vendedor: ${producto.vendedor}</small></p>
                    <button class="btn-login-required" onclick="requireLogin()">
                        Agregar al carrito
                    </button>
                </div>
            `;
        });
        
        html += '</div>';
        productosContainer.innerHTML = html;
    } catch (error) {
        console.error('Error al cargar productos:', error);
        document.getElementById('productosContainer').innerHTML = 
            '<p>Error al cargar productos. Inténtalo de nuevo.</p>';
    }
}