function calcularEdad(fechaNacimiento) {
    var ahora = new Date();
    var edad = ahora.getFullYear() - fechaNacimiento.getFullYear();
    var mesActual = ahora.getMonth() + 1;
    var mesNacimiento = fechaNacimiento.getMonth() + 1;
    if (mesActual < mesNacimiento || (mesActual === mesNacimiento && ahora.getDate() < fechaNacimiento.getDate())) {
        edad--;
    }
    return edad;
}

function validarEdad(input) {
    var fechaNacimiento = new Date(input.value);
    var edad = calcularEdad(fechaNacimiento);
    var edadAlert = document.getElementById("edadAlert");
    if (edad < 14) {
        edadAlert.style.display = "block";
    } else {
        edadAlert.style.display = "none";
    }
}