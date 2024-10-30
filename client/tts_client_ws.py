import asyncio
import json
import time

from websockets import connect
from AudioConverter_cl import AudioConverter
import soundfile as sf


BYTEORDER = 'little'
FIXED_RESULT_LEN = 4
HOST = '70.77.113.32'
PORT = 40755

# HOST = 'localhost'
# PORT = 8083

# 70.77.113.32:40755 -> 8083/tcp 4080s

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
        text = 'Painting the sky with hues of orange and pink.'
        lang = 'en'
        desc_header = make_additional_headers(client_id, text, lang)
        data = json.dumps(desc_header).encode('utf-8')
        print(data)
        await ws.send(data)

        # client_id = "Aaaaaaaaaaaaaaaaaaa2"
        # text = 'And the waves softly lapped against the shore.'
        # lang = 'en'
        # desc_header = make_additional_headers(client_id, text, lang)
        # data = json.dumps(desc_header).encode('utf-8')
        # print(data)
        # await ws.send(data)

        # client_id = "Aaaaaaaaaaaaaaaaaaa2"
        # text = 'Painting the sky with hues of orange and pink.'
        # lang = 'en'
        # desc_header = make_additional_headers(client_id, text, lang)
        # data = json.dumps(desc_header).encode('utf-8')
        # print(data)
        # await ws.send(data)

        # client_id = "Aaaaaaaaaaaaaaaaaaa1"
        # text = 'And the waves softly lapped against the shore.'
        # lang = 'en'
        # desc_header = make_additional_headers(client_id, text, lang)
        # data = json.dumps(desc_header).encode('utf-8')
        # print(data)
        # await ws.send(data)

        # client_id = "Aaaaaaaaaaaaaaaaaaa1"
        # text = 'It was the perfect evening.'
        # lang = 'en'
        # desc_header = make_additional_headers(client_id, text, lang)
        # data = json.dumps(desc_header).encode('utf-8')
        # print(data)
        # await ws.send(data)

        # client_id = "Aaaaaaaaaaaaaaaaaaa1"
        # text = 'One that seemed to hold infinite possibilities.'
        # lang = 'en'
        # desc_header = make_additional_headers(client_id, text, lang)
        # data = json.dumps(desc_header).encode('utf-8')
        # print(data)
        # await ws.send(data)


        # client_id = "Aaaaaaaaaaaaaaaaaaa3"
        # text = 'The sun was setting over the horizon. Painting the sky with hues of orange and pink. The gentle breeze carried the scent of the ocean. And the waves softly lapped against the shore. It was the perfect evening. One that seemed to hold infinite possibilities. As the first stars appeared, a sense of peace washed over me. And I realized that sometimes, the simplest moments can bring the greatest joy. Life felt calm and meaningful in that quiet, serene twilight.'
        # lang = 'en'
        # desc_header = make_additional_headers(client_id, text, lang)
        # data = json.dumps(desc_header).encode('utf-8')
        # print(data)
        # await ws.send(data)

        # client_id = "Aaaaaaaaaaaaaaaaaaa3"
        # text = 'The sun was setting over the horizon. Painting the sky with hues of orange and pink. The gentle breeze carried the scent of the ocean. And the waves softly lapped against the shore. It was the perfect evening. One that seemed to hold infinite possibilities. As the first stars appeared, a sense of peace washed over me. And I realized that sometimes, the simplest moments can bring the greatest joy. Life felt calm and meaningful in that quiet, serene twilight.'
        # lang = 'en'
        # desc_header = make_additional_headers(client_id, text, lang)
        # data = json.dumps(desc_header).encode('utf-8')
        # print(data)
        # await ws.send(data)

        import time
        
        start = time.time()
        num = 0
        while num < 2:
            chunk = await ws.recv()
            print(f'{num} file: {time.time() - start}')
            start = time.time()
            # _ = s_conv.bytes_to_wav(chunk, 
            #                     path_to_res=RESULT_PATH[:-4] + f'{num}.wav')
            # _ = s_conv.wav_to_mp3(path_to_wav_file=RESULT_PATH[:-4] + f'{num}.wav', 
            #                     path_to_res_mp3_file=RESULT_PATH[:-4] + f'{num}.mp3')
            # f_info = sf.info(RESULT_PATH[:-4] + f'{num}.wav')
            # print(f'> format: {f_info.subtype_info}, samplerate: {f_info.samplerate}')
            num += 1

        await ws.close()



if __name__ == '__main__':
    asyncio.run(run_client())