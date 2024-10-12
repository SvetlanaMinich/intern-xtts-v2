import asyncio
import json
import numpy as np
import scipy.io.wavfile as wavfile
import io
import time

from mms_tts import MmsModels

from socketify import App, AppListenOptions, CompressOptions, WebSocket

PORT = 8081            # external: 65.93.185.202:40306
HOST = '0.0.0.0'

ws_queues = {}

async def text_to_speech(tts: MmsModels,
                         text: str,
                         language: str = 'eng'):

# English            eng
# Urdu (script arab) urd
# Arabic             ara
# German             deu
# Russian            rus
# Hindi              hin
    func_name = f'tts_{language}'
    tts_func = getattr(tts, func_name, None)
    
    if not tts_func:
        try:
            func_name = tts.load_model(lang=language)
            tts_func = getattr(tts, func_name, None)
        except Exception:
            print(f'Cannot download model for {language} language')
            return
        
    result_ndarray = tts_func(text=text)    
    sample_rate = 16000  # Target sample rate (Hz)
    result_scaled = np.int16(result_ndarray * 32767)
    wav_buffer = io.BytesIO()
    wavfile.write(wav_buffer, sample_rate, result_scaled)
        
    return wav_buffer.getvalue()


async def process_tts_requests(tts: MmsModels,
                               ws: WebSocket,
                               client_id: str):
    while True:
        queue = ws_queues[client_id]
        # Wait for a request from the queue
        text, language, client_id = await queue.get()

        start = time.time()
        sens = text.split('.')
        for sen in sens:
            if len(sen) == 0:
                continue
            sen = sen.strip().rstrip()
            res_in_bytes = await text_to_speech(tts=tts,
                                                text=sen,
                                                language=language)
            res_in_bytes = res_in_bytes[44:]
            ws.send(res_in_bytes)     
            print(f"Result {len(res_in_bytes)} sent to client {client_id}")
        print(f'    > {time.time() - start}: {text}')
        queue.task_done()  # Indicate that the task is done


async def handle_tts(ws:WebSocket, 
                     msg, 
                     tts:MmsModels):               
    try:
        header = json.loads(msg.decode('utf-8'))
        client_id = header['Client_id']
        print(f'CLIENT {client_id} HERE\nData from client {client_id} received: {header["Text"]}, {header["Language"]}')

        if client_id not in ws_queues.keys():
            ws_queues[client_id] = asyncio.Queue()

            # Start processing TTS requests for this client in a separate task
            asyncio.create_task(process_tts_requests(tts=tts, ws=ws, client_id=client_id))

        await ws_queues[client_id].put((header['Text'], header['Language'], client_id))

    except Exception as ex:
        print(f'     > Error occured: {ex}')


def on_open(ws: WebSocket):
    print('WebSocket opened')


def on_close(ws: WebSocket):
    print('WebSocket closed')


def run_server_tts():
    tts = MmsModels()
    print('tts model done')
    
    app = App()
    app.ws('/', {
                "compression": CompressOptions.SHARED_COMPRESSOR,
                "max_payload_length": 16 * 1024 * 1024,
                "idle_timeout": 0, 
                "open": lambda ws: on_open(ws),
                "message": lambda ws, msg, opcode: asyncio.create_task(
                        handle_tts(ws, msg, tts)),
                "close": lambda ws, code, msg: on_close(ws)
            })
    app.listen(AppListenOptions(PORT, HOST), lambda config: print(f"Listening on port {config.port}"))
    app.run()


if __name__ == "__main__":
    try:
        run_server_tts()
    except Exception as ex:
        print(ex)

