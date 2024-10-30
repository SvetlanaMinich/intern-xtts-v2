from pydub import AudioSegment

sound = AudioSegment.from_mp3(r'C:\intern\xtts-2\voice_samples\woman.mp3')
sound = sound[:5_000]
sound.export(r'C:\intern\xtts-2\server_mms\rvc_try\woman5.wav', format='wav')

sound = AudioSegment.from_mp3(r'C:\intern\xtts-2\voice_samples\Alessia_Cara.mp3')
sound = sound[:5_000]
sound.export(r'C:\intern\xtts-2\server_mms\rvc_try\alessia5.wav', format='wav')