from collections import Counter
import json
from matplotlib.pyplot import cla
from parsivar import Normalizer, Tokenizer, FindStems
from hazm import stopwords_list, word_tokenize
import string
import numpy as np

class DocPose:
    def __init__(self, id):
        self.id = id
        self.positions = []
    
    def addPosition(self, position):
        self.positions.append(position)
    
    def setPosition(self, position):
        self.positions = position

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
    
    def setFreq(self, freq):
        self.freq = freq
    
    def setPosition(self, position):
        self.positions = position

def convertToDocPose(docPose):
    newDoc = DocPose(docPose["id"])
    listIndex.append(docPose["id"])
    positions = []
    for i in docPose["positions"]:
        positions.append(int(i))
    newDoc.setPosition(positions)
    return newDoc

def makePositionalIndex(mode):
    if mode == 1:
        j = 0
        with open('readme.json', 'r') as js_file:
            for jsonObj in js_file:
                js_data = json.loads(jsonObj)
                for i in js_data:
                    listIndex.append(i)
                    content = js_data[i]['content']
                    token_list = word_tokenize(my_normalizer.normalize(content.translate(str.maketrans('', '', punctuations))))
                    for token in token_list:
                        if token not in stopWords:
                            exi = 0
                            token = myStem.convert_to_stem(token)
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
            js_file.close()

        with open('test.json', 'w') as f:
            for list1 in myList:
                for i in range(len(list1.positions)):
                    list1.positions[i] = list1.positions[i].__dict__
            json.dump([index.__dict__ for index in myList], f)
            f.close()


        for list1 in myList:
            for i in range(len(list1.positions)):
                list1.positions[i] = convertToDocPose(list1.positions[i])
    elif mode == 2:
        with open('test.json', 'r') as js_file:
            jsonObj = json.load(js_file)
            for word in jsonObj:
                newWord = Word(word["word"])
                newWord.setFreq(word["freq"])
                subList = []
                for pos in word["positions"]:
                    subList.append(convertToDocPose(pos))
                newWord.setPosition(subList)
                myList.append(newWord)
            js_file.close()


newsList = []
j = 0
myList = []
listIndex = []
my_normalizer = Normalizer(statistical_space_correction=False)
myStem = FindStems()
mytoken = Tokenizer()
punctuations = string.punctuation
stopWords = stopwords_list()
punctuations += ''.join(['،','؛','»','«','؟'])
makePositionalIndex(2)
print(myList[1].positions[0].positions)
print(len(myList))

        # print(list1.positions[i])

j = 0
indexes = listIndex
notExistance = 0
voroodis = input()
quotationMode = 0
offQutation = 0
voroodis = mytoken.tokenize_words(voroodis)
print(voroodis)
list1 = []
list2 = []
for voroodi in voroodis:
    for word in myList:
        if voroodi == "!":
            notExistance = 1
            continue
        if voroodi[0] == '"':
            voroodi = voroodi[1:len(voroodi)]
            quotationMode = 1
        if voroodi[len(voroodi) - 1] == '"':
            voroodi = voroodi[0:len(voroodi) - 1]
            offQutation = 1
        if voroodi == word.word:
            if quotationMode == 1:
                list2 = list1
                list1 = []
                for pos in word.positions:
                    if j == 0:
                        list1.append(pos)
                    else:
                        for item in list2:
                            if pos.id == item.id:
                                for index1 in pos.positions:
                                    for index2 in item.positions:
                                        if (index1 - 1) == index2:
                                            list1.append(pos)
                # if notExistance == 1:
                #     for index in list1:
                #         list1.remove(index)
                #     notExistance = 0
            else:
                if notExistance == 0:
                    for pos in word.positions:
                        list1.append(pos)
                else:
                    if j == 0:
                        for pos in word.positions:
                            # print("want to remove")
                            for index in indexes:
                                if index == pos.id:
                                    # print(pos.id)
                                    indexes.remove(pos)
                                    break
                            list1 = indexes
                    else:
                        for pos in word.positions:
                            for index in indexes:
                                if index == pos.id:
                                    indexes.remove(pos)
                        for item in list1:
                            for index in indexes:
                                if item.id == index:
                                    list1.append(item)
                    notExistance = 0
                    indexes = listIndex
            j += 1

# print(int(listLen[0]))def sort_doc_id_s(doc_list):
list1 = [key for key, value in Counter(list1).most_common()]

# list2.sort(key=lambda x: len(x.positions), reverse=True)
for item in list1:
    with open("IR_data_news_12k.json", "r") as file:
        jsonFile = json.load(file)
        print(jsonFile[item.id]["url"])
        print(jsonFile[item.id]["title"])
        file.close()
# print(list2[0].id)
