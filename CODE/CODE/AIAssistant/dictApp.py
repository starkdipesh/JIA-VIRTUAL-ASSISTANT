
import pyttsx3
import os
import pyautogui
import webbrowser
from time import sleep
import speech_recognition as sr
def Listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening......")
        r.pause_threshold = 1
        r.energy_threshold = 300
        audio = r.listen(source,0,4)
    try:
        print("Understanding..")
        query  = r.recognize_google(audio,language='en-in')
        print(f"You Said: {query}\n")
    except Exception as e:
        print("Say that again",e)
        return "None"
    return query

engine = pyttsx3.init()  # Let pyttsx3 choose the driver automatically
voices = engine.getProperty('voices')
engine.setProperty("voice", voices[1].id)  # Select a different voice (if available)
rate = engine.setProperty('rate', 150)  # Set speech rate
def on_speech_finished(name, completed):
    # This callback is triggered when speech is finished
    if completed:
        print("Speech finished.")  # You can use this to indicate that speech is done

def speak(audio):
    engine.connect('finished-utterance', on_speech_finished)  # Connect the callback
    engine.say(audio)
    engine.runAndWait()  # Wait for speech to finish before continuing

# dict_app={"commandprompt":"cmd","paint":"paint","word":"winword","excel":"excel","chrome":"chrome","vscode":"code","powerpoint":"powerpnt"}

def openAppWeb(query):
    print("Launching sir.....")
    speak("Launching sir.")
    sleep(2)
    if ".com" in query or ".co.in" in query or ".org" in query:
        query=query.replace("open","")
        query=query.replace("jia","")
        query=query.replace("launch","")
        query=query.replace(" ","")
        webbrowser.open(f"https://www.{query}")
        sleep(3)
        speak("Website is opened, what else i can do for you")
    else:
        query=query.replace("open","")
        query=query.replace("jia","")
        query=query.replace("app","")
        query=query.replace("launch","")
        # query=query.replace(" ","")
        pyautogui.press("win")
        sleep(1)
        pyautogui.write(query)
        sleep(1)
        pyautogui.press("enter")
        # Keys=list(dict_app.keys())
        # for app in Keys:
        #     if app in query:
        #         os.system(f"start {dict_app[app]}")
        speak("App is opened, what else i can do for you")
        sleep(2)

def closeAppWeb(query):
    query=query.replace("close","")
    speak(f"Closing {query} sir")
    pyautogui.hotkey("alt","f4")
    # key=list(dict_app.keys())
    # for app in key:
    #     if app in query:
    #         os.system(f"taskkill /f /im {dict_app[app]}.exe")
    speak("App is Closed sir, what else i can do for you")

# com=Listen()
# closeAppWeb(com)
