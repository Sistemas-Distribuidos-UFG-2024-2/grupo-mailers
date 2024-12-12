from flask import Flask, request, jsonify
from flask_cors import CORS
import redis
import json
import requests
import time
from config import REDIS_HOST, REDIS_PORT, REDIS_QUEUE, EMAIL_SERVERS

app = Flask(__name__)
CORS(app)
redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)

# Lista de servidores ativos
servidores_ativos = []

# Função para verificar o status dos servidores de heartbeat
def verificar_heartbeats():
    while True:
        for servidor in EMAIL_SERVERS:
            try:
                response = requests.get(f"{servidor}/heartbeat", timeout=3)
                if response.status_code == 200:
                    if servidor not in servidores_ativos:
                        servidores_ativos.append(servidor)
                        print(f"Servidor {servidor} está ativo.")
                else:
                    if servidor in servidores_ativos:
                        servidores_ativos.remove(servidor)
                        print(f"Servidor {servidor} foi removido.")
            except requests.RequestException:
                if servidor in servidores_ativos:
                    servidores_ativos.remove(servidor)
                    print(f"Servidor {servidor} está inativo.")
        
        time.sleep(10)  # Verificar status a cada 10 segundos

# Função para enfileirar e-mails por lote
def enfileirar_email(lista_emails, assunto, corpo):
    num_servidores = len(servidores_ativos)
    if num_servidores == 0:
        print("Erro: Nenhum servidor de e-mail disponível.")
        return

    # Divide os e-mails em lotes
    lotes_emails = [lista_emails[i::num_servidores] for i in range(num_servidores)]

    for i, lote in enumerate(lotes_emails):
        if lote:
            email_data = {
                'lista_emails': lote,
                'assunto': assunto,
                'corpo': corpo,
                'servidor_index': i
            }
            redis_client.rpush(REDIS_QUEUE, json.dumps(email_data))
            print(f"Lote de e-mails enfileirado para o servidor {i + 1}")

# Função para processar um lote de e-mails
def processar_lote(email_data, servidor):
    try:
        url_servidor = f"{servidor}/enviar_lote"
        response = requests.post(url_servidor, json=email_data)
        print(f"Resposta do servidor {servidor}: {response.status_code}")
    except requests.RequestException as e:
        print(f"Erro ao se comunicar com {servidor}: {e}")

# Função para processar a fila de e-mails
def processar_fila():
    while True:
        email_data = redis_client.lpop(REDIS_QUEUE)
        if email_data:
            email_data = json.loads(email_data)
            index = email_data.get('servidor_index', 0)
            servidor = obter_servidor(index)
            if servidor:
                # Cria uma thread para processar o lote
                thread = Thread(target=processar_lote, args=(email_data, servidor))
                thread.start()
            else:
                print("Erro: Nenhum servidor ativo disponível para processar o lote.")
        else:
            print("Fila vazia, aguardando novos e-mails...")
            time.sleep(2)

# Função para obter o servidor com base no índice
def obter_servidor(index):
    if servidores_ativos:
        return servidores_ativos[index % len(servidores_ativos)]
    else:
        return None

# Rota para receber e-mails do frontend
@app.route('/enviar_lote', methods=['POST'])
def receber_requisicao_frontend():
    data = request.json
    lista_emails = data.get('lista_emails', [])
    assunto = data.get('assunto', 'Sem Assunto')
    corpo = data.get('corpo', '')

    enfileirar_email(lista_emails, assunto, corpo)
    return jsonify({'message': 'E-mails enviados com sucesso!'}), 200

# Inicia as threads para verificar heartbeats e processar a fila
from threading import Thread

heartbeat_thread = Thread(target=verificar_heartbeats)
heartbeat_thread.daemon = True
heartbeat_thread.start()

queue_thread = Thread(target=processar_fila)
queue_thread.daemon = True
queue_thread.start()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)