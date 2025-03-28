from flask import Flask, render_template
from flask_socketio import SocketIO
import speech_recognition as sr

app = Flask(__name__)
socketio = SocketIO(app)

IMAGE_FOLDER = "./static/images"
alphabet_map = {chr(i): f"./static/images/{chr(i)}.jpg" for i in range(65, 91)}  # A-Z mapping
blank_image = "./static/images/blank.jpg"  # Image for spaces

@app.route('/')
def index():
    return render_template('./index.html')

@socketio.on('start_recognition')
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        socketio.emit('listening', {'status': True})  # Indicate listening started
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio).upper()
        print("Detected:", text)

        # Map letters to images, use blank.jpg for spaces
        image_urls = [alphabet_map[char] if char in alphabet_map else blank_image if char == " " else None for char in text]

        # Send recognized text and images to frontend
        socketio.emit('display_results', {'text': text, 'images': image_urls})
    except sr.UnknownValueError:
        socketio.emit('error', {'message': "Could not understand the audio"})
    except sr.RequestError:
        socketio.emit('error', {'message': "Speech recognition error"})

    socketio.emit('listening', {'status': False})  # Indicate listening stopped

if __name__ == '__main__':
    socketio.run(app, debug=True)
