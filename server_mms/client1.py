import asyncio
import json
import io

from websockets import connect

import soundfile as sf

BYTEORDER = 'little'
FIXED_RESULT_LEN = 4
HOST = '172.81.127.5' # 172.81.127.5:64207 -> 8081/tcp
PORT = 64207

RESULT_PATH = 'C:/intern/xtts-2/server_mms/res/res.wav'


def make_additional_headers(id:int,
                            text:str,
                            language:str):
    '''
    header_len - int len value for header,
    desc_headers - [description headers like {'Type': , 'Encoding': , 'Length': , 'Language': }],
    '''
    desc_header = {
        'ClientId': id,
        'Text': text.lower()[:-1],
        'Language': language,
        'RequestId': id
    }

    return desc_header


async def run_client():
    async with connect(f'ws://{HOST}:{PORT}/') as ws:
        
        en_test = ['A small man in a holey yellow bowler hat and a pear-shaped crimson nose.',
    # 'In checkered trousers and patent leather boots rode onto the stage on an ordinary two-wheeled bicycle.',
    # 'He made a circle to the sound of a foxtrot.', 
    # 'And then let out a triumphant cry, causing the bicycle to rear up.',
    # 'Having ridden on one rear wheel, the man turned upside down.', 
    # 'Managed to unscrew the front wheel while moving and let it go behind the scenes.',
    # 'And then continued on one wheel, turning the pedals with his hands.',
    # "On a tall metal pole with a saddle on top,",
    # "a full blonde in tights rode out with one wheel.",
    # "Her skirt was studded with silver stars.",
    # "She started riding in circles around the arena.",
    # "The man greeted her with loud shouts.",
    # "With his foot, he knocked off his hat when meeting.",
    # "Finally, a little boy around eight years old rode out.",
    # "He had an old man’s face and a tiny bike.",
    # "The bike had a big car horn attached to it.",
    # "The boy weaved between adults on the stage.",
    # "Under the drumroll, they approached the stage edge.",
    # "The audience gasped and leaned back in fear.",
    # "They thought all three would fall into the orchestra.",
    ]
        client_id = "Aaaaaaaaaaaaaaaaaaa1"
        lang = 'eng'
        for i in en_test:
            desc_header = make_additional_headers(client_id, i, lang)
            data = json.dumps(desc_header).encode('utf-8')
            print(data)
            await ws.send(data)
        
        ch = await ws.recv()
        ch = json.loads(ch)
        print(ch['Audio'])
            
            # wav_bytes = io.BytesIO(ch)

            # audio_data, sample_rate = sf.read(wav_bytes)

            # sf.write(f'output{i}.wav', audio_data, sample_rate)
            # print(f'received {i}')
        
        # chunk = await ws.recv()
        # print(f'received {len(chunk)} bytes')

        # text = 'det er en meget dejlig dag'
        # desc_header = make_additional_headers(client_id, text, 'nld')
        # data = json.dumps(desc_header).encode('utf-8')
        # print(data)
        # await ws.send(data)

        # chunk = await ws.recv()
        # print(f'received {len(chunk)} bytes')

        await ws.close()



if __name__ == '__main__':
    asyncio.run(run_client())