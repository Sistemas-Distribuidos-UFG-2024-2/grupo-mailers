<template>
  <div class="email-form">
    <h1>Envio de E-mails em Massa</h1>
    <form @submit.prevent="enviarEmails">
      <div class="form-group">
        <label for="assuntoEmail">Assunto do E-mail:</label>
        <input
          id="assuntoEmail"
          v-model="assuntoEmail"
          type="text"
          placeholder="Digite o assunto do e-mail"
        />
      </div>

      <div class="form-group">
        <label for="listaEmails">Lista de E-mails (um por linha):</label>
        <textarea
          id="listaEmails"
          v-model="listaEmails"
          rows="6"
          placeholder="Digite cada e-mail em uma linha separada"
        ></textarea>
      </div>

      <div class="form-group">
        <label for="corpoEmail">Corpo do E-mail:</label>
        <textarea
          id="corpoEmail"
          v-model="corpoEmail"
          rows="8"
          placeholder="Digite o conteúdo do e-mail"
        ></textarea>
      </div>

      <button type="submit" class="btn">Enviar E-mails</button>
    </form>

    <div v-if="mensagem" :class="['mensagem', mensagemTipo]">
      {{ mensagem }}
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      assuntoEmail: "",
      listaEmails: "",
      corpoEmail: "",
      mensagem: "",
      mensagemTipo: "" // Sucesso ou erro
    };
  },
  methods: {
    async enviarEmails() {
      try {
        // Dividir a lista de e-mails por linha
        const emails = this.listaEmails.split("\n").map(email => email.trim()).filter(email => email);

        // Dados para a requisição
        const dados = {
          lista_emails: emails,
          assunto: this.assuntoEmail,
          corpo: this.corpoEmail
        };

        // Enviar requisição para o middleware (garanta que a porta esteja correta)
        const response = await axios.post("http://localhost:5000/enviar_lote", dados);

        // Exibir a mensagem de sucesso
        this.mensagem = response.data.message || "E-mails enviados com sucesso!";
        this.mensagemTipo = "sucesso";
      } catch (error) {
        this.mensagem = "Erro ao enviar e-mails.";
        this.mensagemTipo = "erro";
        console.error("Erro:", error);
      }
    }
  }
};
</script>

<style scoped>
/* Estilização geral */
.email-form {
  max-width: 700px;
  margin: 2rem auto;
  padding: 2rem;
  background: #f9f9f9;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  font-family: Arial, sans-serif;
}

/* Título */
.email-form h1 {
  text-align: center;
  margin-bottom: 1.5rem;
  color: #333;
}

/* Grupos de formulário */
.form-group {
  margin-bottom: 1.5rem;
}

label {
  display: block;
  font-weight: bold;
  margin-bottom: 0.5rem;
  color: #555;
}

input, textarea {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 5px;
  font-size: 16px;
  outline: none;
}

input:focus, textarea:focus {
  border-color: #007BFF;
  box-shadow: 0 0 5px rgba(0, 123, 255, 0.3);
}

/* Botão */
.btn {
  display: block;
  width: 100%;
  padding: 12px;
  background: #007BFF;
  color: #fff;
  border: none;
  border-radius: 5px;
  font-size: 18px;
  font-weight: bold;
  cursor: pointer;
  transition: background 0.3s ease;
}

.btn:hover {
  background: #0056b3;
}

/* Mensagens de feedback */
.mensagem {
  margin-top: 1rem;
  padding: 1rem;
  text-align: center;
  font-weight: bold;
  border-radius: 5px;
}

.mensagem.sucesso {
  background: #d4edda;
  color: #155724;
  border: 1px solid #c3e6cb;
}

.mensagem.erro {
  background: #f8d7da;
  color: #721c24;
  border: 1px solid #f5c6cb;
}
</style>
