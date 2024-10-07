import asyncio
import json
import time

from websockets import connect
from AudioConverter_cl import AudioConverter
import soundfile as sf


BYTEORDER = 'little'
FIXED_RESULT_LEN = 4
HOST = '213.108.196.111'
PORT = 20199

# HOST = 'localhost'
# PORT = 8083

# 213.108.196.111:20199 -> 8083/tcp

RESULT_PATH = 'C:/intern/xtts-2/client/res/output.wav'


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

        # client_id = "As4"
        # text = 'Солнце садилось за горизонт, отбрасывая золотой свет. Птицы пели, наполняя воздух покоем.'
        # lang = 'ru'
        # desc_header = make_additional_headers(client_id, text, lang)
        # data = json.dumps(desc_header).encode('utf-8')
        # print(data)
        # await ws.send(data)

        # time.sleep(1)

        client_id = "As4"
        text1 = 'В шумном городе жизнь текла быстро.'
        lang = 'ru'
        desc_header = make_additional_headers(client_id, text1, lang)
        data = json.dumps(desc_header).encode('utf-8')
        print(data)
        await ws.send(data)

        # time.sleep(1)

        client_id = "As4"
        text2 = 'Тихим вечером мягкий ветерок шелестел листьями. Это был идеальный момент для мира и размышлений.'
        lang = 'ru'
        desc_header = make_additional_headers(client_id, text2, lang)
        data = json.dumps(desc_header).encode('utf-8')
        print(data)
        await ws.send(data)
        
        results = []

        # result_wav_file_in_bytes = b''
        # chunk = b'a'
        # file_num = 0
        # while len(chunk) > 0:
        #     chunk = await ws.recv()
        #     result_wav_file_in_bytes += chunk 
        #     if len(chunk) < 50_000:
        #         file_num += 1
        #         _ = s_conv.bytes_to_wav(result_wav_file_in_bytes, 
        #                             path_to_res=RESULT_PATH[:-4] + f' {file_num}.wav')
        #         _ = s_conv.wav_to_mp3(path_to_wav_file=RESULT_PATH[:-4] + f' {file_num}.wav', 
        #                           path_to_res_mp3_file=RESULT_PATH[:-4] + f' {file_num}.mp3')
        #         f_info = sf.info(RESULT_PATH)
        #         print(f'> format: {f_info.subtype_info}, samplerate: {f_info.samplerate}')
        #         result_wav_file_in_bytes = b'' 
        #     print(f'    > Received {len(result_wav_file_in_bytes)} bytes')

        ws.close()



if __name__ == '__main__':
    client_id = 11

    text = input('Enter text: ')
    lang = input('Enter lang code: ')

    asyncio.run(run_client(client_id=client_id, text=text, lang=lang))