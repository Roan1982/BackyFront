function guardarPreguntaYRespuesta() {
    var preguntaSeleccionada = document.getElementById("pregunta").value;
    var respuesta = document.getElementById("respuesta").value;

    // Guardar la pregunta y la respuesta en el sessionStorage
    sessionStorage.setItem("preguntaSeguridad", preguntaSeleccionada);
    sessionStorage.setItem("respuestaSeguridad", respuesta);
}

function enviarFormulario() {
    var formularioValido = validarFormulario();
    if (formularioValido) {
        document.getElementById("registroForm").action = "../templates/login.html";
        document.getElementById("registroForm").submit();
    }
}

function ocultarAlertaPregunta() {
    document.getElementById("edadAlert").style.display = "none";
}

// Guardar respuesta en sessionStorage cuando el usuario se registra
function guardarPreguntaYRespuesta() {
    var pregunta = document.getElementById("pregunta").value;
    var respuesta = document.getElementById("respuesta").value;
    
    // Guardar pregunta y respuesta en sessionStorage
    sessionStorage.setItem("preguntaSeguridad", pregunta);
    sessionStorage.setItem("respuestaSeguridad", respuesta);
}