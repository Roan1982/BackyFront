
   /* function toggleFloatingContainer() {
        document.getElementById("floating-container").classList.toggle
("open");
    }
    function enviarhistoria() {
        const historiaContainer = document.getElementById
("opinion-container");
        const enviarButton = document.getElementById("enviar-historia");
        const thankYouMessage = document.getElementById
("thank-you-message");
        historiaContainer.style.display = "none";
        enviarButton.style.display = "none";
        thankYouMessage.style.display = "block";
    }
    document.querySelectorAll(".star").forEach(star => {
        star.addEventListener("click", () => {
            const value = parseInt(star.getAttribute("data-value"));
            document.querySelectorAll(".star").forEach(s => {
                const sValue = parseInt(s.getAttribute("data-value"));
                if (sValue <= value) {
                    s.classList.add("active");
                } else {
                    s.classList.remove("active");
                }
            });
        });
    });

    // Función para mostrar u ocultar el contenedor flotante
// Función para mostrar u ocultar el contenedor flotante

function toggleFloatingContainer() {
    document.getElementById("floating-container").classList.toggle("open");
}

// Función para enviar el cuento y mostrar el mensaje de agradecimiento
// Función para manejar el contenedor flotante
function toggleFloatingContainer() {
    const floatingContainer = document.getElementById("floating-container");
    if (floatingContainer) {
        floatingContainer.classList.toggle("open");
    }
}

// Función para enviar el cuento y mostrar el mensaje de agradecimiento
function enviarhistoria() {
    console.log("Enviando historia...");

    // Ocultar el formulario completo si existe
    const cuentoForm = document.getElementById('cuentoForm');
    if (cuentoForm) {
        cuentoForm.style.display = 'none';
    }

    // Ocultar el título de la sección "Mi Cuento" si existe
    const miCuentoTitle = document.getElementById('miCuentoTitle');
    if (miCuentoTitle) {
        miCuentoTitle.style.display = 'none';
    }

    // Mostrar el mensaje de agradecimiento si existe
    const thankYouContainer = document.getElementById('thank-you-container');
    if (thankYouContainer) {
        thankYouContainer.style.display = 'unblock';
        console.log('Mensaje de agradecimiento mostrado');
    }
}

// Función principal que se ejecuta cuando el DOM está completamente cargado
document.addEventListener('DOMContentLoaded', function() {
    console.log('El DOM ha sido completamente cargado');

    // Agregar evento click al botón para enviar el cuento
    const enviarButton = document.querySelector('button[type="button"][onclick="enviarhistoria()"]');
    if (enviarButton) {
        enviarButton.addEventListener('click', enviarhistoria);
        console.log('Evento de clic agregado al botón de enviar');
    } else {
        console.log('No se encontró el botón de enviar');
    }
});*/

function toggleFloatingContainer() {
    const floatingContainer = document.getElementById("floating-container");
    if (floatingContainer) {
        floatingContainer.classList.toggle("open");
    }
}

// Función para enviar el cuento y mostrar el mensaje de agradecimiento
function enviarhistoria() {
    console.log("Enviando historia...");

    // Ocultar el formulario completo si existe
    const cuentoForm = document.getElementById('cuentoForm');
    if (cuentoForm) {
        cuentoForm.style.display = 'none';
    }

    // Ocultar el título de la sección "Mi Cuento" si existe
    const miCuentoTitle = document.getElementById('miCuentoTitle');
    if (miCuentoTitle) {
        miCuentoTitle.style.display = 'none';
    }

    // Cambiar el mensaje inicial por el mensaje de agradecimiento
    const mensajeInicial = document.getElementById('mensajeInicial');
    if (mensajeInicial) {
        mensajeInicial.innerHTML = '¡Gracias por contarnos tu cuento! Pronto estará disponible para compartirlo e una nueva sección llamada "Leamos nuestros cuentos"';
    }

    // Agregar log para depurar
    console.log('Mensaje de agradecimiento mostrado');
}

// Función principal que se ejecuta cuando el DOM está completamente cargado
document.addEventListener('DOMContentLoaded', function() {
    console.log('El DOM ha sido completamente cargado');

    // Agregar evento click al botón para enviar el cuento
    const enviarButton = document.querySelector('button[type="button"][onclick="enviarhistoria()"]');
    if (enviarButton) {
        enviarButton.addEventListener('click', enviarhistoria);
        console.log('Evento de clic agregado al botón de enviar');
    } else {
        console.log('No se encontró el botón de enviar');
    }
});