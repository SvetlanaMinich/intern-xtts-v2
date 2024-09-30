import asyncio
import json
import os
import aiofiles

from socketify import App, AppListenOptions, CompressOptions, WebSocket

from AudioConverter_sv import AudioConverter
from xtts2 import XTTS_V2
from JsonStorage import JsonStorage

CLIENT_ID_MAX_LEN = 4
FIXED_HEADER_LEN = 4
BYTEORDER = 'little'
PORT = 8080
HOST = '0.0.0.0'


async def clear_buf_files(f_paths) -> None:
    for fp in f_paths:
        if fp and os.path.isfile(fp):
            await asyncio.to_thread(os.remove, fp)


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
    
    await asyncio.to_thread(audio_conv.wav24_to_wav16,
                            path_to_wav=result_path)

    async with aiofiles.open(result_path, 'rb') as voice:
        result_voice_in_bytes = await voice.read()

    await clear_buf_files([result_path])

    return result_voice_in_bytes


async def handle_tts(ws:WebSocket, msg, clients: JsonStorage, tts_model: XTTS_V2, audio_conv: AudioConverter):
    client_id = int.from_bytes(msg[:CLIENT_ID_MAX_LEN], byteorder=BYTEORDER)
    print(f'    > Client {client_id} here')

    client_exists = await clients.client_exists_async(client_id=client_id)
    if not client_exists:
        async with aiofiles.open('def.wav', 'rb') as file:
            client_voice = await file.read()
        await clients.add_client_async(client_id=client_id, voice=client_voice)
    else:
        client_voice = await clients.get_voice_by_client_id_async(client_id=client_id)

    client_voice_path = await asyncio.to_thread(audio_conv.bytes_to_wav,
                                                audiobytes=client_voice,
                                                res_path=f'cl {client_id} target_voice.wav')

    json_header = msg[CLIENT_ID_MAX_LEN:].decode('utf-8')
    header = json.loads(json_header)
    print(f"    > Data from client {client_id} received: {header['Text']}, {header['Language']}")

    # process text-to-speech
    res_in_bytes = await text_to_speech(tts_model=tts_model,
                                        audio_conv=audio_conv,
                                        text=header['Text'],
                                        client_voice_path=client_voice_path,
                                        language=header['Language'])
    
    ws.send(res_in_bytes)
    print(f"    > Result {len(res_in_bytes)} sent to client {client_id}")
    await clear_buf_files([os.getcwd() + fr'\cl {client_id} target_voice.wav'])
    ws.end()
    


def run_server() -> None:
    tts_model = XTTS_V2()
    audio_conv = AudioConverter()

    clients_dir = 'clients'
    os.makedirs(name=clients_dir, exist_ok=True)
    clients = JsonStorage(path_to_json_dir=clients_dir)


    app = App()
    app.ws('/', {
        "compression": CompressOptions.SHARED_COMPRESSOR,
        "max_payload_length": 16 * 1024 * 1024,
        "idle_timeout": 60,
        "message": lambda ws, msg, opcode: asyncio.create_task(handle_tts(ws, msg, clients, tts_model, audio_conv)),
        "close": lambda ws, code, msg: print("WebSocket closed")
    })
    
    app.listen(AppListenOptions(PORT, HOST), lambda config: print(f"Listening on port {config.port}"))
    
    app.run()



if __name__ == "__main__":
    try:
        run_server()
    except Exception as ex:
        print(f"Exception {ex} detected")
