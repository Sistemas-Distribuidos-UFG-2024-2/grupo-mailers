# config.py

REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_QUEUE = 'email_queue'

# Lista de URLs dos servidores de e-mail para balanceamento de carga
EMAIL_SERVERS = [
    'http://localhost:5001/enviar_lote',  # Servidor de envio de e-mail 1
    'http://localhost:5002/enviar_lote',  # Servidor de envio de e-mail 2
    # Adicione mais servidores se necessário
]

BALANCE_STRATEGY = 'round_robin'  # Estratégia de balanceamento