from gtts import gTTS
import speech_recognition as sr
import wikipedia
import os
from io import BytesIO
from pydub import AudioSegment
from pydub.playback import play

class Assistant(object):
    def __init__(self, audio=None):
        self.recognizer = sr.Recognizer()
        self.mic = sr.Microphone()
        self.audio = audio

    def listen(self):
        with self.mic as source:
            self.audio = self.recognizer.listen(source)
            self.wiki_search()

    def google_search():
        pass

    def wiki_search(self):
        voice_input = self.recognizer.recognize_google(self.audio)
        voice_input = voice_input.split("search for")
        search_term = voice_input[1].strip(" ")
        res = wikipedia.page(search_term).content[0:195]
        os.system("clear")
        mp3 = BytesIO()
        tts = gTTS(text=res, lang='en', slow=False)
        tts.write_to_fp(mp3)
        mp3.seek(0)
        sound = AudioSegment.from_mp3(mp3)
        print(res)
        play(sound)


if __name__ == '__main__':
    assistant = Assistant()
    assistant.listen()
