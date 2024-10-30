import asyncio
import json
import os
import aiofiles
import time

from xtts2 import XTTS_v2
from AudioConverter_sv import AudioConverter
from JsonStorage import JsonStorage

from socketify import App, AppListenOptions, CompressOptions, WebSocket
import torch.multiprocessing  as mp

CLIENT_ID_MAX_LEN = 4
BYTEORDER = 'little'
PORT = 8083            # external: 65.93.185.202:40306
HOST = '0.0.0.0'

FILE_NAME = 'logs.txt'

ws_queues = {}
ws_results = {}
task_queue = {}
msg_count = {}

def clear_buf_files(f_paths) -> None:
    for fp in f_paths:
        if fp and os.path.isfile(fp):
            try:
                os.remove(fp)
                print(f'file {fp} removed')
            except Exception:
                print(f'file {fp} was not deleted')
    

def text_to_speech(tts_model: XTTS_v2,
                         audio_conv:AudioConverter,
                         client_id:str,
                         text: str,
                         client_voice_path: str,
                         language: str = 'en',
                         msg_id:int=0):
    print('in tts')
    result_path = os.curdir + fr'\{client_id}.wav'
    print(f'tts for {text} started')
    tts_model.run(text=text,
                  speaker_wav=client_voice_path,
                  language=language,
                  file_path=result_path)
    audio_conv.wav22_to_wav16(path_to_wav=result_path)

    with open(result_path, 'rb') as voice:
        result_voice_in_bytes = voice.read()

    clear_buf_files([result_path])
    return result_voice_in_bytes

# async def text_to_speech(tts_model: XTTS_v2,
#                          audio_conv:AudioConverter,
#                          client_id:str,
#                          text: str,
#                          client_voice_path: str,
#                          language: str = 'en'):
#     result_path = os.curdir + fr'\{client_id}.wav'
#     print(f'tts for {text} started')
#     await asyncio.to_thread(tts_model.run,
#                             text=text,
#                             speaker_wav=client_voice_path,
#                             language=language,
#                             file_path=result_path)
#     await asyncio.to_thread(audio_conv.wav22_to_wav16,
#                             path_to_wav=result_path)
#     async with aiofiles.open(result_path, 'rb') as voice:
#         result_voice_in_bytes = await voice.read()

#     await clear_buf_files([result_path])
#     return result_voice_in_bytes


# async def start_workers(tts_model, audio_conv, client_id):
#     tasks = task_queue[client_id]
#     processes = []
#     while True:
#         # Получаем данные из очереди
#         text, language, client_voice_path, msg_id = await tasks.get()
        
#         processes = [p for p in processes if p.is_alive()]

#         while len(processes) == 3:
#             await asyncio.sleep(0.5)
#             processes = [p for p in processes if p.is_alive()]

#         p = Thread(target=text_to_speech, args=(tts_model, audio_conv, client_id, text, client_voice_path, language, msg_id))
#         p.run()
#         processes.append(p)

#         tasks.task_done()


# async def process_tts_requests(client_id: str, client_voice_path:str):
#     queue = ws_queues[client_id]
#     tasks = task_queue[client_id]
    
#     while True:
#         text, language, msg_id = await queue.get()
        
#         await tasks.put((text, language, client_voice_path, msg_id))
#         queue.task_done()


# async def send_results(ws: WebSocket, client_id: str):
#     result_queue = ws_results[client_id]
#     expected_id = 0
#     buf = {}

#     while True:
#         # Получаем результат из очереди
#         msg_id, res_in_bytes = await result_queue.get()
#         print(f'RECEIVED NUMBER {msg_id}')
        
#         if msg_id == expected_id:
#             ws.send(res_in_bytes)
#             print(f"Result {len(res_in_bytes)} sent to client {client_id}, msg_id: {msg_id}")
#             expected_id += 1
#         if expected_id in buf.keys():
#             ws.send(buf[expected_id])
#             print(f"Result {len(buf[expected_id])} sent to client {client_id}, msg_id: {msg_id}")
#             expected_id += 1
#         if msg_id != expected_id and msg_id not in buf.keys():
#             buf[msg_id] = res_in_bytes

#         result_queue.task_done()


# async def handle_tts(ws: WebSocket, msg, 
#                      clients: JsonStorage = None, 
#                      tts_model: XTTS_v2 = None, 
#                      audio_conv: AudioConverter = None):
    
#     try:
#         header = json.loads(msg.decode('utf-8'))
#         client_id = header['Client_id']
#         print(f'\n\n    > CLIENT {client_id} HERE\n    > Data from client {client_id} received: {header["Text"]}, {header["Language"]}')

#         if client_id not in ws_queues.keys():
#             ws_queues[client_id] = asyncio.Queue()
#             ws_results[client_id] = asyncio.Queue()
#             task_queue[client_id] = asyncio.Queue()
#             msg_count[client_id] = 0

#             if not os.path.exists(f'cl {client_id} target_voice.wav'):
#                 client_exists = await clients.client_exists_async(client_id=client_id)
#                 if not client_exists:
#                     async with aiofiles.open('def.wav', 'rb') as file:
#                         client_voice = await file.read()
#                     await clients.add_client_async(client_id=client_id, voice=client_voice)
#                 else:
#                     client_voice = await clients.get_voice_by_client_id_async(client_id=client_id)

#                 client_voice_path = audio_conv.bytes_to_wav(audiobytes=client_voice,
#                                                             res_path=f'cl {client_id} target_voice.wav')
#             else:
#                 client_voice_path = f'cl {client_id} target_voice.wav'
#             # Запуск обработки запросов через очереди
#             asyncio.create_task(process_tts_requests(client_id=client_id, client_voice_path=client_voice_path))
#             asyncio.create_task(send_results(ws=ws, client_id=client_id))
#             asyncio.create_task(start_workers(tts_model, audio_conv, client_id))

#         msg_id = msg_count[client_id]
#         await ws_queues[client_id].put((header['Text'], header['Language'], msg_id))
#         msg_count[client_id] += 1

#     except Exception:
#         print(f'Error occured')


async def process_tts_requests(tts_model_1: XTTS_v2, 
                               tts_model_2: XTTS_v2, 
                               audio_conv: AudioConverter,
                               ws:WebSocket,
                               client_id:int,
                               client_voice_path:str):
    queue = ws_queues[client_id]
    result_queue = ws_results[client_id]

    def handle_single_tts(tts_model, text, language, msg_id):
        res_in_bytes = text_to_speech(tts_model=tts_model,
                                            text=text,
                                            client_voice_path=client_voice_path,
                                            language=language,
                                            audio_conv=audio_conv,
                                            client_id=client_id)
        res_in_bytes = res_in_bytes[44:]  # Remove WAV header
        result_queue.put((msg_id, res_in_bytes))
    
    processes = []
    while True:
        text, language, msg_id = await queue.get()
        if len(processes) < 2:
            if msg_id % 2 == 0:
                p = mp.Process(target=handle_single_tts, args=(tts_model_1, text, language, msg_id))
            else:
                p = mp.Process(target=handle_single_tts, args=(tts_model_2, text, language, msg_id))
            p.run()
            processes.append(p)
            queue.task_done()
            
        else:
            while len(processes) == 2:
                time.sleep(0.5)
                processes = [p for p in processes if p.is_active()]



async def send_results(ws: WebSocket, client_id: str):
    result_queue = ws_results[client_id]
    expected_id = 0
    buf = {}

    while True:
        msg_id, res_in_bytes = await result_queue.get()
        print(f'RECEIVED NUMBER {msg_id}')
        
        if msg_id == expected_id:
            ws.send(res_in_bytes)
            print(f"Result {len(res_in_bytes)} sent to client {client_id}, msg_id: {msg_id}")
            expected_id += 1
        if expected_id in buf.keys():
            ws.send(buf[expected_id])
            print(f"Result {len(buf[expected_id])} sent to client {client_id}, msg_id: {msg_id}")
            expected_id += 1
        if msg_id != expected_id and msg_id not in buf.keys():
            buf[msg_id] = res_in_bytes

        result_queue.task_done()


async def handle_tts(ws:WebSocket, msg, 
                     clients:JsonStorage = None, 
                     tts_model_1:XTTS_v2 = None, 
                     tts_model_2:XTTS_v2 = None,
                     audio_conv: AudioConverter = None):
                     
    try:
        header = json.loads(msg.decode('utf-8'))
        client_id = header['Client_id']
        print(f'CLIENT {client_id} HERE\nData from client {client_id} received: {header["Text"]}, {header["Language"]}')

        if client_id not in ws_queues.keys():
            ws_queues[client_id] = asyncio.Queue()
            ws_results[client_id] = asyncio.Queue()
            msg_count[client_id] = 0

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
            
            asyncio.create_task(process_tts_requests(tts_model_1, tts_model_2, audio_conv, ws, client_id, client_voice_path))
            asyncio.create_task(send_results(ws=ws, client_id=client_id))

        msg_id = msg_count[client_id]
        await ws_queues[client_id].put((header['Text'], header['Language'], msg_id))
        msg_count[client_id] += 1

    except Exception as ex:
        print(f'\n     > Error occured: {ex}')


def on_open(ws: WebSocket):
    print('\nWebSocket opened')


def on_close(ws: WebSocket, msg:str):
    print('\nWebSocket closed')


def run_server_tts():
    tts_model_1 = XTTS_v2()
    tts_model_2 = XTTS_v2()
    audio_conv = AudioConverter()

    clients_dir = 'clients'
    os.makedirs(name=clients_dir, exist_ok=True)
    clients = JsonStorage(path_to_json_dir=clients_dir)

    app = App()
    app.ws('/', {
                "compression": CompressOptions.SHARED_COMPRESSOR,
                "max_payload_length": 16 * 1024 * 1024,
                "idle_timeout": 0, 
                "open": lambda ws: on_open(ws),
                "message": lambda ws, msg, opcode: asyncio.create_task(
                        handle_tts(ws, msg, clients, tts_model_1, tts_model_2, audio_conv)),
                "close": lambda ws, code, msg: on_close(ws, msg)
            })
    app.listen(AppListenOptions(PORT, HOST), lambda config: print(f"Listening on port {config.port}"))
    app.run()


if __name__ == "__main__":
    try:
        run_server_tts()
    except Exception as ex:
        print(ex)

