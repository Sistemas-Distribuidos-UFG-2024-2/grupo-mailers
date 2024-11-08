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

# Função para dividir e enfileirar os e-mails por lote, considerando os servidores disponíveis
def enfileirar_email(lista_emails, assunto, corpo):
    num_servidores = len(EMAIL_SERVERS)
    # Divide os e-mails em lotes iguais, distribuindo entre os servidores
    lotes_emails = [lista_emails[i::num_servidores] for i in range(num_servidores)]

    for i, lote in enumerate(lotes_emails):
        if lote:
            # Enfileira cada lote com o índice para associar ao servidor
            email_data = {
                'lista_emails': lote,
                'assunto': assunto,
                'corpo': corpo,
                'servidor_index': i  # Índice para balancear os servidores
            }
            redis_client.rpush(REDIS_QUEUE, json.dumps(email_data))
            print(f"Lote de e-mails enfileirado para o servidor {i + 1}")

# Função para escolher o servidor baseado no índice
def obter_servidor(index):
    return EMAIL_SERVERS[index % len(EMAIL_SERVERS)]

# Função para processar a fila de e-mails
def processar_fila():
    while True:
        email_data = redis_client.lpop(REDIS_QUEUE)
        if email_data:
            email_data = json.loads(email_data)
            servidor_index = email_data['servidor_index']
            servidor = obter_servidor(servidor_index)  # Obtém o servidor baseado no índice
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

    # Enfileira os e-mails dividindo em lotes
    enfileirar_email(lista_emails, assunto, corpo)
    
    return jsonify({'message': 'E-mails enfileirados com sucesso!'}), 200

# Inicia o processamento da fila em um processo paralelo
from threading import Thread
thread = Thread(target=processar_fila)
thread.daemon = True
thread.start()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)  # Middleware escutando na porta 5000