# Virtuassistant
# Created 6/10/21

# Imports

from bs4 import BeautifulSoup
from googlesearch import search
from datetime import datetime
import pyttsx3
import speech_recognition as sr
import requests, json
import config
import socket


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
        r.pause_threshold = .5
        r.adjust_for_ambient_noise(source, duration=.5)
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
    elif "weather" in user_input:
        weather()
    elif "Bitcoin" in user_input:
        btc_price()
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
        speak("Good Afternoon" + socket.gethostname())
    else:
        speak("Good Morning" + socket.gethostname())

def get_location():
    try:
        URL = 'https://iplocation.com/'
        page = requests.get(URL, headers=headers)
        soup = BeautifulSoup(page.content, 'html.parser')
        city = soup.find(class_='city').get_text()
        region = soup.find(class_='region_name').get_text()
        country = soup.find(class_='country_name').get_text()
        latitude = soup.find(class_='lat').get_text()
        longitude = soup.find(class_='lng').get_text()
        return city, region, country, latitude, longitude
    except Exception as e:
        print('Error: location could not be retrieved.')
        speak('Error, unknown location')

def google_search(user_input):
    link = []
    for i in search(user_input, tld="ca", stop=10, pause=2):
        link.append(i)
    return link

def btc_price():
    try:
        URL = 'https://api.coindesk.com/v1/bpi/currentprice.json'
        response = requests.get(URL).json()
        print(response["bpi"]["USD"]["rate"])
    except Exception as e:
        print('Error: price could not be retrieved.')
        speak('Error')



def weather():
    try:
        api_key = config.wea_api_key # Must have API key for OpenWeatherMap located in config.py
        location = get_location()
        lat = location[3]
        lon = location[4]
        base_url = 'http://api.openweathermap.org/data/2.5/weather?'
        full_url = base_url + 'lat=' + lat + '&lon=' + lon + '&appid=' + api_key
        response = requests.get(full_url).json()

        if response["cod"] != "404":

            main = response["main"]
            temp = main["temp"] # Returns temp in Kelvin
            temp = int((temp - 273.15) * 9/5 + 32) # Kelvin to Fahrenheit
            w = response["weather"]
            desc = w[0]["description"] # Returns weather description

            print("Temperature: " + str(temp) + "\nDescription: " + str(desc))
            speak(str(temp) + " degrees Fahrenheit")
            speak(str(desc))

        else:
            return False

    except Exception as e:
        print('Error: weather could not be retrieved.')
        speak('Error')

# Main

greeting()
voice_selection()
