// Funcionalidad para la página de login

document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('loginForm');

    // Verificar si hay un usuario recordado
    const rememberedUser = localStorage.getItem('rememberedUser');
    if (rememberedUser) {
        document.getElementById('email').value = rememberedUser;
        document.querySelector('input[name="remember"]').checked = true;
    }

    // Guardar email si marca "Recordarme" antes de enviar
    loginForm.addEventListener('submit', function(e) {
        e.preventDefault(); // Prevenir envío normal

        const remember = document.querySelector('input[name="remember"]').checked;
        const email = document.getElementById('email').value;

        // Guardar sesión si se marca "Recordarme"
        if (remember) {
            localStorage.setItem('rememberedUser', email);
        } else {
            localStorage.removeItem('rememberedUser');
        }

        // Enviar formulario con AJAX para capturar la respuesta
        const formData = new FormData(loginForm);

        fetch(loginForm.action, {
            method: 'POST',
            body: formData
        })
        .then(response => {
            // Si hay redirección, mostrar animación
            if (response.redirected) {
                const redirectUrl = response.url;

                // Si redirige a /inicio (tiene sistema), mostrar animación
                if (redirectUrl.includes('/inicio')) {
                    showSyncAnimation().then(() => {
                        window.location.href = redirectUrl;
                    });
                } else {
                    // Si redirige a otra parte (add-system o error), ir directo
                    window.location.href = redirectUrl;
                }
            } else {
                // Si no hay redirección, recargar para mostrar error
                window.location.reload();
            }
        })
        .catch(error => {
            console.error('Error:', error);
            window.location.reload();
        });
    });
});

async function showSyncAnimation() {
    const overlay = document.getElementById('syncOverlay');
    overlay.classList.add('show');

    const steps = [
        { id: 'loginStep1', duration: 600 },
        { id: 'loginStep2', duration: 800 },
        { id: 'loginStep3', duration: 700 },
        { id: 'loginStep4', duration: 600 }
    ];

    for (let step of steps) {
        const stepElement = document.getElementById(step.id);
        stepElement.classList.add('active');

        await new Promise(resolve => setTimeout(resolve, step.duration));

        stepElement.classList.add('completed');
        stepElement.querySelector('.step-check').textContent = '✓';
    }

    await new Promise(resolve => setTimeout(resolve, 300));
}
