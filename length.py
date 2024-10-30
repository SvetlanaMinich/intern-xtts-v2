from pydub import AudioSegment

for i in range(15):
    sound = AudioSegment.from_wav(f'res/{i}.wav')
    sound.export(f'res/a{i}.mp3', format='mp3')