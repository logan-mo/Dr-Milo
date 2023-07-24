# import gradio as gr
# import random

# def random_response(message, history):
#     return random.choice(["Yes", "No"])

# gr.ChatInterface(random_response).launch()


from transformers import pipeline
from threading import Thread
import gradio as gr
import pandas as pd
import pyttsx3
import openai
import time
import os
import pickle
import re
from nltk.corpus import stopwords

Wav2VecPipeline = pipeline("automatic-speech-recognition")                          # Load a pretrained speech recognition model
openai.api_key = ''              # Loading APIKey for ChatGPT
medical_classification_model = pickle.load(open('./models/model.pkl', 'rb'))        # Load our custom classification model

messages = [
    {"role": "system", "content": "You are a helpful Medical Assistant. Your goal is to answer a users query if it's a question. If it's a medical question you summarize it for them."},
]

def get_completion(prompt, messages, model="gpt-3.5-turbo"):

    messages.append({"role": "user", "content": prompt})
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0
    )
    
    messages.append({"role": "assistant", "content": response.choices[0].message["content"]})

    return response.choices[0].message["content"]

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
   
REPLACE_BY_SPACE_RE = re.compile('[/(){}\[\]\|@,;]')
BAD_SYMBOLS_RE = re.compile('[^0-9a-z #+_]')
STOPWORDS = set(stopwords.words('english'))

def clean_text(text):
    """
        text: a string
        
        return: modified initial string
    """
    text = text.lower() # lowercase text
    text = REPLACE_BY_SPACE_RE.sub(' ', text) # replace REPLACE_BY_SPACE_RE symbols by space in text
    text = BAD_SYMBOLS_RE.sub('', text) # delete symbols which are in BAD_SYMBOLS_RE from text
    #text = ' '.join(word for word in text.split() if word not in STOPWORDS) # delete stopwors from text
    return text   
   
def isMedical(prompt):
    predicted_class = medical_classification_model.predict([str(clean_text(prompt))])
    print(f"User prompt '{prompt}' is {predicted_class}")
    return predicted_class == 'MEDICAL'

def transcribe(audio = None, text=None):
    DEFAULT_RESPONSE = "I'm sorry, I can only respond to medical questions!"
    if audio is not None:
        text = Wav2VecPipeline(audio)["text"]
        
    if isMedical(text):
        response = get_completion(text, messages=messages)
        Thread(target=speak, args=(response,)).start()
        #speak(response)
        return response
    else:
        speak(DEFAULT_RESPONSE)
        return DEFAULT_RESPONSE

gr.Interface(
    fn=transcribe, 
    inputs=[gr.Audio(source="microphone", type="filepath"), gr.Textbox(lines=2, placeholder="Copy and Paste the Doctor's remarks")], 
    outputs="text").launch()