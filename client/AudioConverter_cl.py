from pydub import AudioSegment
import io


class AudioConverter:
    def wav_to_mp3(self, path_to_wav_file:str, path_to_res_mp3_file:str):
        '''Converting .wav file from <path_to_wav_file> path to .mp3 format.
        Saving result to <path_to_res_mp3_file> path. Return <path_to_res_mp3_file> path.'''
        sound = AudioSegment.from_wav(path_to_wav_file)
        sound.export(path_to_res_mp3_file, format='mp3')
        return path_to_res_mp3_file    

    def bytes_to_wav(self, audiobytes, path_to_res:str) -> str:
        wav_audio = AudioSegment.from_file(io.BytesIO(audiobytes), format="wav")
        wav_audio.export(path_to_res, format="wav")
        return path_to_res
    
    def wav_to_16bytes(self, wav_file_path:str):
        sound = AudioSegment.from_wav(wav_file_path)
        sound = sound.set_frame_rate(16_000)
        sound = sound.set_sample_width(2)
        byte_io = io.BytesIO()
        sound.export(byte_io, format="wav")  # Export sound to BytesIO as a WAV format
        return byte_io.getvalue()
    
    def wav_to_bytes(self, wav_file_path:str):
        sound = AudioSegment.from_wav(wav_file_path)
        byte_io = io.BytesIO()
        sound.export(byte_io, format="wav")  # Export sound to BytesIO as a WAV format
        return byte_io.getvalue()
    