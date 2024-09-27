import asyncio
import json
import os
import aiofiles
import functools

from AudioConverter_sv import AudioConverter
from xtts2 import XTTS_V2
from JsonStorage import JsonStorage

CLIENT_ID_MAX_LEN = 4
FIXED_HEADER_LEN = 4
BYTEORDER = 'little'
PORT = 8080
HOST = '0.0.0.0'
CHUNK_SIZE = 3000


async def clear_buf_files(f_paths) -> None:
    for fp in f_paths:
        if fp and os.path.isfile(fp):
            await asyncio.to_thread(os.remove, fp)
            print(f'Buf result file {fp} removed')


async def text_to_speech(tts_model: XTTS_V2,
                         audio_conv: AudioConverter,
                         text: str,
                         client_voice_path: str,
                         language: str = 'en'):
    
    result_path = os.curdir + fr'\{text[:15]}.wav'
    
    await asyncio.to_thread(tts_model.run,
                            text,
                            client_voice_path,
                            language,
                            result_path)
    
    await asyncio.to_thread(audio_conv.wav24_to_wav16, path_to_wav=result_path)

    async with aiofiles.open(result_path, 'rb') as voice:
        result_voice_in_bytes = await voice.read()

    await clear_buf_files([result_path])

    return result_voice_in_bytes


async def handle_tts(reader:asyncio.StreamReader, 
                     writer:asyncio.StreamWriter,
                     clients:JsonStorage,
                     tts_model:XTTS_V2,
                     audio_conv:AudioConverter):
    
    client_addr = writer.get_extra_info('peername')

    client_id = await reader.read(CLIENT_ID_MAX_LEN)
    client_id = int.from_bytes(client_id, byteorder=BYTEORDER)
    print(f'Client {client_id} here')

    client_exists = await clients.client_exists(client_id=client_id)
    if not client_exists:
        async with aiofiles.open('server/def.wav', 'rb') as file:
            client_voice_start = await file.read()

        await clients.add_client(client_id=client_id,
                                 voice=client_voice_start)
    else:
        client_voice_start = await clients.get_voice_by_client_id(client_id=client_id)
    

    client_voice_path = await asyncio.to_thread(audio_conv.bytes_to_wav,
                                                audiobytes=client_voice_start,
                                                res_path=f'cl {client_id} target_voice.wav')
    
    while True:
        # reading json-header len
        header_len = await reader.read(FIXED_HEADER_LEN)
        try:
            check_text = header_len.decode('utf-8')
            if check_text.lower() == 'quit':
                break
            else:
                header_len = int.from_bytes(header_len, byteorder=BYTEORDER)
        except Exception:
            try: 
                header_len = int.from_bytes(header_len, byteorder=BYTEORDER)
            except Exception as ex:
                print(ex)
                continue
        
        # reading descr json-header
        received_header = await reader.read(header_len)
        json_header = received_header.decode('utf-8')
        print(json_header)
        header = json.loads(json_header)

        # reading content
        data_to_proceed = dict()
        text_len = header['Length_text']

        received_text = await reader.read(text_len)
        data_to_proceed['text'] = received_text.decode(header['Encoding'])

        print(f'Data from client {client_id} from {client_addr} received')
        
        client_voice = await clients.get_voice_by_client_id(client_id=client_id)
        if client_voice != client_voice_start:
            client_voice_path = await asyncio.to_thread(audio_conv.bytes_to_wav,
                                                        audiobytes=client_voice_start,
                                                        res_path=f'cl {client_id} target_voice.wav')
            print(f'Clients {client_id} voice changed')

        res_in_bytes = await text_to_speech(tts_model=tts_model,
                                            audio_conv=audio_conv,
                                            text=data_to_proceed['text'],
                                            client_voice_path=client_voice_path,
                                            language=header['Language'])
        
        # return size of result bytes:
        res_in_bytes_len = len(res_in_bytes)
        writer.write(res_in_bytes_len.to_bytes(4, byteorder=BYTEORDER)) 
        await writer.drain()
        print(f'\n\nResult bin_file len for client {client_id} is {res_in_bytes_len}\n\n')

        chunk_size = 3000
        for i in range(0, res_in_bytes_len, chunk_size):
            if res_in_bytes_len - i < chunk_size:
                chunk = res_in_bytes[i:res_in_bytes_len]
            else:
                chunk = res_in_bytes[i:i+chunk_size]
            writer.write(chunk)
            await writer.drain()

        print(f'Result bin_file {len(chunk)} for client {client_id} is sent\n\n')

    writer.close()
    await writer.wait_closed()
    await clear_buf_files([client_voice_path])
    print(f'Client {client_id} closed')


async def run_server(host:str=HOST, port:int=PORT) -> None:
    tts_model = XTTS_V2()
    audio_conv = AudioConverter()

    clients_dir = 'clients'
    os.makedirs(name=clients_dir,
                exist_ok=True)
    
    clients = JsonStorage(path_to_json_dir=clients_dir)
    
    handle_tts_with_params = functools.partial(handle_tts, 
                                               clients=clients, 
                                               tts_model=tts_model,
                                               audio_conv=audio_conv)
    
    server = await asyncio.start_server(client_connected_cb=handle_tts_with_params,
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