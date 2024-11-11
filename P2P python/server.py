import asyncio
import websockets
import json

connected_users = {}

async def handler(websocket, path):
    async for message in websocket:
        data = json.loads(message)
        
        if data['action'] == 'register':
            connected_users[data['username']] = websocket
        elif data['action'] == 'signal':
            recipient = data['to']
            if recipient in connected_users:
                await connected_users[recipient].send(json.dumps(data['data']))
        elif data['action'] == 'unregister':
            connected_users.pop(data['username'], None)

start_server = websockets.serve(handler, "localhost", 6789)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
