import speech_recognition as sr
import pyttsx4

class Avatar:
    """A class that represents an avatar that can speak and listen"""

    def __init__(self, name="Elsa", useSr=True, speed=200) -> None:
        self.name = name
        self.useSr = useSr
        self.speed = speed
        self.initSR()
        self.initVoice()


    def initSR(self):
        self.sample_rate = 48000
        self.chunk_size = 2048
        self.r = sr.Recognizer()
        self.min_energy_threshold = 10 # can't hear if too low or high
        self.max_energy_threshold = 3500

    def initVoice(self):
        self.__engine = pyttsx4.init()

        self.__voices = self.__engine.getProperty('voices')
        self.__vix = 1 # 0 is male, 1 is female
        self.__voice = self.__voices[self.__vix]
        self.__engine.setProperty('voice', self.__voice.id)
        self.__engine.setProperty('rate', self.speed) #TODO change to reasonable
        self.__engine.setProperty('volume', 1.0)

        self.r.energy_threshold = self.min_energy_threshold

    def say(self, words):
        self.__engine.say(words)
        print("\033[31m"+words+"\033[0m") # print in red
        self.__engine.runAndWait()


    def introduce(self):
        self.say("Hello, I am "+self.name)

    def listen(self, prompt="I am listening, please speak:", useSR=True):
        """Listen to the user and return the words spoken"""
        words = ""
        if self.useSr and useSR:
            try:
                with sr.Microphone(sample_rate=self.sample_rate, chunk_size=self.chunk_size) as source:
                    # listen for 1 second to calibrate the energy threshold for ambient noise levels, then adjust the threshold so it can actually hear
                    self.r.adjust_for_ambient_noise(source)
                    if self.r.energy_threshold < self.min_energy_threshold:
                        self.r.energy_threshold = self.min_energy_threshold
                    if self.r.energy_threshold > self.max_energy_threshold:
                        self.r.energy_threshold = self.max_energy_threshold

                    self.say(prompt)
                    print("Listening...", end='\r')
                    audio = self.r.listen(source)
                try:
                    print("Recognizing...", end='\r')
                    words = self.r.recognize_google(audio)
                    print(f"\033[36m{words.ljust(15)}\033[0m") #change color and padding to remove previous text
                except sr.UnknownValueError:
                    self.say("Could not understand what you said.")
                except sr.RequestError as e:
                    self.say("Could not request results; {0}".format(e))

            except Exception as e:
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
