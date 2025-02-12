const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');
const rectangles = []; // Array para almacenar las coordenadas de los rectángulos
let canvasWidth = canvas.width; // Ancho del canvas
let canvasHeight = canvas.height;
let startX, startY, isDrawing = false;
let currentType = ''; // Tipo de rectángulo a dibujar
let currentRect = null; // Variable para almacenar el rectángulo actual

// Evento para cambiar las dimensiones del canvas
document.getElementById('aplicarDimensiones').addEventListener('click', () => {
    const dimensiones = document.getElementById('dimensiones').value.split('x');
    canvasWidth = parseInt(dimensiones[0]);
    canvasHeight = parseInt(dimensiones[1]);
    canvas.width = canvasWidth;
    canvas.height = canvasHeight;
    drawAllRectangles(); // Redibujar los rectángulos con las nuevas dimensiones
});

// Evento para seleccionar el tipo de rectángulo
document.getElementById('btn1').addEventListener('click', () => { currentType = 'Imagen 1'; });
document.getElementById('btn2').addEventListener('click', () => { currentType = 'Imagen 2'; });
document.getElementById('btn3').addEventListener('click', () => { currentType = 'Titulo'; });
document.getElementById('btn4').addEventListener('click', () => { currentType = 'Legal'; });
document.getElementById('btn5').addEventListener('click', () => { currentType = 'Logo'; });

// Evento para iniciar el dibujo
canvas.addEventListener('mousedown', (event) => {
    if (currentType) { // Solo dibujar si se ha seleccionado un tipo
        startX = event.offsetX; // Coordenada X inicial
        startY = event.offsetY; // Coordenada Y inicial
        isDrawing = true; // Cambia el estado a "dibujando"
    }
});

// Evento para dibujar en el canvas
canvas.addEventListener('mousemove', (event) => {
    if (isDrawing) {
        ctx.clearRect(0, 0, canvas.width, canvas.height); // Limpiar el canvas
        // Redibujar todos los rectángulos existentes
        drawAllRectangles(); // Llamar a la función para redibujar todos los rectángulos
        const width = event.offsetX - startX; // Calcular el ancho del rectángulo
        const height = event.offsetY - startY; // Calcular la altura del rectángulo
        ctx.strokeRect(startX, startY, width, height); // Dibujar el rectángulo actual
    }
});

// Evento para finalizar el dibujo
canvas.addEventListener('mouseup', (event) => {
    if (isDrawing) {
        const width = event.offsetX - startX; // Calcular el ancho final
        const height = event.offsetY - startY; // Calcular la altura final
        // Almacenar las coordenadas normalizadas en el objeto currentRect
        currentRect = { 
            x: startX / canvasWidth, 
            y: startY / canvasHeight, 
            width: width / canvasWidth, 
            height: height / canvasHeight,
            type: currentType // Guardar el tipo de rectángulo
        };
        isDrawing = false; // Cambiar el estado a "no dibujando"
    }
});

// Evento para guardar las coordenadas
document.getElementById('saveButton').addEventListener('click', () => {
    if (currentRect) {
        rectangles.push(currentRect); // Agregar el nuevo rectángulo al array
        drawAllRectangles(); // Redibujar todos los rectángulos con sus textos
        displayCoordinates(currentRect); // Mostrar las coordenadas en el div
        currentRect = null; // Reiniciar currentRect
    } else {
        alert('No hay coordenadas para guardar. Dibuja un rectángulo primero.');
    }
});

// Función para dibujar todos los rectángulos y sus textos
function drawAllRectangles() {
    ctx.clearRect(0, 0, canvas.width, canvas.height); // Limpiar el lienzo
    rectangles.forEach(rect => {
        ctx.strokeRect(rect.x * canvasWidth, rect.y * canvasHeight, rect.width * canvasWidth, rect.height * canvasHeight); // Dibujar el rectángulo
        ctx.fillStyle = 'black'; // Color del texto
        ctx.textAlign = 'center'; // Alinear el texto al centro
        ctx.textBaseline = 'middle'; // Alinear el texto verticalmente al medio
        ctx.font = '16px Arial'; // Establecer el tamaño y tipo de fuente
        ctx.fillText(rect.type, 
 rect.x * canvasWidth + (rect.width * canvasWidth) / 2, 
        rect.y * canvasHeight + (rect.height * canvasHeight) / 2); // Dibujar el texto en el centro del rectángulo
    });
}

// Función para mostrar las coordenadas en el div
function displayCoordinates(rect) {
    const coordinatesDiv = document.getElementById('coordinates');
    const coordText = `Tipo: ${rect.type}, X: ${rect.x.toFixed(3)}, Y: ${rect.y.toFixed(3)}, Width: ${rect.width.toFixed(3)}, Height: ${rect.height.toFixed(3)}`; // Usar comillas invertidas
    const coordElement = document.createElement('div');
    coordElement.textContent = coordText; // Establecer el texto del nuevo div
    coordinatesDiv.appendChild(coordElement); // Agregar el nuevo div al contenedor de coordenadas
}

// Evento para descargar las coordenadas
document.getElementById('descargar').addEventListener('click', () => {
    if (rectangles.length === 0) {
        alert('No hay coordenadas guardadas para descargar.');
        return;
    }

        // Obtener la resolución seleccionada
    const dimensiones = document.getElementById('dimensiones').value;

    // Crear un objeto que incluya las coordenadas y la resolución
    const data = {
        resolucion: dimensiones, // Agregar la resolución seleccionada
        rectangulos: rectangles // Incluir las coordenadas de los rectángulos
    };

    const dataStr = JSON.stringify(data, null, 2); // Convertir las coordenadas a formato JSON
    const blob = new Blob([dataStr], { type: 'application/json' }); // Crear un blob con el contenido
    const url = URL.createObjectURL(blob); // Crear una URL para el blob
    const a = document.createElement('a'); // Crear un elemento <a> para la descarga
    a.href = url; // Establecer la URL del blob como href
    a.download = 'coordenadas.json'; // Nombre del archivo a descargar
    document.body.appendChild(a); // Agregar el elemento al DOM
    a.click(); // Simular un clic para iniciar la descarga
    document.body.removeChild(a); // Eliminar el elemento del DOM
    URL.revokeObjectURL(url); // Liberar la URL del blob
});

document.querySelectorAll('.button').forEach(button => {
    let div = document.createElement('div'),
        letters = button.textContent.trim().split('');

    function elements(letter, index, array) {
        let element = document.createElement('span'),
            part = (index >= array.length / 2) ? -1 : 1,
            position = (index >= array.length / 2) ? array.length / 2 - index + (array.length / 2 - 1) : index,
            move = position / (array.length / 2),
            rotate = 1 - move;

        element.innerHTML = !letter.trim() ? '&nbsp;' : letter;
        element.style.setProperty('--move', move);
        element.style.setProperty('--rotate', rotate);

        div.appendChild(element);
    }

    letters.forEach(elements);
    button.innerHTML = div.outerHTML;

    button.addEventListener('mouseenter', e => {
        if (!button.classList.contains('out')) {
            button.classList.add('in');
        }
    });

    button.addEventListener('mouseleave', e => {
        if (button.classList.contains('in')) {
            button.classList.add('out');
            setTimeout(() => button.classList.remove('in', 'out'), 950);
        }
    });

    // Evento para seleccionar el botón
    button.addEventListener('click', () => {
        // Restablecer el color de todos los botones
        document.querySelectorAll('.button').forEach(btn => {
            btn.style.backgroundColor = 'lightgray'; // Color original
        });
        // Cambiar el color del botón seleccionado
        button.style.backgroundColor = '#007bff'; // 
    });
});
