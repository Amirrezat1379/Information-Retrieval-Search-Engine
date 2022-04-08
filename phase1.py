from genericpath import exists
import json
from typing import Dict
from matplotlib.pyplot import cla
from parsivar import Normalizer, Tokenizer, FindStems
from hazm import stopwords_list, word_tokenize
import string

# def estekhrajToken(newsList):
#     return thisList

class DocPose:
    def __init__(self, id):
        self.id = id
        self.positions = []
    
    def addPosition(self, position):
        self.positions.append(position)

class Word:
    def __init__(self, word):
        self.word = word
        self.freq = 0
        self.positions = []
    
    def addPosition(self, docId, position):
        self.freq += 1
        for docu in self.positions:
            if docId == docu.id:
                docu.addPosition(position)
                return
        doc = DocPose(docId)
        doc.addPosition(position)
        self.positions.append(doc)

def addAdad(i, content, position):
    print("kiramo bokhor")

newsList = []
j = 0
myList = []
thisList = []
my_normalizer = Normalizer(statistical_space_correction=False)
myStem = FindStems()
mytoken = Tokenizer()
LINK_REGEX = r"((http|https)\:\/\/)?[a-zA-Z0-9\.\/\?\:@\-_=#]+\.([a-zA-Z]){2,6}([ا-یa-zA-Z0-9\.\&\/\?\:@\-_=# ])*"
punctuations = string.punctuation
punctuations += ''.join(['،','؛','»','«','؟'])
with open('readme.json', 'r') as js_file:
    for jsonObj in js_file:
        js_data = json.loads(jsonObj)
        newsList.append(js_data)
        for i in js_data:
            content = js_data[i]['content']
            token_list = word_tokenize(my_normalizer.normalize(content))
            for token in token_list:
                exi = 0
                j += 1
                for wor in myList:
                    if (wor.word == token):
                        wor.addPosition(i, j)
                        exi = 1
                        break
                if exi == 0:
                    word = Word(token)
                    word.addPosition(i, j)
                    myList.append(word)
            j = 0
        
# myList = estekhrajToken(newsList)
# print(myList)
# print(myList)
# for word in myList:
#     print(word.word)
#     print(word.freq)
#     for pos in word.positions:
#         print(pos.id)
with open('readme.txt', 'w') as f:
    for word in myList:
        f.write(word.word)
        f.write('\n')
        for pos in word.positions:
            f.write(pos.id)
            f.write('\n')
