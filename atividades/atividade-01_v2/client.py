from middleware import Middleware

class Client:
    def __init__(self, servers):
        self.middleware = Middleware(servers)

    def send_message(self, message):
        print(f"Enviando mensagem: {message}")
        response = self.middleware.send_message(message)
        print(f"Resposta do servidor: {response}")


if __name__ == "__main__":
    servers = [('localhost', 65432), ('localhost', 65433), ('localhost', 65434)]
    
    client = Client(servers)
    client.send_message("Olá, servidor!")