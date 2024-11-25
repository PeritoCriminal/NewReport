// image_processor.js

// Função para abrir o explorador de arquivos ao clicar no botão
document.querySelector('#openImageModal').addEventListener('click', function () {
    document.querySelector('#imageInput').click();
});

// Carregar a imagem no canvas e abrir o modal
document.querySelector('#imageInput').addEventListener('change', function (event) {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function (e) {
            const canvas = document.querySelector('#imageCanvas');
            const ctx = canvas.getContext('2d');
            const img = new Image();

            img.onload = function () {
                // Define o tamanho máximo
                const maxWidth = 800; // Largura máxima
                const maxHeight = 600; // Altura máxima
                const ratio = Math.min(maxWidth / img.width, maxHeight / img.height);

                // Redimensiona a imagem
                const newWidth = img.width * ratio;
                const newHeight = img.height * ratio;

                canvas.width = newWidth;
                canvas.height = newHeight;
                ctx.drawImage(img, 0, 0, newWidth, newHeight);

                // Gera o novo arquivo redimensionado
                canvas.toBlob(function (blob) {
                    // Converte o canvas para um arquivo Blob
                    const reducedFile = new File([blob], file.name, {
                        type: file.type,
                        lastModified: Date.now(),
                    });

                    // Agora você pode usar `reducedFile` para fazer o upload
                    console.log('Novo arquivo reduzido:', reducedFile);

                    // Abrir o modal após carregar a imagem
                    $('#imageModal').modal('show');
                }, file.type, 0.8); // Qualidade da imagem (0.8 = 80%)
            };

            img.src = e.target.result;
        };
        reader.readAsDataURL(file);
    }
});

// Função para salvar a imagem após editar (salvando como Base64)
document.querySelector('#saveImageButton').addEventListener('click', function (event) {
    event.preventDefault();

    // Captura o formulário
    const form = document.querySelector('#imageForm');
    if (!form) {
        console.error("Formulário não encontrado!");
        return;
    }

    // Serializa os dados do formulário
    const formData = new FormData(form);

    // Adiciona manualmente a imagem em Base64, caso necessário
    const canvas = document.querySelector('#imageCanvas');
    if (canvas) {
        const imageBase64 = canvas.toDataURL('image/png'); // Gera a imagem como Base64
        formData.append('image_data', imageBase64); // Adiciona ao FormData
    } else {
        console.error("Canvas não encontrado!");
        return;
    }

    // Enviar via AJAX
    fetch(form.action, {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value // CSRF Token
        },
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`Erro na resposta: ${response.statusText}`);
        }
        return response.json(); // Assume que o servidor retorna JSON
    })
    .then(data => {
        console.log("Imagem salva com sucesso!", data);
        $('#imageModal').modal('hide'); // Fecha o modal
        window.location.reload();
    })
    .catch(error => {
        console.error("Erro ao salvar a imagem:", error);
    });
});

// Função para editar a imagem (abertura do modal de edição)
document.querySelectorAll('.fa-edit').forEach((element) => {
    element.addEventListener('click', (event) => {
        event.preventDefault(); // Previne o comportamento padrão do link

        // Obtém os dados armazenados nos atributos data-*
        const imageId = element.getAttribute('data-image-id');
        const description = element.getAttribute('data-description');
        const caption = element.getAttribute('data-caption');
        const imageUrl = element.getAttribute('data-image-url');

        // Preenche os elementos da janela modal com os dados da imagem
        document.querySelector('#image_id').value = imageId;
        document.querySelector('#imageDescription').value = description;
        document.querySelector('#imageCaption').value = caption;

        // Carrega a imagem no canvas
        const canvas = document.querySelector('#imageCanvas');
        const ctx = canvas.getContext('2d');
        const img = new Image();
        img.onload = () => {
            canvas.width = img.width;
            canvas.height = img.height;
            ctx.drawImage(img, 0, 0);
        };
        img.src = imageUrl;

        // Abre o modal de edição
        $('#imageModal').modal('show');
    });
});

// Função para trocar a imagem carregada no canvas (simula clique no input de imagem)
document.querySelector('#change_img').addEventListener('click', (event) => {
    event.preventDefault(); // Previne o comportamento padrão do link
    document.querySelector('#imageInput').click(); // Simula o clique no input de arquivo
});
