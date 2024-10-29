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
		conn, err := server.Accept()

		if err != nil {
			log.Fatal(err)
		}

		go read(conn)
	}
}

func read(conn net.Conn) {
	for {
		var buffer = make([]byte, 256)
		nbytes, err := conn.Read(buffer)

		if err != nil {
			log.Fatal(err)
		}

		if nbytes > 0 {
			fmt.Println(conn.RemoteAddr().String() + ">=< : " + string(buffer))
		}

	}
}

func client(ip string) {
	fmt.Println("Concetando: " + ip + porta)
	conn, err := net.Dial("tcp", ip+porta)

	if err != nil {
		log.Fatal(err)
	}

	reader := bufio.NewReader(os.Stdin)

	for {
		msg, err := reader.ReadString('\n')
		if err != nil {
			log.Fatal(err)
		}

		_, err = conn.Write([]byte(msg))

		if err != nil {
			log.Fatal(err)
		}
	}

}

func GetOutboundIp() net.IP {
	conn, err := net.Dial("udp", "8.8.8.8:80")

	if err != nil {
		log.Fatal(err)
	}

	defer conn.Close()

	localAdd := conn.LocalAddr().(*net.UDPAddr)

	return localAdd.IP

}
