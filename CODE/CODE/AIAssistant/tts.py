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

# speak("hello sir how are you,priyanshu pranami")