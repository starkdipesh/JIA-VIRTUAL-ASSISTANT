# import datetime 
# import os
# from time import sleep
import pyttsx3
# import pygame

# # Initialize pygame mixer
# pygame.mixer.init()

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

# extractedtime = open(fr"Z:\PROJECT_O\CODE\CODE\AlarmText.txt.txt","rt")
# time = extractedtime.read()
# Time = str(time)
# extractedtime.close()

# deletetime = open(fr"Z:\PROJECT_O\CODE\CODE\AlarmText.txt.txt","r+")
# deletetime.truncate(0)
# deletetime.close()

# def ring(time):
#     timeset = str(time)
#     timenow = timeset.replace("jiya","")
#     timenow = timenow.replace("set an alarm","")
#     timenow = timenow.replace(" and ",":")
#     Alarmtime = str(timenow)
#     print(Alarmtime)
#     while True:
#         currenttime = datetime.datetime.now().strftime("%H:%M:%S")
#         if currenttime == Alarmtime:
#             speak("Alarm ringing,sir")
#             # Load and play the music
#             pygame.mixer.music.load(fr"music.mp3")
#             pygame.mixer.music.play()
#             sleep(15)
#             # break
#             exit()

# ring(time)
import time,datetime,playsound

def setalarm(alarmtime):
    print(f"Alarm is set for {alarmtime}")
    while True:
        curenttime=datetime.datetime.now().strftime("%H:%M:%S")
        if curenttime==alarmtime:
            print("Time to wake up!")
            speak("Time to wake up!")
            # play a beep sound 5 times
            for _ in range(5):
                # winsound.Beep(1000, 500)
                playsound.playsound("music.mp3")
                # frequency: 1000Hz, Duration: 500ms 
            break
        time.sleep(1)# Check the time every seconds 

# alarmtime=input("Enter alarm time in HH:MM:SS format:")
# setalarm(alarmtime)
# speak("Alarm is Ringed.")