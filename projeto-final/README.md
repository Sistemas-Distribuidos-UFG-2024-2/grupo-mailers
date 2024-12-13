## Como Rodar o Projeto

1. Executar frontend:
````
cd frontend
npm install
npm run serve
````

2. Servidor de Envio Email:
````
cd backend
pip install -r requirements.txt
python3 email_service.py --port=5001 --smtp_port=1025
python3 email_service.py --port=5002 --smtp_port=1026
python3 email_service.py --port=5003 --smtp_port=1027
# obs: é possível configurar vários servidores na arquitetura
````

3. Middleware:
````
cd middleware
pip install -r requirements.txt
python3 middleware.py
````

4. Inicie os Servidores SMTPs Locais
````
python3 -m smtpd -c DebuggingServer -n localhost:1025
python3 -m smtpd -c DebuggingServer -n localhost:1026
python3 -m smtpd -c DebuggingServer -n localhost:1027
# obs: é possível configurar vários servidores na arquitetura
````

5. Heartbeats
````
cd heartbeats
pip install -r requirements.txt
python3 heartbeat.py
````

6. Redis 
- Duas opções: 
   - instalar e utilizar o redis instalado na sua maquina
   - criar uma instancia docker:
      - ``docker pull redis``
      - ``docker run --name redis -p 6379:6379 -d redis``

6. Acesse a aplicação **http://localhost:8080/**

<br>

## Status atual do projeto

### Estrutura de Pastas

````
projeto_envio_emails/
├── frontend/                # Aplicação Vue.js
│   ├── public/
│   ├── src/
│   │   ├── assets/
│   │   ├── components/
│   │   │   └── EmailForm.vue   # Formulário de envio de e-mails
│   │   ├── App.vue           # Componente raiz
│   │   └── main.js           # Arquivo principal de entrada
│   └── package.json          # Dependências do Vue.js
├── middleware/              # Middleware de gerenciamento de filas e balanceamento
│   ├── middleware.py         # Código principal do middleware
│   ├── config.py             # Configurações do Redis e balanceamento
│   └── requirements.txt      # Dependências do middleware (Redis, Flask-CORS)
├── servidor_email/          # Servidor de envio de e-mails via API
│   ├── email_service.py      # Código principal do servidor de e-mails
│   ├── config.py             # Configurações do servidor SMTP e dados da API
│   └── requirements.txt      # Dependências do servidor de e-mail (Flask)
├── heartbeats/          # Servidor de heartbeats
│   ├── heartbeat.py          # Código principal do servidor de heartbeats
│   └── requirements.txt      # Dependências do servidor de heartbeats (Flask)
├── README.md                # Instruções de instalação e execução do projeto
└── .gitignore                # Arquivo de exclusão para Git
````

### Arquitetura do sistema

<img src="https://raw.githubusercontent.com/Sistemas-Distribuidos-UFG-2024-2/grupo-mailers/037689f4bb44a6c56b837ef1336e65e9e84f4c2f/projeto-final/diagrama-arquitetura-sistema.png"></img>

### Componentes Implementados

1. **Frontend (Vue.js)**:
   - Formulário para envio de e-mails.
   - Envio de requisição para o middleware, com lista de e-mails e conteúdo.
   - Interface simples para interação do usuário.

2. **Middleware (Flask + Redis)**:
   - **Fila de E-mails**: Gerencia as requisições e as coloca em uma fila (Redis).
   - **Balanceamento de Carga**: Distribui as requisições entre os servidores de e-mail disponíveis.

3. **Servidor de Heartbeat**:
   - Envia periodicamente uma requisição para verificar se os servidores de envio de e-mail estão ativos.

4. **Servidores de Envio de E-mail (Flask)**:
   - Recebem uma lista de e-mails via API e enviam para o servidor SMTP.
   - Implementação de **Retry** para tentar enviar os e-mails novamente em caso de falha.
   - **Circuit Breaker** para evitar sobrecarga e falhas constantes.

5. **Servidores de SMTP**:
   - Recebem e-mails e enviam para os destinatários.

### Conceitos Implementados

- **Envio de e-mails em massa**: O sistema permite enviar e-mails para uma lista de destinatários fornecida pelo usuário no frontend.
- **Workload**: O sistema está preparado para lidar com um grande número de e-mails.
- **Balanceamento de carga**: A carga de envio de e-mails é distribuída entre múltiplos servidores de envio de e-mail, garantindo melhor desempenho e escalabilidade.
- **Monitoramento de servidores de e-mail (Heartbeat)**: O sistema verifica periodicamente quais servidores estão disponíveis e ajusta a distribuição da carga dinamicamente.
- **Retry e Circuit Breaker**: Se um servidor falhar, o sistema tenta reprocessar a solicitação com um atraso exponencial, e se o servidor continuar com falhas, ele entra em um estado de "circuito aberto".

### Apresentação do projeto:
https://www.youtube.com/watch?v=MaU5SGy7Ppk
