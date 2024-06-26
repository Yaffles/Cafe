from datetime import datetime

import spacy

class NLP():
    def __init__(self):
        # print("loading model")
        self.nlp = spacy.load("en_core_web_sm")
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

def main():
    nlpDemo = NLP()
    nlpDemo.getNameByPartsOfSpeech("My name is John Doe")
    nlpDemo.getNameByPartsOfSpeech("I am John Doe")
    nlpDemo.getNameByPartsOfSpeech("John Doe is my name")
    nlpDemo.getNameByPartsOfSpeech("John Doe")
    nlpDemo.getNameByPartsOfSpeech("John")

if __name__ == "__main__":
    main()