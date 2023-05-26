import json
import openai
from flask import Flask, request, jsonify
from flask_cors import CORS

# Carrega os dados do arquivo JSON
with open('eventos_teste.json', encoding="utf-8") as file:
    eventos_data = json.loads(file.read())

# Configuração da API da OpenAI
openai.api_key = "SUA_CHAVE_API"

# Inicialização do servidor Flask
app = Flask(__name__)
CORS(app)  # Adicione esta linha para habilitar o CORS

# Histórico inicial vazio
historico = []

# Função para calcular o número de tokens em uma lista de mensagens
def calcular_numero_tokens(mensagens):
    return sum(len(msg['content'].split()) for msg in mensagens)

# Rota para lidar com as perguntas sobre eventos
@app.route('/pergunta-evento', methods=['POST'])
def pergunta_evento():
    pergunta = request.json['pergunta']

    # Adiciona a pergunta ao histórico
    # Adiciona a pergunta atual ao histórico
    historico.append({"role": "user", "content": pergunta})

    # Calcula o número de tokens utilizados no histórico atual
    num_tokens_historico = calcular_numero_tokens(historico)

    # Remove mensagens mais antigas do histórico, se o número de tokens ultrapassar um limite
    limite_tokens = 4000  # Defina o limite de tokens desejado
    while num_tokens_historico > limite_tokens:
        primeira_mensagem = historico.pop(0)
        num_tokens_historico = calcular_numero_tokens(historico)

    # Cria uma cópia dos eventos do JSON
    eventos = eventos_data.copy()

    # Realiza a chamada à API do ChatGPT com o histórico completo e os eventos
    resposta = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=historico + [{"role": "system", "content": json.dumps(eventos)}]
    )

    # Obtém a resposta do modelo
    resposta_modelo = resposta.choices[0].message.content

    # Adiciona a resposta do modelo ao histórico
    historico.append({"role": "system", "content": resposta_modelo})

    return jsonify({'resposta': resposta_modelo})

# Execução do servidor Flask
if __name__ == '__main__':
    app.run()

##teste no postman
## http://localhost:5000/pergunta-evento

## pergunta teste

##    {
 ##   "pergunta": "quais os eventos?"
 ##     }
##
##
##
##
##
##
##