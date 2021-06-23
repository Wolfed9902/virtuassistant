# Virtuassistant
# Created 6/10/21

# Imports

from bs4 import BeautifulSoup
from googlesearch import search
from datetime import datetime
import pyttsx3
import speech_recognition as sr
import requests


# Definitions

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36'}
URL = ''
running = True

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
    user_input = ""
    try:
        print("Recognizing...")
        speak('Recognizing')
        user_input = r.recognize_google(audio, language='en-US')
    except sr.UnknownValueError:
        print("I cannot hear you")
        speak("I cannot hear you")
    except sr.RequestError:
        print("Say that again please")
        speak("Say that again please")
        return "None"
    return user_input

def listen_test(): # listen/response for testing
    user_input = listen()
    print("User said: {}".format(user_input))
    speak("User said " + user_input)

# -------------Voice Selection-------------- #

def voice_selection():
    global running
    user_input = listen()
    if "listen test" in user_input:
        print("Listen Test")
        listen_test()
    elif "location" in user_input:
        print(get_location())
    elif "time" in user_input:
        current_time = (datetime.now()).strftime("%X") # obtains current time in H,M,S format
        print(current_time)
        speak(current_time)
    elif "search" in user_input:
        user_input = listen()
        print(google_search(user_input))
    elif "quit" or "goodbye" in user_input:
        running = False
        print("Have a nice day.")
        speak("Have a nice day.")

    if (running == True):
        voice_selection()

# ------------------------------------------ #

def greeting():
    greeting_time = (datetime.now()).strftime("%H")
    if int(greeting_time) >= 12:
        speak("Good Afternoon")
    else:
        speak("Good Morning")

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

def google_search(user_input):
    link = []
    for i in search(user_input, tld="ca", stop=10, pause=2):
        link.append(i)
    return link

# Main

greeting()
voice_selection()
