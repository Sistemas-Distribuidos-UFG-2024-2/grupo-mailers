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
python3 email_service.py --port=5001
python3 email_service.py --port=5002
python3 email_service.py --port=5003
# obs: é possível configurar vários servidores na arquitetura
````

3. Middleware:
````
cd middleware
pip install -r requirements.txt
python3 middleware.py
````

4. Inicie o Servidor SMTP Local
````
python3 -m smtpd -c DebuggingServer -n localhost:1025
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
├── README.md                # Instruções de instalação e execução do projeto
└── .gitignore                # Arquivo de exclusão para Git
````

### Descrição do Projeto

Este projeto visa criar um sistema de envio de e-mails em massa com ênfase em **resiliência**, **escalabilidade** e **recuperação de falhas**. O sistema é composto por três componentes principais:

1. **Frontend (Vue.js)**:
   - A interface do usuário foi desenvolvida em **Vue.js**. Ela permite ao usuário carregar uma lista de e-mails, definir o assunto e o corpo do e-mail e enviar para os servidores de e-mail. O frontend se comunica com o **middleware** via **API REST**.
   
2. **Middleware (Flask + Redis)**:
   - O **middleware** gerencia a fila de e-mails e faz o balanceamento de carga entre os servidores de e-mails. Ele usa **Redis** para enfileirar as requisições de e-mails e distribui a carga entre os servidores de envio utilizando a estratégia de **round robin**. O balanceamento de servidores é dinâmico e baseado em **status de disponibilidade** de cada servidor.
   - O **heartbeat** foi implementado para monitorar a disponibilidade dos servidores de e-mail e atualizar dinamicamente a lista de servidores ativos.
   
3. **Servidores de E-mail (Flask + SMTP)**:
   - Cada servidor de e-mail é implementado com **Flask** e **SMTP**. Eles recebem uma requisição com a lista de e-mails e enviam as mensagens. O sistema de envio é robusto, com **tentativas de reenvio (Retry)** e **circuit breaker** para lidar com falhas temporárias. Quando o limite de falhas é atingido, o servidor entra em um estado de espera antes de ser reabilitado.

### Componentes Implementados

1. **Frontend (Vue.js)**:
   - Formulário para envio de e-mails.
   - Envio de requisição para o middleware, com lista de e-mails e conteúdo.
   - Interface simples para interação do usuário.

2. **Middleware (Flask + Redis)**:
   - **Fila de E-mails**: Gerencia as requisições e as coloca em uma fila (Redis).
   - **Balanceamento de Carga**: Distribui as requisições entre os servidores de e-mail disponíveis.
   - **Monitoramento (Heartbeat)**: Verifica periodicamente a disponibilidade dos servidores e atualiza a lista de servidores ativos.

3. **Servidores de E-mail (Flask + SMTP)**:
   - Recebem e-mails via API e enviam para os destinatários.
   - Implementação de **Retry** para tentar enviar os e-mails novamente em caso de falha.
   - **Circuit Breaker** para evitar sobrecarga e falhas constantes.

### Funcionalidades Implementadas

- **Envio de e-mails em massa**: O sistema permite enviar e-mails para uma lista de destinatários fornecida pelo usuário no frontend.
- **Balanceamento de carga**: A carga de envio de e-mails é distribuída entre múltiplos servidores de e-mail, garantindo melhor desempenho e escalabilidade.
- **Monitoramento de servidores de e-mail**: O sistema verifica periodicamente quais servidores estão disponíveis e ajusta a distribuição da carga dinamicamente.
- **Retry e Circuit Breaker**: Se um servidor falhar, o sistema tenta reprocessar a solicitação com um atraso exponencial, e se o servidor continuar com falhas, ele entra em um estado de "circuito aberto".

<br>

## Próximas Etapas do Projeto

#### 1. Implementar um servidor SMTP para cada servidor de envio de e-mail
- Configurar servidores SMTP individuais para cada servidor de e-mail.
- Testar o envio de e-mails com diferentes servidores SMTP.

#### 2. Implementar Serviço de Descoberta de Servidores de E-mail
- Criar serviço de heartbeat para monitorar a disponibilidade dos servidores de e-mail.
- Implementar um servidor de descoberta para manter a lista de servidores ativos.
- Atualizar o middleware para consultar o servidor de descoberta e usar servidores disponíveis dinamicamente.

#### 3. Estilizar Frontend

#### 4. Testes e Ajustes Finais
- Testar servidores SMTP em paralelo.
- Validar a descoberta dinâmica de servidores.
- Testar o balanceamento de carga e recuperação de falhas.