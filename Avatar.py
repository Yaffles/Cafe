import speech_recognition as sr
import pyttsx4
from pydub import AudioSegment
from pydub.playback import play

from google.cloud import texttospeech
import io

class Avatar:
    """A class that represents an avatar that can speak and listen"""

    def __init__(self, name="Elsa", useSr=True) -> None:
        self.name = name
        self.initSR()
        self.initVoice()
        self.useSr = useSr


    def initSR(self):
        self.sample_rate = 48000
        self.chunk_size = 2048
        self.r = sr.Recognizer()
        self.min_energy_threshold = 10 # can bug out if too low

    def initVoice(self):
        self.__engine = pyttsx4.init()
        self.__voices = self.__engine.getProperty('voices')
        self.__vix = 1 # 0 is male, 1 is female
        self.__voice = self.__voices[self.__vix]
        self.__engine.setProperty('voice', self.__voice.id)
        self.__engine.setProperty('rate', 300) #TODO change to reasonable
        self.__engine.setProperty('volume', 1.0)
        # manually set energy threshold
        self.r.energy_threshold = self.min_energy_threshold

    def say(self, words):
        self.__engine.say(words)
        print("\033[31m"+words+"\033[0m")
        self.__engine.runAndWait()






    def introduce(self):
        # response = ai("Introduce yourself")
        self.say("Hello, I am "+self.name)

    def listen(self, prompt="I am listening, please speak:", useSR=True):
        """Listen to the user and return the words spoken"""
        words = ""
        if self.useSr and useSR:
            try:
                # raise Exception("Not working")
                #print(sr.Microphone.list_microphone_names())
                with sr.Microphone(sample_rate=self.sample_rate, chunk_size=self.chunk_size) as source:
                    # listen for 1 second to calibrate the energy threshold for ambient noise levels
                    self.r.adjust_for_ambient_noise(source)
                    if self.r.energy_threshold < self.min_energy_threshold:
                        self.r.energy_threshold = self.min_energy_threshold

                    self.say(prompt)
                    print("Listening...")
                    audio = self.r.listen(source)
                try:
                    print("Recognizing...")
                    #print("You said: '" + r.recognize_google(audio)+"'")
                    words = self.r.recognize_google(audio)
                    print("\033[36m"+words+"\033[0m")
                except sr.UnknownValueError:
                    self.say("Could not understand what you said.")
                except sr.RequestError as e:
                    self.say("Could not request results; {0}".format(e))

            except Exception as e:
                # print(e)
                self.say(f"Please type")
                words = input("\033[33m- ")
                print("\033[0m", end="")
        else:
            self.say(prompt)

            words = input("Please type: ")
        return words

if __name__ == "__main__":
    avatar = Avatar()
    while True:
        words = avatar.listen()
        if words.lower() == "exit":
            break
        avatar.say("You said: "+words)
        print("You said: ", words)
    avatar.say("Goodbye")
    print("Goodbye")
