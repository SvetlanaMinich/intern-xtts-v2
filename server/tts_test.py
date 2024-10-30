import os
import torch
import torchaudio
from TTS.tts.configs.xtts_config import XttsConfig
from TTS.tts.models.xtts import Xtts

print("Loading model...")
model_dir = '/root/.local/share/tts/tts_models--multilingual--multi-dataset--xtts_v2'
config = XttsConfig()
config.load_json(model_dir + "/config.json")
model = Xtts.init_from_config(config)
model.load_checkpoint(config, checkpoint_dir=model_dir)
model.to(torch.device("cuda")).eval()

print("Computing speaker latents...")
gpt_cond_latent, speaker_embedding = model.get_conditioning_latents(audio_path=["def.wav"])

import time

print("Inference...")
start = time.time()
out = model.inference(
    "It took me quite a long time to develop a voice and now that I have it I am not going to be silent.",
    "en",
    gpt_cond_latent,
    speaker_embedding,
    temperature=0.7, # Add custom parameters here
)
print(f'Time: {time.time() - start}')