# pip install --upgrade transformers accelerate
# python3 -m pip install uroman

# langs:
# English            eng
# Urdu (script arab) urd
# Arabic             ara
# German             deu
# Russian            rus
# Hindi              hin

from transformers import VitsModel, AutoTokenizer
import torch


class MmsModels:
    def __init__(self) -> None:
        self.device = "cuda:0" if torch.cuda.is_available() else "cpu"

        self.model_urd = VitsModel.from_pretrained("facebook/mms-tts-urd-script_arabic")
        self.tokenizer_urd = AutoTokenizer.from_pretrained("facebook/mms-tts-urd-script_arabic")
        self.model_urd.to(self.device).eval()

        self.model_eng = VitsModel.from_pretrained("facebook/mms-tts-eng")
        self.tokenizer_eng = AutoTokenizer.from_pretrained("facebook/mms-tts-eng")
        self.model_eng.to(self.device).eval()

        self.model_arab = VitsModel.from_pretrained("facebook/mms-tts-ara")
        self.tokenizer_arab = AutoTokenizer.from_pretrained("facebook/mms-tts-ara")
        self.model_arab.to(self.device).eval()

        self.model_deu = VitsModel.from_pretrained("facebook/mms-tts-deu")
        self.tokenizer_deu = AutoTokenizer.from_pretrained("facebook/mms-tts-deu")
        self.model_deu.to(self.device).eval()

        self.model_rus = VitsModel.from_pretrained("facebook/mms-tts-rus")
        self.tokenizer_rus = AutoTokenizer.from_pretrained("facebook/mms-tts-rus")
        self.model_rus.to(self.device).eval()

        self.model_hin = VitsModel.from_pretrained("facebook/mms-tts-hin")
        self.tokenizer_hin = AutoTokenizer.from_pretrained("facebook/mms-tts-hin")
        self.model_hin.to(self.device).eval()

    def load_model(self, lang:str):
        model_name = f'facebook/mms-tts-{lang}'
                
        model_attr = f'model_{lang}'
        tokenizer_attr = f'tokenizer_{lang}'

        if not hasattr(self, model_attr) or not hasattr(self, tokenizer_attr):
            print(f"Loading model and tokenizer for {lang}...")

            setattr(self, model_attr, VitsModel.from_pretrained(model_name))
            setattr(self, tokenizer_attr, AutoTokenizer.from_pretrained(model_name))
            getattr(self, model_attr).to(self.device).eval()

            # Dynamically create the TTS function for this language
            def tts_func(text: str):
                inputs = getattr(self, tokenizer_attr)(text=text, return_tensors="pt")
                with torch.no_grad():
                    outputs = getattr(self, model_attr)(**inputs.to(self.device))
                return outputs.waveform[0].cpu().float().numpy()

            setattr(self, f'tts_{lang}', tts_func)
            return f'tts_{lang}'


    def tts_urd(self, text):
        inputs = self.tokenizer_urd(text=text, return_tensors="pt")
        with torch.no_grad():
            outputs = self.model_urd(**inputs.to(self.device))
        return outputs.waveform[0].cpu().float().numpy()

    def tts_eng(self, text):
        print('in tts_eng')
        inputs = self.tokenizer_eng(text=text, return_tensors="pt")
        with torch.no_grad():
            outputs = self.model_eng(**inputs.to(self.device))
        return outputs.waveform[0].cpu().float().numpy()

    def tts_ara(self, text):
        inputs = self.tokenizer_arab(text=text, return_tensors="pt")
        with torch.no_grad():
            outputs = self.model_arab(**inputs.to(self.device))
        return outputs.waveform[0].cpu().float().numpy()

    def tts_deu(self, text):
        inputs = self.tokenizer_deu(text=text, return_tensors="pt")
        with torch.no_grad():
            outputs = self.model_deu(**inputs.to(self.device))
        return outputs.waveform[0].cpu().float().numpy()

    def tts_rus(self, text):
        inputs = self.tokenizer_rus(text=text, return_tensors="pt")
        with torch.no_grad():
            outputs = self.model_rus(**inputs.to(self.device))
        return outputs.waveform[0].cpu().float().numpy()

    def tts_hin(self, text):
        inputs = self.tokenizer_hin(text=text, return_tensors="pt")
        with torch.no_grad():
            outputs = self.model_hin(**inputs.to(self.device))
        return outputs.waveform[0].cpu().float().numpy()