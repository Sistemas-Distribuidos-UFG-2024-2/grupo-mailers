import socket

serv_addr_list = [('localhost', 12345), ('localhost', 12346), ('localhost', 12347)]

while True:
    input('')

    for serv_addr in serv_addr_list:
        try:
            conn = socket.create_connection(serv_addr)
            conn.send('Hello'.encode())
            print('Hello enviado')
            resposta = conn.recv(64).decode()
            print(resposta)
            conn.close()
            break
        except:
            pass
