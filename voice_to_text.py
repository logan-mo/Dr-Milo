import speech_recognition as sr
import pyttsx3
recognizer = sr.Recognizer()
engine = pyttsx3.init()
def recognize_speech():
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        print("You said:", text)
        return text
    except sr.UnknownValueError:
        print("Sorry, could not understand audio.")
    except sr.RequestError as e:
        print("Error accessing the Google Speech Recognition service: {0}".format(e))

    return ""
def speak(text):
    engine.say(text)
    engine.runAndWait()
if __name__ == "__main__":
    while True:
        text = recognize_speech()
        speak(text)