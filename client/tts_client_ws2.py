import asyncio
import json

from websockets import connect
from AudioConverter_cl import AudioConverter
import soundfile as sf


BYTEORDER = 'little'
FIXED_RESULT_LEN = 4
HOST = '65.93.185.202'
PORT = 40297

# 65.93.185.202:40297 to 8082

RESULT_PATH = 'C:/intern/xtts-2/client/res/output.wav'


def make_additional_headers(text:str,
                            language:str):
    '''
    header_len - int len value for header,
    desc_headers - [description headers like {'Type': , 'Encoding': , 'Length': , 'Language': }],
    '''

    desc_header = {
        'Text': text,
        'Language': language
    }

    return desc_header


async def run_client(client_id: int, text:str, lang:str='en'):
    s_conv = AudioConverter()
    async with connect(f'ws://{HOST}:{PORT}/') as ws:
        client_id_bytes = client_id.to_bytes(4, byteorder=BYTEORDER)
        desc_header = make_additional_headers(text, lang)
        data = json.dumps(desc_header).encode('utf-8')
        await ws.send(client_id_bytes + data)

        result_wav_file_in_bytes = await ws.recv()
        print(f'    > Received {len(result_wav_file_in_bytes)} bytes')
        # Saving received audio to file
        _ = s_conv.bytes_to_wav(result_wav_file_in_bytes, path_to_res=RESULT_PATH[:-4] + f'{client_id}.wav')
        _ = s_conv.wav_to_mp3(path_to_wav_file=RESULT_PATH[:-4] + f'{client_id}.wav', path_to_res_mp3_file=RESULT_PATH[:-4] + f'{client_id}.mp3')

        f_info = sf.info(RESULT_PATH)
        print(f'> format: {f_info.subtype_info}, samplerate: {f_info.samplerate}')



if __name__ == '__main__':
    client_id = 2

    text = input('Enter text: ')
    lang = input('Enter lang code: ')

    asyncio.run(run_client(client_id=client_id, text=text, lang=lang))