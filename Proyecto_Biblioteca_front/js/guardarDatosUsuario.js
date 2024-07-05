function guardarDatosUsuario() {
    // Recolecta los datos del formulario
    var nombre = document.getElementById('nombre').value;
    var apellido = document.getElementById('apellido').value;
    var username = document.getElementById('username').value;
    var fechaNacimiento = document.getElementById('fecha_nacimiento').value;
    var genero = document.querySelector('input[name="genero"]:checked').value;
    var pais = document.getElementById('pais').value;
    var otroPais = document.getElementById('otro_pais').value;
    var email = document.getElementById('email').value;
    var password = document.getElementById('password').value;
    var preguntaSeguridad = document.getElementById('pregunta').value;
    var respuestaSeguridad = document.getElementById('respuesta').value;

    // Crea un objeto con los datos del usuario
    var datosUsuario = {
        nombre: nombre,
        apellido: apellido,
        username: username,
        fechaNacimiento: fechaNacimiento,
        genero: genero,
        pais: pais === 'OTRO' ? otroPais : pais, // Si el usuario selecciona 'Otro', usa el valor de otroPais
        email: email,
        password: password, // Se guarda la contraseña del usuario
        preguntaSeguridad: preguntaSeguridad,
        respuestaSeguridad: respuestaSeguridad
    };

    // Guarda los datos del usuario en localStorage
    localStorage.setItem('datosUsuario', JSON.stringify(datosUsuario));

    // Redirecciona al usuario a otra página después de guardar los datos
    window.location.href = "./login.html";
}


async function guardarDatosUsuarioo() {
    const form = document.getElementById('registroForm');
    const formData = new FormData(form);

    const datos = {
        nombre: formData.get('nombre'),
        apellido: formData.get('apellido'),
        username: formData.get('username'),
        email: formData.get('email'),
        fecha_nacimiento: formData.get('fecha_nacimiento'),
        genero: formData.get('genero'),
        pais: formData.get('pais') === 'OTRO' ? formData.get('otro_pais') : formData.get('pais'),
        password: formData.get('password'),
        rol_id: 2  // Cambiar según el ID del rol deseado
    };

    try {
        const response = await fetch('https://roan82.pythonanywhere.com/usuarios', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(datos)
        });

        console.log('Estado de la respuesta:', response.status);
        console.log('Texto de la respuesta:', await response.text());

        if (!response.ok) {
            throw new Error('Error al registrar usuario');
        }

        const jsonResponse = await response.json();
        console.log(jsonResponse);  // Manejar la respuesta según sea necesario
        alert('Usuario registrado exitosamente');
        window.location.href = './login.html';  // Redirigir a la página de inicio de sesión
    } catch (error) {
        console.error('Error:', error);
        alert('Error al registrar usuario');
    }
}
