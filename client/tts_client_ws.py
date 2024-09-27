import asyncio
import json

from websockets import connect
from AudioConverter_cl import AudioConverter
import soundfile as sf


BYTEORDER = 'little'
FIXED_RESULT_LEN = 4
HOST = 'localhost'
PORT = 8080
CHUNK_SIZE = 3000


def make_additional_headers(text:str,
                            language:str):
    '''
    header_len - int len value for header,
    desc_headers - [description headers like {'Type': , 'Encoding': , 'Length': , 'Language': }],
    '''

    desc_header = {
        'Type': 'unicode text',
        'Encoding': 'utf-8',
        'Length_text': len(text.encode('utf-8')),
        'Language': language
    }

    header_len = len(json.dumps(desc_header).encode('utf-8'))
    
    return header_len, desc_header


async def clean_chunk_filename(chunk:str) -> str:
    punkt = ',.?!;:'
    text = ''
    for ch in chunk:
        if ch not in punkt:
            text += ch
    return text


def get_contents():
    chunk = input('  > Enter text: ')

    if chunk.lower() == 'quit':
        return chunk, '', ''

    language = input('  > Enter language code or <Enter> for "en" default: ')
    language = 'en' if language == '' else language
    
    save_path = input('  > Enter path to save result file: ')
    if save_path != '' and not save_path.endswith('.wav'):
        save_path += r'\output.wav'
    if save_path == '':
        save_path = 'output.wav'
    
    return chunk, language, save_path


async def run_client(client_id: int):
    s_conv = AudioConverter()

    async with connect(f'ws://{HOST}:{PORT}') as ws:
        client_id_bytes = client_id.to_bytes(4, byteorder=BYTEORDER)
        await ws.send(client_id_bytes)

        print("Enter text chunks. If you want to stop, enter 'quit'.")

        while True:
            text, language, result_path = get_contents()

            if text.lower() == 'quit':
                await ws.send(text)
                break

            header_len, desc_header = make_additional_headers(text, language)
            await ws.send(header_len.to_bytes(4, byteorder=BYTEORDER))

            data = json.dumps(desc_header)
            await ws.send(data)

            await ws.send(text)

            # Receiving result
            result_bytes_len = int.from_bytes(await ws.recv(), byteorder=BYTEORDER)
            print(f'Must receive {result_bytes_len} bytes')

            result_wav_file_in_bytes = bytes()
            while len(result_wav_file_in_bytes) < result_bytes_len:
                chunk = await ws.recv()
                result_wav_file_in_bytes += chunk
                print(f'Received {len(result_wav_file_in_bytes)} bytes')

            # Saving received audio to file
            _ = s_conv.bytes_to_wav(result_wav_file_in_bytes, path_to_res=result_path)
            _ = s_conv.wav_to_mp3(path_to_wav_file=result_path, path_to_res_mp3_file=result_path[:-3] + 'mp3')

            f_info = sf.info(result_path)
            print(f'> format: {f_info.subtype_info}, samplerate: {f_info.samplerate}')



if __name__ == '__main__':
    client_id = 1
    asyncio.run(run_client(client_id=client_id))