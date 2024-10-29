package main

import (
	"log"

	"github.com/gofiber/fiber/v2"
	"github.com/gofiber/websocket/v2"
)

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

func main() {
	app := fiber.New()

	// Serve static files
	app.Static("/", "./public")

	// WebSocket endpoint
	app.Get("/ws", websocket.New(func(c *websocket.Conn) {
		defer c.Close()
		for {
			// Lendo mensagens do cliente
			mt, msg, err := c.ReadMessage()
			if err != nil {
				log.Println("read:", err)
				break
			}
			decrypted := caesarCipher(string(msg), -3)
			log.Printf("recv: %s", decrypted)

			// Enviando mensagens para o cliente
			encryptedMsg := caesarCipher(decrypted, 3)
			if err = c.WriteMessage(mt, []byte(encryptedMsg)); err != nil {
				log.Println("write:", err)
				break
			}
		}
	}))

	log.Fatal(app.Listen("0.0.0.0:3000"))
}
