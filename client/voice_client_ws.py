import asyncio

from websockets import connect
from AudioConverter_cl import AudioConverter


BYTEORDER = 'little'
FIXED_RESULT_LEN = 4
HOST = '213.108.196.111'
PORT = 46965


# 213.108.196.111:46965 -> 8081/tcp


async def run_client(client_id:int, wav_buffer:bytes) -> None:
    async with connect(f'ws://{HOST}:{PORT}') as ws:
        client_id_bytes = client_id.to_bytes(4, byteorder=BYTEORDER)
        
        print(f'    > Send {len(wav_buffer)}')
        await ws.send(client_id_bytes + wav_buffer)
        res = await ws.recv()
        print(res)


if __name__ == '__main__':
    client_id = 11

    aud_conv = AudioConverter()
    wav_buf = aud_conv.wav_to_16bytes(r'C:\intern\xtts-2\voice_samples\Faib 10 wav.wav')

    asyncio.run(run_client(client_id=client_id,
                           wav_buffer=wav_buf))