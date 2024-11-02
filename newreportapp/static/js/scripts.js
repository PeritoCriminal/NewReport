//newreportapp/static/js/scripts.js


/*
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

    */
    function hideMsg(selector, duration) {
        document.addEventListener('DOMContentLoaded', function() {
            setTimeout(function() {
                var alerts = document.querySelectorAll(selector);
                alerts.forEach(function(alert) {
                    // Define a opacidade inicial
                    let opacity = 1;
                    // Define a duração do fade out
                    const fadeOutDuration = 800;
                    const interval = fadeOutDuration / 100; // Número de incrementos (100)
    
                    const fadeOut = setInterval(function() {
                        if (opacity <= 0) {
                            clearInterval(fadeOut);
                            alert.style.display = 'none'; // Esconde o elemento após a animação
                        } else {
                            opacity -= 0.01; // Decrementa a opacidade
                            alert.style.opacity = opacity; // Aplica a opacidade ao elemento
                        }
                    }, interval);
                });
            }, duration);
        });
    }

