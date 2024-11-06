# email_service.py

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from time import sleep
from config import SMTP_SERVER, SMTP_PORT, SMTP_USER, SMTP_PASSWORD, RETRY_LIMIT, RETRY_DELAY, CIRCUIT_BREAKER_THRESHOLD

# Estado do Circuit Breaker
class CircuitBreaker:
    def __init__(self):
        self.failures = 0
        self.is_open = False

    def record_failure(self):
        self.failures += 1
        if self.failures >= CIRCUIT_BREAKER_THRESHOLD:
            self.is_open = True
            print("Circuit Breaker ativado - servidor temporariamente desativado")

    def reset(self):
        self.failures = 0
        self.is_open = False

# Instância do Circuit Breaker
circuit_breaker = CircuitBreaker()

def enviar_email(destinatario, assunto, corpo, formato_html=False):
    # Verificar se o Circuit Breaker está ativado
    if circuit_breaker.is_open:
        print("Envio cancelado: Circuit Breaker está ativado.")
        return False

    tentativas = 0
    while tentativas < RETRY_LIMIT:
        try:
            # Conectar ao servidor SMTP local
            servidor = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)

            mensagem = MIMEMultipart()
            mensagem['From'] = SMTP_USER
            mensagem['To'] = destinatario
            mensagem['Subject'] = assunto
            mensagem.attach(MIMEText(corpo, 'html' if formato_html else 'plain'))

            servidor.sendmail(SMTP_USER, destinatario, mensagem.as_string())
            servidor.quit()
            print(f"E-mail enviado para {destinatario}")
            circuit_breaker.reset()
            return True

        except Exception as e:
            tentativas += 1
            print(f"Erro ao enviar para {destinatario}, tentativa {tentativas}: {e}")
            circuit_breaker.record_failure()

            if tentativas < RETRY_LIMIT:
                sleep(RETRY_DELAY)

    print(f"Falha ao enviar e-mail para {destinatario} após {RETRY_LIMIT} tentativas.")
    return False

# Função para envio em lote
def enviar_lote(lista_emails, assunto, corpo, formato_html=False):
    for destinatario in lista_emails:
        enviar_email(destinatario, assunto, corpo, formato_html)

# Simulação para testar
if __name__ == "__main__":
    lista_emails = ["destinatario1@exemplo.com", "destinatario2@exemplo.com"]
    assunto = "Teste de Envio"
    corpo = "Esse é um teste de envio de e-mails com retry e circuit breaker."
    enviar_lote(lista_emails, assunto, corpo)