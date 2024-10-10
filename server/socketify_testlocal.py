import asyncio
import json
import os
import aiofiles
from concurrent.futures import ProcessPoolExecutor

from xtts2 import XTTS_v2
from AudioConverter_sv import AudioConverter
from JsonStorage import JsonStorage

from socketify import App, AppListenOptions, CompressOptions, WebSocket

CLIENT_ID_MAX_LEN = 4
BYTEORDER = 'little'
PORT = 8083            # external: 65.93.185.202:40306
HOST = '0.0.0.0'

FILE_NAME = 'logs.txt'

ws_queues = {}

async def clear_buf_files(f_paths) -> None:
    for fp in f_paths:
        if fp and os.path.isfile(fp):
            try:
                await asyncio.to_thread(os.remove, fp)
                async with aiofiles.open(FILE_NAME, 'a') as f:
                    await f.write(f'\n     > file {fp} removed')
            except Exception:
                async with aiofiles.open(FILE_NAME, 'a') as f:
                    await f.write(f'\n    > file {fp} was not deleted')


async def text_to_speech(tts_model: XTTS_v2,
                         audio_conv:AudioConverter,
                         client_id:str,
                         text: str,
                         client_voice_path: str,
                         language: str = 'en'):

    result_path = os.curdir + fr'\{client_id}.wav'

    await asyncio.to_thread(tts_model.run,
                            text=text,
                            speaker_wav=client_voice_path,
                            language=language,
                            file_path=result_path)
    
    audio_conv.wav24_to_wav16(path_to_wav=result_path)

    async with aiofiles.open(result_path, 'rb') as voice:
        result_voice_in_bytes = await voice.read()

    await clear_buf_files([result_path])
    return result_voice_in_bytes


async def process_tts_requests(tts_model: XTTS_v2, 
                               audio_conv: AudioConverter,
                               ws:WebSocket,
                               client_id:int,
                               client_voice_path:str):
    while True:
        queue = ws_queues[client_id]
        # Wait for a request from the queue
        text, language, client_id = await queue.get()

        async with aiofiles.open(FILE_NAME, 'a') as f:
            await f.write(f'\n     Task started: {text}')
        
        sens = text.split('.')
        for sen in sens:
            if len(sen) == 0:
                continue
            sen = sen.strip().rstrip()
            res_in_bytes = await text_to_speech(tts_model=tts_model,
                                                text=sen,
                                                client_voice_path=client_voice_path,
                                                language=language,
                                                audio_conv=audio_conv,
                                                client_id=client_id)
            # res_in_bytes = res_in_bytes[44:]
            ws.send(res_in_bytes)

            # if ws.get_remote_address() is not None: # work only with different machines
            #     ws.send(res_in_bytes)
            # else:
            #     async with aiofiles.open(FILE_NAME, 'a') as f:
            #         await f.write(f"\n    > WebSocket closed")
            #     break            
        
        async with aiofiles.open(FILE_NAME, 'a') as f:
            await f.write(f"\n    > Result {len(res_in_bytes)} sent to client {client_id}")

        # await asyncio.sleep(0.1)

        queue.task_done()  # Indicate that the task is done


async def handle_tts(ws:WebSocket, msg, 
                     clients:JsonStorage = None, 
                     tts_model:XTTS_v2 = None, 
                     audio_conv: AudioConverter = None):
                     
    try:
        header = json.loads(msg.decode('utf-8'))
        client_id = header['Client_id']
        async with aiofiles.open(FILE_NAME, 'a') as f:
            await f.write(f'\n\n    > CLIENT {client_id} HERE\n    > Data from client {client_id} received: {header["Text"]}, {header["Language"]}')

        if client_id not in ws_queues.keys():
            ws_queues[client_id] = asyncio.Queue()

            if not os.path.exists(f'cl {client_id} target_voice.wav'):
                client_exists = await clients.client_exists_async(client_id=client_id)
                if not client_exists:
                    async with aiofiles.open('def.wav', 'rb') as file:
                        client_voice = await file.read()
                    await clients.add_client_async(client_id=client_id, voice=client_voice)
                else:
                    client_voice = await clients.get_voice_by_client_id_async(client_id=client_id)

                client_voice_path = audio_conv.bytes_to_wav(audiobytes=client_voice,
                                                            res_path=f'cl {client_id} target_voice.wav')
            else:
                client_voice_path = f'cl {client_id} target_voice.wav'
            # Start processing TTS requests for this client in a separate task
            asyncio.create_task(process_tts_requests(tts_model, audio_conv, ws, client_id, client_voice_path))

        await ws_queues[client_id].put((header['Text'], header['Language'], client_id))

    except Exception as ex:
        async with aiofiles.open(FILE_NAME, 'a') as f:
            await f.write(f'\n     > Error occured: {ex}')


def handle_tts_sync(ws:WebSocket, msg, 
               clients:JsonStorage = None, 
               tts_model:XTTS_v2 = None, 
               audio_conv: AudioConverter = None):
                     
    try:
        header = json.loads(msg.decode('utf-8'))
        client_id = header['Client_id']
        
        if client_id not in ws_queues.keys():
            ws_queues[client_id] = asyncio.Queue()

            if not os.path.exists(f'cl {client_id} target_voice.wav'):
                with open('def.wav', 'rb') as file:
                    client_voice = file.read()
                client_voice_path = audio_conv.bytes_to_wav(audiobytes=client_voice,
                                                            res_path=f'cl {client_id} target_voice.wav')
            else:
                client_voice_path = f'cl {client_id} target_voice.wav'
            # Start processing TTS requests for this client in a separate task
            asyncio.create_task(process_tts_requests(tts_model, audio_conv, ws, client_id, client_voice_path))

        ws_queues[client_id].put((header['Text'], header['Language'], client_id))

    except Exception as ex:
        print(f'\n     > Error occured: {ex}')


def on_open(ws: WebSocket):
    with open(FILE_NAME, 'a') as f:
        f.write('\nWebSocket opened')


def on_close(ws: WebSocket, msg:str):
    print('closed:', ws.get_remote_address())
    with open(FILE_NAME, 'a') as f:
        f.write('\nWebSocket closed')


def run_server_tts():
    tts_model = XTTS_v2()
    audio_conv = AudioConverter()

    clients_dir = 'clients'
    os.makedirs(name=clients_dir, exist_ok=True)
    clients = JsonStorage(path_to_json_dir=clients_dir)

    with ProcessPoolExecutor(max_workers=10) as executor:
        app = App()
        app.ws('/', {
                "compression": CompressOptions.SHARED_COMPRESSOR,
                "max_payload_length": 16 * 1024 * 1024,
                "idle_timeout": 0, 
                "open": lambda ws: on_open(ws),
                "message": lambda ws, msg, opcode: executor.submit(
                    asyncio.create_task(
                        handle_tts(ws, msg, clients, tts_model, audio_conv))),
                "close": lambda ws, code, msg: on_close(ws, msg)
            })
        app.listen(AppListenOptions(PORT, HOST), lambda config: print(f"Listening on port {config.port}"))
        app.run()


if __name__ == "__main__":
    try:
        run_server_tts()
    except Exception as ex:
        print(ex)

