# pip install --upgrade transformers accelerate
# python3 -m pip install uroman

# langs:
# English            eng
# Urdu (script arab) urd
# Arabic             ara
# German             deu
# Russian            rus
# Hindi              hin

from transformers import VitsModel, AutoTokenizer, set_seed
import torch

import scipy

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


    def tts_urd(self, text, res_file_path):
        inputs = self.tokenizer_urd(text=text, return_tensors="pt")
        set_seed(555)
        with torch.no_grad():
            outputs = self.model_urd(**inputs.to(self.device)).waveform

    def tts_eng(self, text, res_file_path):
        inputs = self.tokenizer_eng(text=text, return_tensors="pt")
        set_seed(555)
        with torch.no_grad():
            outputs = self.model_eng(**inputs.to(self.device)).waveform

    def tts_arab(self, text, res_file_path):
        inputs = self.tokenizer_arab(text=text, return_tensors="pt")
        set_seed(555)
        with torch.no_grad():
            outputs = self.model_arab(**inputs.to(self.device)).waveform

    def tts_deu(self, text, res_file_path):
        inputs = self.tokenizer_deu(text=text, return_tensors="pt")
        set_seed(555)
        with torch.no_grad():
            outputs = self.model_deu(**inputs.to(self.device)).waveform

    def tts_rus(self, text, res_file_path):
        inputs = self.tokenizer_rus(text=text, return_tensors="pt")
        set_seed(555)
        with torch.no_grad():
            outputs = self.model_rus(**inputs.to(self.device)).waveform

    def tts_hin(self, text, res_file_path):
        inputs = self.tokenizer_hin(text=text, return_tensors="pt")
        set_seed(555)
        with torch.no_grad():
            outputs = self.model_hin(**inputs.to(self.device)).waveform

import time

model = MmsModels()

start = time.time()
model.tts_urd(text='آپ جس خامی کا سامنا کر رہے ہیں اس کا تعلق ملٹی پروسیسنگ ماڈیول سے ہے اور یہ کہ پراسیسز کے درمیان اشیاء کو کس طرح شیئر کیا جاتا ہے۔',
              res_file_path='output urd.wav')
print(f'urd: {time.time() - start}')

start = time.time()
model.tts_arab(text='يرتبط الخطأ الذي تواجهه بوحدة المعالجة المتعددة وكيفية مشاركة الكائنات بين العمليات.',
               res_file_path='output arab.wav')
print(f'arab: {time.time() - start}')

start = time.time()
model.tts_deu(text='Der aufgetretene Fehler hängt mit dem Multiprocessing-Modul und der Art und Weise zusammen, wie Objekte zwischen Prozessen gemeinsam genutzt werden.',
              res_file_path='output deu.wav')
print(f'deu: {time.time() - start}')

start = time.time()
model.tts_eng(text="The error you're encountering is related to the multiprocessing module and how objects are shared between processes.",
              res_file_path='output eng.wav')
print(f'eng: {time.time() - start}')

start = time.time()
model.tts_rus(text="Ошибка, с которой вы столкнулись, связана с модулем многопроцессорности и тем, как объекты распределяются между процессами.",
              res_file_path='output rus.wav')
print(f'rus: {time.time() - start}')

start = time.time()
model.tts_hin(text="आप जिस त्रुटि का सामना कर रहे हैं वह मल्टीप्रोसेसिंग मॉड्यूल और प्रक्रियाओं के बीच वस्तुओं को कैसे साझा किया जाता है, से संबंधित है।",
              res_file_path='output hin.wav')
print(f'hin: {time.time() - start}')