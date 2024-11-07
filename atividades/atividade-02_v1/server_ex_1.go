package main

import (
	"encoding/json"
	"fmt"
	"net"
)

type Funcionario struct {
	Nome   string  `json:"nome"`
	Cargo  string  `json:"cargo"`
	Salario float64 `json:"salario"`
}

func calcularReajuste(funcionario Funcionario) (string, float64) {
	var reajuste float64

	switch funcionario.Cargo {
	case "operador":
		reajuste = funcionario.Salario * 0.20
	case "programador":
		reajuste = funcionario.Salario * 0.18
	default:
		reajuste = 0
	}

	salarioReajustado := funcionario.Salario + reajuste
	return funcionario.Nome, salarioReajustado
}

func main() {
	listener, err := net.Listen("tcp", ":8080")
	if err != nil {
		fmt.Println("Erro ao iniciar o servidor:", err)
		return
	}
	defer listener.Close()
	fmt.Println("Servidor ouvindo na porta 8080...")

	for {
		conn, err := listener.Accept()
		if err != nil {
			fmt.Println("Erro ao aceitar conexão:", err)
			continue
		}

		go func(c net.Conn) {
			defer c.Close()
			var funcionario Funcionario

			// Lê dados do cliente
			decoder := json.NewDecoder(c)
			err := decoder.Decode(&funcionario)
			if err != nil {
				fmt.Println("Erro ao decodificar dados:", err)
				return
			}

			// Calcula o salário reajustado
			nome, salarioReajustado := calcularReajuste(funcionario)

			// Envia o resultado de volta
			resultado := map[string]interface{}{
				"nome":              nome,
				"salario_reajustado": salarioReajustado,
			}
			encoder := json.NewEncoder(c)
			encoder.Encode(resultado)
		}(conn)
	}
}