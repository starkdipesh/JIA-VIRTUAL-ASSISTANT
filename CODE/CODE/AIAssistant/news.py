from bs4 import BeautifulSoup
import pyttsx3
import requests
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

def latestNews(query):
    # Preprocess the query to remove unnecessary words
    query = query.replace("give news on ", "")
    query = query.replace("check news on ", "")
    query = query.replace("provide news on ", "")
    query = query.replace("field", "")
    query = query.strip()

    # API Endpoint and Parameters
    url = "http://api.mediastack.com/v1/news"
    params = {
        'access_key': '8b1f4c9d8ace4272a748a4d5fcbec480',  # Replace with your access key
        'countries': 'us',  # Fetch news from the US
        'keywords': query,
        'limit': 10,  # Limit to 10 articles
    }

    # Make the API request
    response = requests.get(url, params=params)

    # Check if the response is successful
    if response.status_code == 200:
        data = response.json()

        # Check if there are any news articles
        if 'data' in data and len(data['data']) > 0:
            for article in data['data']:
                print(f"Title: {article['title']}")
                speak(article['title'])  # Speak the title
                print(f"Description: {article['description']}")
                speak(article['description'])  # Speak the description
                print(f"For more info, visit this URL: {article['url']}")
                print("-" * 50)

                # Ask if the user wants more news
                speak("Do you want more news, sir?")
                user_response = Listen().lower()

                if user_response in ['no', 'stop', 'exit']:
                    speak("Alright, stopping the news updates. Have a great day!")
                    break  # Exit the loop if the user says 'no'
        else:
            speak(f"No news articles found for the keyword or category '{query}'.")
    else:
        speak(f"Failed to fetch news. Status Code: {response.status_code}")

def getNews():
    url="https://www.bbc.com/news"
    try:
        response=requests.get(url)
        if response.status_code==200:
            soup=BeautifulSoup(response.content,"html.parser")
            headlines=soup.find_all("h2",class_="sc-8ea7699c-3 dhclWg")
            print("Latest News Headlines:")
            speak("Latest News Headlines")
            for i, headline in enumerate(headlines[:10],1):# get top 10 headlines
                print(f"{i}. {headline.text}")
                speak(f"{i}. {headline.text}")
                
        else:
            print("Failed to fetch news.Please try again later.")
            speak("Failed to fetch news.Please try again later.")
            
    except Exception as e:
        print(f"An Error Occured: {e}")
        speak(f"An Error Occured: {e}")
        
