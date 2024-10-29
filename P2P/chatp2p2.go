package main

import (
	"bufio"
	"fmt"
	"log"
	"net"
	"os"
)

const porta = ":9000"

func main() {
	if len(os.Args) != 2 {
		fmt.Println("User chatp2p <ip_server>")
		os.Exit(0)
	}

	go client(os.Args[1])
	server()
}

func server() {
	server, err := net.Listen("tcp", porta)
	if err != nil {
		log.Fatal(err)
	}

	fmt.Println("Servidor: " + GetOutboundIp().String())

	for {
		// Adicione o código do servidor aqui
	}
}

func client(ip string) {
	fmt.Println("Conectando: " + ip + porta)
	conn, err := net.Dial("tcp", ip+porta)
	if err != nil {
		log.Fatal(err)
	}
	defer conn.Close()

	reader := bufio.NewReader(os.Stdin)
	for {
		fmt.Print("Digite uma mensagem: ")
		text, _ := reader.ReadString('\n')
		fmt.Fprintf(conn, text+"\n")
	}
}

func GetOutboundIp() net.IP {
	conn, err := net.Dial("udp", "8.8.8.8:80")
	if err != nil {
		log.Fatal(err)
	}
	defer conn.Close()

	localAddr := conn.LocalAddr().(*net.UDPAddr)
	return localAddr.IP
}
