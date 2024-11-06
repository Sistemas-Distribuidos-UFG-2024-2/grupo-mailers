# email_service.py

from flask import Flask, request, jsonify
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import argparse
import time
from config import SMTP_SERVER, SMTP_PORT, SMTP_USER, SMTP_PASSWORD, RETRY_LIMIT, RETRY_DELAY, CIRCUIT_BREAKER_THRESHOLD, CIRCUIT_BREAKER_TIMEOUT

app = Flask(__name__)

class CircuitBreaker:
    def __init__(self):
        self.failures = 0
        self.is_open = False
        self.last_failure_time = 0

    def record_failure(self):
        self.failures += 1
        self.last_failure_time = time.time()
        if self.failures >= CIRCUIT_BREAKER_THRESHOLD:
            self.is_open = True
            print("Circuit Breaker ativado - servidor temporariamente desativado")

    def reset(self):
        self.failures = 0
        self.is_open = False

    def is_available(self):
        if self.is_open:
            if time.time() - self.last_failure_time > CIRCUIT_BREAKER_TIMEOUT:
                print("Circuit Breaker fechado - servidor reativado")
                self.reset()
            else:
                return False
        return True

circuit_breaker = CircuitBreaker()

def enviar_email(destinatario, assunto, corpo, formato_html=False):
    if not circuit_breaker.is_available():
        print("Envio cancelado: Circuit Breaker está ativado.")
        return False

    tentativas = 0
    while tentativas < RETRY_LIMIT:
        try:
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
                delay = RETRY_DELAY * (2 ** (tentativas - 1))  # Atraso exponencial
                print(f"Aguardando {delay} segundos antes da próxima tentativa...")
                time.sleep(delay)

    print(f"Falha ao enviar e-mail para {destinatario} após {RETRY_LIMIT} tentativas.")
    return False

@app.route('/enviar_lote', methods=['POST'])
def enviar_lote():
    data = request.json
    lista_emails = data.get('lista_emails', [])
    assunto = data.get('assunto', 'Sem Assunto')
    corpo = data.get('corpo', '')

    resultados = []
    for destinatario in lista_emails:
        sucesso = enviar_email(destinatario.strip(), assunto, corpo)
        resultados.append({'destinatario': destinatario, 'sucesso': sucesso})

    return jsonify({'status': 'Processado', 'resultados': resultados})

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Servidor de Envio de E-mails")
    parser.add_argument('--port', type=int, default=5001, help='Porta para rodar o servidor')
    args = parser.parse_args()

    app.run(host='0.0.0.0', port=args.port)
