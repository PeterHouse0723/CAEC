// Funcionalidad para la página de login

document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('loginForm');

    loginForm.addEventListener('submit', function(e) {
        e.preventDefault();

        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;
        const remember = document.querySelector('input[name="remember"]').checked;

        // Validación básica
        if (!email || !password) {
            alert('Por favor, completa todos los campos');
            return;
        }

        // Validar formato de email
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(email)) {
            alert('Por favor, ingresa un correo electrónico válido');
            return;
        }

        // Simulación de login exitoso
        console.log('Intentando iniciar sesión con:', { email, remember });

        // Guardar sesión si se marca "Recordarme"
        if (remember) {
            localStorage.setItem('rememberedUser', email);
        }

        // Redirigir al dashboard
        alert('Inicio de sesión exitoso');
        window.location.href = '/inicio';
    });

    // Verificar si hay un usuario recordado
    const rememberedUser = localStorage.getItem('rememberedUser');
    if (rememberedUser) {
        document.getElementById('email').value = rememberedUser;
        document.querySelector('input[name="remember"]').checked = true;
    }
});
