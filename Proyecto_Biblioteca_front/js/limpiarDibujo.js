
        function limpiarDibujo() {
            var canvas = document.getElementById('areaDibujo');
            var ctx = canvas.getContext('2d');
            
            // Limpiar el área de dibujo
            ctx.clearRect(0, 0, canvas.width, canvas.height);
        }
