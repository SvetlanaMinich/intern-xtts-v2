# import soundfile as sf

# f_info = sf.info(r'C:\intern\xtts-2\def.wav')
# print(f_info.samplerate)


# from pydub import AudioSegment

# sound = AudioSegment.from_mp3(r'C:\intern\xtts-2\voice_samples\Usachev.mp3')
# sound = sound[:10_000]
# sound.export(r'C:\intern\xtts-2\voice_samples\Usachev 10.mp3', format='mp3')

from pydub import AudioSegment

sound = AudioSegment.from_mp3(r'C:\intern\xtts-2\voice_samples\Usachev 10.mp3')
sound.export(r'C:\intern\xtts-2\voice_samples\Usachev 10.wav', format='wav')