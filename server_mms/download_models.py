from mms_tts import MmsModels
from TTS.api import TTS
import torch

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)

models = MmsModels()