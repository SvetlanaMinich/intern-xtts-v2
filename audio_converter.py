from pydub import AudioSegment

sound = AudioSegment.from_wav(r'C:\intern\xtts-2\res\en\The sun sets behind .wav')
sound.export(r'C:\intern\xtts-2\res\en\The sun sets behind .mp3', format='mp3')