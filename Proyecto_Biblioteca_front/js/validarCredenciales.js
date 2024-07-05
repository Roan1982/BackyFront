function validarCredenciales() {
    var username = document.getElementById('username').value;
    var password = document.getElementById('password').value;

    // Recupera los datos del usuario almacenados en localStorage
    var datosUsuario = localStorage.getItem('datosUsuario');
    if (datosUsuario) {
        datosUsuario = JSON.parse(datosUsuario);
        
        // Comprueba si las credenciales ingresadas coinciden con los datos almacenados
        if ((username === datosUsuario.email || username === datosUsuario.username) &&
            password === datosUsuario.password) {
            // Si las credenciales son válidas, redirige al usuario a la página de bienvenida
            window.location.href = "./bienvenido.html";

            // Actualiza la visibilidad de los enlaces en el menú de navegación
            localStorage.setItem('isAuthenticated', 'true');
            actualizarVisibilidadEnlaces();

            return; // Importante: salir de la función aquí para evitar la redirección no deseada
        }
    }

    // Si las credenciales son incorrectas o no hay datos de usuario almacenados, muestra un mensaje de error
    alert("Credenciales incorrectas. Por favor, inténtalo de nuevo.");
}

function logout() {
    // Elimina la autenticación almacenada en localStorage
    localStorage.removeItem('isAuthenticated');

    // Redirige al usuario a la página de inicio de sesión u otra página deseada
    window.location.href = "./login.html"; // Cambia "./login.html" por la URL de tu página de inicio de sesión
}

document.addEventListener("DOMContentLoaded", function() {
    // Verifica si el usuario está autenticado consultando localStorage
    var isAuthenticated = localStorage.getItem('isAuthenticated') === 'true';

    // Actualiza la visibilidad de los enlaces en el menú de navegación según el estado de autenticación
    if (isAuthenticated) {
        document.getElementById("bienvenidoLink").style.display = "inline";
        document.getElementById("loginLink").style.display = "none";
        document.getElementById("signupLink").style.display = "none";
        document.getElementById("logoutLink").style.display = "inline"; // Mostrar enlace de logout
    } else {
        document.getElementById("bienvenidoLink").style.display = "none";
        document.getElementById("loginLink").style.display = "inline";
        document.getElementById("signupLink").style.display = "inline";
        document.getElementById("logoutLink").style.display = "none"; // Ocultar enlace de logout
    }
});

async function validarCredencialess() {
    event.preventDefault();

    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    try {
        // Realizar la solicitud POST al endpoint de login
        const response = await fetch('https://roan82.pythonanywhere.com/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                username: username,
                password: password
            })
        });

        if (!response.ok) {
            throw new Error('Credenciales inválidas. Por favor, inténtalo de nuevo.');
        }

        const userData = await response.json();

        // Guardar datos del usuario en el localStorage o manejar la sesión
        localStorage.setItem('userId', userData.id); // Ejemplo: si la API devuelve un ID de usuario

        // Redirigir a la página de bienvenida u otra página según la respuesta
        window.location.href = './bienvenido.html';
    } catch (error) {
        console.error('Error al autenticar:', error.message);
        // Mostrar un mensaje de error o realizar alguna acción adecuada
    }
}
