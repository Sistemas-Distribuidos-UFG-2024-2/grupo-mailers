import rpyc
import socket
import threading

server_ip = 'localhost'
server_port = 12345

server_conn = None


def connect_to_server (server_ip, server_port):
    global server_conn

    try:
        server_conn.ping()
    except:
        server_conn = rpyc.connect(server_ip, server_port)
    
    return server_conn
    

def send_messages (oth_user_ip, oth_user_port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    while True:
        msg = input().encode()
        sock.sendto(msg, (oth_user_ip, oth_user_port))


def listen_messages (own_ip, own_port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((own_ip, own_port))

    while True:
        msg, addr = sock.recvfrom(1024)
        print(msg.decode())


while True:
    cmd = input(
        f'Escolha uma opção:\n'
        f'1. Login\n'
        f'2. Registrar\n'
    )

    match cmd:
        # Login
        case '1':
            user_id = input('Digite seu ID de usuário.\n')
            psw = input('Digite a sua senha.\n')

            conn = connect_to_server(server_ip, server_port)
            server = conn.root

            if server.auth_user(user_id, psw):
                print('Login realizado com sucesso.')
                break
            else:
                print('Falha ao fazer login.')


        case '2':
            # Registrar
            user_id = input('Digite seu ID de usuário.\n')
            user_ip = input('Digite o IP para recebimento de mensagens.\n')
            user_port = int(input('Digite a porta para recebimento de mensagens.\n'))
            user_psw = input('Digite uma senha.\n')

            conn = connect_to_server(server_ip, server_port)
            server = conn.root

            if server.register_user(user_id, user_ip, user_port, user_psw):
                print('Registro realizado com sucesso.')
            else:
                print('Falha ao registrar.')


        case _:
            print(f'{cmd} não é uma opção válida.\n')



while True:
    oth_user_id = input('Digite o ID do usuário com quem quer trocar mensagens.\n')
    conn = connect_to_server(server_ip, server_port)
    server = conn.root

    oth_user_ip, oth_user_port = server.search_user(oth_user_id)
    own_ip, own_port = server.search_user(user_id)

    if oth_user_ip == -1:
        print('Usuário não encontrado.')
        continue

    # send_thread = threading.Thread(target=send_messages, args=(oth_user_ip, oth_user_port))
    listen_thread = threading.Thread(target=listen_messages, args=(own_ip, own_port))
    listen_thread.start()

    send_messages(oth_user_ip, oth_user_port)
