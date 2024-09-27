import asyncio
import os
import functools

import websockets 

from socketify import App, AppListenOptions, OpCode, CompressOptions, WebSocket
import websockets.asyncio
import websockets.asyncio.server

from JsonStorage import JsonStorage

CLIENT_ID_MAX_LEN = 4
FIXED_HEADER_LEN = 4
BYTEORDER = 'little'
PORT = 8080
HOST = '0.0.0.0'
CHUNK_SIZE = 3000


async def handle_voice_async(ws, clients:JsonStorage=None):
    client_id = await ws.recv()
    client_id = int.from_bytes(client_id, byteorder=BYTEORDER)
    print(f'    > Client {client_id} here')

    voice_buffer_len = await ws.recv()
    voice_buffer_len = int.from_bytes(voice_buffer_len, byteorder=BYTEORDER)
    print(f'    > Must receive {voice_buffer_len}')

    voice_buffer = bytes()
        
    while len(voice_buffer) < voice_buffer_len:
        received_chunk = await ws.recv()
        voice_buffer += received_chunk
        print(len(voice_buffer))

    print(f'    > Received {len(voice_buffer)} bytes of voice') 

    client_exists = await clients.client_exists(client_id=client_id)
    if client_exists:
        await clients.update_client(client_id=client_id,
                                    voice=voice_buffer)
    else:
        await clients.add_client(client_id=client_id,
                                 voice=voice_buffer)

    await ws.send('done')



async def run_server(host:str=HOST, port:int=PORT) -> None:
    clients_dir = 'clients'
    os.makedirs(name=clients_dir,
                exist_ok=True)
    clients = JsonStorage(path_to_json_dir=clients_dir)

    handler = functools.partial(handle_voice_async, 
                                clients=clients)
    
    async with websockets.asyncio.server.serve(handler, host, port):
        await asyncio.get_running_loop().create_future()  # run forever


if __name__ == '__main__':
    try:
        asyncio.run(run_server())
    except Exception as ex:
        print(f'\nException {ex} detected')        