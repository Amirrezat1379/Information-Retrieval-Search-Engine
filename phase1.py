from genericpath import exists
import json
from typing import Dict
from matplotlib.pyplot import cla
from parsivar import Normalizer, Tokenizer, FindStems
from hazm import stopwords_list, word_tokenize
import string

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

newsList = []
j = 0
myList = []
thisList = []
my_normalizer = Normalizer(statistical_space_correction=False)
myStem = FindStems()
mytoken = Tokenizer()
punctuations = string.punctuation
punctuations += ''.join(['،','؛','»','«','؟'])
with open('readme.json', 'r') as js_file:
    for jsonObj in js_file:
        js_data = json.loads(jsonObj)
        newsList.append(js_data)
        for i in js_data:
            content = js_data[i]['content']
            token_list = word_tokenize(my_normalizer.normalize(content.translate(str.maketrans('', '', punctuations))))
            for token in token_list:
                stopWords  =stopwords_list()
                if token not in stopWords:
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
        
# with open('file.txt', 'w') as f:
#     for word in myList:
#         f.write(word.word)
#         f.write('\n')
#         for pos in word.positions:
#             f.write(pos.id)
#             f.write('\n')

j = 0
voroodis = input()
voroodis = mytoken.tokenize_words(voroodis)
list1 = []
list2 = []
for word in myList:
    for voroodi in voroodis:
        if voroodi == word.word:
            list1 = list2
            list2 = []
            for pos in word.positions:
                if j == 0:
                    list2.append(pos.id)
                else:
                    for item in list1:
                        if pos.id == item:
                            print(item)
                            list2.append(pos.id)
            j += 1

print(voroodis)
print(list2)
