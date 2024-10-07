# from pydub import AudioSegment

# sound = AudioSegment.from_mp3(r'C:\intern\xtts-2\voice_samples\Faib 10.mp3')
# sound.export(r'C:\intern\xtts-2\voice_samples\Faib 10 wav.wav', format='wav')

import json

desc_header = {
        'Client_id': 123,
        'Text': "Answer successfully set and ",
        'Language': "en"
    }


data = bytearray(json.dumps(desc_header).encode('utf-8'))
for i in data:
    print(i, end=' ')

print(data)