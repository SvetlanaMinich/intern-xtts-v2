import asyncio
import json
import time

from websockets import connect
from AudioConverter_cl import AudioConverter
import soundfile as sf


BYTEORDER = 'little'
FIXED_RESULT_LEN = 4
HOST = '218.172.74.127'
PORT = 42183

# HOST = 'localhost'
# PORT = 8083

# 213.108.196.111:20199 -> 8083/tcp 3080
# 218.172.74.127:42183 -> 8083/tcp 4090

RESULT_PATH = 'C:/intern/xtts-2/client/res/res.wav'


def make_additional_headers(id:int,
                            text:str,
                            language:str):
    '''
    header_len - int len value for header,
    desc_headers - [description headers like {'Type': , 'Encoding': , 'Length': , 'Language': }],
    '''
    desc_header = {
        'Client_id': id,
        'Text': text,
        'Language': language
    }

    return desc_header


async def run_client(client_id: int, text:str, lang:str='en'):
    s_conv = AudioConverter()
    async with connect(f'ws://{HOST}:{PORT}/') as ws:
        client_id = "Aaaaaaaaaaaaaaaaaaa4"
        text = 'The sun was setting over the horizon. Painting the sky with hues of orange and pink. The gentle breeze carried the scent of the ocean. And the waves softly lapped against the shore. It was the perfect evening. One that seemed to hold infinite possibilities. As the first stars appeared, a sense of peace washed over me. And I realized that sometimes, the simplest moments can bring the greatest joy. Life felt calm and meaningful in that quiet, serene twilight.'
        lang = 'en'
        desc_header = make_additional_headers(client_id, text, lang)
        data = json.dumps(desc_header).encode('utf-8')
        print(data)
        await ws.send(data)

        client_id = "Aaaaaaaaaaaaaaaaaaa4"
        text = 'The sun was setting over the horizon. Painting the sky with hues of orange and pink. The gentle breeze carried the scent of the ocean. And the waves softly lapped against the shore. It was the perfect evening. One that seemed to hold infinite possibilities. As the first stars appeared, a sense of peace washed over me. And I realized that sometimes, the simplest moments can bring the greatest joy. Life felt calm and meaningful in that quiet, serene twilight.'
        lang = 'en'
        desc_header = make_additional_headers(client_id, text, lang)
        data = json.dumps(desc_header).encode('utf-8')
        print(data)
        await ws.send(data)

        client_id = "Aaaaaaaaaaaaaaaaaaa4"
        text = 'The sun was setting over the horizon. Painting the sky with hues of orange and pink. The gentle breeze carried the scent of the ocean. And the waves softly lapped against the shore. It was the perfect evening. One that seemed to hold infinite possibilities. As the first stars appeared, a sense of peace washed over me. And I realized that sometimes, the simplest moments can bring the greatest joy. Life felt calm and meaningful in that quiet, serene twilight.'
        lang = 'en'
        desc_header = make_additional_headers(client_id, text, lang)
        data = json.dumps(desc_header).encode('utf-8')
        print(data)
        await ws.send(data)

        
        num = 0
        while num < 27:
            chunk = await ws.recv()
            _ = s_conv.bytes_to_wav(chunk, 
                                path_to_res=RESULT_PATH[:-4] + f'{num}.wav')
            _ = s_conv.wav_to_mp3(path_to_wav_file=RESULT_PATH[:-4] + f'{num}.wav', 
                                path_to_res_mp3_file=RESULT_PATH[:-4] + f'{num}.mp3')
            f_info = sf.info(RESULT_PATH[:-4] + f'{num}.wav')
            print(f'> format: {f_info.subtype_info}, samplerate: {f_info.samplerate}')
            num += 1

        await ws.close()



if __name__ == '__main__':
    client_id = 11

    text = input('Enter text: ')
    lang = input('Enter lang code: ')

    asyncio.run(run_client(client_id=client_id, text=text, lang=lang))