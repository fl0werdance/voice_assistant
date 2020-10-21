from gtts import gTTS
import speech_recognition as sr
import wikipedia
import os
from io import BytesIO
from pydub import AudioSegment
from pydub.playback import play
import requests
from bs4 import BeautifulSoup
# from googlesearch import search

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

    def google_search(self, query):
        url = f"https://google.com/search?q={query}"
        resp = requests.get(url)
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.content, "html.parser")
        results = []
        for g in soup.find_all('h3', class_='r'):
            anchors = g.find_all('a')
            link = g.find('a')['href']
            text = g.find('a').text.strip()
            result = {'text': text, 'link': link}
            results.append(result)
        # print(search(query))

    def wiki_search(self, query):
        res = wikipedia.page(query).content[0:195]
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
    if command[0].lower() == "google":
        query = command[1] + "+" + command[2]
        assistant.google_search(query.lower())
    elif command[0].lower() == "wikipedia":
        query = command[1] + " " + command[2]
        assistant.wiki_search(query)
    else:
        print("feature not yet supported")
