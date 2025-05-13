
from tts import speak
from stt import Listen
import random 
# Open a New File and Name it as game.py and paste the following code: -
def game_play():
    speak("How much round do you want to play, sir")
    num=Listen()
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
    try:
        n=int(num)
    except:
        speak("Wrong input")
    speak("Lets Play ROCK PAPER SCISSORS !!")
    print("LETS PLAYYYYYYYYYYYYYY")
    i = 0
    Me_score = 0
    Com_score = 0
    while(i<n):
        choose = ("rock","paper","scissors") #Tuple
        com_choose = random.choice(choose)
        query = Listen().lower()
        if (query == "rock"):
            if (com_choose == "rock"):
                speak("ROCK")
                print(f"Score:- ME :- {Me_score} : COM :- {Com_score}")
            elif (com_choose == "paper"):
                speak("paper")
                Com_score += 1
                print(f"Score:- ME :- {Me_score} : COM :- {Com_score}")
            else:
                speak("Scissors")
                Me_score += 1
                print(f"Score:- ME :- {Me_score} : COM :- {Com_score}")

        elif (query == "paper" ):
            if (com_choose == "rock"):
                speak("ROCK")
                Me_score += 1
                print(f"Score:- ME :- {Me_score} : COM :- {Com_score}")

            elif (com_choose == "paper"):
                speak("paper")
                print(f"Score:- ME :- {Me_score} : COM :- {Com_score}")
            else:
                speak("Scissors")
                Com_score += 1
                print(f"Score:- ME :- {Me_score} : COM :- {Com_score}")

        elif (query == "scissors" or query == "scissor"):
            if (com_choose == "rock"):
                speak("ROCK")
                Com_score += 1
                print(f"Score:- ME :- {Me_score} : COM :- {Com_score}")
            elif (com_choose == "paper"):
                speak("paper")
                Me_score += 1
                print(f"Score:- ME :- {Me_score} : COM :- {Com_score}")
            else:
                speak("Scissors")
                print(f"Score:- ME :- {Me_score} : COM :- {Com_score}")
        i += 1
    print(f"FINAL SCORE :- ME :- {Me_score} : COM :- {Com_score}")
    speak(f"FINAL SCORE :- ME :- {Me_score} : COM :- {Com_score}")
    
