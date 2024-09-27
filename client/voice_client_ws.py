import asyncio

from websockets import connect
from AudioConverter_cl import AudioConverter


BYTEORDER = 'little'
FIXED_RESULT_LEN = 4
HOST = 'localhost'
PORT = 8080
CHUNK_SIZE = 3_000


async def run_client(client_id:int, wav_buffer:bytes) -> None:
    async with connect('ws://localhost:8080/') as ws:
        client_id_bytes = client_id.to_bytes(4, byteorder=BYTEORDER)
        
        print(f'    > Send {len(wav_buffer)}')
        await ws.send(client_id_bytes + wav_buffer)
        res = await ws.recv()
        print(res)


if __name__ == '__main__':
    client_id = 1

    aud_conv = AudioConverter()
    wav_buf = aud_conv.wav_to_16bytes(r'C:\intern\xtts-2\voice_samples\Usachev 10.wav')

    asyncio.run(run_client(client_id=client_id,
                           wav_buffer=wav_buf))