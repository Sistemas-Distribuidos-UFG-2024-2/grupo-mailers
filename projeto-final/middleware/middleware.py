# middleware.py

import redis
import json
import time
from config import REDIS_HOST, REDIS_PORT, REDIS_QUEUE, EMAIL_SERVERS, BALANCE_STRATEGY

# Conexão com o Redis
redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)

# Controlador para balanceamento de carga
server_index = 0

# Função para enfileirar os e-mails
def enfileirar_email(lista_emails, assunto, corpo, formato_html=False):
    email_data = {
        'lista_emails': lista_emails,
        'assunto': assunto,
        'corpo': corpo,
        'formato_html': formato_html
    }
    redis_client.rpush(REDIS_QUEUE, json.dumps(email_data))
    print(f"Lote de e-mails enfileirado com sucesso!")

# Função para balancear a carga entre os servidores de e-mail
def obter_servidor():
    global server_index
    if BALANCE_STRATEGY == 'round_robin':
        servidor = EMAIL_SERVERS[server_index]
        server_index = (server_index + 1) % len(EMAIL_SERVERS)
        return servidor
    # Outras estratégias de balanceamento podem ser adicionadas aqui
    return EMAIL_SERVERS[0]

# Função para processar a fila e enviar e-mails para os servidores
def processar_fila():
    while True:
        # Extrair um item da fila
        email_data = redis_client.lpop(REDIS_QUEUE)
        if email_data:
            email_data = json.loads(email_data)
            servidor = obter_servidor()

            # Enviar o lote de e-mails ao servidor de e-mail selecionado
            enviar_para_servidor(email_data, servidor)
        else:
            print("Fila vazia, aguardando novos e-mails...")
            time.sleep(2)  # Espera antes de verificar a fila novamente

# Função para enviar os e-mails para o servidor específico
def enviar_para_servidor(email_data, servidor):
    print(f"Enviando lote de e-mails para o servidor {servidor['host']}:{servidor['port']}")
    # Aqui, implementamos a lógica de comunicação com o servidor de e-mail
    # Para uma implementação completa, usaria-se um protocolo como HTTP para
    # enviar os dados ao servidor de e-mail
    # Exemplo:
    # response = requests.post(f"http://{servidor['host']}:{servidor['port']}/enviar_lote", json=email_data)
    # print(f"Resposta do servidor: {response.status_code}")
    pass  # Substituir com a chamada ao servidor de e-mail real

# Exemplo de uso
if __name__ == "__main__":
    # Enfileirar um lote de e-mails
    lista_emails = ["destinatario1@exemplo.com", "destinatario2@exemplo.com"]
    assunto = "Teste de Envio"
    corpo = "Esse é um teste de envio de e-mails com middleware e balanceamento de carga."
    enfileirar_email(lista_emails, assunto, corpo)

    # Processar a fila e distribuir os e-mails
    processar_fila()