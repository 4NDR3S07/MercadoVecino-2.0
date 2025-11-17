document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('registerForm');
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

    // Función para validar contraseña
    function isValidPassword(password) {
        return password.length >= 6;
    }

    // Función para validar teléfono (opcional pero si se ingresa debe ser válido)
    function isValidPhone(phone) {
        if (!phone || phone.trim() === '') return true; // Es opcional
        const phoneRegex = /^[+]?[\d\s\-\(\)]{7,20}$/;
        return phoneRegex.test(phone);
    }

    // Validación en tiempo real
    const nombreInput = document.getElementById('nombre');
    const correoInput = document.getElementById('correo');
    const passwordInput = document.getElementById('password');
    const confirmPasswordInput = document.getElementById('confirm_password');
    const telefonoInput = document.getElementById('telefono');

    // Validar nombre
    nombreInput.addEventListener('input', function() {
        const nombre = this.value.trim();
        if (nombre.length > 0) {
            if (nombre.length < 2 || nombre.length > 60) {
                this.style.borderColor = '#ff4757';
            } else {
                this.style.borderColor = '#27ae60';
                clearMessage();
            }
        } else {
            this.style.borderColor = '';
        }
    });

    // Validar email
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

    // Validar teléfono
    telefonoInput.addEventListener('input', function() {
        const telefono = this.value.trim();
        if (telefono.length > 0) {
            if (!isValidPhone(telefono)) {
                this.style.borderColor = '#ff4757';
            } else {
                this.style.borderColor = '#27ae60';
                clearMessage();
            }
        } else {
            this.style.borderColor = '';
        }
    });

    // Validar contraseña
    passwordInput.addEventListener('input', function() {
        const password = this.value;
        if (password.length > 0) {
            if (!isValidPassword(password)) {
                this.style.borderColor = '#ff4757';
            } else {
                this.style.borderColor = '#27ae60';
                clearMessage();
            }
        } else {
            this.style.borderColor = '';
        }
        
        // Re-validar confirmación si ya hay texto
        if (confirmPasswordInput.value.length > 0) {
            if (confirmPasswordInput.value !== password) {
                confirmPasswordInput.style.borderColor = '#ff4757';
            } else {
                confirmPasswordInput.style.borderColor = '#27ae60';
            }
        }
    });

    // Validar confirmación de contraseña
    confirmPasswordInput.addEventListener('input', function() {
        const confirmPassword = this.value;
        const password = passwordInput.value;
        
        if (confirmPassword.length > 0) {
            if (confirmPassword !== password) {
                this.style.borderColor = '#ff4757';
            } else {
                this.style.borderColor = '#27ae60';
                clearMessage();
            }
        } else {
            this.style.borderColor = '';
        }
    });

    // Manejar envío del formulario
    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        // Obtener datos del formulario
        const nombre = document.getElementById('nombre').value.trim();
        const correo = document.getElementById('correo').value.trim();
        const telefono = document.getElementById('telefono').value.trim();
        const password = document.getElementById('password').value;
        const confirmPassword = document.getElementById('confirm_password').value;
        const rol = document.getElementById('rol').value;
        const direccion = document.getElementById('direccion').value.trim();

        // Validaciones del lado cliente
        if (!nombre || nombre.length < 2 || nombre.length > 60) {
            showMessage('El nombre debe tener entre 2 y 60 caracteres', 'error');
            nombreInput.focus();
            return;
        }

        if (!correo || !isValidEmail(correo)) {
            showMessage('Ingresa un correo electrónico válido', 'error');
            correoInput.focus();
            return;
        }

        if (telefono && !isValidPhone(telefono)) {
            showMessage('El formato del teléfono no es válido', 'error');
            telefonoInput.focus();
            return;
        }

        if (!password || !isValidPassword(password)) {
            showMessage('La contraseña debe tener al menos 6 caracteres', 'error');
            passwordInput.focus();
            return;
        }

        if (password !== confirmPassword) {
            showMessage('Las contraseñas no coinciden', 'error');
            confirmPasswordInput.focus();
            return;
        }

        // Preparar datos para envío
        const formData = new FormData();
        formData.append('nombre', nombre);
        formData.append('correo', correo);
        formData.append('password', password);
        formData.append('rol', rol);
        
        if (telefono) {
            formData.append('telefono', telefono);
        }
        
        if (direccion) {
            formData.append('direccion', direccion);
        }

        // Mostrar estado de carga
        submitBtn.disabled = true;
        btnText.style.display = 'none';
        loading.style.display = 'inline';
        clearMessage();

        try {
            // Enviar datos al servidor - RUTA CORREGIDA PARA TU ESTRUCTURA
            const response = await fetch('../php/registrar.php', {
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
                showMessage('¡Cuenta creada exitosamente! Redirigiendo...', 'success');
                
                // Limpiar formulario
                form.reset();
                
                // Limpiar estilos de validación
                const inputs = form.querySelectorAll('input, select, textarea');
                inputs.forEach(input => {
                    input.style.borderColor = '';
                });
                
                // Redireccionar después de 2 segundos
                setTimeout(() => {
                    window.location.href = data.redirect || '../index.html';
                }, 2000);
                
            } else {
                showMessage(data.message || 'Error al crear la cuenta', 'error');
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

    // Limpiar estilos de error al escribir
    const inputs = form.querySelectorAll('input, select, textarea');
    inputs.forEach(input => {
        input.addEventListener('focus', function() {
            clearMessage();
        });
    });
});