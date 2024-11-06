# config.py

# Implementar API GMAIL
#SMTP_SERVER = 'smtp.gmail.com'
#SMTP_PORT = 587

SMTP_SERVER = 'localhost'
SMTP_PORT = 1025
SMTP_USER = 'test@localhost'
SMTP_PASSWORD = 'sua_senha_de_app'  # Use uma senha de aplicativo

# Parâmetros do servidor Flask
API_HOST = '0.0.0.0'
API_PORT = 5001

# Configurações do Circuit Breaker e Retry
RETRY_LIMIT = 3         # Número máximo de tentativas de retry
RETRY_DELAY = 2         # Intervalo entre tentativas de retry, em segundos
CIRCUIT_BREAKER_THRESHOLD = 5  # Máximo de falhas antes de abrir o circuito
CIRCUIT_BREAKER_TIMEOUT = 30   # Tempo de espera para o Circuit Breaker reiniciar, em segundos
