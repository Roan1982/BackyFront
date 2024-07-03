function submitCuento() {
    const titulo = document.getElementById('titulo').value;
    const autor = document.getElementById('autor').value;
    const edad = document.getElementById('edad').value;
    const cuento = document.getElementById('cuento').value;
    const canvasData = canvas.toDataURL();

    // Combine data into an object
    const formData = {
        titulo,
        autor,
        edad,
        cuento,
        dibujo: canvasData
    };

    // Send the form data (e.g., via AJAX)
    console.log('Form Data:', formData);

    document.getElementById('thank-you-message').style.display = 'block';
}

let color = 'black'; // Color predeterminado

function setColor(selectedColor) {
    color = selectedColor;
}

const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');
let drawing = false;

// Ajustar tamaño del canvas al tamaño de la ventana
function resizeCanvas() {
    canvas.width = window.innerWidth * 0.9;
    canvas.height = window.innerHeight * 0.6;
}

window.addEventListener('resize', resizeCanvas);
resizeCanvas(); // Inicializar tamaño del canvas

function startDrawing(e) {
    drawing = true;
    draw(e);
}

function endDrawing() {
    drawing = false;
    ctx.beginPath();
}

function draw(e) {
    if (!drawing) return;
    ctx.lineWidth = 2;
    ctx.lineCap = 'round';
    ctx.strokeStyle = color;

    const rect = canvas.getBoundingClientRect();
    ctx.lineTo(e.clientX - rect.left, e.clientY - rect.top);
    ctx.stroke();
    ctx.beginPath();
    ctx.moveTo(e.clientX - rect.left, e.clientY - rect.top);
}

function clearCanvas() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
}

canvas.addEventListener('mousedown', startDrawing);
canvas.addEventListener('mouseup', endDrawing);
canvas.addEventListener('mousemove', draw);
canvas.addEventListener('mouseleave', endDrawing);