import pywhatkit as pw
import webbrowser
import wikipedia as wk
import pyttsx3
from time import sleep

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

def searchGoogle(query):
    if "google" in query:
        google_keywords = [
        "google search", "search on google", "search in google",
        "search google", "google"
    ]
        for word in google_keywords:
            query = query.replace(word, "")
        speak("This is what I found on google. ")
        try: 
            pw.search(query)
            result=wk.summary(query,2)
            speak(result)
            print(result)
            ret=result
            # pyautogui.hotkey("alt","f4")
        except :
            speak("No speakable output available")
            ret="No speakable output available"
    else:
        speak("Query is not proper,give command properly.")
        ret="Query is not proper, give command properly."
    return ret

def searchYoutube(query):
    if "youtube" in query:
        youtube_keywords = [
        "youtube search", "search on youtube", "search in youtube", 
        "search youtube", "youtube"
    ]
        # Clean query for YouTube
        for word in youtube_keywords:
            query = query.replace(word, "")
        speak(f"Searching on YouTube for: {query}")
        sleep(2)
        speak("This is what i found for your search.")
        # Logic to open YouTube search
        webbrowser.open(f"https://www.youtube.com/results?search_query={query}")
        pw.playonyt(query)
        speak("Done Sir")
        ret="Done Sir"
    else:
        speak("Query is not proper,give command properly.")
        ret="Query is not proper,give command properly."
    return ret

def searchWikipedia(query):
    if "wikipedia" in query :
         # Remove Wikipedia-related keywords
        wikipedia_keywords = [
            "search on wikipedia", "search in wikipedia", 
            "wikipedia search", "wikipedia", "find in wikipedia"
        ]
    
        # Clean query for Wikipedia
        for word in wikipedia_keywords:
            query = query.replace(word, "")

        # Trim extra spaces
            search_query = query.strip()

        if search_query:
            speak(f"Searching Wikipedia for: {search_query}")
            try:
                # Perform a Wikipedia search and get a summary
                import wikipedia
                results = wikipedia.summary(search_query, sentences=2)
                speak("According to Wikipedia")
                speak(results)
                print(results)
                ret=results
            except wikipedia.exceptions.DisambiguationError as e:
                speak("Your query is too broad. Here are some suggestions:")
                speak(", ".join(e.options[:5]))
                ret=", ".join(e.options[:5])
            except wikipedia.exceptions.PageError:
                speak("Sorry, I couldn't find any results for that query.")
                ret="Sorry, I couldn't find any results for that query."
            except Exception as e:
                speak("Something went wrong. Please try again.")
                ret="Something went wrong. Please try again."
        else:
            speak("Please provide a valid search term for Wikipedia.")
            ret="Please provide a valid search term for Wikipedia."
    else:
        speak("Query is not proper,give command properly.")
        ret="Query is not proper,give command properly."
    return ret
