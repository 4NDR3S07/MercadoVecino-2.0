// registrar.js - JavaScript para el formulario de registro
document.addEventListener('DOMContentLoaded', function() {
    const registerForm = document.getElementById('registerForm');
    const submitBtn = document.getElementById('submitBtn');
    
    // Añadir validación en tiempo real a todos los campos
    setupValidation();
    
    // Manejar envío del formulario
    registerForm.addEventListener('submit', handleSubmit);
});

function setupValidation() {
    const fields = [
        { id: 'nombre', validator: validateName },
        { id: 'apellido', validator: validateLastName },
        { id: 'correo', validator: validateEmail },
        { id: 'telefono', validator: validatePhone },
        { id: 'contraseña', validator: validatePassword },
        { id: 'confirm_password', validator: validateConfirmPassword }
    ];
    
    fields.forEach(field => {
        const input = document.getElementById(field.id);
        if (input) {
            input.addEventListener('blur', field.validator);
            input.addEventListener('input', field.validator);
        }
    });
}

function validateName() {
    const input = document.getElementById('nombre');
    const value = input.value.trim();
    
    if (value.length >= 2 && /^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$/.test(value)) {
        setValidStyle(input);
        return true;
    } else if (value.length > 0) {
        setInvalidStyle(input);
        return false;
    } else {
        resetStyle(input);
        return false;
    }
}

function validateLastName() {
    const input = document.getElementById('apellido');
    const value = input.value.trim();
    
    if (value.length >= 2 && /^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$/.test(value)) {
        setValidStyle(input);
        return true;
    } else if (value.length > 0) {
        setInvalidStyle(input);
        return false;
    } else {
        resetStyle(input);
        return false;
    }
}

function validateEmail() {
    const input = document.getElementById('correo');
    const value = input.value.trim();
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    
    if (value && emailRegex.test(value)) {
        setValidStyle(input);
        return true;
    } else if (value) {
        setInvalidStyle(input);
        return false;
    } else {
        resetStyle(input);
        return false;
    }
}

function validatePhone() {
    const input = document.getElementById('telefono');
    const value = input.value.trim();
    const phoneRegex = /^[0-9\+\-\s\(\)]+$/;
    
    if (value.length >= 7 && phoneRegex.test(value)) {
        setValidStyle(input);
        return true;
    } else if (value.length > 0) {
        setInvalidStyle(input);
        return false;
    } else {
        resetStyle(input);
        return false;
    }
}

function validatePassword() {
    const input = document.getElementById('contraseña');
    const value = input.value;
    
    if (value.length >= 6) {
        setValidStyle(input);
        // También validar confirm password si ya tiene contenido
        validateConfirmPassword();
        return true;
    } else if (value.length > 0) {
        setInvalidStyle(input);
        return false;
    } else {
        resetStyle(input);
        return false;
    }
}

function validateConfirmPassword() {
    const passwordInput = document.getElementById('contraseña');
    const confirmInput = document.getElementById('confirm_password');
    const password = passwordInput.value;
    const confirmPassword = confirmInput.value;
    
    if (confirmPassword && password === confirmPassword) {
        setValidStyle(confirmInput);
        return true;
    } else if (confirmPassword) {
        setInvalidStyle(confirmInput);
        return false;
    } else {
        resetStyle(confirmInput);
        return false;
    }
}

function setValidStyle(input) {
    input.classList.remove('invalid');
    input.classList.add('valid');
}

function setInvalidStyle(input) {
    input.classList.remove('valid');
    input.classList.add('invalid');
}

function resetStyle(input) {
    input.classList.remove('valid', 'invalid');
}

function handleSubmit(e) {
    const submitBtn = document.getElementById('submitBtn');
    const btnText = submitBtn.querySelector('.btn-text');
    const loading = submitBtn.querySelector('.loading');
    
    // Validar todos los campos
    const isValid = validateAllFields();
    
    if (!isValid) {
        e.preventDefault();
        showMessage('Por favor corrige los errores en el formulario', 'error');
        shakeForm();
        return;
    }
    
    // Mostrar estado de carga
    submitBtn.disabled = true;
    btnText.style.display = 'none';
    loading.style.display = 'inline';
}

function validateAllFields() {
    const validations = [
        validateName(),
        validateLastName(),
        validateEmail(),
        validatePhone(),
        validatePassword(),
        validateConfirmPassword()
    ];
    
    return validations.every(validation => validation === true);
}

function showMessage(text, type) {
    const messageDiv = document.getElementById('message');
    messageDiv.textContent = text;
    messageDiv.className = `message ${type}`;
    messageDiv.style.display = 'block';
    
    setTimeout(() => {
        messageDiv.style.display = 'none';
    }, 5000);
}

function shakeForm() {
    const form = document.querySelector('.register-box');
    form.classList.add('shake');
    
    setTimeout(() => {
        form.classList.remove('shake');
    }, 500);
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