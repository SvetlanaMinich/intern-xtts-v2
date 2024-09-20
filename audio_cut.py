from pydub import AudioSegment

sound = AudioSegment.from_mp3(r'C:\intern\xtts-2\voice_samples\en\KENDALL JENNER.mp3')
sound = sound[:len(sound)/2]
sound.export(r'C:\intern\xtts-2\voice_samples\en\KENDALL JENNER 12_sec.mp3', 'mp3')