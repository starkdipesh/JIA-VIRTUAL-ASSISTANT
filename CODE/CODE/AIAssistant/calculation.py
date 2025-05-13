
import wolframalpha
import pyttsx3

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

def wolfRam(query):
    apiKey="8L5X5K-XULLKE9V3V"
    request=wolframalpha.Client(apiKey)
    requested=request.query(query)

    try:
        ans=next(requested.results).text
        return ans
    except:
        speak("Value is not answerable")
        return "Value is not answerable."

def calc(query):
    term=str(query)
    term=term.replace("JIA calculate","")
    term=term.replace("multiply","*")
    term=term.replace("into","*")
    term=term.replace("plus","+")
    term=term.replace("minus","-")
    term=term.replace("divide","/")

    final=str(term)
    try:
        result=wolfRam(final)
        print(f"Result is {result}")
        speak(f"Result is {result}")
    except:
        speak("Calculations goes wrong.")

def cal(query):
    term=str(query)
    term=term.replace("JIA calculate","")
    term=term.replace("multiply","*")
    term=term.replace("into","*")
    term=term.replace("plus","+")
    term=term.replace("minus","-")
    term=term.replace("divide","/")

    final=str(term)
    try:
        result=wolfRam(final)
        print(f"Result is {result}")
        speak(f"Result is {result}")
        return f"Result is {result}"
    except:
        speak("Calculations goes wrong.")
        return "Calculations goes wrong."
    
