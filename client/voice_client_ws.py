import asyncio
import time 

from websocket import create_connection
from websockets import connect
from AudioConverter_cl import AudioConverter


BYTEORDER = 'little'
FIXED_RESULT_LEN = 4
HOST = 'localhost'
PORT = 8083


async def run_client(client_id:str, wav_buffer:bytes) -> None:
    async with connect(f'ws://{HOST}:{PORT}/save-audio') as ws:
        for i in range(1, 960):
            time.sleep(1)
            print(i)
        # client_id_bytes = client_id.encode('utf-8')
        
        # print(f'    > Send {len(wav_buffer)}')
        # await ws.send(client_id_bytes + wav_buffer)
        # res = await ws.recv()
        # print(res.decode('utf-8'))


if __name__ == '__main__':
    client_id = 'aaaaaaaaaaaaaaaaaaaa'

    aud_conv = AudioConverter()
    wav_buf = aud_conv.wav_to_16bytes(r'C:\intern\xtts-2\voice_samples\Faib 10 wav.wav')

    asyncio.run(run_client(client_id=client_id,
                           wav_buffer=wav_buf))