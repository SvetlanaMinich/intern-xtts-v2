from transformers import VitsModel, AutoTokenizer
import torch
from scipy.signal import resample

from TTS.tts.configs.xtts_config import XttsConfig
from TTS.tts.models.xtts import Xtts
model_path = '/root/.local/share/tts/tts_models--multilingual--multi-dataset--xtts_v2/'

models_dir = 'models'


class MmsModels:
    def __init__(self, devices=['cuda:0']) -> None:
        self.models_dir = 'models'
        # Load models and tokenizers for each device
        self.models = {}
        self.tokenizers = {}

        for device in devices:
            if not torch.cuda.is_available() and device.startswith("cuda"):
                print(f"{device} is not available. Skipping...")
                continue
            
            config = XttsConfig()
            config.load_json(model_path+"config.json")
            model = Xtts.init_from_config(config)
            model.load_checkpoint(config, checkpoint_dir=model_path, use_deepspeed=True)
            model.to(device)
            # Load models
            self.models[device] = {
                "urd": VitsModel.from_pretrained("facebook/mms-tts-urd-script_arabic", cache_dir=self.models_dir).to(device).eval(),
                "eng": model,
                "ara": VitsModel.from_pretrained("facebook/mms-tts-ara", cache_dir=self.models_dir).to(device).eval(),
                "deu": model,
                "rus": VitsModel.from_pretrained("facebook/mms-tts-rus", cache_dir=self.models_dir).to(device).eval(),
                "hin": model,
                "ben": VitsModel.from_pretrained("facebook/mms-tts-ben", cache_dir=self.models_dir).to(device).eval(),
                "mya": VitsModel.from_pretrained("facebook/mms-tts-mya", cache_dir=self.models_dir).to(device).eval(),
                "nld": VitsModel.from_pretrained("facebook/mms-tts-nld", cache_dir=self.models_dir).to(device).eval(),
                "fin": VitsModel.from_pretrained("facebook/mms-tts-fin", cache_dir=self.models_dir).to(device).eval(),
                "heb": VitsModel.from_pretrained("facebook/mms-tts-heb", cache_dir=self.models_dir).to(device).eval(),
                "ind": VitsModel.from_pretrained("facebook/mms-tts-ind", cache_dir=self.models_dir).to(device).eval(),
                "spa": VitsModel.from_pretrained("facebook/mms-tts-spa", cache_dir=self.models_dir).to(device).eval(),
                "kan": VitsModel.from_pretrained("facebook/mms-tts-kan", cache_dir=self.models_dir).to(device).eval(),
                "mkn": VitsModel.from_pretrained("facebook/mms-tts-mkn", cache_dir=self.models_dir).to(device).eval(),
            }
            
            # Load tokenizers
            self.tokenizers[device] = {
                "urd": AutoTokenizer.from_pretrained("facebook/mms-tts-urd-script_arabic", cache_dir=self.models_dir),
                "ara": AutoTokenizer.from_pretrained("facebook/mms-tts-ara", cache_dir=self.models_dir),
                "rus": AutoTokenizer.from_pretrained("facebook/mms-tts-rus", cache_dir=self.models_dir),
                "ben": AutoTokenizer.from_pretrained("facebook/mms-tts-ben", cache_dir=self.models_dir),
                "mya": AutoTokenizer.from_pretrained("facebook/mms-tts-mya", cache_dir=self.models_dir),
                "nld": AutoTokenizer.from_pretrained("facebook/mms-tts-nld", cache_dir=self.models_dir),
                "fin": AutoTokenizer.from_pretrained("facebook/mms-tts-fin", cache_dir=self.models_dir),
                "heb": AutoTokenizer.from_pretrained("facebook/mms-tts-heb", cache_dir=self.models_dir),
                "ind": AutoTokenizer.from_pretrained("facebook/mms-tts-ind", cache_dir=self.models_dir),
                "spa": AutoTokenizer.from_pretrained("facebook/mms-tts-spa", cache_dir=self.models_dir),
                "kan": AutoTokenizer.from_pretrained("facebook/mms-tts-kan", cache_dir=self.models_dir),
                "mkn": AutoTokenizer.from_pretrained("facebook/mms-tts-mkn", cache_dir=self.models_dir),
            }

    def get_latents(self):
        print("Computing speaker latents...")
        gpt_cond_latent, speaker_embedding = self.models['cuda:0'].get_conditioning_latents(audio_path=["def.wav"])
        return (gpt_cond_latent, speaker_embedding)

    def tts(self, text, lang, device):
        inputs = self.tokenizers[device][lang](text=text, return_tensors="pt")
        with torch.no_grad():
            outputs = self.models[device][lang](**inputs.to(device))
        return outputs.waveform[0].cpu().float().numpy()

    def tts_urd(self, text, device):
        return self.tts(text, "urd", device)
    
    def tts_mkn(self, text, device):
        return self.tts(text, "mkn", device)

    def tts_eng(self, text, device, gpt_cond_latent, speaker_embedding):
        output = self.models[device]["eng"].inference(
            text,
            "en",
            gpt_cond_latent,
            speaker_embedding,
            temperature=0.7, # Add custom parameters here
        )
        output = torch.tensor(output["wav"]).unsqueeze(0)
        num_samples = int(len(output) * (16000 / 24000))  # Calculate the new number of samples
        output_resampled = resample(output, num_samples)
        return output_resampled

    def tts_ara(self, text, device):
        return self.tts(text, "ara", device)

    def tts_deu(self, text, device, gpt_cond_latent, speaker_embedding):
        output = self.models[device]["deu"].inference(
            text,
            "de",
            gpt_cond_latent,
            speaker_embedding,
            temperature=0.7, # Add custom parameters here
        )
        output = torch.tensor(output["wav"]).unsqueeze(0)
        num_samples = int(len(output) * (16000 / 24000))  # Calculate the new number of samples
        output_resampled = resample(output, num_samples)
        return output_resampled

    def tts_rus(self, text, device):
        return self.tts(text, "rus", device)

    def tts_hin(self, text, device, gpt_cond_latent, speaker_embedding):
        output = self.models[device]["hin"].inference(
            text,
            "hi",
            gpt_cond_latent,
            speaker_embedding,
            temperature=0.7, # Add custom parameters here
        )
        output = torch.tensor(output["wav"]).unsqueeze(0)
        num_samples = int(len(output) * (16000 / 24000))  # Calculate the new number of samples
        output_resampled = resample(output, num_samples)
        return output_resampled

    def tts_ben(self, text, device):
        return self.tts(text, "ben", device)

    def tts_mya(self, text, device):
        return self.tts(text, "mya", device)

    def tts_nld(self, text, device):
        return self.tts(text, "nld", device)

    def tts_fin(self, text, device):
        return self.tts(text, "fin", device)

    def tts_heb(self, text, device):
        return self.tts(text, "heb", device)

    def tts_ind(self, text, device):
        return self.tts(text, "ind", device)

    def tts_spa(self, text, device):
        return self.tts(text, "spa", device)

    def tts_kan(self, text, device):
        return self.tts(text, "kan", device)


mmstts = MmsModels()