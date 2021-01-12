from gtts import gTTS
import speech_recognition as sr
import wikipedia
import os
from io import BytesIO
from pydub import AudioSegment
from pydub.playback import play
from gsearch.googlesearch import search
import json
import subprocess

class Assistant(object):
    # make a main function to handle input
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.mic = sr.Microphone()

    def speak(self, text):
        mp3 = BytesIO()
        tts = gTTS(text=text, lang='en', slow=False)
        tts.write_to_fp(mp3)
        mp3.seek(0)
        sound = AudioSegment.from_mp3(mp3)
        play(sound)

    def listen(self):
        print("Assistant is listening...")
        with self.mic as source:
            audio = self.recognizer.listen(source)
        voice_input = self.recognizer.recognize_google(audio)
        voice_input = voice_input.split(" ", 1)
        return voice_input

    def google_search(self, query):
        res = search(query)
        for i in range(0, len(res['items']) - 1):
            item = {'title': res['items'][i]['title'], 'link': res['items'][i]['link']}
            print(item['title'] + " " + item['link'])
        self.speak(f"Google results for {query}")

    def wiki_search(self, query):
        res = wikipedia.summary(query, sentences=2)
        os.system("clear")
        self.speak(res)

    def open_app(self, query):
        subprocess.Popen(query)


if __name__ == '__main__':
    assistant = Assistant()
    command = assistant.listen()
    if command[0].lower() == "google":
        query = command[1]
        assistant.google_search(query.lower())
    elif command[0].lower() == "wikipedia":
        query = command[1]
        assistant.wiki_search(query)
    elif command[0].lower() == "open":
        query = command[1].lower()
        assistant.open_app(query)
    else:
        print("feature not yet supported")
