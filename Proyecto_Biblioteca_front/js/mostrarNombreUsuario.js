// Recupera el nombre de usuario del localStorage
document.addEventListener("DOMContentLoaded", function () {
    var datosUsuario = localStorage.getItem('datosUsuario');
    if (datosUsuario) {
        datosUsuario = JSON.parse(datosUsuario);
        var username = datosUsuario.username;

    var usernameHeader = document.getElementById('usernameHeader');
        if (usernameHeader) {
            usernameHeader.textContent = username;
        }

    // Inserta el nombre de usuario en el HTML
    var usernameBody = document.getElementById('usernameBody');
        if (usernameBody) {
            usernameBody.textContent = username;
        }
    }
});