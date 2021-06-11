# Assistant
# Created 6/10/21
#

import pyttsx3
import speech_recognition as sr

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

def listentest():
    query = listen()
    print("User said: {}".format(query))
    speak("User said " + query)

listentest()
