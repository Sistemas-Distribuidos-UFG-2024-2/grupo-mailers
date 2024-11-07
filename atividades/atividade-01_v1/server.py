import socket
from sys import argv


addr = ('', int(argv[1]))
server = socket.create_server(addr)


while True:
    server.listen()
    conn, client_addr = server.accept()


    msg = conn.recv(64).decode()
    if msg == 'Hello':
        print('Hello')
        conn.send('World'.encode())
        print('World enviado')