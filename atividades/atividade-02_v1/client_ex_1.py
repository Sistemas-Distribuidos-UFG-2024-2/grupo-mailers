import socket
import json

def main():
    # Dados do funcionário
    nome = input("Digite o nome do funcionário: ")
    cargo = input("Digite o cargo do funcionário (operador/programador): ")
    salario = float(input("Digite o salário do funcionário: "))

    funcionario = {
        "nome": nome,
        "cargo": cargo,
        "salario": salario
    }

    # Conecta ao servidor
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(("localhost", 8080))

        # Envia os dados do funcionário
        s.sendall(json.dumps(funcionario).encode('utf-8'))

        # Recebe o resultado do salário reajustado
        data = s.recv(1024)
        resultado = json.loads(data.decode('utf-8'))

        # Exibe o resultado
        print(f"Funcionário: {resultado['nome']}, Salário Reajustado: {resultado['salario_reajustado']}")

if __name__ == "__main__":
    main()
