from pydub import AudioSegment

# 获取音频对象
song = AudioSegment.from_mp3("./Audio/audio_mangzhong.mp3", "mp3")

song.export("./Audio/ss.mp4", format="mp4")