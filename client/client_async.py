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
    # C:\intern\xtts-2\voice_samples\en\KENDALL JENNER.mp3
    # C:\intern\xtts-2\server\def.mp3
    # C:\intern\xtts-2\client\voice_samples\ru\01_cutted.mp3
    # C:\intern\xtts-2\voice_samples\Usachev.mp3
    # C:\intern\xtts-2\voice_samples\woman.mp3
    # C:\intern\xtts-2\voice_samples\Faib.mp3

    # path_to_save_file = r'C:\intern\xtts-2\res\en'

    # The cat jumped swiftly onto the wooden windowsill.
    # She picked up her book and settled into the cozy chair.
    # He smiled as he watched the children play in the park.
    # Hello, this is a test.
    # The sun set behind the hills, casting a warm glow across the sky. The day slowly turned into night, and the stars began to appear, twinkling softly as the world around them quieted down for rest.

    # Осенний вечер принес прохладу и легкий ветерок, листья мягко кружатся в воздухе, создавая атмосферу уюта. В домах загораются теплые огни, а люди наслаждаются спокойствием уходящего дня.
    # Солнце скрылось за горами, окрашивая небо в оранжевый.
    # Он улыбался, наблюдая за детьми, играющими в парке.

    # Il sourit en regardant les enfants jouer dans le parc.
    # Le soleil se couche, illuminant l'horizon rouge.
    # En plein cœur de l'automne, les arbres se parent de teintes orangées et rouges. Le vent souffle doucement, emportant avec lui les feuilles mortes qui tourbillonnent avant de toucher le sol humide.





    sentences_en = [
        # English
        "The sun sets so fast.",
        "He loves coding daily.",
        "She read a new book.",
        "The stars twinkle bright.",
        "Time flies when happy."]
    
    sentences_ru_not_dot = [
        # Russian
        "Солнце садится быстро",
        "Он любит кодить каждый день",
        "Она прочитала новую книгу",
        "Звезды ярко мерцают",
        "Время летит, когда счастлив"]

    sentences_fr = [
        # French
        "Le soleil se couche vite.",
        "Il aime coder tous les jours.",
        "Elle a lu un nouveau livre.",
        "Les étoiles brillent fort.",
        "Le temps passe vite quand on est heureux."
    ]

    texts_en = [
        # English
        "The sun was setting over the horizon, casting a golden glow. Birds sang, filling the air with calm.",
        "In the busy city, life moved quickly. People rushed through the streets, deep in their own thoughts.",
        "On a quiet evening, a soft breeze rustled the leaves. It was the perfect moment for peace and reflection."]
    texts_fr = [
        # French
        "Le soleil se couchait à l'horizon, projetant une lueur dorée. Les oiseaux chantaient, remplissant l'air de calme.",
        "Dans la ville animée, la vie avançait rapidement. Les gens se précipitaient dans les rues, perdus dans leurs pensées.",
        "Par une soirée tranquille, une douce brise faisait bruisser les feuilles. C'était le moment parfait pour la paix et la réflexion."]
    texts_sp = [
        # Spanish
        "El sol se ponía en el horizonte, proyectando un brillo dorado. Los pájaros cantaban, llenando el aire de calma.",
        "En la ciudad ocupada, la vida se movía rápido. La gente se apresuraba por las calles, sumida en sus propios pensamientos.",
        "En una tarde tranquila, una suave brisa movía las hojas. Era el momento perfecto para la paz y la reflexión."]
    texts_ru = [
        # Russian
        "Солнце садилось за горизонт, отбрасывая золотой свет. Птицы пели, наполняя воздух покоем.",
        "В шумном городе жизнь текла быстро. Люди спешили по улицам, погруженные в свои мысли.",
        "Тихим вечером мягкий ветерок шелестел листьями. Это был идеальный момент для мира и размышлений."
    ]



    short_sentences_en = [
        # English
        "I'm so sad.",  
        "I'm so mad!",  
        "How funny!",   
        "I'm afraid.",  
        "So peaceful."]
    short_sentences_ru = [
        # Russian
        "Мне так грустно.",  
        "Я в ярости!",       
        "Как смешно!",       
        "Я боюсь.",          
        "Так спокойно."]
    
    short_sentences_fr = [
        # French
        "Je suis triste.",    
        "Je suis furieux!",   
        "C'est drôle!",       
        "J'ai peur.",         
        "Si paisible."]
    short_sentences_es = [
        # Spanish
        "Estoy triste.",      
        "¡Estoy furioso!",    
        "¡Qué gracioso!",     
        "Tengo miedo.",       
        "Tan tranquilo.",     
    ]



    big_text_en = "The sun was setting over the horizon, painting the sky with hues of orange and pink. The gentle breeze carried the scent of the ocean, and the waves softly lapped against the shore. It was the perfect evening, one that seemed to hold infinite possibilities. As the first stars appeared, a sense of peace washed over me, and I realized that sometimes, the simplest moments can bring the greatest joy. Life felt calm and meaningful in that quiet, serene twilight."
    big_text_ru = "Солнце заходило за горизонт, окрашивая небо в оттенки оранжевого и розового. Лёгкий ветерок приносил аромат моря, а волны мягко омывали берег. Это был идеальный вечер, казалось, он хранил в себе бесконечные возможности. Когда появились первые звезды, на меня нахлынуло чувство умиротворения, и я осознал, что иногда самые простые моменты могут принести наибольшую радость. Жизнь казалась спокойной и значимой в этом тихом, безмятежном сумраке."

    asyncio.run(run_client(client_id=client_id))