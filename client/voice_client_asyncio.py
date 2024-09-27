import asyncio
from AudioConverter_cl import AudioConverter


BYTEORDER = 'little'
FIXED_RESULT_LEN = 4
HOST = 'localhost'
PORT = 8080
CHUNK_SIZE = 3_000


async def run_client(client_id:int, wav_buffer:bytes) -> None:
    reader, writer = await asyncio.open_connection(host=HOST, port=PORT)

    writer.write(client_id.to_bytes(4, byteorder=BYTEORDER))
    await writer.drain()
    
    wav_buffer_len = len(wav_buffer)
    writer.write(wav_buffer_len.to_bytes(4, byteorder=BYTEORDER))
    await writer.drain()

    for i in range(0, wav_buffer_len, CHUNK_SIZE):
        if wav_buffer_len - i < CHUNK_SIZE:
            chunk = wav_buffer[i:wav_buffer_len]
        else:
            chunk = wav_buffer[i:i+CHUNK_SIZE]
            
        writer.write(chunk)
        await writer.drain()

    res = await reader.read(256)
    res = res.decode('utf-8')
    print(res) 


if __name__ == '__main__':
    client_id = 12

    aud_conv = AudioConverter()
    wav_buf = aud_conv.wav_to_16bytes(r'C:\intern\xtts-2\voice_samples\Usachev 10.wav')

    asyncio.run(run_client(client_id=client_id,
                           wav_buffer=wav_buf))