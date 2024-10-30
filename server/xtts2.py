from TTS.api import TTS

import soundfile as sf
import torch
FILE_NAME = 'logs.txt'

class XTTS_v2:
    def __init__(self,
                 model_name:str='tts_models/multilingual/multi-dataset/xtts_v2') -> None:
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = TTS(model_name=model_name).to(device)


    def run(self,
            text:str,
            speaker_wav:str,
            language:str='en',
            file_path:str='output.wav') -> None:
        wav = self.model.tts(text=text,
                             speaker_wav=speaker_wav,
                             language=language)
        sf.write(file=file_path,
                 data=wav,
                 samplerate=22050)