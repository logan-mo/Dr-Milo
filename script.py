import pyttsx3

engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def get_input():
    text = input("What would you like me to speak? ")
    return text

while True:
    text = get_input()
    speak(text)
    if text=='q':
        break