#import library
import time
import speech_recognition as sr

# Initialize recognizer class (for recognizing the speech)

r = sr.Recognizer()
r.pause_threshold = 0.5 #minimum num of seconds at last to consider closing the listening of microphone.

# Reading Microphone as source
# listening the speech and store in audio_text variable

def stt_listen():

    with sr.Microphone() as source:
        start0 = int(time.time()*1000)
        print("Talk")

        #r.adjust_for_ambient_noise(source)
        audio_text = r.listen(source , phrase_time_limit=3) # will only record for 3 seconds. Will cut off after that.


        print("Time over, thanks")

        start1 = int(time.time()*1000)
    # recoginize_() method will throw a request error if the API is unreachable, hence using exception handling
        
        try:
            # using google speech recognition
            aud_txt =  r.recognize_google(audio_text ,  language= "en-US")
            end = int(time.time()*1000)
            print("time for audio to text conversion fully = " , start1 - start0)
            print("time for audio to text conversion only by the google API = " , end - start1)
            return aud_txt
        except:
            aud_txt =  "Not recognized"
            end = int(time.time()*1000)
            print("time for audio to text conversion fully = " , end - start0)
            print("time for audio to text conversion only by the google API = " , end - start1)
            return aud_txt
            

#print(stt_listen())            