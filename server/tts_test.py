from TTS.api import TTS
import torch
import torch.multiprocessing as mp

class XTTS_v2:
    def __init__(self,
                 model_name:str='tts_models/multilingual/multi-dataset/xtts_v2') -> None:
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = TTS(model_name=model_name).to(device)


    def run(self,
            text:str,
            speaker_wav:str,
            language:str='en',
            file_path:str='output.wav',
            speaker_name_cust:str="") -> None:
        sens = text.split('.')
        sens = sens[:-1]
        for sen in sens:
            print(sen, 'start')

            wav = self.model.tts(text=sen[:-1],
                                 speaker_wav=speaker_wav,
                                 language=language,
                                 speaker_name_cust=speaker_name_cust)
                

            print(sen, 'end')
        # sf.write(file=file_path,
        #          data=wav,
        #          samplerate=24000)

def forward_pass_method(text, speaker_wav, speaker_name_cust, language):
    tts = XTTS_v2()
    tts.run(text=text, speaker_wav=speaker_wav, speaker_name_cust=speaker_name_cust, language=language)


def run_parallel_tts():
    text = "To maximize the speed of the XTTS-v2 model on GPU. There are several steps and optimizations you can apply."
    speaker_wav = 'def.wav'
    speaker_name_cust = 'aaaaaaaaaaaaaaaaaaa1'
    streams_count = 3
    language = 'en'
    

    processes = []
    for i in range(streams_count):
        # Create a separate process for each forward pass
        p = mp.Process(target=forward_pass_method, args=(text, speaker_wav, speaker_name_cust, language))
        p.start()
        processes.append(p)
    
    # Join all processes to ensure they complete
    for p in processes:
        p.join()


if __name__ == '__main__':
    # For multiprocessing to work correctly in Windows or MacOS
    mp.set_start_method('spawn')

    # Run parallel TTS
    run_parallel_tts()