from gtts import gTTS
import speech_recognition as sr
import wikipedia
import os
from io import BytesIO
from pydub import AudioSegment
from pydub.playback import play

recognizer = sr.Recognizer()
mic = sr.Microphone()

with mic as source:
    audio = recognizer.listen(source)

voice_input = recognizer.recognize_google(audio)
voice_input = voice_input.split("search for")
search_term = voice_input[1].strip(" ")
res = wikipedia.page(search_term).content[0:195]
os.system("clear")
print(res)
mp3_fp = BytesIO()
tts = gTTS(text=res, lang='en')
tts.write_to_fp(mp3_fp)
mp3_fp.seek(0)
sound = AudioSegment.from_mp3(mp3_fp)
play(sound)
