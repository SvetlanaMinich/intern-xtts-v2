from pydub import AudioSegment
import io


class AudioConverter:
    def wav_to_mp3(self, path_to_wav_file:str, path_to_res_mp3_file:str):
        '''Converting .wav file from <path_to_wav_file> path to .mp3 format.
        Saving result to <path_to_res_mp3_file> path. Return <path_to_res_mp3_file> path.'''
        sound = AudioSegment.from_wav(path_to_wav_file)
        sound.export(path_to_res_mp3_file, format='mp3')
        return path_to_res_mp3_file
    

    def mp3_to_wav(self, path_to_mp3_file:str, path_to_res_wav_file:str):
        '''Converting .mp3 file from <path_to_mp3_file> path to .wav format.
        Saving result to <path_to_res_wav_file> path. Return <path_to_res_wav_file> path.'''
        sound = AudioSegment.from_mp3(path_to_mp3_file)
        sound.export(path_to_res_wav_file, format='wav')
        return path_to_res_wav_file
    
    
    def bytes_from_mp3_to_mp3(self, audio_bytes, path_to_result_mp3_file:str):
        '''Converting bytes list to file with .mp3 format.
        Saving result to <path_to_res_mp3_file> path. Return <path_to_res_mp3_file> path.'''
        sound = AudioSegment.from_file(io.BytesIO(audio_bytes), format='mp3')
        sound.export(path_to_result_mp3_file, format='mp3')
        return path_to_result_mp3_file
    

    def bytes_from_mp3_to_wav(self, audio_bytes, path_to_result_wav_file:str):
        '''Converting bytes list to file with .wav format.
        Saving result to <path_to_res_wav_file> path. Return <path_to_res_wav_file> path.'''
        sound = AudioSegment.from_file(io.BytesIO(audio_bytes), format='mp3')
        sound.export(path_to_result_wav_file, format='wav')
        return path_to_result_wav_file
    
    