<template>
  <div class="email-form">
    <h1>Envio de E-mails em Massa</h1>
    <form @submit.prevent="enviarEmails">
      <label for="listaEmails">Lista de E-mails (um por linha):</label>
      <textarea
        id="listaEmails"
        v-model="listaEmails"
        rows="10"
        placeholder="Digite cada e-mail em uma linha separada"
      ></textarea>

      <label for="corpoEmail">Corpo do E-mail:</label>
      <textarea
        id="corpoEmail"
        v-model="corpoEmail"
        rows="10"
        placeholder="Digite o conteúdo do e-mail"
      ></textarea>

      <button type="submit">Enviar E-mails</button>
    </form>

    <div v-if="mensagem" class="mensagem">{{ mensagem }}</div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      listaEmails: "",
      corpoEmail: "",
      mensagem: ""
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
          assunto: "Assunto do E-mail",  // Você pode adicionar um campo de input para o assunto também
          corpo: this.corpoEmail
        };

        // Enviar requisição para o middleware (garanta que a porta esteja correta)
        const response = await axios.post("http://localhost:5000/enviar_lote", dados);

        // Exibir a mensagem de sucesso
        this.mensagem = response.data.message || "E-mails enviados com sucesso!";
      } catch (error) {
        this.mensagem = "Erro ao enviar e-mails.";
        console.error("Erro:", error);
      }
    }
  }
};
</script>

<style scoped>
.email-form {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
}

textarea {
  width: 100%;
  margin-bottom: 10px;
}

button {
  padding: 10px 15px;
  cursor: pointer;
}

.mensagem {
  margin-top: 15px;
  font-weight: bold;
}
</style>
