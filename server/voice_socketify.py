import os
import asyncio

from socketify import App, OpCode, WebSocket, CompressOptions, AppListenOptions, AppOptions

from JsonStorage import JsonStorage

CLIENT_ID_MAX_LEN = 4
BYTEORDER = 'little'
PORT = 8081             #external: 83.26.104.147:40865 -> 8081/tcp
HOST = '0.0.0.0'


async def handle_voice(ws: WebSocket, message, clients:JsonStorage=None):
    try:
        client_id = int.from_bytes(message[:CLIENT_ID_MAX_LEN], byteorder=BYTEORDER)
        print(f'    > Client {client_id} here')

        voice_buffer = bytes()
        voice_buffer = message[CLIENT_ID_MAX_LEN:]
        print(f'    > Received buffer: {len(voice_buffer)}')

        client_exists = await clients.client_exists_async(client_id=client_id)
        if client_exists:
            await clients.update_client_async(client_id=client_id, voice=bytes(voice_buffer))
        else:
            await clients.add_client_async(client_id=client_id, voice=bytes(voice_buffer))

        ws.send('done', OpCode.TEXT)  # Send completion response
    except Exception as ex:
        print(f'    > Error here: {ex.__context__}')
        ws.end()
    finally:
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
        "message": lambda ws, msg, opcode: asyncio.create_task(handle_voice(ws, msg, clients)),
        "close": lambda ws, code, msg: print("WebSocket closed")
    })
    
    app.listen(AppListenOptions(PORT, HOST), lambda config: print(f"Listening on port {config.port}"))
    
    app.run()


if __name__ == '__main__':
    try:
        run_server()
    except Exception as ex:
        print(f"Exception occurred: {ex}")
