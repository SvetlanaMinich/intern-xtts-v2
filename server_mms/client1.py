import asyncio
import json

from websockets import connect
from AudioConverter_cl import AudioConverter

import soundfile as sf

BYTEORDER = 'little'
FIXED_RESULT_LEN = 4
HOST = '172.81.127.5' # 172.81.127.5:64139 -> 8081/tcp
PORT = 64139

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


async def run_client():
    s_conv = AudioConverter()
    async with connect(f'ws://{HOST}:{PORT}/') as ws:
        client_id = "Aaaaaaaaaaaaaaaaaaa2"
        text = 'The sun was just beginning to rise, casting a warm golden glow across the horizon. Birds chirped happily, welcoming the new day with their melodic songs. In the distance, a gentle breeze rustled the leaves of the tall trees. The streets were quiet, with only a few early risers going about their morning routines. A cat stretched lazily on the windowsill, basking in the soft sunlight. The smell of freshly brewed coffee wafted through the air, promising a comforting start to the day. Across the park, joggers moved in a rhythmic pace, their breaths visible in the cool morning air. Children’s laughter echoed faintly as they played by the swings. Nearby, a dog chased after a butterfly, its tail wagging excitedly. The morning was peaceful, and it felt like a perfect beginning to a productive day.'
        lang = 'eng'
        desc_header = make_additional_headers(client_id, text, lang)
        data = json.dumps(desc_header).encode('utf-8')
        print(data)
        await ws.send(data)

        
        num = 0
        while num < 10:
            chunk = await ws.recv()
            print(f'received chunk №{num}: {len(chunk)}')
            _ = s_conv.bytes_to_wav(chunk, 
                                path_to_res=RESULT_PATH[:-4] + f'{num}.wav')
            _ = s_conv.wav_to_mp3(path_to_wav_file=RESULT_PATH[:-4] + f'{num}.wav', 
                                path_to_res_mp3_file=RESULT_PATH[:-4] + f'{num}.mp3')
            f_info = sf.info(RESULT_PATH[:-4] + f'{num}.wav')
            print(f'> format: {f_info.subtype_info}, samplerate: {f_info.samplerate}')
            num += 1

        await ws.close()



if __name__ == '__main__':
    asyncio.run(run_client())