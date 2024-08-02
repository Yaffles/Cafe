from datetime import datetime

import spacy

class NLP():
    def __init__(self):
        # print("loading model")
        self.nlp = spacy.load("en_core_web_sm")
        self.numbers = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten'] #TODO allow any number
        # print("model loaded")
    
    def getNameByPartsOfSpeech(self, speech):
        names = []
        doc = self.nlp(speech)
        for token in doc:
            print(token.text, token.pos_)
            if token.pos_ == "PROPN":
                names.append(token.text)
        
        name = " ".join(names)
        print(f"Name: {name}")
        return name

    def getNameByEntityType(self, speech):
        names = []
        doc = self.nlp(speech)
        print("Entities")
        for ent in doc.ents:
            print(ent.text, ent.label_)
            if ent.label_ == "PERSON":
                names.append(ent.text)
        
        name = " ".join(names)
        print(f"Name: {name}")
        return name

    def getNumber(self, string):
        """Extracts a number from a string"""
        numbers = []
        doc = self.nlp(string)
        print("Entities")
        for ent in doc.ents:
            if ent.label_ == "CARDINAL":
                numbers.append(ent.text)
        
        if len(numbers) != 1:
            return None
        else:
            return numbers[0]

        
    
    def getInteger(self, word):
        """Converts a word to an integer ('one' -> 1)"""
        number = self.numbers.index(word) if word in self.numbers else None
        if number:
            return number
        # Try different expressions
        


def main():
    nlpDemo = NLP()
    numberWord = nlpDemo.getNumber("I woudld like seven steak")
    
    number = nlpDemo.getInteger(numberWord)
    print(f"{numberWord} is {number}")


    # nlpDemo.getNameByPartsOfSpeech("My name is John Doe")
    # nlpDemo.getNameByPartsOfSpeech("I am John Doe")
    # nlpDemo.getNameByPartsOfSpeech("John Doe is my name")
    # nlpDemo.getNameByPartsOfSpeech("John Doe")
    # nlpDemo.getNameByPartsOfSpeech("John")

if __name__ == "__main__":
    main()