from gtts import gTTS
import speech_recognition as sr
import wikipedia
import os
from io import BytesIO
from pydub import AudioSegment
from pydub.playback import play
from googleapiclient.discovery import build
from secrets import MY_API_KEY, SEARCH_ENGINE_ID
import json
import subprocess

class Assistant(object):
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.mic = sr.Microphone()

    def listen(self):
        print("Assistant is listening...")
        with self.mic as source:
            audio = self.recognizer.listen(source)
        voice_input = self.recognizer.recognize_google(audio)
        voice_input = voice_input.split(" ", 1)
        return voice_input

    def google_search(self, query):
        service = build("customsearch", "v1", developerKey=MY_API_KEY)
        res = service.cse().list(q=query, cx=SEARCH_ENGINE_ID).execute()
        for i in range(0, len(res['items']) - 1):
            item = {'title': res['items'][i]['title'], 'link': res['items'][i]['link']}
            print(item['title'] + " " + item['link'])
        mp3 = BytesIO()
        answer = f"Google results for {query}"
        tts = gTTS(text=answer, lang='en', slow=False)
        tts.write_to_fp(mp3)
        mp3.seek(0)
        sound = AudioSegment.from_mp3(mp3)
        play(sound)

    def wiki_search(self, query):
        res = wikipedia.summary(query, sentences=2)
        os.system("clear")
        mp3 = BytesIO()
        tts = gTTS(text=res, lang='en', slow=False)
        tts.write_to_fp(mp3)
        mp3.seek(0)
        sound = AudioSegment.from_mp3(mp3)
        print(res)
        play(sound)

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
