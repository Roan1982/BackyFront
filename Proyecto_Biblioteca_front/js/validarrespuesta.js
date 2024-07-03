function validarRespuesta() {
    // Obtener la respuesta ingresada por el usuario y normalizarla a minúsculas
    var respuestaIngresada = document.getElementById("respuesta").value.toLowerCase();

    // Obtener la respuesta almacenada en sessionStorage y normalizarla a minúsculas
    var respuestaRegistrada = sessionStorage.getItem("respuestaSeguridad").toLowerCase();

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

