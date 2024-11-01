import rpyc
from rpyc.utils.server import ThreadedServer
import json

try:
    with open('usuarios.json', mode='r') as f:
        users_dict = json.load(f)

except FileNotFoundError:
    users_dict = {}

class MessageServer (rpyc.Service):
    def on_connect (self, conn):
        pass

    def on_disconnect (self, conn):
        pass

    def exposed_search_user (self, user_id):
        if user_id not in users_dict.keys():
            return (-1, -1)

        user_info = users_dict[user_id]
        return user_info['ip'], user_info['port']

    def exposed_register_user (self, user_id, user_ip, user_port, psw):
        if user_id in users_dict.keys():
            return False

        users_dict[user_id] = {'ip': user_ip, 'port': user_port, 'psw': psw}

        # salvar registro em disco
        with open('usuarios.json', mode='w') as f:
            json.dump(users_dict, f)

        print(
            f'Usuário {user_id} registrado.\n'
            f'IP: {user_ip}\n'
            f'Porta: {user_port}\n'
        )
        return True

    def exposed_auth_user (self, user_id, psw):
        if (user_id not in users_dict.keys()) or (users_dict[user_id]['psw'] != psw):
            return False

        return True


s = ThreadedServer(MessageServer, hostname='localhost' ,port=12345)
s.start()