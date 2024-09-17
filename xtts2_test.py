from TTS.api import TTS
import torch

# Get device
device = "cuda" if torch.cuda.is_available() else "cpu"

tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)
text = 'The sun sets behind the mountains.'
tts.tts_to_file(text=text, 
                speaker_wav=r"C:\intern\xtts-2\voice_samples\en\Alessia_Cara.mp3", 
                language="en", 
                file_path=fr"C:\intern\xtts-2\res\en\{text[:20]}.wav")
