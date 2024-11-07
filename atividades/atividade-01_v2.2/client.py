from middleware import Middleware

class Client:
    def __init__(self):
        self.middleware = Middleware()

    def send_message(self, message):
        print(f"Enviando mensagem: {message}")
        response = self.middleware.send_message(message)
        print(f"Resposta do servidor: {response}")

if __name__ == "__main__":
    client = Client()
    
    while True:
        input("Pressione Enter para enviar 'Olá'...")
        client.send_message("Olá")