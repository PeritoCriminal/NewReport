const operationState = {
    isCropping: false,
    isZooming: false,
    isDrawing: false,
    // Outras operações
};

function getCord(elementCanvas, event) {
    const rect = elementCanvas.getBoundingClientRect(); // Pega as dimensões e posição do canvas
    const xx = event.clientX - rect.left; // Calcula a coordenada X relativa ao canvas
    const yy = event.clientY - rect.top;  // Calcula a coordenada Y relativa ao canvas
    return { x: xx, y: yy }; // Retorna as coordenadas como um objeto
}