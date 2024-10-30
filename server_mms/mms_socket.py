import asyncio
import json
import time
import numpy as np

import io
import soundfile as sf
import base64 

import GPUtil

from mms_tts import MmsModels

from socketify import App, AppListenOptions, CompressOptions, WebSocket, OpCode

PORT = 8081 
HOST = '0.0.0.0'
DEVICES = ['cuda:0']

ws_count = 0

ws_queues = {}
ws_results = {}
msg_count = {}
client_params = {}

websocket_instances = {}


async def get_least_loaded_device():
        gpus = GPUtil.getGPUs()
        load = {gpu.id: gpu.load for gpu in gpus}

        least_loaded_device = min(load, key=load.get)
        return least_loaded_device


async def text_to_speech(tts: MmsModels,
                         text: str,
                         msg_id: int,
                         client_id: str,
                         request_id: str,
                         language: str = 'eng'):
    result_queue = ws_results[client_id]

    start = time.time()
    func_name = f'tts_{language}'
    tts_func = getattr(tts, func_name, None)
    
    device_id = await get_least_loaded_device()
    print(device_id)

    if language in ['eng', 'deu', 'hin']:
        params = client_params[client_id]
        result_array = tts_func(text=text, device=f"cuda:{device_id}", gpt_cond_latent=params[0], speaker_embedding=params[1]) 
    else:
        result_array = tts_func(text=text, device=f"cuda:{device_id}") 

    sample_rate = 16000
    result_scaled = np.int16(result_array * 32767)
    wav_buffer = io.BytesIO()
    sf.write(wav_buffer, result_scaled, 16000, format='WAV')
    wav_bytes = wav_buffer.getvalue()

    print(f'    > Time: {time.time() - start}')
    wav_bytes = wav_bytes[44:]
    await result_queue.put((msg_id, wav_bytes, request_id))

    num_samples = len(result_scaled)
    duration_seconds = (num_samples / sample_rate) * 1000
    print('     > duration:', duration_seconds)

    return wav_bytes 


async def process_tts_requests(tts: MmsModels,
                               ws: WebSocket,
                               client_id: str):
    queue = ws_queues[client_id]
    while True:
        # Wait for a request from the queue
        text, language, request_id, msg_id = await queue.get()

        await text_to_speech(tts=tts,
                             text=text,
                             language=language,
                             msg_id=msg_id,
                             client_id=client_id,
                             request_id=request_id)

        queue.task_done() 


async def send_results(ws: WebSocket, client_id: str):
    result_queue = ws_results[client_id]
    expected_id = 0
    buf = {}

    while True:
        msg_id, res_in_bytes, request_id = await result_queue.get()
        print(f'RECEIVED NUMBER {msg_id}')

        result = {
            "RequestId": request_id,
            "Audio": base64.b64encode(res_in_bytes).decode('utf-8')
        }

        if msg_id == expected_id:
            if ws.ws not in websocket_instances:
                break
            ws.send(result)
            print(f"Result {len(result['Audio'])} sent to client {client_id}, msg_id: {msg_id}")
            expected_id += 1
        if expected_id in buf.keys():
            if ws.ws not in websocket_instances:
                break
            ws.send(buf[expected_id])
            print(f"Result {len(buf[expected_id]['Audio'])} sent to client {client_id}, msg_id: {msg_id}")
            expected_id += 1
        if msg_id != expected_id and msg_id not in buf.keys():
            buf[msg_id] = result

        result_queue.task_done()
        
            

async def handle_tts(ws:WebSocket, 
                     msg, 
                     tts:MmsModels):               
    try:
        header = json.loads(msg.decode('utf-8'))
        client_id = header['ClientId']
        request_id = header['RequestId']
        print(f'CLIENT {client_id} HERE\nData from client {client_id} received: {header["Text"]}, {header["Language"]}')

        if client_id not in ws_queues.keys():
            websocket_instances[ws.ws] = client_id
            ws_queues[client_id] = asyncio.Queue()
            ws_results[client_id] = asyncio.Queue()
            msg_count[client_id] = 0
            client_params[client_id] = tts.get_latents()

            asyncio.create_task(process_tts_requests(tts=tts, ws=ws, client_id=client_id))
            asyncio.create_task(send_results(ws=ws, client_id=client_id))

        msg_id = msg_count[client_id]
        await ws_queues[client_id].put((header['Text'], header['Language'], request_id, msg_id))
        msg_count[client_id] += 1

    except Exception as ex:
        print(f'     > Error occured: {ex}')


def on_open(ws: WebSocket):
    websocket_instances[ws.ws] = ''
    print(f"WebSocket {ws.ws} opened")


def on_close(ws: WebSocket, code, msg):
    if ws.ws in websocket_instances.keys():
        client_id = websocket_instances.pop(ws.ws)
        ws_results.pop(client_id)
        msg_count.pop(client_id)
        ws_queues.pop(client_id)
        print(f"Client {client_id} removed")
        print(f"WebSocket {ws.ws} closed")
    else:
        print('WebSocket closed, but not in storage')


def run_server_tts():
    tts = MmsModels(devices=DEVICES)
    
    app = App()
    app.ws('/', {
                "compression": CompressOptions.SHARED_COMPRESSOR,
                "max_payload_length": 16 * 1024 * 1024,
                "idle_timeout": 960, 
                "open": on_open,
                "message": lambda ws, msg, opcode: asyncio.create_task(
                        handle_tts(ws, msg, tts)),
                "close": on_close
            })
    app.listen(AppListenOptions(PORT, HOST), lambda config: print(f"Listening on port {config.port}"))
    app.run()


if __name__ == "__main__":
    try:
        run_server_tts()
    except Exception as ex:
        print(ex)

