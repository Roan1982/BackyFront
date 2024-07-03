function validarRespuesta() {
    // Obtener la respuesta ingresada por el usuario
    var respuestaIngresada = document.getElementById("respuesta").value;

    // Obtener la respuesta almacenada en sessionStorage
    var respuestaRegistrada = sessionStorage.getItem("respuestaSeguridad");

    // Log para verificar valores
    console.log("Respuesta ingresada:", respuestaIngresada);
    console.log("Respuesta registrada:", respuestaRegistrada);

    // Verificar si la respuesta ingresada coincide con la respuesta almacenada
    if (respuestaIngresada === respuestaRegistrada) {
        console.log("Respuesta correcta, redirigiendo a home.html");
        // Redirigir al usuario a la página de inicio (home.html)
        window.location.href = "home.html";
    } else {
        console.log("Respuesta incorrecta, redirigiendo a ingreso_email.html");
        // Redirigir al usuario a la página de ingreso de email (ingreso_email.html)
        window.location.href = "ingreso_email.html";
    }
}

// Función para manejar el envío del email
function submitEmail() {
    // Obtener el correo electrónico ingresado por el usuario
    var email = document.getElementById("e-mail").value;

    if (email.trim() === "") {
        alert("Por favor, ingresa tu correo electrónico.");
        return;
    }

    var emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    if (!emailPattern.test(email)) {
        alert("Por favor, ingresa un correo electrónico válido.");
        return;
    }

    // Aquí realizarías el envío del correo electrónico

    // Mostrar el mensaje de éxito
    document.getElementById("envio-de-link").style.display = "block";

    // Ocultar el campo de email y el botón
    document.getElementById("e-mail").style.display = "none";
    document.getElementById("submit-email").style.display = "none";
    document.getElementById("email-label").style.display = "none";
}

// Evento para manejar la validación de la respuesta de seguridad al enviar el formulario
document.getElementById("securityForm").addEventListener("submit", function(event) {
    event.preventDefault(); // Prevenir el envío del formulario
    validarRespuesta();
});

function submitEmail() {
    var respuesta = document.getElementById('respuesta').value;
    var pregunta = document.getElementById('pregunta').value;
    
    // Aquí debes verificar la respuesta a la pregunta de seguridad
    // Este es un ejemplo básico, debes ajustarlo a tu lógica específica
    if (pregunta === "1" && respuesta.toLowerCase() === "nombre de tu mascota") {
        // Mostrar el grupo de email y ocultar la pregunta de seguridad
        document.getElementById('preguntaSeguridadGroup').style.display = 'none';
        document.getElementById('emailGroup').style.display = 'block';
        
        // Opcional: Mostrar el mensaje de envío de link
        document.getElementById('envio-de-link').style.display = 'block';
    } else {
        // Mostrar una alerta o mensaje de error
        alert("La respuesta a la pregunta de seguridad es incorrecta.");
    }
}