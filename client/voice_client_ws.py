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
        await ws.send(client_id_bytes)

        wav_buffer_len = len(wav_buffer)
        wav_buffer_len_bytes = wav_buffer_len.to_bytes(4, byteorder=BYTEORDER)
        await ws.send(wav_buffer_len_bytes)

        for i in range(0, wav_buffer_len, CHUNK_SIZE):
            if wav_buffer_len - i < CHUNK_SIZE:
                chunk = wav_buffer[i:wav_buffer_len]
            else:
                chunk = wav_buffer[i:i+CHUNK_SIZE]
                
            await ws.send(chunk)

        res = await ws.recv()
        print(res)


if __name__ == '__main__':
    client_id = 1

    aud_conv = AudioConverter()
    wav_buf = aud_conv.wav_to_16bytes(r'C:\intern\xtts-2\voice_samples\Usachev 10.wav')

    asyncio.run(run_client(client_id=client_id,
                           wav_buffer=wav_buf))