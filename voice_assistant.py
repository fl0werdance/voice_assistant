from gtts import gTTS
import speech_recognition as sr
import wikipedia
import os
from io import BytesIO
from pydub import AudioSegment
from pydub.playback import play
import requests

class Assistant(object):
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.mic = sr.Microphone()

    def listen(self):
        with self.mic as source:
            audio = self.recognizer.listen(source)
        voice_input = self.recognizer.recognize_google(audio)
        voice_input = voice_input.split(" ")
        return voice_input

    def google_search(self):
        print("google search")

    def wiki_search(self, search_term):
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
    command = assistant.listen()
    print(command)
    print(command[1], command[2])
    if command[0].lower() == "google":
        assistant.google_search()
    elif command[0].lower() == "wikipedia":
        query = command[1] + " " + command[2]
        assistant.wiki_search(query)
    else:
        print("feature not yet supported")
