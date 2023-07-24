import pandas as pd
import pyttsx3
import openai
import time
import os

openai.api_key = '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'
engine = pyttsx3.init()

def get_completion(prompt, model="gpt-3.5-turbo", messages=None):

    if messages is None:
        messages = [{"role": "user", "content": prompt}]
    else:
        messages.append({"role": "user", "content": prompt})
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0
    )

    return response.choices[0].message["content"]

def speak(text):
    engine.say(text)
    engine.runAndWait()

def audio_capture():
    ...
   
def isMedical():
    ...   
 
user_input = audio_capture()
if isMedical(user_input):
    prompt = user_input
    response = get_completion(prompt)
    speak(response)
else:
    speak("Meow")
