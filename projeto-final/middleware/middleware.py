# middleware.py

import redis
import json
import requests
import time
from config import REDIS_HOST, REDIS_PORT, REDIS_QUEUE, EMAIL_SERVERS, BALANCE_STRATEGY

redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)
server_index = 0

def enfileirar_email(lista_emails, assunto, corpo):
    email_data = {
        'lista_emails': lista_emails,
        'assunto': assunto,
        'corpo': corpo,
    }
    redis_client.rpush(REDIS_QUEUE, json.dumps(email_data))
    print(f"E-mails enfileirados com sucesso!")

def obter_servidor():
    global server_index
    if BALANCE_STRATEGY == 'round_robin':
        servidor = EMAIL_SERVERS[server_index]
        server_index = (server_index + 1) % len(EMAIL_SERVERS)
        return servidor
    return EMAIL_SERVERS[0]

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

if __name__ == "__main__":
    processar_fila()