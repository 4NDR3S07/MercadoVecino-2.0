// login.js - JavaScript para el formulario de login
document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('loginForm');
    const submitBtn = document.getElementById('submitBtn');
    const messageDiv = document.getElementById('message');
    
    // Validación en tiempo real
    const correoInput = document.getElementById('correo');
    const contraseñaInput = document.getElementById('contraseña');
    
    correoInput.addEventListener('blur', validateEmail);
    contraseñaInput.addEventListener('input', validatePassword);
    
    // Manejar envío del formulario
    loginForm.addEventListener('submit', handleSubmit);
});

function validateEmail() {
    const correoInput = document.getElementById('correo');
    const email = correoInput.value.trim();
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    
    if (email && emailRegex.test(email)) {
        correoInput.style.borderColor = '#27ae60';
        correoInput.classList.remove('invalid');
        correoInput.classList.add('valid');
    } else if (email) {
        correoInput.style.borderColor = '#ff4757';
        correoInput.classList.remove('valid');
        correoInput.classList.add('invalid');
    } else {
        resetInputStyle(correoInput);
    }
}

function validatePassword() {
    const contraseñaInput = document.getElementById('contraseña');
    const password = contraseñaInput.value;
    
    if (password.length >= 6) {
        contraseñaInput.style.borderColor = '#27ae60';
        contraseñaInput.classList.remove('invalid');
        contraseñaInput.classList.add('valid');
    } else if (password.length > 0) {
        contraseñaInput.style.borderColor = '#ff4757';
        contraseñaInput.classList.remove('valid');
        contraseñaInput.classList.add('invalid');
    } else {
        resetInputStyle(contraseñaInput);
    }
}

function resetInputStyle(input) {
    input.style.borderColor = '';
    input.classList.remove('valid', 'invalid');
}

function handleSubmit(e) {
    const correoInput = document.getElementById('correo');
    const contraseñaInput = document.getElementById('contraseña');
    const submitBtn = document.getElementById('submitBtn');
    const btnText = submitBtn.querySelector('.btn-text');
    const loading = submitBtn.querySelector('.loading');
    
    // Validar campos antes de enviar
    const email = correoInput.value.trim();
    const password = contraseñaInput.value;
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    
    if (!email) {
        showMessage('Por favor ingresa tu correo electrónico', 'error');
        correoInput.focus();
        e.preventDefault();
        return;
    }
    
    if (!emailRegex.test(email)) {
        showMessage('Por favor ingresa un correo electrónico válido', 'error');
        correoInput.focus();
        e.preventDefault();
        return;
    }
    
    if (!password) {
        showMessage('Por favor ingresa tu contraseña', 'error');
        contraseñaInput.focus();
        e.preventDefault();
        return;
    }
    
    if (password.length < 6) {
        showMessage('La contraseña debe tener al menos 6 caracteres', 'error');
        contraseñaInput.focus();
        e.preventDefault();
        return;
    }
    
    // Mostrar estado de carga
    submitBtn.disabled = true;
    btnText.style.display = 'none';
    loading.style.display = 'inline';
    
    // El formulario se enviará normalmente si no se previene el evento
}

function showMessage(text, type) {
    const messageDiv = document.getElementById('message');
    messageDiv.textContent = text;
    messageDiv.className = `message ${type}`;
    messageDiv.style.display = 'block';
    
    // Auto-ocultar después de 5 segundos
    setTimeout(() => {
        messageDiv.style.display = 'none';
    }, 5000);
}

// Función para manejar respuestas del servidor
function handleServerResponse() {
    const urlParams = new URLSearchParams(window.location.search);
    const error = urlParams.get('error');
    const success = urlParams.get('success');
    
    if (error) {
        showMessage(decodeURIComponent(error), 'error');
    }
    
    if (success) {
        showMessage(decodeURIComponent(success), 'success');
    }
}

// Ejecutar al cargar la página
document.addEventListener('DOMContentLoaded', handleServerResponse);