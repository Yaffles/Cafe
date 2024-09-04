import spacy
from word2number import w2n
import subprocess
import sys

class NLP():
    def __init__(self):
        """Constructor Method"""
        self.__nlpVersion = "en_core_web_md"
        try:
            self.nlp = spacy.load(self.__nlpVersion)
        except OSError:
            print("Downloading model...")
            subprocess.call([sys.executable, "-m", "spacy", "download", self.__nlpVersion])
            self.nlp = spacy.load(self.__nlpVersion)

    def getNameByPartsOfSpeech(self, speech):
        """Extracts a name from a string using parts of speech"""
        names = []
        doc = self.nlp(speech.lower())
        for token in doc:
            if token.pos_ == "PROPN": # Proper Noun
                names.append(token.text)

        name = " ".join(names)
        return name

    def getNameByEntityType(self, speech):
        """Extracts a name from a string using entity types"""
        names = []
        doc = self.nlp(speech.title())
        for ent in doc.ents:
            if ent.label_ == "PERSON":
                names.append(ent.text)

        name = " ".join(names)
        return name

    def getName(self, speech):
        """Extracts a name from a string using all methods"""
        if len(speech.split()) == 1:
            return speech

        name = self.getNameByPartsOfSpeech(speech)
        if name == "":
            name = self.getNameByEntityType(speech)
        return name

    def getNumber(self, string):
        """Extracts a cardinal from a string"""
        numbers = []
        doc = self.nlp(string)
        for ent in doc.ents:
            if ent.label_ == "CARDINAL":
                numbers.append(ent.text)

        # handle special cases
        if len(numbers) == 0:
            words = string.split()
            if "few" in words:
                return None # cannot determine number

            if "couple" in words:
                return "2"
            elif "a" in words or "an" in words:
                return "1"

        if len(numbers) == 1: # cannot determine number
            return numbers[0]

        return None



    def getInteger(self, word):
        """Converts a string to an integer ('one' -> 1, '1' -> 1)"""
        try:
            return w2n.word_to_num(word)
        except ValueError:
            try:
                return int(word)
            except ValueError:
                return None



def main():
    nlpDemo = NLP()


    name = "my name is furini"
    print("propn: " + nlpDemo.getNameByPartsOfSpeech(name))
    print("entity: "+nlpDemo.getNameByEntityType(name))

if __name__ == "__main__":
    main()
