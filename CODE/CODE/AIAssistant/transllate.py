
import asyncio
from googletrans import Translator, LANGUAGES
from gtts import gTTS
import os
from playsound import playsound

from stt import Listen
from tts import speak
# Define a mapping of full language names to language codes
language_name_to_code = {name.lower(): code for code, name in LANGUAGES.items()}

def get_language_code(language_input):
    # If the user inputs a language code (e.g., 'en'), return it
    if language_input in LANGUAGES:
        return language_input
    # If the user inputs the full language name (e.g., 'english'), return the corresponding language code
    language_input = language_input.lower()
    return language_name_to_code.get(language_input, None)

async def translategl(query):
    print("SURE SIR")
    speak("SURE SIR")
    print(LANGUAGES)
    translator = Translator()
    # Ask user for target language
    print("Choose the language in which you want to translate (e.g., 'en' for English, 'es' for Spanish, etc.)")
    speak("Choose the language in which you want to translate (e.g., 'en' for English, 'es' for Spanish, etc.)")
    # b = input("To_Lang :- ")
    b=Listen().lower()
     # Get the language code, handling both language names and language codes
    language_code = get_language_code(b)
    
    # Check if the entered language code is valid
    if language_code is None:
        print(f"Sorry, '{b}' is not a valid language code or language name.")
        return f"Sorry, '{b}' is not a valid language code or language name."
    else:
        print(f"Language code for '{b}' is: {language_code}")
        # Proceed with translation or any further operations as required
        try:
            # Translate text asynchronously
            text_to_translate = await translator.translate(query, src="auto", dest=language_code)
            text = text_to_translate.text
            
            # Convert translated text to speech and save it as an MP3 file
            speakgl = gTTS(text=text, lang=language_code, slow=False)
            speakgl.save("voice.mp3")
            
            # Play the translated speech
            playsound("voice.mp3")
            
            # Remove the file after playing it
            os.remove("voice.mp3")
            return text
        except Exception as e:
            print(f"An error occurred: {e}")

