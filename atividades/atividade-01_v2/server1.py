import socket
import pickle
from middleware import Middleware

class Server:
    def __init__(self, host='localhost', port=65432):
        self.host = host
        self.port = port

    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.host, self.port))  # Vinculando o socket ao host e porta
            s.listen()

            print(f"Servidor rodando em {self.host}:{self.port}")

            while True:
                conn, addr = s.accept()  # Aceita a conexão de um cliente
                with conn:
                    print(f"Conectado por {addr}")
                    message = pickle.loads(conn.recv(1024))  # Recebe a mensagem
                    print(f"Mensagem recebida: {message}")

                    response = f"Mensagem '{message}' recebida e processada com sucesso."
                    conn.sendall(pickle.dumps(response))

if __name__ == "__main__":
    server = Server(host='localhost', port=65432)
    server.start()