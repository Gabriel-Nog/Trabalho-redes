package main

import (
	"bufio"
	"fmt"
	"net"
	"os"
)

func main() {
	listener, err := net.Listen("tcp", ":8080")
	if err != nil {
		fmt.Println("Erro ao iniciar o servidor:", err)
		os.Exit(1)
	}
	defer listener.Close()

	fmt.Println("Servidor iniciado na porta 8080")

	for {
		conn, err := listener.Accept()
		if err != nil {
			fmt.Println("Erro ao aceitar conexão:", err)
			continue
		}
		go handleConnection(conn)
	}
}

func handleConnection(conn net.Conn) {
	defer conn.Close()
	reader := bufio.NewReader(conn)
	for {
		message, err := reader.ReadString('\n')
		if err != nil {
			fmt.Println("Erro ao ler mensagem:", err)
			return
		}
		decryptedMessage := caesarCipher(message, -3)
		fmt.Println("Mensagem recebida:", decryptedMessage)
	}
}

func caesarCipher(input string, shift int) string {
	// Ajusta o valor do shift para estar dentro do intervalo de 0 a 25
	shift = shift % 26

	// Cria um slice de bytes para armazenar os caracteres cifrados
	shifted := make([]byte, len(input))

	// Itera sobre cada caractere da string de entrada
	for i, char := range []byte(input) {
		// Verifica se o caractere é uma letra minúscula
		if char >= 'a' && char <= 'z' {
			// Aplica a cifra de César para letras minúsculas
			shifted[i] = 'a' + (char-'a'+byte(shift)+26)%26
		} else if char >= 'A' && char <= 'Z' {
			// Aplica a cifra de César para letras maiúsculas
			shifted[i] = 'A' + (char-'A'+byte(shift)+26)%26
		} else {
			// Mantém caracteres não alfabéticos inalterados
			shifted[i] = char
		}
	}

	// Converte o slice de bytes de volta para string e retorna
	return string(shifted)
}
