import asyncio
import websockets

async def response(websocket, path):
    message = await websocket.recv()
    print("Message received: {message}")
    await websocket.send("I got ur message")
    
start_server = websockets.serve(response, 'localhost', 1234)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()