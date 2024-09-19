from pydub import AudioSegment

sound = AudioSegment.from_mp3(r'C:\intern\xtts-2\client\voice_samples\ru\01.mp3')
sound = sound[25_000:100_000]
sound.export(r'C:\intern\xtts-2\client\voice_samples\ru\01_cutted.mp3', 'mp3')