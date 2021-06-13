# Virtuassistant
# Created 6/10/21

# Imports

from bs4 import BeautifulSoup
import pyttsx3
import speech_recognition as sr
import requests

# Definitions
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36'}
URL = ''

# Initialize Text to Speech
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

# Speak Function
def speak(audio):
    engine.say(audio)
    engine.runAndWait()

# Listen to user input
def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        speak("I'm Listening")
        print("Listening...")
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)
    try:
        print("Recognizing...")
        speak('Recognizing')
        query = r.recognize_google(audio, language='en-US')
    except sr.UnknownValueError:
        print("I cannot hear you")
        speak("I cannot hear you")
    except sr.RequestError:
        print("Say that again please")
        speak("Say that again please")
        return "None"
    return query

def listen_test():
    query = listen()
    print("User said: {}".format(query))
    speak("User said " + query)

def voice_selection():
    select = listen()
    if select == "1":
        print("Listen Test")
        listen_test()
    elif select == "2":
        speak("Have a nice day.")
    elif select == "location":
        print(get_location())

def get_location():
    try:
        URL = 'https://iplocation.com/'
        page = requests.get(URL, headers=headers)
        soup = BeautifulSoup(page.content, 'html.parser')
        city = soup.find(class_='city').get_text()
        region = soup.find(class_='region_name').get_text()
        country = soup.find(class_='country_name').get_text()
        return city, region, country
    except Exception as e:
        print('Error: location could not be retrieved.')
        speak('Error, unknown location')

voice_selection()
