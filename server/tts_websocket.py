import asyncio
import json
import os
import aiofiles
import functools

import socketify
import websockets
import websockets.asyncio
import websockets.asyncio.server

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
            print(f'    > Buf result file {fp} removed')


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


async def handle_tts(ws, clients: JsonStorage, tts_model: XTTS_V2, audio_conv: AudioConverter):
    client_id = await ws.recv()
    client_id = int.from_bytes(client_id, byteorder=BYTEORDER)
    print(f'    > Client {client_id} connected')

    client_exists = await clients.client_exists(client_id=client_id)
    if not client_exists:
        async with aiofiles.open('def.wav', 'rb') as file:
            client_voice = await file.read()
        await clients.add_client(client_id=client_id, voice=client_voice)
    else:
        client_voice = await clients.get_voice_by_client_id(client_id=client_id)

    client_voice_path = await asyncio.to_thread(audio_conv.bytes_to_wav,
                                                audiobytes=client_voice,
                                                res_path=f'cl {client_id} target_voice.wav')

    while True:
        # reading json-header length
        header_len = await ws.recv()
        if header_len.lower() == 'quit':
            await asyncio.to_thread(clear_buf_files,
                                    f_paths=[client_voice_path])
            break
        header_len = int.from_bytes(header_len, byteorder=BYTEORDER)

        # reading json-header
        received_header = await ws.recv()
        header = json.loads(received_header)

        # reading text content
        text = await ws.recv()
        
        print(f"    > Data from client {client_id} received: {text}, {header['Language']}")

        # process text-to-speech
        res_in_bytes = await text_to_speech(tts_model=tts_model,
                                            audio_conv=audio_conv,
                                            text=text,
                                            client_voice_path=client_voice_path,
                                            language=header['Language'])

        # sending result to the client
        res_in_bytes_len = len(res_in_bytes)
        await ws.send(res_in_bytes_len.to_bytes(4, byteorder=BYTEORDER))

        for i in range(0, res_in_bytes_len, CHUNK_SIZE):
            chunk = res_in_bytes[i:i + CHUNK_SIZE]
            await ws.send(chunk)

        print(f"    > Result sent to client {client_id}")

    print(f'    > Client {client_id} closed')


async def run_socketify_server(host:str = HOST, port: int = PORT) -> None:
    tts_model = XTTS_V2()
    audio_conv = AudioConverter()

    clients_dir = 'clients'
    os.makedirs(name=clients_dir, exist_ok=True)
    clients = JsonStorage(path_to_json_dir=clients_dir)

    handler = functools.partial(handle_tts, 
                                clients=clients,
                                tts_model=tts_model,
                                audio_conv=audio_conv)
    
    async with websockets.asyncio.server.serve(handler, host, port):
        await asyncio.get_running_loop().create_future()  # run forever

    # async def tts_handler(ws):
    #     await handle_tts(ws, clients, tts_model, audio_conv)

    # app.ws('/', {
    #     'compression': socketify.CompressOptions.SHARED_COMPRESSOR,
    #     'max_payload_length': 16 * 1024 * 1024,
    #     'idle_timeout': 12,
    #     'open': tts_handler
    # })

    # app.listen(socketify.AppListenOptions(port=port, host="0.0.0.0"),
    #            lambda config: print(f"Listening on 0.0.0.0:{config.port}..."))

    # await asyncio.Event().wait()  # To keep the asyncio loop running


if __name__ == "__main__":
    try:
        asyncio.run(run_socketify_server())
    except Exception as ex:
        print(f"Exception {ex} detected")
