import speech_recognition as sr
from flask import Flask, render_template, jsonify
import pyttsx3

app = Flask(__name__)

def get_assistant_response(user_input):
    user_input = user_input.lower()
    if "hello" in user_input:
        return "Hello! How can I help you?"
    elif "how are you" in user_input:
        return "I'm fine, thank you. How about you?"
    elif "weather" in user_input:
        return "The weather is sunny today."
    elif "time" in user_input:
        return "The current time is 10:00 AM."
    else:
        return "I'm sorry, I didn't understand that."

def listen_and_reply():
    recognizer = sr.Recognizer()
    engine = pyttsx3.init()
    
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
    try:
        user_input = recognizer.recognize_google(audio)
        print("You said:", user_input)
        
        assistant_response = get_assistant_response(user_input)
        print("Assistant:", assistant_response)
        
        # Speak the assistant's response
        engine.say(assistant_response)
        engine.runAndWait()
        
        return {"user_input": user_input, "assistant_response": assistant_response}
    except sr.UnknownValueError:
        print("Sorry, could not understand audio")
        return {"error": "Sorry, could not understand audio"}
    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))
        return {"error": "Could not request results"}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recognize')
def recognize_speech():
    return jsonify(listen_and_reply())

if __name__ == '__main__':
    app.run(debug=True)
