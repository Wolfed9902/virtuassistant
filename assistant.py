# Virtuassistant
# Created 6/10/21
# By Dylan Wolfe (wolfed9902)

# Imports

from bs4 import BeautifulSoup
from googlesearch import search
from datetime import datetime
import pyttsx3
import speech_recognition as sr
import requests, json
import config
import socket
import random


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

# Listen/response for testing

def listen_test():
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
    elif "math" in user_input:
        math_query()
    elif "dice" in user_input:
        result = roll_dice()
        print(result)
        speak(result)
    elif "quit" or "goodbye" in user_input:
        running = False
        print("Have a nice day.")
        speak("Have a nice day.")

    if (running == True):
        voice_selection()

# ------------------------------------------ #

# ----------------Functions----------------- #

def greeting(): # Greets user according to time of day
    greeting_time = (datetime.now()).strftime("%H")
    if int(greeting_time) >= 12:
        print("Good Afternoon " + socket.gethostname())
        speak("Good Afternoon " + socket.gethostname())
    else:
        print("Good Morning " + socket.gethostname())
        speak("Good Morning " + socket.gethostname())


def get_location(): # Retrieves location (city, region, etc)
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

def google_search(user_input): # Performs a google qeury according to input and returns results
    link = []
    for i in search(user_input, tld="ca", stop=10, pause=2):
        link.append(i)
    return link

def roll_dice(): # Selects a random integer from range of 1 to X.
    try:
        print("Number of Sides?")
        speak("How many sides?")
        user_input = listen()
        print('Rolling')
        result = random.randint(1,int(user_input))
        return result

    except Exception as e:
        print('Error: Number of sides must be Integer')
        speak('Error')

def btc_price(): # Returns current price of Bitcoin
    try:
        URL = 'https://api.coindesk.com/v1/bpi/currentprice.json'
        response = requests.get(URL).json()
        print('Current Price [USD, GBP, EUR]:')
        print('$' + response["bpi"]["USD"]["rate"])
        print('£' + response["bpi"]["GBP"]["rate"])
        print('€' + response["bpi"]["EUR"]["rate"])
        print('(Powered by CoinDesk)')

    except Exception as e:
        print('Error: price could not be retrieved.')
        speak('Error')


def weather(): # Returns weather based on location (calls get_location())
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


def math_query(): # Perform simple math operations
    try:
        print("Math(+, -, *, /)")
        user_input = listen()
        sentence = user_input.lower().split()
        if "+" in sentence[1:]:
            first = sentence[sentence.index('+')-1]
            second = sentence[sentence.index('+')+1]
            result = float(first) + float(second)
        elif "-" in sentence[1:]:
            first = sentence[sentence.index('-')-1]
            second = sentence[sentence.index('-')+1]
            result = float(first) - float(second)
        elif "/" in sentence[1:]:
            first = sentence[sentence.index('/')-1]
            second = sentence[sentence.index('/')+1]
            result = float(first) / float(second)
        elif "*" in sentence[1:]:
            first = sentence[sentence.index('*')-1]
            second = sentence[sentence.index('*')+1]
            result = float(first) * float(second)
        print(result)
        speak(str(result))

    except Exception as e:
        print('Error.') # TO-DO: Better error handling and error messages.
        speak('Error')

# ------------------------------------------ #

# ------------------Main-------------------- #

greeting()
voice_selection()
