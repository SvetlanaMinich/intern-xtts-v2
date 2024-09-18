from TTS.api import TTS
import torch

class XTTS_V2:
    def __init__(self,
                 model_name:str='tts_models/multilingual/multi-dataset/xtts_v2') -> None:
        device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = TTS(model_name=model_name).to(device)

    def run(self,
            text:str,
            speaker_wav:str,
            language:str='en',
            file_path:str='output.wav') -> None:
        
        self.model.tts_to_file(text=text, 
                               speaker_wav=speaker_wav, 
                               language=language, 
                               file_path=file_path)


from pydub import AudioSegment
import os
model = XTTS_V2()
while True:
    text = input('Enter text: ')
    if text.lower() == 'quit':
        break
    model.run(text=text,
            speaker_wav=r'C:\intern\xtts-2\server\def.wav',
            language='en',
            file_path=r'C:\intern\xtts-2\res\en\output.wav')
    sound = AudioSegment.from_wav(r'C:\intern\xtts-2\res\en\output.wav')
    sound.export(r'C:\intern\xtts-2\res\en\output.mp3', 'mp3')
    print(' > file size:', os.stat(r'C:\intern\xtts-2\res\en\output.mp3').st_size)

os.remove(r'C:\intern\xtts-2\res\en\output.wav')
