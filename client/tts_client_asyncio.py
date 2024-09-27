import asyncio
import json
from AudioConverter_cl import AudioConverter


BYTEORDER = 'little'
FIXED_RESULT_LEN = 4
HOST = 'localhost'
PORT = 8080
CHUNK_SIZE = 3_000


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
    chunk = input('Enter text chunk: ')

    if chunk.lower() == 'quit':
        return chunk, '', ''

    language = input('Enter language code or <Enter> for "en" default: ')
    language = 'en' if language == '' else language
    
    save_path = input('Enter path to save result file: ')
    if save_path != '' and not save_path.endswith('.wav'):
        save_path += r'\output.wav'
    if save_path == '':
        save_path = 'output.wav'
    
    return chunk, language, save_path



async def run_client(client_id:int) -> None:
    """
    contents - [content], content is text str or
    list of text str and path to mp3 file
    """

    s_conv = AudioConverter()
    reader, writer = await asyncio.open_connection(host=HOST, port=PORT)

    writer.write(client_id.to_bytes(4, byteorder=BYTEORDER))
    await writer.drain()
    print("Enter text chunks. If you wanna stop, enter 'quit'.")

    while True:
        text, language, result_path = get_contents()

        if text.lower() == 'quit':
            writer.write(text.encode('utf-8'))
            await writer.drain()
            break

        header_len, desc_header = make_additional_headers(text=text,
                                                          language=language)

        writer.write(header_len.to_bytes(4, byteorder=BYTEORDER))
        await writer.drain()
        print(header_len.to_bytes(4, byteorder=BYTEORDER), 'header len sended')
            
        data = json.dumps(desc_header)
        print(data)
        writer.write(data.encode('utf-8'))
        await writer.drain()
            
        writer.write(text.encode('utf-8'))
        await writer.drain()
        
        result_bytes_len = await reader.read(FIXED_RESULT_LEN)
        result_bytes_len = int.from_bytes(result_bytes_len, byteorder=BYTEORDER)
        print(f'must receive {result_bytes_len}')

        result_wav_file_in_bytes = bytes()
        
        while len(result_wav_file_in_bytes) < result_bytes_len:
            received_chunk = await reader.read(CHUNK_SIZE)
            result_wav_file_in_bytes += received_chunk
            print(len(result_wav_file_in_bytes))

        print(f'Received {len(result_wav_file_in_bytes)} bytes of voice')        

        _ = s_conv.bytes_to_wav(audiobytes=result_wav_file_in_bytes,
                                path_to_res=result_path)
        _ = s_conv.wav_to_mp3(path_to_wav_file=result_path,
                              path_to_res_mp3_file=result_path[:-3] + 'mp3')



if __name__ == '__main__':
    client_id = 12
    asyncio.run(run_client(client_id=client_id))