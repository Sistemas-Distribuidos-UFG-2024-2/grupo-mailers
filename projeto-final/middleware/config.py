# config.py

REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_QUEUE = 'email_queue'

# Lista de servidores de e-mail disponíveis
EMAIL_SERVERS = [
    {'host': 'localhost', 'port': 1025},  # Servidor de e-mail 1
    # Adicione outros servidores aqui para balanceamento
]

BALANCE_STRATEGY = 'round_robin'  # Estratégia de balanceamento