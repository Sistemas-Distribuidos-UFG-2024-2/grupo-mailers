from flask import Flask
import time

app = Flask(__name__)

@app.route('/heartbeat', methods=['GET'])
def heartbeat():
    return "Servidor está ativo", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=6000)