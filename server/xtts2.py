from TTS.api import TTS
import torch

from scipy.io.wavfile import write
import soundfile as sf

class XTTS_V2:
    def __init__(self,
                #  model_name:str='tts_models/multilingual/multi-dataset/xtts_v2') -> None:
                model_name:str='tts_models/multilingual/multi-dataset/xtts_v2') -> None:
        device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = TTS(model_name=model_name).to(device)

    def run(self,
            text:str,
            speaker_wav:str,
            language:str='en',
            file_path:str='output.wav') -> None:
        
        wav = self.model.tts_to_file(text=text, 
                                    speaker_wav=speaker_wav, 
                                    language=language, 
                                    file_path=file_path)
        sf.write(file=file_path,
                 data=wav,
                 samplerate=24000)
