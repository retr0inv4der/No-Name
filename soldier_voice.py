import requests
import speech_recognition as sr
from gtts import gTTS
import aiml
import os
import subprocess
import whisper
import numpy as np
import tempfile
import pyttsx3




class bot : 
    def ping(self):
        try:
            r = requests.get("https://google.com/", timeout=3)
            self.internet = r.status_code == 200
        except requests.exceptions.ConnectionError:
            self.internet = False
        except requests.exceptions.Timeout:
            self.internet = False
    
    def __init__(self):
        self.internet = False
        self.model = whisper.load_model("base")
        self.ping()
        if not self.internet : 
            self.offline_engine = pyttsx3.init()



    def listen(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("I am listening: ")
            audio = r.listen(source)
        
        # Save to a temporary WAV file
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
            temp_file.write(audio.get_wav_data())
            temp_path = temp_file.name
        
        # Load with Whisper
        data = self.model.transcribe(temp_path)
        

        print(data["text"])
        return data["text"]

    def speak(self , text ):
        if self.internet : 
            tts = gTTS(text=text, lang='en')
            tts.save("temp_soundtrack_tts.mp3")
        else : 
            self.offline_engine.say(text)
            self.offline_engine.runAndWait()

        subprocess.run(["ffmpeg" , "-i" , "temp_soundtrack_tts.mp3" , "temp_soundtrack_tts.wav" , "-y"])
        
        subprocess.run(["paplay" , "temp_soundtrack_tts.wav"])
            
        


    def mainloop(self):
        kernel = aiml.Kernel()
        if os.path.isfile("bot_brain.brn"):
            kernel.bootstrap(brainFile = "bot_brain.brn")
        else:
            kernel.bootstrap(learnFiles = "std-startup.xml", commands = "load aiml b")
            #kernel.saveBrain("bot_brain.brn")

        while True:
            que = self.listen()
            if que.strip().lower() in ['shutdown','exit','quit','gotosleep','goodbye','terminate']:
                break
            res = kernel.respond(que)
            if res != "":
                print("Answer: " + res)
                self.speak(res)
                



if __name__ == "__main__" : 
    b = bot() 
    b.mainloop()