package main

import (
	"bufio"
	"fmt"
	"net"
	"os"
)

func main() {
	conn, err := net.Dial("tcp", "localhost:8080")
	if err != nil {
		fmt.Println("Erro ao conectar ao servidor:", err)
		os.Exit(1)
	}
	defer conn.Close()

	fmt.Println("Conectado ao servidor. Digite suas mensagens:")

	reader := bufio.NewReader(os.Stdin)
	for {
		fmt.Print("Você: ")
		message, _ := reader.ReadString('\n')
		encryptedMessage := caesarCipher(message, 3)
		conn.Write([]byte(encryptedMessage))
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

	// Converte o slice de bytes de volta para uma string e retorna
	return string(shifted)
}
