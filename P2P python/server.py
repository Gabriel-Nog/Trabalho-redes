import asyncio
import websockets

connected_clients = set()

def caesar_cipher(text, shift):
    result = ""
    for char in text:
        if char.isalpha():
            shift_amount = 65 if char.isupper() else 97
            result += chr((ord(char) + shift - shift_amount) % 26 + shift_amount)
        else:
            result += char
    return result

def caesar_decipher(text, shift):
    return caesar_cipher(text, -shift)

async def handler(websocket, path):
    connected_clients.add(websocket)
    try:
        async for message in websocket:
            decrypted_message = caesar_decipher(message, 3)
            print(f"Received: {decrypted_message}")
            for client in connected_clients:
                if client != websocket:
                    encrypted_message = caesar_cipher(decrypted_message, 3)
                    await client.send(encrypted_message)
    finally:
        connected_clients.remove(websocket)

start_server = websockets.serve(handler, "0.0.0.0", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()