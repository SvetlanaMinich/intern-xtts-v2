import asyncio
import os
import functools

from JsonStorage import JsonStorage

CLIENT_ID_MAX_LEN = 4
FIXED_HEADER_LEN = 4
BYTEORDER = 'little'
PORT = 8080
HOST = '0.0.0.0'
CHUNK_SIZE = 3000


async def handle_voice(reader:asyncio.StreamReader, 
                       writer:asyncio.StreamWriter,
                       clients:JsonStorage):
    
    client_id = await reader.read(CLIENT_ID_MAX_LEN)
    client_id = int.from_bytes(client_id, byteorder=BYTEORDER)
    print(f'Client {client_id} here')

    voice_buffer_len = await reader.read(4)
    voice_buffer_len = int.from_bytes(voice_buffer_len, byteorder=BYTEORDER)
    print(f'must receive {voice_buffer_len}')

    voice_buffer = bytes()
        
    while len(voice_buffer) < voice_buffer_len:
        received_chunk = await reader.read(CHUNK_SIZE)
        voice_buffer += received_chunk
        print(len(voice_buffer))

    print(f'Received {len(voice_buffer)} bytes of voice') 


    client_exists = await clients.client_exists(client_id=client_id)
    if client_exists:
        await clients.update_client(client_id=client_id,
                                    voice=voice_buffer)
    else:
        await clients.add_client(client_id=client_id,
                                 voice=voice_buffer)
        
    writer.write('done'.encode('utf-8'))
    await writer.drain()
        
    writer.close()
    await writer.wait_closed()
    print(f'Client {client_id} closed')


async def run_server(host:str=HOST, port:int=PORT) -> None:
    clients_dir = 'clients'
    os.makedirs(name=clients_dir,
                exist_ok=True)
    
    clients = JsonStorage(path_to_json_dir=clients_dir)
    
    handle_voice_with_params = functools.partial(handle_voice, 
                                               clients=clients)
    
    server = await asyncio.start_server(client_connected_cb=handle_voice_with_params,
                                        host=host,
                                        port=port)
    
    async with server:
        print(f'Server listening on {host}:{port}')
        try:
            await server.serve_forever()
        except Exception as ex:
            print(f'\n\nException {ex} detected')
        finally:
            server.close()
            await server.wait_closed()
            print('Server closed')


if __name__ == '__main__':
    try:
        asyncio.run(run_server())
    except Exception as ex:
        print(f'\nException {ex} detected')        