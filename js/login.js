document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('loginForm');
    const messageDiv = document.getElementById('message');
    const submitBtn = document.getElementById('submitBtn');
    const btnText = submitBtn.querySelector('.btn-text');
    const loading = submitBtn.querySelector('.loading');

    // Función para mostrar mensajes
    function showMessage(message, type = 'error') {
        messageDiv.textContent = message;
        messageDiv.className = `message ${type}`;
        messageDiv.style.display = 'block';
        
        // Scroll hacia el mensaje
        messageDiv.scrollIntoView({ behavior: 'smooth', block: 'center' });
        
        // Auto-hide después de 5 segundos para mensajes de éxito
        if (type === 'success') {
            setTimeout(() => {
                messageDiv.style.display = 'none';
            }, 5000);
        }
    }

    // Función para limpiar mensajes
    function clearMessage() {
        messageDiv.style.display = 'none';
    }

    // Función para validar email
    function isValidEmail(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    }

    // Referencias a campos
    const correoInput = document.getElementById('correo');
    const passwordInput = document.getElementById('password');

    // Validación en tiempo real
    correoInput.addEventListener('input', function() {
        const correo = this.value.trim();
        if (correo.length > 0) {
            if (!isValidEmail(correo)) {
                this.style.borderColor = '#ff4757';
            } else {
                this.style.borderColor = '#27ae60';
                clearMessage();
            }
        } else {
            this.style.borderColor = '';
        }
    });

    passwordInput.addEventListener('input', function() {
        const password = this.value;
        if (password.length > 0) {
            if (password.length < 6) {
                this.style.borderColor = '#ff4757';
            } else {
                this.style.borderColor = '#27ae60';
                clearMessage();
            }
        } else {
            this.style.borderColor = '';
        }
    });

    // Limpiar mensajes al hacer focus
    [correoInput, passwordInput].forEach(input => {
        input.addEventListener('focus', function() {
            clearMessage();
        });
    });

    // Manejar envío del formulario
    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        // Obtener datos del formulario
        const correo = correoInput.value.trim();
        const password = passwordInput.value;

        // Validaciones del lado cliente
        if (!correo) {
            showMessage('El correo electrónico es obligatorio', 'error');
            correoInput.focus();
            return;
        }

        if (!isValidEmail(correo)) {
            showMessage('Ingresa un correo electrónico válido', 'error');
            correoInput.focus();
            return;
        }

        if (!password) {
            showMessage('La contraseña es obligatoria', 'error');
            passwordInput.focus();
            return;
        }

        if (password.length < 6) {
            showMessage('La contraseña debe tener al menos 6 caracteres', 'error');
            passwordInput.focus();
            return;
        }

        // Preparar datos para envío
        const formData = new FormData();
        formData.append('correo', correo);
        formData.append('password', password);

        // Mostrar estado de carga
        submitBtn.disabled = true;
        btnText.style.display = 'none';
        loading.style.display = 'inline';
        clearMessage();

        try {
            // Enviar datos al servidor
            const response = await fetch('../php/login.php', {
                method: 'POST',
                body: formData
            });

            // Verificar si la respuesta es JSON válido
            let data;
            const contentType = response.headers.get('content-type');
            if (contentType && contentType.includes('application/json')) {
                data = await response.json();
            } else {
                // Si no es JSON, obtener texto para debugging
                const text = await response.text();
                console.error('Respuesta no JSON:', text);
                throw new Error('Error en la respuesta del servidor');
            }

            if (data.success) {
                showMessage('Inicio de sesión exitoso. Redirigiendo...', 'success');
                
                // Limpiar formulario
                form.reset();
                
                // Limpiar estilos de validación
                correoInput.style.borderColor = '';
                passwordInput.style.borderColor = '';
                
                // Redireccionar después de 1.5 segundos
                setTimeout(() => {
                    window.location.href = data.redirect || 'index.html';
                }, 1500);
                
            } else {
                showMessage(data.message || 'Error al iniciar sesión', 'error');
            }

        } catch (error) {
            console.error('Error:', error);
            showMessage('Error de conexión. Verifica que el servidor esté funcionando.', 'error');
        } finally {
            // Restaurar botón
            submitBtn.disabled = false;
            btnText.style.display = 'inline';
            loading.style.display = 'none';
        }
    });

    // Detectar Enter en los campos para enviar formulario
    [correoInput, passwordInput].forEach(input => {
        input.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                form.requestSubmit();
            }
        });
    });
});