document.addEventListener("DOMContentLoaded", function() {
    // Função para enviar a pergunta para a API
    function enviarPergunta(pergunta) {
        // Cria o objeto com os dados da pergunta
        var dados = {
            "pergunta": pergunta
        };

        // Faz a requisição POST para a rota '/pergunta-evento' da sua API
        fetch('http://localhost:5000/pergunta-evento', {  // Atualize a URL para o endereço correto da sua API
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(dados)
        })
        .then(function(response) {
            return response.json();
        })
        .then(function(data) {
            // Exibe a resposta do modelo na página
            exibirMensagem('assistant', data.resposta);
        })
        .catch(function(error) {
            console.error('Erro:', error);
        });
    }

        // Função para exibir mensagens na interface do chat
        function exibirMensagem(papel, conteudo) {
            var chatBody = document.querySelector('.chat-body');

            // Cria o elemento de mensagem
            var mensagem = document.createElement('div');
            mensagem.className = 'message';

            // Define a classe da mensagem com base no papel
            if (papel === 'user') {
                mensagem.classList.add('user-message');
            } else if (papel === 'assistant') {
                mensagem.classList.add('assistant-message');
            }

            // Quebra as linhas no conteúdo da mensagem
            var linhas = conteudo.split('\n');
            for (var i = 0; i < linhas.length; i++) {
                var linha = document.createElement('div');
                linha.textContent = linhas[i];
                mensagem.appendChild(linha);

                // Adiciona uma quebra de linha adicional, exceto para a última linha
                if (i < linhas.length - 1) {
                    var quebraDeLinha = document.createElement('br');
                    mensagem.appendChild(quebraDeLinha);
                }
            }

            // Adiciona a mensagem ao corpo do chat
            chatBody.appendChild(mensagem);

            // Rola o chat para exibir a mensagem mais recente
            chatBody.scrollTop = chatBody.scrollHeight;
        }

    // Função para tratar o envio do formulário
    function enviarFormulario(event) {
        event.preventDefault();

        // Obtém o valor do campo de texto
        var input = document.querySelector('#mensagem-input');
        var pergunta = input.value;

        // Verifica se a pergunta não está vazia
        if (pergunta.trim() === '') {
            return; // Retorna imediatamente se a pergunta estiver vazia
        }

        // Exibe a pergunta do usuário na interface
        exibirMensagem('user', pergunta);

        // Envia a pergunta para a API
        enviarPergunta(pergunta);

        // Limpa o campo de texto
        input.value = '';
    }

    // Função para ativar o reconhecimento de voz
    function ativarReconhecimentoVoz() {
        var recognition = new webkitSpeechRecognition();
        recognition.lang = 'pt-BR';
        recognition.start();

        recognition.onresult = function(event) {
            var resultado = event.results[0][0].transcript;
            var input = document.querySelector('#mensagem-input');
            input.value = resultado;
        };
    }

    // Adiciona o evento de envio do formulário ao botão 'Enviar'
    var enviarButton = document.querySelector('#enviar-button');
    enviarButton.addEventListener('click', enviarFormulario);

    // Adiciona o evento de envio do formulário ao pressionar Enter
    var inputText = document.querySelector('#mensagem-input');
    inputText.addEventListener('keydown', function(event) {
        if (event.key === 'Enter') {
            enviarFormulario(event);
        }
    });

    // Adiciona o evento de ativar reconhecimento de voz ao botão do microfone
    var microfoneButton = document.querySelector('#microfone-button');
    microfoneButton.addEventListener('click', ativarReconhecimentoVoz);
});
