# import gradio as gr
# import random

# def random_response(message, history):
#     return random.choice(["Yes", "No"])

# gr.ChatInterface(random_response).launch()


from transformers import pipeline
import gradio as gr

p = pipeline("automatic-speech-recognition")

def transcribe(audio = None, text=None):
    if audio is not None:
        text = p(audio)["text"]
    return text

gr.Interface(
    fn=transcribe, 
    inputs=[gr.Audio(source="microphone", type="filepath"), gr.Textbox(lines=2, placeholder="Paste a link to an audio file or upload one from your device.")], 
    outputs="text").launch()