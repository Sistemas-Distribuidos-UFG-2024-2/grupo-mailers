import socket
import pickle

class Server:
    def __init__(self, host='localhost', port=65434):
        self.host = host
        self.port = port

    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.host, self.port))
            s.listen()

            print(f"Servidor rodando em {self.host}:{self.port}")

            while True:
                conn, addr = s.accept()
                with conn:
                    print(f"Conectado por {addr}")
                    # Usar um buffer maior para garantir que a mensagem seja lida completamente
                    data = conn.recv(1024)
                    if not data:
                        continue  # Se não houver dados, continua o loop

                    message = pickle.loads(data)
                    print(f"Mensagem recebida: {message}")

                    if message == "Olá":
                        response = "Mundo"
                    else:
                        response = f"Mensagem '{message}' recebida e processada com sucesso."
                    
                    conn.sendall(pickle.dumps(response))

if __name__ == "__main__":
    server = Server(host='localhost', port=65434)
    server.start()