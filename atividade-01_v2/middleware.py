
import socket
import pickle
import threading
import time

class ServerMonitor:
    def __init__(self, servers, check_interval=5):
        self.servers = servers  # Lista de servidores (host, port)
        self.check_interval = check_interval  # Intervalo de verificação
        self.server_status = {server: False for server in servers}  # Status inicial de todos os servidores (False = offline)

    def check_server_status(self, server):
        host, port = server
        try:
            # Tentativa de conexão ao servidor com timeout curto (1 segundo)
            with socket.create_connection((host, port), timeout=1):
                return True
        except OSError:
            return False

    def monitor_servers(self):
        while True:
            for server in self.servers:
                is_active = self.check_server_status(server)
                self.server_status[server] = is_active
                status = "ativo" if is_active else "inativo"
                print(f"Servidor {server[0]}:{server[1]} está {status}.")
            
            time.sleep(self.check_interval)

    def start_monitoring(self):
        monitor_thread = threading.Thread(target=self.monitor_servers)
        monitor_thread.daemon = True
        monitor_thread.start()

    def get_active_servers(self):
        return [server for server, status in self.server_status.items() if status]

class Middleware:
    def __init__(self, servers):
        self.monitor = ServerMonitor(servers)
        self.monitor.start_monitoring()

    def send_message(self, message):
        active_servers = self.monitor.get_active_servers()
        if not active_servers:
            raise ConnectionError("Nenhum servidor ativo disponível no momento.")
        
        host, port = active_servers[0]
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
            serialized_message = pickle.dumps(message)
            s.sendall(serialized_message)

            data = s.recv(1024)
            return pickle.loads(data)