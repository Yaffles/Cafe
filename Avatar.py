import openai
import speech_recognition as sr
import pyttsx4
from pydub import AudioSegment
from pydub.playback import play

class Avatar:
    def __init__(self, name="Elsa") -> None:
        self.name = name
        self.initSR()
        self.initVoice()

        self.introduce()

    def initSR(self):
        self.sample_rate = 48000
        self.chunk_size = 2048
        self.r = sr.Recognizer()
        self.useSr = False # temporarily disable speech recognition
        self.energy_threshold = 1000

    def initVoice(self):
        self.__engine = pyttsx4.init()
        self.__voices = self.__engine.getProperty('voices')
        self.__vix = 1
        self.__voice = self.__voices[self.__vix]
        self.__engine.setProperty('voice', self.__voice.id)
        self.__engine.setProperty('rate', 300)
        self.__engine.setProperty('volume', 1.0)
        # manually set energy threshold
        self.r.energy_threshold = self.energy_threshold

    def say(self, words):
        self.__engine.say(words)
        print("\033[31m"+words+"\033[0m")
        self.__engine.runAndWait()



        # self.__engine.runAndWait()
        # client = texttospeech.TextToSpeechClient()

        # # Set the text input to be synthesized
        # synthesis_input = texttospeech.SynthesisInput(text=words)

        # # Build the voice request, select the language code ("en-US") and the ssml
        # # voice gender ("neutral")
        # voice = texttospeech.VoiceSelectionParams(
        #     language_code="en-AU", name="en-AU-Wavenet-B", ssml_gender=texttospeech.SsmlVoiceGender.MALE
        # )

        # # Select the type of audio file you want returned
        # audio_config = texttospeech.AudioConfig(
        #     audio_encoding=texttospeech.AudioEncoding.MP3
        # )

        # # Perform the text-to-speech request on the text input with the selected
        # # voice parameters and audio file type
        # response = client.synthesize_speech(
        #     input=synthesis_input, voice=voice, audio_config=audio_config
        # )

        # # The response's audio_content is binary.
        # audio_file = io.BytesIO(response.audio_content)

        # # Load audio
        # audio = AudioSegment.from_file(audio_file, format="mp3")

        # # Play the audio file
        # play(audio)


    def introduce(self):
        # response = ai("Introduce yourself")
        self.say("Hello, I am "+self.name)

    def listen(self, prompt="I am listening, please speak:", useSR=True):
        words = ""
        if self.useSr and useSR:
            try:
                # raise Exception("Not working")
                #print(sr.Microphone.list_microphone_names())
                with sr.Microphone(sample_rate=self.sample_rate, chunk_size=self.chunk_size) as source:
                    # listen for 1 second to calibrate the energy threshold for ambient noise levels
                    self.r.adjust_for_ambient_noise(source)
                    print("Energy threshold: ", self.r.energy_threshold)
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
