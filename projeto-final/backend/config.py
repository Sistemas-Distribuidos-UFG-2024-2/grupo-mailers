# config.py

#SMTP_SERVER = 'smtp.gmail.com'
SMTP_SERVER = 'localhost'
#SMTP_PORT = 587
SMTP_PORT = 1025
SMTP_USER = 'test@localhost'
SMTP_PASSWORD = 'sua_senha_de_app'  # Use uma senha de aplicativo

# Parâmetros de retry
#RETRY_LIMIT = 3            # Número máximo de tentativas de retry
#RETRY_DELAY = 5            # Tempo em segundos entre tentativas (pode ser aumentado)

# Circuit Breaker
#CIRCUIT_BREAKER_THRESHOLD = 3   # Máximo de falhas consecutivas antes de desativar

# Parâmetros do servidor Flask
API_HOST = '0.0.0.0'
API_PORT = 5001