import socket 
import google.generativeai as genai

googleapi="AIzaSyAjwv94NAt5SPCzqpNlT0Ye1kwwKV4AXhk"
# model = genai.GenerativeModel('gemini-pro')
model = genai.GenerativeModel('gemini-2.0-flash')
genai.configure(api_key=googleapi)

def prompt(usertext, max_words=500):
    # Generate a response
    reply = model.generate_content(usertext)
    
    # Split the response into words and limit it
    reply_text = reply.text
    reply_words = reply_text.split()[:max_words]  # Limit to the max_words count
    limited_reply = ' '.join(reply_words)  # Join the words back into a string
    # limited_reply=limited_reply.replace(" ","\n")
    # Print and return the limited response
    if "code" in usertext:
        print(reply_text)
        return reply_text
    else:
        print(limited_reply)
        return limited_reply

def isConnect():
    try:
        socket.create_connection(("8.8.8.8",53),timeout=3)
        return True
    except OSError:
        return False
# prompt("provide only code to find factorial without any explanation")
# prompt("who is parth?")