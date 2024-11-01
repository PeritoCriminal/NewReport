//newreportapp/static/js/scripts.js

function startVoiceRecognition(inputId) {
    const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    recognition.lang = 'pt-BR'; // Defina o idioma conforme necessário
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;

    recognition.start();

    recognition.onresult = function(event) {
        const transcript = event.results[0][0].transcript; // Captura o resultado
        document.getElementById(inputId).value = transcript; // Atribui o texto ao campo
    };

    recognition.onerror = function(event) {
        console.error('Error occurred in recognition: ' + event.error);
    };
}