from kivy.clock import Clock
import mysql.connector as msct
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import *
from kivymd.uix.screenmanager import MDScreenManager
from GreetMe import gretme
from plyer import notification
import speech_recognition as sr 
import pyautogui
import os
import random
import pyttsx3
import requests
from transllate import translategl
import asyncio
from datetime import datetime
from game import game_play
from volumSet import volumedown,volumeup
import languagemodels as lm
from alarm import setalarm
import threading
from time import sleep,time
import playsound
from gemini import isConnect, prompt

class LOGIN(MDScreen): 
    # Login validation and checking user in registered to database or not 
    def validateCredential(self):
        username=self.ids.userName.text
        paswrd=self.ids.pswd.text
        errors=[]
        # validating user Name
        if not username:
            errors.append("User Name Required")
        # validate password
        if not paswrd:
            errors.append("Password is Required")
        elif len(paswrd) < 6 :
            errors.append("Password must be at least 6 character long.")
        if errors:
            error_message='\n'.join(errors)
            self.showAlert("Validation Error",error_message)
        else:
            host='localhost'
            port='3306'
            user='root'
            password=''
            database='AIuser'
            print(f"Connecting to database {database}")
            try:
                mycon=msct.Connect(host=host,port=port,user=user,password=password,database=database)
                print(f"Connection is successfully to db: {database}")
                sqlquery=f"""select * from owner where username='{username}' and pasword='{paswrd}'"""
                myCursor=mycon.cursor()
                myCursor.execute(sqlquery)
                record=myCursor.fetchone()
                if record:
                    if record[0]==username and record[3]==paswrd:
                        self.showAlert("Congratulations","User LoggedIn Successfuly...")
                        # runing tkinter window
                        # threading.Thread(target=self.homePage).start()
                        # running kivymd window
                        self.changingScreen("homepage")
                        print("record matched..")
                    else:
                        self.showAlert("Login Error!","Invalid User Name and Password")
                        print("Record does not match...")
                else:
                    self.showAlert("Login Error!","Record not found...User is Not Registered.")
                    print("Record not found...")
            except msct.Error as msg:
                print(f"Cause for the errror : {msg}")
            finally:
                mycon.close()
                print("Database is closed.")
                
    # changing to another screen
    def changingScreen(self,screnname):
        self.manager.current=screnname

    # creating alert dialog box           
    def showAlert(self,title,message):
        # create the dialog instance 
        self.dialog=MDDialog(
            title=title,
            text=message,
            size_hint=(0.8,1),
            auto_dismiss=False,
            buttons=[
                 MDRoundFlatButton(
                    text= "OK",
                    on_release=self.dismiss_dialog
                 ),
                 MDRoundFlatButton(
                    text= "EXIT",
                    on_release=self.exit_app
                 )
            ]
        )
        # open the dialog 
        self.dialog.open()
    def dismiss_dialog(self,instance):
        self.dialog.dismiss()
    
    def exit_app(self,instance):
        self.dismiss_dialog(instance)
        MDApp.get_running_app().stop()
        
class REGISTER(MDScreen):
    # validating registeration form and register user using database
    def validate_form(self):
        username=self.ids.userName.text
        email=self.ids.emailId.text
        dob=self.ids.dob.text
        pasword=self.ids.pswd.text
        confirmPassword=self.ids.cmpswd.text
        errors=[]

        # validating user Name
        if not username:
            errors.append("User Name Required")
        
        # validate email 
        if not email:
            errors.append("Email ID is Required")
        elif not self.is_valid_email(email):
            errors.append("Invalid Email Address.")

        # validate DateOfBirth
        if not dob:
            errors.append("Date of Birth is Required")
        elif not self.is_valid_date(dob):
            errors.append("Invalid date Format. Use YYYY-MM-DD")

        # validate password
        if not pasword:
            errors.append("Password is Required")
        elif len(pasword) < 6 :
            errors.append("Password must be at least 6 character long.")
        
        # validate confirm password
        if not confirmPassword:
            errors.append("Password Must be ReEntered")
        elif pasword != confirmPassword:
            errors.append("Password Does not matched")

        if errors:
            error_message='\n'.join(errors)
            self.show_error_dialog("Validation Error",error_message)
        else:
            
            host='localhost'
            port='3306'
            user='root'
            password=''
            database='AIuser'
            print(f"Connecting to database {database}")
            try:
                mycon=msct.Connect(host=host,port=port,user=user,password=password,database=database)
                print(f"Connection is successfully to db: {database}")
                sqlquery=f"""insert into owner Values('{username}','{email}','{dob}','{pasword}')"""
                myCursor=mycon.cursor()
                myCursor.execute(sqlquery)
                mycon.commit()
                self.show_error_dialog("Congratulations","User Registered Successfuly...")
                print("Data inserted.")
            except msct.Error as msg:
                print(f"Cause for the errror : {msg}")
            finally:
                mycon.close()
                print("Database is closed.")

    # add further actions upon successfull validation
    def is_valid_email(self,email):
        # simple regex for email validation
        import re
        return re.match(r'^[a-zA-Z0-9._%+-]+@gmail\.com$',email) is not None
    def is_valid_date(self,date):
        # Example date Validation (YYYY-MM-DD)
        try:
            from datetime import datetime
            datetime.strptime(date,'%Y-%m-%d')
            return True
        except ValueError:
            return False
    # alert box to show error occured
    def show_error_dialog(self,title,message):
        # create the dialog instance 
        self.dialog=MDDialog(
            title=title,
            text=message,
            size_hint=(0.8,1),
            auto_dismiss=False,
            buttons=[
                 MDRoundFlatButton(
                    text= "OK",
                    on_release=self.dismiss_dialog
                 ),
                 MDRoundFlatButton(
                    text= "EXIT",
                    on_release=self.exit_app
                 )
            ]
        )
        # open the dialog 
        self.dialog.open()
    def dismiss_dialog(self,instance):
        self.dialog.dismiss()

    def exit_app(self,instance):
        self.dismiss_dialog(instance)
        MDApp.get_running_app().stop()

class HomePage(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._running = False  # Flag to control the thread

    def on_speech_finished(self,name, completed):
        # This callback is triggered when speech is finished
        if completed:
            print("Speech finished.")  # You can use this to indicate that speech is done

    def speak(self,audio):
        engine = pyttsx3.init()  # Let pyttsx3 choose the driver automatically
        voices = engine.getProperty('voices')
        engine.setProperty("voice", voices[1].id)  # Select a different voice (if available)
        rate = engine.setProperty('rate', 150)  # Set speech rate
        engine.connect('finished-utterance', self.on_speech_finished)  # Connect the callback
        engine.say(audio)
        engine.runAndWait()  # Wait for speech to finish before continuing

    def deleteQuerys(self):
        self.ids.query.text = ""
        self.ids.output.text = ""

    def processinput(self):
        userInput = self.ids.query.text
        usertext = userInput.lower()
        if not usertext:
            self.ids.output.text = "Please enter some text."
            # Run speak in a background thread
            threading.Thread(target=self.speak,args=("Please enter some text.",),daemon=True).start()
            return
        else:
            if "greet me" in usertext or "good morning" in usertext or "good afternoon" in usertext or "good evening" in usertext:
                response=gretme()
                self.ids.output.text = response
                threading.Thread(target=self.speak,args=(response,),daemon=True).start()
            # Regular conversation
            elif "hello" in usertext.lower():
                response="Hello Sir, How are you?"
                self.ids.output.text = response
                threading.Thread(target=self.speak,args=(response,),daemon=True).start()
            elif "i am fine" in usertext.lower():
                response="That's great sir, How can I help you."
                self.ids.output.text = response
                threading.Thread(target=self.speak,args=(response,),daemon=True).start()
            elif "how r u" in usertext.lower() or "how are you" in usertext.lower():
                response="Perfect, Sir how are you"
                self.ids.output.text = response
                threading.Thread(target=self.speak,args=(response,),daemon=True).start()
            elif "thank you" in usertext.lower():
                response="You are Wellcome, sir"
                self.ids.output.text = response
                threading.Thread(target=self.speak,args=(response,),daemon=True).start()
            # Self Introduction
            elif "your name" in usertext.lower():
                response="My name is JIYA,Junior Inteligent Assistant,Created by Dipesh Patel."
                self.ids.output.text = response
                threading.Thread(target=self.speak,args=(response,),daemon=True).start()
            # 2. Searching on Google
            elif "google" in usertext.lower():
                from searchNow import searchGoogle
                self.speak("Searching On Google")
                retg=searchGoogle(usertext)
                response=retg
                self.ids.output.text = response
                # searchGoogle(usertext)
            # 2. Searching on Youtube 
            elif "youtube" in usertext.lower():
                from searchNow import searchYoutube
                self.speak("Searching On Youtube")
                rety=searchYoutube(usertext)
                response=rety
                self.ids.output.text = response
                # searchYoutube(usertext)
            # 2. Searching on Wikipedia
            elif "wikipedia" in usertext.lower():
                from searchNow import searchWikipedia
                self.speak("Searching On Wikipedia")
                retw=searchWikipedia(usertext)
                response=retw
                self.ids.output.text = response
                # searchWikipedia(usertext)
            # 3. Checking Temperature
            elif "temperature" in usertext.lower():
                searchT=usertext.replace("check temperature in ","")
                searchT=usertext.replace("what is current temperature in ","")
                searchT=usertext.replace("current temperature in ","")
                searchT=usertext.replace("what is temperature update in ","")
                searchT=usertext.replace("temperature update in ","")
                # city="ahmedabad"
                url=f"https://wttr.in/{searchT}?format=%t"# t returns temperature only
                try :
                    response=requests.get(url)
                    if response.status_code==200:
                        print(f"The current temperature in {searchT} is {response.text.strip()}.")
                        # self.speak(f"The current temperature in {searchT} is {response.text.strip()}.")
                        tem=f"The current temperature in {searchT} is {response.text.strip()}."
                    else:
                        print(f"Failed to fetched temperature of {searchT}")
                        # self.speak(f"Failed to fetched temperature of {searchT}")
                        tem=f"Failed to fetched temperature of {searchT}"
                except Exception as e:
                    print(f"Something went wrong on fetching temperature:{e}")
                    # self.speak(f"Something went wrong on fetching temperature:{e}")
                    tem=f"Something went wrong on fetching temperature:{e}"
                response=tem
                self.ids.output.text = response
                threading.Thread(target=self.speak,args=(response,),daemon=True).start()
            # 3. Checking Weather
            elif "weather" in usertext.lower():
                searchw=usertext.replace("check weather in ","")
                searchw=usertext.replace("what is current weather in ","")
                searchw=usertext.replace("current weather in ","")
                searchw=usertext.replace("what is weather update in ","")
                searchw=usertext.replace("weather update in ","")
                # city="ahmedabad"
                url=f"https://wttr.in/{searchw}?format=%C+%t+%w"#%C for Conditions, %t for temperature, %w for wind
                try :
                    response=requests.get(url)
                    if response.status_code==200:
                        print(f"The current Weather update in {searchw} is {response.text.strip()}.")
                        # self.speak(f"The current Weather update in {searchw} is {response.text.strip()}.")
                        wet=f"The current Weather update in {searchw} is {response.text.strip()}."
                    else:
                        print(f"Failed to fetched weather of {searchw},Please check the city name and try again.")
                        # self.speak(f"Failed to fetched weather of {searchw},Please check the city name and try again.")
                        wet=f"Failed to fetched weather of {searchw},Please check the city name and try again."
                except Exception as e:
                    print(f"Something went wrong on fetching weather:{e}")
                    # self.speak(f"Something went wrong on fetching weather:{e}")
                    wet=f"Something went wrong on fetching weather:{e}"
                response=wet
                self.ids.output.text = response
                threading.Thread(target=self.speak,args=(response,),daemon=True).start()
            # 4. Checking Time
            elif "current time" in usertext.lower():
                strtime=datetime.now().strftime("%H:%M:%S")
                response=f"Sir, Current time is {strtime}"
                self.ids.output.text = response
                threading.Thread(target=self.speak,args=(response,),daemon=True).start()
                print(f"Sir, Current time is {strtime}")
            # 5. Setting An Alarm 
            elif "set an alarm" in usertext.lower():
                # error is occuring fix later
                tm=usertext.replace("set an alarm on ","")
                self.speak(f"Setting alarm on {str(tm)}")
                self.alarm(tm)
                response=f"Alarm is Setted for {tm}"
                self.ids.output.text = response
                threading.Thread(target=self.speak,args=(response,),daemon=True).start()
            # 6. Automating Video Controls
            elif "pause video" in usertext.lower() or "stop video" in usertext.lower():
                pyautogui.press("k")
                response="Video is Paused"
                self.ids.output.text = response
                threading.Thread(target=self.speak,args=(response,),daemon=True).start()
            elif "play video" in usertext.lower() or "start video" in usertext.lower():
                pyautogui.press("k")
                response="Video is Played"
                self.ids.output.text = response
                threading.Thread(target=self.speak,args=(response,),daemon=True).start()
            elif "mute" in usertext.lower() or "turn off voice" in usertext.lower():
                pyautogui.press("m")
                response="Video is Muted"
                self.ids.output.text = response
                threading.Thread(target=self.speak,args=(response,),daemon=True).start()
            elif "volume up" in usertext.lower() or "increase voice" in usertext.lower() or "increase sound" in usertext.lower():
                volumeup()
                response = "Volume is increased"
                self.ids.output.text = response
                threading.Thread(target=self.speak,args=(response,),daemon=True).start()
            elif "volume down" in usertext.lower() or "decrease voice" in usertext.lower() or "decrease sound" in usertext.lower():
                volumedown()
                response="Volume is Decreased"
                self.ids.output.text = response
                threading.Thread(target=self.speak,args=(response,),daemon=True).start()
            # 7. Taking ScreenShot 
            elif "screenshot" in usertext.lower():
                # Random sequence of 5 numbers from 1 to 50, repetitions allowed
                random_sequence = random.choices(range(1, 51), k=5)
                # Store the numbers as a continuous string in a variable
                rancom = "".join(map(str, random_sequence))
                im = pyautogui.screenshot()
                pyautogui.screenshot()
                im.save(f"ss{rancom}.jpg")
                response="Screenshot is saved on similar folder to AIAssistant."
                self.ids.output.text = response
                threading.Thread(target=self.speak,args=(response,),daemon=True).start()
            # 8. Camera Accesing
            elif "click my photo" in usertext.lower():
                pyautogui.press("super")
                pyautogui.typewrite("camera")
                pyautogui.press("enter")
                sleep(2)
                self.speak("SMILE")
                print("SMILE")
                pyautogui.press("enter")
                response="Photo is Clicked, sir"
                self.ids.output.text = response
                threading.Thread(target=self.speak,args=(response,),daemon=True).start()
            # 9. Remembering Tasks
            elif "remember that" in usertext.lower():
                remembermsg=usertext.replace("remember that i","")
                remembermsg=remembermsg.replace("jiya","")
                try:
                    remember=open(fr"AIAssistant\Remember.txt","a")
                    remember.write("\n"+remembermsg)
                    remember.close()
                    response="I have Remembered that "+remembermsg
                    self.ids.output.text = response
                    threading.Thread(target=self.speak,args=(response,),daemon=True).start()
                except:
                    response="File Does not found."
                    self.ids.output.text = response
                    threading.Thread(target=self.speak,args=(response,),daemon=True).start()
            # 9. Reminding Tasks
            elif "what do you remember" in usertext.lower():
                try:
                    getremem=open(fr"AIAssistant\Remember.txt","r")
                    response="You told me to remember that "+getremem.read()
                    self.ids.output.text = response
                    threading.Thread(target=self.speak,args=(response,),daemon=True).start()
                    getremem.close() 
                except:
                    response="File Does not found." 
                    self.ids.output.text = response
                    threading.Thread(target=self.speak,args=(response,),daemon=True).start()
            # 10. Providing News Headlines
            elif "news" in usertext.lower():
                from news import getNews,latestNews
                try:
                    latestNews(usertext)
                except:
                    getNews()
                response="News speaked, anything else, sir"
                self.ids.output.text = response
                threading.Thread(target=self.speak,args=(response,),daemon=True).start()
            # 11. Calculating Values
            elif "calculate" in usertext.lower():
                from calculation import cal
                usertext=usertext.replace("calculate","")
                usertext=usertext.replace("jiya","")
                c=cal(usertext)
                response=c
                self.ids.output.text = response
            # 12. Translating given Statement  
            elif "translate" in usertext.lower():
                self.speak("Speak Statement that you want to get Translated.")
                cm=self.Listen()
                # Run the translation function
                try:
                    tl=asyncio.run(translategl(cm))
                    response="Translated text: "+tl
                    self.ids.output.text = response
                except Exception as e:
                    print("Error occurred:", e)
                    response="Error occured:"+e
                    self.ids.output.text = response
                    threading.Thread(target=self.speak,args=(response,),daemon=True).start()
            # 13. Shutdown the System
            elif "shutdown" in usertext.lower():
                self.speak("Are you sure you want to shutdown")
                shutdown=self.Listen()
                # shutdown=input("Enter Your Choice:")
                if "yes" in shutdown:
                    response="System is Turning Off Sir, GoodBye"
                    self.ids.output.text = response
                    threading.Thread(target=self.speak,args=(response,),daemon=True).start()
                    os.system("shutdown /s /t 1")
                elif "no" in shutdown:
                    response= "Shutdown Process is Stoped, sir." 
                    self.ids.output.text = response
                    threading.Thread(target=self.speak,args=(response,),daemon=True).start()
            # 14. Opening Applications and Websites                
            elif "open" in usertext.lower():
                from dictApp import openAppWeb
                openAppWeb(usertext)
                response="App is Opened."
                self.ids.output.text = response
            # 15. Closing Applications and Websites
            elif "close" in usertext.lower():
                from dictApp import closeAppWeb
                closeAppWeb(usertext)
                response="App is closed."
                self.ids.output.text = response
            # 16. Checking Internet Speed
            elif "internet speed" in usertext.lower():
                url="https://www.google.com"
                try:
                    start=time()
                    reponse=requests.get(url)
                    end=time()
                    if reponse.status_code==200:
                        latency=(end-start)*1000
                        print(f"Speed Of Internet is {latency:.2f} mbps")
                        response=f"Speed Of Internet is {latency:.2f} mbps"
                        self.ids.output.text = response
                        threading.Thread(target=self.speak,args=(response,),daemon=True).start()
                    else:
                        print(f"Failed to connect. Status code:{reponse.status_code}")
                        response=f"Failed to connect. Status code:{reponse.status_code}"
                        self.ids.output.text = response
                        threading.Thread(target=self.speak,args=(response,),daemon=True).start()
                except Exception as e:
                    print(f"Error ocured: {e}")
            # 17. Playing Rock Paper Scissor Game
            elif "game" in usertext.lower():
                response="Game Can only Playable on Talking Mode."
                self.ids.output.text = response
                # game_play()
                threading.Thread(target=self.speak,args=(response,),daemon=True).start()
            # 18. Scheduling Day 
            elif "schedule my day" in usertext.lower():
                tasks = [] #Empty list 
                self.ids.output.text = "Do you want to clear old tasks (Plz speak YES or NO)"
                self.speak("Do you want to clear old tasks (Plz speak YES or NO)")
                print("Do you want to clear old tasks (Plz speak YES or NO)")
                query = self.Listen()
                # query =input()
                if "yes" in query:
                    file = open("tasks.txt","w")
                    file.write(f"")
                    file.close()
                    self.ids.output.text ="Give number of tasks"
                    self.speak("Give number of tasks ")
                    num=self.Listen()
                    num=num.replace("one","1")
                    num=num.replace("two","2")
                    num=num.replace("three","3")
                    num=num.replace("four","4")
                    num=num.replace("five","5")
                    num=num.replace("six","6")
                    num=num.replace("seven","7")
                    num=num.replace("eight","8")
                    num=num.replace("nine","9")
                    num=num.replace("ten","10")
                    no_tasks = int(num)
                    i = 0
                    for i in range(no_tasks):
                        self.ids.output.text ="Speak the task"
                        self.speak("Speak the task ")
                        task=self.Listen()
                        tasks.append(task)
                        file = open("tasks.txt","a")
                        file.write(f"{i}. {tasks[i]}\n")
                        file.close()
                    response="Schedule is Setted"
                    self.ids.output.text =response
                    threading.Thread(target=self.speak,args=(response,),daemon=True).start()
                elif "no" in query:
                    i = 0
                    self.ids.output.text ="Give number of tasks"
                    self.speak("Give number of tasks ")
                    num=self.Listen()
                    num=num.replace("one","1")
                    num=num.replace("two","2")
                    num=num.replace("three","3")
                    num=num.replace("four","4")
                    num=num.replace("five","5")
                    num=num.replace("six","6")
                    num=num.replace("seven","7")
                    num=num.replace("eight","8")
                    num=num.replace("nine","9")
                    num=num.replace("ten","10")
                    no_tasks = int(num)
                    for i in range(no_tasks):
                        self.ids.output.text ="Speak the tasks"
                        self.speak("Speak the task ")
                        task=self.Listen()
                        tasks.append(task)
                        file = open("tasks.txt","a")
                        file.write(f"{i}. {tasks[i]}\n")
                        file.close()
                    response="Schedule is Setted."
                    self.ids.output.text = response
                    threading.Thread(target=self.speak,args=(response,),daemon=True).start()
            # Show My Schedule using Desktop Notification Function :-
            elif "show my schedule" in usertext.lower():
                file = open("tasks.txt","r")
                content = file.read()
                file.close()
                playsound.playsound("music.mp3")
                notification.notify(
                    title = "My schedule :-",
                    message = content,
                    timeout = 15
                    )
                response=content
                self.ids.output.text =response
                threading.Thread(target=self.speak,args=(response,),daemon=True).start()
            # 19. Turning Off The Assistant
            elif "go to rest" in usertext.lower() or "go for rest" in usertext.lower() or "over and out" in usertext.lower():
                hour=datetime.now().strftime("%H")
                if int(hour)>6 and int(hour)<18:
                    response=f"Going for deep sleep sir, have a good day"
                    self.ids.output.text = response
                    self.speak(response)
                else:
                    response=f"Going for deep sleep sir, Good Night"
                    self.ids.output.text = response
                    self.speak(response)
                # Code to Destroy Kivy Window
                MDApp.get_running_app().stop()
            # 20. Replying by llm module if usertext doesn't match to any Condition
            else:
                if isConnect():
                    if usertext:
                        self.speak("let me think boss.")
                        response=prompt(usertext)
                    else:
                        threading.Thread(target=self.speak,args=("Boss you have not speaked with me, what happened.",),daemon=True).start()
                else:
                    if usertext:
                        self.speak("let me think boss.") 
                        response = lm.do(usertext)
                    else:
                        threading.Thread(target=self.speak,args=("Boss you have not speaked with me, what happened.",),daemon=True).start()
                response=response.replace("*","")
                response=response.replace("'''","")
                response=response.replace("'''","")
                # Run speak in a background thread
                self.ids.output.text = response
                threading.Thread(target=self.speak,args=(response,),daemon=True).start()

    # Alarm Function
    def alarm(self,tm):
        timeset = str(tm)
        timenow = timeset.replace("jiya","")
        timenow = timenow.replace("set an alarm","")
        timenow = timenow.replace(" and ",":")
        Alarmtime = str(timenow)
        threading.Thread(target=setalarm,args=(Alarmtime,)).start()

    # online Recognition 
    def Listen(self):
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
    
    def alarm(self,tm):
        timeset = str(tm)
        timenow = timeset.replace("jiya","")
        timenow = timenow.replace("set an alarm","")
        timenow = timenow.replace(" and ",":")
        Alarmtime = str(timenow)
        threading.Thread(target=setalarm,args=(Alarmtime,)).start()

    def talkOnline(self):
        try:
            while self._running:
                # self.speak("I am ready to Assist you sir.")
                # Read audio data from microphone
                usertext=self.Listen()
                # 1. hot ward detection
                if "wake up" in usertext.lower():
                    res=gretme()
                    self.speak(res)
                    while self._running:
                        usertext=self.Listen().lower()
                        if "go to sleep" in usertext.lower() or "go for sleep" in usertext.lower():
                            self.speak("Ok Sir, You Can Call me any time.")
                            self._running=False
                            sleep(1)
                            break
                        elif "stop listening" in usertext.lower():
                            self._running=False
                            break
                        elif "switch to text input page" in usertext.lower():
                            self.changingScreen('homepage')
                            self.speak("We are now on homepage, i will accept input by using keyboard.")
                            self._running=False
                            break
                        # Regular conversation
                        elif "hello" in usertext.lower():
                            self.speak("Hello Sir, How are you?")
                            sleep(1)
                        elif "i am fine" in usertext.lower():
                            self.speak("That's great sir, How can I help you.")
                            sleep(1)
                        elif "how r u" in usertext.lower() or "how are you" in usertext.lower():
                            self.speak("Perfect ,Sir how are you")
                            sleep(1)
                        elif "thank you" in usertext.lower():
                            self.speak("You are Wellcome, sir")
                            sleep(1)
                        # Self Introduction
                        elif "your name" in usertext.lower():
                            self.speak("My name is JIYA,Junior Inteligent Assistant,Created by Dipesh Patel.")
                        # 2. Searching on Google
                        elif "google" in usertext.lower():
                            from searchNow import searchGoogle
                            self.speak("Searching On Google")
                            searchGoogle(usertext)
                            sleep(1)
                            # searchGoogle(usertext)
                        # 2. Searching on Youtube 
                        elif "youtube" in usertext.lower():
                            from searchNow import searchYoutube
                            self.speak("Searching On Youtube")
                            searchYoutube(usertext)
                            sleep(1)
                            # searchYoutube(usertext)
                        # 2. Searching on Wikipedia
                        elif "wikipedia" in usertext.lower():
                            from searchNow import searchWikipedia
                            self.speak("Searching On Wikipedia")
                            try:
                                searchWikipedia(usertext)
                            except Exception as e:
                                self.speak()
                            sleep(1)
                            # searchWikipedia(usertext)
                        # 3. Checking Temperature
                        elif "temperature" in usertext.lower():
                            self.speak("Where's Temperature you wan't to know.")
                            sleep(1)
                            searchT=self.Listen()
                            sleep(1)
                            # city="ahmedabad"
                            url=f"https://wttr.in/{searchT}?format=%t"# t returns temperature only
                            try :
                                response=requests.get(url)
                                if response.status_code==200:
                                    print(f"The current temperature in {searchT} is {response.text.strip()}.")
                                    self.speak(f"The current temperature in {searchT} is {response.text.strip()}.")
                                else:
                                    print(f"Failed to fetched temperature of {searchT}")
                                    self.speak(f"Failed to fetched temperature of {searchT}")
                            except Exception as e:
                                print(f"Something went wrong on fetching temperature:{e}")
                                self.speak(f"Something went wrong on fetching temperature:{e}")
                            sleep(1)
                        # 3. Checking Weather
                        elif "weather" in usertext.lower():
                            self.speak("Where's Weather you wan't to know.")
                            sleep(1)
                            searchw=self.Listen()
                            sleep(1)
                            # city="ahmedabad"
                            url=f"https://wttr.in/{searchw}?format=%C+%t+%w"#%C for Conditions, %t for temperature, %w for wind
                            try :
                                response=requests.get(url)
                                if response.status_code==200:
                                    print(f"The current Weather update in {searchw} is {response.text.strip()}.")
                                    self.speak(f"The current Weather update in {searchw} is {response.text.strip()}.")
                                else:
                                    print(f"Failed to fetched weather of {searchw},Please check the city name and try again.")
                                    self.speak(f"Failed to fetched weather of {searchw},Please check the city name and try again.")
                            except Exception as e:
                                print(f"Something went wrong on fetching weather:{e}")
                                self.speak(f"Something went wrong on fetching weather:{e}")
                            sleep(1)
                        # 4. Checking Time
                        elif "current time" in usertext.lower():
                            strtime=datetime.now().strftime("%H:%M:%S")
                            self.speak(f"Sir, Current time is {strtime}")
                            print(f"Sir, Current time is {strtime}")
                            sleep(1)
                        # 5. Setting An Alarm 
                        elif "set an alarm" in usertext.lower():
                            # error is occuring fix later
                            self.speak(f"Setting the Alarm time format will be 10 and 10 and 10.")
                            self.speak(f"Sir,please tell the time for alarm.")
                            sleep(1)
                            tm=self.Listen()
                            self.speak(f"Setting alarm on {str(tm)}")
                            sleep(1)
                            self.alarm(tm)
                            sleep(1)
                            self.speak(f"Alarm is Setted ")
                            sleep(1)
                        # 6. Automating Video Controls
                        elif "pause video" in usertext.lower() or "stop video" in usertext.lower():
                            pyautogui.press("k")
                            self.speak("Video Paused")
                        elif "play video" in usertext.lower() or "start video" in usertext.lower():
                            pyautogui.press("k")
                            self.speak("Video Played")
                        elif "mute" in usertext.lower() or "turn off voice" in usertext.lower():
                            pyautogui.press("m")
                            self.speak("Video muted")
                        elif "volume up" in usertext.lower() or "increase voice" in usertext.lower() or "increase sound" in usertext.lower():
                            volumeup()
                            self.speak("Volume is increased")
                        elif "volume down" in usertext.lower() or "decrease voice" in usertext.lower() or "decrease sound" in usertext.lower():
                            volumedown()
                            self.speak("Volume is Decreased")
                        # 7. Taking ScreenShot 
                        elif "screenshot" in usertext.lower():
                            # Random sequence of 5 numbers from 1 to 50, repetitions allowed
                            random_sequence = random.choices(range(1, 51), k=5)
                            # Store the numbers as a continuous string in a variable
                            racom = "".join(map(str, random_sequence))
                            im = pyautogui.screenshot()
                            pyautogui.screenshot()
                            im.save(f"ss{racom}.jpg")
                            self.speak("Screenshot is saved on similar folder to AIAssistant.")
                        # 8. Camera Accesing
                        elif "click my photo" in usertext.lower():
                            pyautogui.press("super")
                            pyautogui.typewrite("camera")
                            pyautogui.press("enter")
                            sleep(2)
                            self.speak("SMILE")
                            print("SMILE")
                            pyautogui.press("enter")
                        # 9. Remembering Tasks
                        elif "remember that" in usertext.lower():
                            remembermsg=usertext.replace("remember that i","")
                            remembermsg=remembermsg.replace("jiya","")
                            self.speak("I have Remembered that "+remembermsg)
                            try:
                                remember=open(fr"AIAssistant\Remember.txt","a")
                                remember.write("\n"+remembermsg)
                                remember.close()
                            except:
                                self.speak("File Does not found.")
                        # 9. Reminding Tasks
                        elif "what do you remember" in usertext.lower():
                            try:
                                getremem=open(fr"AIAssistant\Remember.txt","r")
                                self.speak("You told me to remember that "+getremem.read())
                                getremem.close() 
                            except:
                                self.speak("File Does not Found.") 
                        # 10. Providing News Headlines
                        elif "news" in usertext.lower():
                            from news import getNews,latestNews
                            try:
                                latestNews(usertext)
                            except:
                                getNews()
                        # 11. Calculating Values
                        elif "calculate" in usertext.lower():
                            from calculation import calc
                            usertext=usertext.replace("calculate","")
                            usertext=usertext.replace("jiya","")
                            calc(usertext)   
                            sleep(1)
                        # 12. Translating given Statement  
                        elif "translate" in usertext.lower():
                            self.speak("Give Statement that you want to get Translated.")
                            cm=self.Listen()
                            # Run the translation function
                            try:
                                asyncio.run(translategl(cm))
                            except Exception as e:
                                print("Error occurred:", e)
                        # 13. Shutdown the System
                        elif "shutdown" in usertext.lower():
                            self.speak("Are you sure you want to shutdown")
                            shutdown=self.Listen()
                            # shutdown=input("Enter Your Choice:")
                            if "yes" in shutdown:
                                self.speak("System is Turning Off Sir , GoodBye")
                                os.system("shutdown /s /t 1")
                            elif "no" in shutdown:
                                self.speak("Shutdown Process is Stoped, sir.")  
                        # 14. Opening Applications and Websites                
                        elif "open" in usertext.lower():
                            from dictApp import openAppWeb
                            openAppWeb(usertext)
                            sleep(1)
                        # 15. Closing Applications and Websites
                        elif "close" in usertext.lower():
                            from dictApp import closeAppWeb
                            closeAppWeb(usertext)
                            sleep(1)
                        # 16. Checking Internet Speed
                        elif "internet speed" in usertext.lower():
                            url="https://www.google.com"
                            try:
                                start=time()
                                reponse=requests.get(url)
                                end=time()
                                if reponse.status_code==200:
                                    latency=(end-start)*1000
                                    print(f"Speed Of Internet is {latency:.2f} mbps")
                                    response=f"Speed Of Internet is {latency:.2f} mbps"
                                    self.speak(response)
                                else:
                                    print(f"Failed to connect. Status code:{reponse.status_code}")
                                    response=f"Failed to connect. Status code:{reponse.status_code}"
                                    self.speak(response)
                            except Exception as e:
                                print(f"Error ocured: {e}")
                                self.speak(f"Error Occured: {e}")
                        # 17. Playing Rock Paper Scissor Game
                        elif "game" in usertext.lower():
                            game_play()
                        # 18. Scheduling Day 
                        elif "schedule my day" in usertext.lower():
                            tasks = [] #Empty list 
                            self.speak("Do you want to clear old tasks (Plz speak YES or NO)")
                            print("Do you want to clear old tasks (Plz speak YES or NO)")
                            query = self.Listen().lower()
                            # query =input()
                            if "yes" in query:
                                file = open("tasks.txt","w")
                                file.write(f"")
                                file.close()
                                self.speak("Give number of tasks ")
                                num=self.Listen()
                                num=num.replace("one","1")
                                num=num.replace("two","2")
                                num=num.replace("three","3")
                                num=num.replace("four","4")
                                num=num.replace("five","5")
                                num=num.replace("six","6")
                                num=num.replace("seven","7")
                                num=num.replace("eight","8")
                                num=num.replace("nine","9")
                                num=num.replace("ten","10")
                                no_tasks = int(num)
                                i = 0
                                for i in range(no_tasks):
                                    self.speak("Enter the task ")
                                    task=self.Listen()
                                    tasks.append(task)
                                    file = open("tasks.txt","a")
                                    file.write(f"{i}. {tasks[i]}\n")
                                    file.close()
                            elif "no" in query:
                                i = 0
                                self.speak("Give number of tasks ")
                                num=self.Listen()
                                num=num.replace("one","1")
                                num=num.replace("two","2")
                                num=num.replace("three","3")
                                num=num.replace("four","4")
                                num=num.replace("five","5")
                                num=num.replace("six","6")
                                num=num.replace("seven","7")
                                num=num.replace("eight","8")
                                num=num.replace("nine","9")
                                num=num.replace("ten","10")
                                no_tasks = int(num)
                                for i in range(no_tasks):
                                    self.speak("Enter the task ")
                                    task=self.Listen()
                                    tasks.append(task)
                                    file = open("tasks.txt","a")
                                    file.write(f"{i}. {tasks[i]}\n")
                                    file.close()
                        # Show My Schedule using Desktop Notification Function :-
                        elif "show my schedule" in usertext.lower():
                            file = open("tasks.txt","r")
                            content = file.read()
                            file.close()
                            playsound.playsound("music.mp3")
                            notification.notify(
                                title = "My schedule :-",
                                message = content,
                                timeout = 15
                                )
                            self.speak(content)
                        # 19. Turning Off The Assistant
                        elif "go for rest" in usertext.lower() or "go to rest" in usertext.lower() or "over and out" in usertext.lower():
                            hour=datetime.now().strftime("%H")
                            if int(hour)>6 and int(hour)<18:
                                self.speak(f"Going for deep sleep sir, have a good day")
                            else:
                                self.speak(f"Going for deep sleep sir, Good Night")
                            # Code to Destroy Kivy Window
                            MDApp.get_running_app().stop()
                        # 20. Replying by llm module if usertext doesn't match to any Condition
                        else:
                            if isConnect():
                                if usertext:
                                    self.speak("let me think boss.") 
                                    response=prompt(usertext)
                                else:
                                    self.speak("Boss you have not speaked with me, what happened.")
                            else:
                                if usertext:
                                    self.speak("let me think boss.") 
                                    response = lm.do(usertext)
                                else:
                                    self.speak("Boss you have not speaked with me, what happened.")
                            response=response.replace("*","")
                            # Run speak in a background thread
                            self.speak(response)     
        except Exception as e:
            print(f"Error Occured: {e}")

    def go_to_talk(self):
        # Switch to talk screen
        self.manager.current = 'talkpage'
        if isConnect():
            """ Start a background thread that will run a while loop."""
            self._running = True  # Set the flag to True to allow the loop to run
            self._thread =threading.Thread(target=self.talkOnline)
            self._thread.start()
            
        else:
            print("I am offline and cannot able to hear you please connect to internet then try")
            threading.Thread(target=self.speak,args=("I am Offline And Cannot Able to Hear you Please Connect to internet and then try.",),daemon=True).start()

    # changing to another screen
    def changingScreen(self,screnname):
        self.manager.current=screnname

    # def loadAssistant(self):
    #     self.changingScreen('talkpage')
    #     # Offline Recognition
    #     # threading.Thread(target=self.talkToJia).start()
    #     # Online Recognition
    #     threading.Thread(target=self.talkOnline).start()

class TalkPage(MDScreen):
    video_initialized = False
    
    def on_enter(self):
        # Start video when screen opens
        if not self.video_initialized:
            self.init_video()
        self.ids.bg_video.state = 'play'
    
    def on_leave(self):
        # Pause video when leaving screen
        self.ids.bg_video.state = 'stop'
    
    def init_video(self):
        # Initialize video widget
        video = self.ids.bg_video
        video.source = 'EnergyBombing.mp4'  # Your video path
        video.options = {'eos': 'loop'}  # Loop video
        video.allow_stretch = True
        video.keep_ratio = False
        self.video_initialized = True
   
class JIA(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        screen_manager = MDScreenManager()
        screen_manager.add_widget(LOGIN(name='login'))
        screen_manager.add_widget(REGISTER(name='register'))
        screen_manager.add_widget(HomePage(name='homepage'))
        screen_manager.add_widget(TalkPage(name='talkpage'))
        return screen_manager

if __name__=='__main__':
    JIA().run()
