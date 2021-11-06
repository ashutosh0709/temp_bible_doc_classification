# Import the required module for text
# to speech conversion
import pyttsx3
from time import sleep


def tts_speak(text_to_be_spoken):
    
    text_to_be_spoken = str(text_to_be_spoken)
    # init function to get an engine instance for the speech synthesis
    engine = pyttsx3.init()

    # say method on the engine that passing input text to be spoken
    engine.say(text_to_be_spoken)

    # run and wait method, it processes the voice commands.
    engine.runAndWait()



