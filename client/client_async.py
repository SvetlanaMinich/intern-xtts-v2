import asyncio
import json
from AudioConverter_cl import AudioConverter


BYTEORDER = 'little'
FIXED_RESULT_LEN = 4
HOST = 'localhost'
PORT = 8080


def make_additional_headers(contents,
                            language:str):
    '''
    header_len - int len value for header,
    desc_headers - [description headers like {'Type': , 'Encoding': , 'Length': , 'Language': }],
    '''

    desc_header = {
        'Type': 'unicode text',
        'Encoding': 'utf-8',
        'Length_text': len(contents[0].encode('utf-8')),
        'Length_voice': 0,
        'Language': language
    }

    if len(contents) == 2:
        voice_path = contents[1]
        if voice_path[-3:] == 'wav':
            s_conv = AudioConverter()
            path_to_mp3 = voice_path[:-3]+'mp3'
            path_to_mp3 = s_conv.wav_to_mp3(path_to_wav_file=voice_path,
                                            path_to_res_mp3_file=path_to_mp3)
            with open(path_to_mp3, 'rb') as file:
                voice_content = file.read()
        else:
            with open(voice_path, 'rb') as file:
                voice_content = file.read()
        
        desc_header['Length_voice'] = len(voice_content)

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
    contents = []
    chunk = input('Enter text chunk: ')

    if chunk.lower() == 'quit':
        contents.append(chunk)
        return contents, '', ''

    voice_content = input('Enter target voice path or <Enter> for def: ')

    contents.append(chunk)
    if voice_content.endswith('.mp3') or voice_content.endswith('.wav'):
        print(voice_content)
        contents.append(voice_content)

    language = input('Enter language code or <Enter> for "en" default: ')
    language = 'en' if language == '' else language
    
    save_path = input('Enter path to save result file: ')
    if save_path != '' and not save_path.endswith('.mp3'):
        save_path += r'\output.mp3'
    if save_path == '':
        save_path = 'output.mp3'
    
    return contents, language, save_path



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
        contents = []
        contents, language, result_path = get_contents()

        if contents[0].lower() == 'quit':
            writer.write(contents[0].encode('utf-8'))
            await writer.drain()
            break

        header_len, desc_header = make_additional_headers(contents=contents,
                                                          language=language)

        writer.write(header_len.to_bytes(4, byteorder=BYTEORDER))
        await writer.drain()
        print(header_len.to_bytes(4, byteorder=BYTEORDER), 'header len sended')
            
        data = json.dumps(desc_header)
        print(data)
        writer.write(data.encode('utf-8'))
        await writer.drain()
            
        for content in contents:
            if isinstance(content, str) and not content.endswith('.mp3') and not content.endswith('.wav'):
                content = content.encode('utf-8')
                writer.write(content)
                await writer.drain()
            else:
                if content[-3:] == 'wav':
                    path_to_mp3 = s_conv.wav_to_mp3(path_to_wav_file=content,
                                                    path_to_res_mp3_file=content[:-3]+'mp3')
                    with open(path_to_mp3, 'rb') as file:
                        voice_content = file.read()
                else:
                    with open(content, 'rb') as file:
                        voice_content = file.read()

                if len(voice_content) > 3_000:
                    chunk_size = 3_000
                    for i in range(0, len(voice_content), chunk_size):
                        if i + chunk_size > len(voice_content):
                            chunk_size = len(voice_content) - i
                        content_to_send = voice_content[i:i+chunk_size]
                        writer.write(content_to_send)
                        await writer.drain()
                        print(f'sended {len(content_to_send)}')
                else:
                    writer.write(voice_content)
                    await writer.drain()
        
        result_bytes_len = await reader.read(FIXED_RESULT_LEN)
        result_bytes_len = int.from_bytes(result_bytes_len, byteorder=BYTEORDER)
        print(f'must receive {result_bytes_len}')

        result_mp3_file_in_bytes = bytes()
        chunk_size = 1024

        while len(result_mp3_file_in_bytes) < result_bytes_len:
            received_chunk = await reader.read(chunk_size)
            result_mp3_file_in_bytes += received_chunk
            print(len(result_mp3_file_in_bytes))

        print(f'Received {len(result_mp3_file_in_bytes)} bytes of voice')        

        _ = s_conv.bytes_from_mp3_to_mp3(audio_bytes=result_mp3_file_in_bytes,
                                         path_to_result_mp3_file=result_path)



if __name__ == '__main__':
    client_id = 12
    # C:\intern\xtts-2\client\voice_samples\en\KENDALL JENNER.mp3
    # C:\intern\xtts-2\client\voice_samples\ru\01_cutted.mp3
    
    # path_to_save_file = r'C:\intern\xtts-2\res\en'

    # The cat jumped swiftly onto the wooden windowsill.
    # She picked up her book and settled into the cozy chair.
    # He smiled as he watched the children play in the park.
    asyncio.run(run_client(client_id=client_id))