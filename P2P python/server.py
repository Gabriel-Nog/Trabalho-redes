import asyncio
import websockets
import socket

PORT = 8765  # Porta para WebSocket
connected_clients = set()  # Para armazenar conexões de clientes

# Cifra de César para criptografar/descriptografar as mensagens
def caesar_cipher(text, shift):
    result = []
    for char in text:
        result.append(chr((ord(char) + shift) % 256))  # Criptografa com mod 256 para garantir que seja um byte válido
    return ''.join(result)

def caesar_decipher(text, shift):
    return caesar_cipher(text, -shift)

# Função para lidar com a comunicação entre os clientes
async def handler(websocket, path):
    connected_clients.add(websocket)
    try:
        async for message in websocket:
            # Descriptografa a mensagem recebida
            decrypted_message = caesar_decipher(message, 3)
            print(f"Recebido: {decrypted_message}")

            # Envia a mensagem cifrada para todos os outros clientes conectados
            for client in connected_clients:
                if client != websocket:  # Não envie a mensagem de volta para o próprio cliente
                    encrypted_message = caesar_cipher(decrypted_message, 3)  # Cifra a mensagem novamente
                    await client.send(encrypted_message)
    finally:
        connected_clients.remove(websocket)

# Função para iniciar o servidor WebSocket (escutando por conexões de outros clientes)
async def start_server():
    server = await websockets.serve(handler, "0.0.0.0", PORT)
    print(f"Servidor WebSocket iniciado em ws://0.0.0.0:{PORT}")
    await server.wait_closed()  # Mantém o servidor ativo aguardando conexões

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

# Inicia o servidor WebSocket
if __name__ == "__main__":
    local_ip = get_local_ip()
    print(f"IP local do servidor: {local_ip}")
    asyncio.get_event_loop().run_until_complete(start_server())
    asyncio.get_event_loop().run_forever()