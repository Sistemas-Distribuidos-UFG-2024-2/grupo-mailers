from flask import Flask, request, jsonify
from flask_cors import CORS
import redis
import json
import requests
import time
from config import REDIS_HOST, REDIS_PORT, REDIS_QUEUE, EMAIL_SERVERS, BALANCE_STRATEGY

app = Flask(__name__)
CORS(app)
redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)
server_index = 0

# Função para enfileirar os e-mails no Redis
def enfileirar_email(lista_emails, assunto, corpo):
    email_data = {
        'lista_emails': lista_emails,
        'assunto': assunto,
        'corpo': corpo,
    }
    redis_client.rpush(REDIS_QUEUE, json.dumps(email_data))
    print(f"E-mails enfileirados com sucesso!")

# Função para escolher o próximo servidor de e-mail usando a estratégia de balanceamento de carga
def obter_servidor():
    global server_index
    if BALANCE_STRATEGY == 'round_robin':
        servidor = EMAIL_SERVERS[server_index]
        server_index = (server_index + 1) % len(EMAIL_SERVERS)
        return servidor
    return EMAIL_SERVERS[0]

# Função para processar a fila de e-mails
def processar_fila():
    while True:
        email_data = redis_client.lpop(REDIS_QUEUE)
        if email_data:
            email_data = json.loads(email_data)
            servidor = obter_servidor()
            try:
                response = requests.post(servidor, json=email_data)
                print(f"Resposta do servidor {servidor}: {response.status_code}")
            except requests.RequestException as e:
                print(f"Erro ao se comunicar com {servidor}: {e}")
        else:
            print("Fila vazia, aguardando novos e-mails...")
            time.sleep(2)

# Rota para receber e-mails do frontend
@app.route('/enviar_lote', methods=['POST'])
def receber_requisicao_frontend():
    data = request.json
    lista_emails = data.get('lista_emails', [])
    assunto = data.get('assunto', 'Sem Assunto')
    corpo = data.get('corpo', '')

    # Enfileira os e-mails recebidos
    enfileirar_email(lista_emails, assunto, corpo)
    
    return jsonify({'message': 'E-mails enfileirados com sucesso!'}), 200

# Inicia o processamento da fila em um processo paralelo
from threading import Thread
thread = Thread(target=processar_fila)
thread.daemon = True
thread.start()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)  # Middleware escutando na porta 5000
