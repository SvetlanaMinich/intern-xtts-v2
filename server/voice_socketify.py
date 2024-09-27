import asyncio
import os
import functools

import websockets 

from socketify import App, OpCode, WebSocket, CompressOptions, AppListenOptions
import websockets.asyncio
import websockets.asyncio.server

from JsonStorage import JsonStorage

CLIENT_ID_MAX_LEN = 4
FIXED_HEADER_LEN = 4
BYTEORDER = 'little'
PORT = 8080
HOST = '0.0.0.0'
CHUNK_SIZE = 3000


def handle_voice(ws: WebSocket, message, clients:JsonStorage=None):
    client_id = int.from_bytes(message[:CLIENT_ID_MAX_LEN], byteorder=BYTEORDER)
    print(f'    > Client {client_id} here')

    voice_buffer_len = int.from_bytes(message[CLIENT_ID_MAX_LEN:CLIENT_ID_MAX_LEN + 4], byteorder=BYTEORDER)
    print(f'    > Must receive {voice_buffer_len} bytes')

    voice_buffer = bytes()
    voice_buffer = message[CLIENT_ID_MAX_LEN+4:]

    client_exists = clients.client_exists(client_id=client_id)
    if client_exists:
        clients.update_client(client_id=client_id, voice=bytes(voice_buffer))
    else:
        clients.add_client(client_id=client_id, voice=bytes(voice_buffer))

    ws.send('done', OpCode.TEXT)  # Send completion response
    ws.end()


def run_server():
    clients_dir = 'clients'
    os.makedirs(clients_dir, exist_ok=True)
    clients = JsonStorage(path_to_json_dir=clients_dir)

    app = App()
    app.ws('/', {
        "compression": CompressOptions.SHARED_COMPRESSOR,
        "max_payload_length": 16 * 1024 * 1024,
        "idle_timeout": 60,
        "message": lambda ws, msg, opcode: handle_voice(ws, msg, clients),
        "close": lambda ws, code, msg: print("WebSocket closed")
    })
    
    app.listen(AppListenOptions(PORT, HOST), lambda config: print(f"Listening on port {config.port}"))
    
    app.run()


if __name__ == '__main__':
    try:
        run_server()
    except Exception as ex:
        print(f"Exception occurred: {ex}")
