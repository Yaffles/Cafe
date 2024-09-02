from datetime import datetime

import spacy
from word2number import w2n

class NLP():
    def __init__(self):
        """Constructor Method"""
        self.nlp = spacy.load("en_core_web_sm")

    def getNameByPartsOfSpeech(self, speech):
        """Extracts a name from a string using parts of speech"""
        names = []
        doc = self.nlp(speech)
        for token in doc:
            if token.pos_ == "PROPN": # Proper Noun
                names.append(token.text)

        name = " ".join(names)
        return name

    def getNameByEntityType(self, speech):
        """Extracts a name from a string using entity types"""
        names = []
        doc = self.nlp(speech)
        for ent in doc.ents:
            print(ent.text, ent.label_)
            if ent.label_ == "PERSON":
                names.append(ent.text)

        name = " ".join(names)
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
    numberWord = nlpDemo.getNumber("a couple steak")


    print(f"Number: {numberWord}")
    number = nlpDemo.getInteger(numberWord)
    print(f"{numberWord} is {number}")


    # nlpDemo.getNameByPartsOfSpeech("My name is John Doe")
    # nlpDemo.getNameByPartsOfSpeech("I am John Doe")
    # nlpDemo.getNameByPartsOfSpeech("John Doe is my name")
    # nlpDemo.getNameByPartsOfSpeech("John Doe")
    # nlpDemo.getNameByPartsOfSpeech("John")

if __name__ == "__main__":
    main()
