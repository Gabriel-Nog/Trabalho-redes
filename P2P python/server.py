import asyncio
import websockets
import socket
import threading

PORT = 8765  # Porta para WebSocket
connected_clients = set()  # Para armazenar conexões de clientes

# Cifra de César para criptografar/descriptografar as mensagens
def caesar_cipher(text, shift):
    result = []
    for char in text:
        result.append(chr((ord(char) + shift) % 256))
    return ''.join(result)

def caesar_decipher(text, shift):
    return caesar_cipher(text, -shift)

# Função para lidar com a comunicação entre os clientes
async def handler(websocket, path):
    connected_clients.add(websocket)
    try:
        async for message in websocket:
            decrypted_message = caesar_decipher(message, 3)
            print(f"Received: {decrypted_message}")
            
            # Envia a mensagem cifrada para todos os outros clientes conectados
            for client in connected_clients:
                if client != websocket:
                    encrypted_message = caesar_cipher(decrypted_message, 3)
                    await client.send(encrypted_message)
    finally:
        connected_clients.remove(websocket)

# Função para iniciar o servidor WebSocket (escutando por conexões de outros clientes)
async def start_server():
    server = await websockets.serve(handler, "0.0.0.0", PORT)
    print(f"Servidor WebSocket iniciado em ws://0.0.0.0:{PORT}")
    await server.wait_closed()  # Mantém o servidor ativo aguardando conexões

# Função para o cliente se conectar a outro cliente (como cliente WebSocket)
async def start_client(ip):
    uri = f"ws://{ip}:{PORT}"
    try:
        async with websockets.connect(uri) as websocket:
            print(f"Conectado ao servidor WebSocket em {uri}")
            while True:
                # A mensagem é recebida de qualquer cliente e enviada automaticamente
                response = await websocket.recv()
                print(f"Mensagem recebida: {caesar_decipher(response, 3)}")
    except Exception as e:
        print(f"Erro ao conectar: {e}")

# Função para obter o IP local (útil para exibir ao usuário)
def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        s.connect(('10.254.254.254', 1))  # Não precisa ser um IP válido
        local_ip = s.getsockname()[0]
    except Exception:
        local_ip = '127.0.0.1'
    finally:
        s.close()
    return local_ip

# Função para iniciar a conexão P2P entre dois clientes
def start_p2p_connection(ip):
    loop = asyncio.get_event_loop()
    
    # Iniciar o servidor WebSocket para o cliente
    server_thread = threading.Thread(target=lambda: loop.run_until_complete(start_server()))
    server_thread.daemon = True  # A thread será encerrada quando o programa terminar
    server_thread.start()
    
    # Iniciar a conexão com o outro cliente (cliente WebSocket)
    loop.run_until_complete(start_client(ip))

if __name__ == "__main__":
    local_ip = get_local_ip()
    print(f"Seu IP local é: {local_ip}")

    # Aqui, o IP do outro cliente será passado pela interface HTML
    pass  # A interação com o terminal foi removida, pois será controlada pela interface HTML

    # A execução do loop principal é garantida com `loop.run_forever()`
    asyncio.get_event_loop().run_forever()
# async def main():
#     local_ip = get_local_ip()
#     print(f"Seu IP local é: {local_ip}")

#     # Aqui, o IP do outro cliente será passado pela interface HTML
#     pass  # A interação com o terminal foi removida, pois será controlada pela interface HTML

#     # Substitua esta parte pelo seu código assíncrono, se houver.
#     await asyncio.sleep(1)  # Exemplo de tarefa assíncrona

# if __name__ == "__main__":
#     asyncio.run(main())
