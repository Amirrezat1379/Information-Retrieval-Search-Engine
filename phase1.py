from collections import Counter
import json
from locale import normalize
from turtle import position
from matplotlib.pyplot import cla
from parsivar import FindStems
from hazm import *
import string
import numpy as np

def makePositionalIndex(mode, deleteStopWords=True, stemWords=True):
    j = 0
    with open('IR_data_news_12k.json', 'r') as js_file:
        for jsonObj in js_file:
            js_data = json.loads(jsonObj)
            for i in js_data:
                content = js_data[i]['content']
                token_list = word_tokenize(my_normalizer.normalize(content.translate(str.maketrans('', '', punctuations))))
                for position, token in enumerate(token_list):
                    if deleteStopWords == True:
                        if token not in stopWords:
                            if (stemWords == True):
                                token = myStem.convert_to_stem(token)
                            j += 1
                            if token in dictionary:
                                dictionary[token][0] += 1
                                if i in dictionary[token][1]:
                                    dictionary[token][1][i].append(position)
                                else:
                                    dictionary[token][1][i] = [position]
                            else:
                                dictionary[token] = []
                                dictionary[token].append(1)
                                dictionary[token].append({})
                                dictionary[token][1][i] = [position]
                    else:
                        if (stemWords == True):
                            token = myStem.convert_to_stem(token)
                        j += 1
                        if token in dictionary:
                            dictionary[token][0] += 1
                            if i in dictionary[token][1]:
                                dictionary[token][1][i].append(position)
                            else:
                                dictionary[token][1][i] = [position]
                        else:
                            dictionary[token] = []
                            dictionary[token].append(1)
                            dictionary[token].append({})
                            dictionary[token][1][i] = [position]
                j = 0
    js_file.close()

def findQuery(voroodis):
    print(voroodis)
    returnList = []
    returnNotList = []
    j = 0
    quotationMode = 0
    notExistance = 0
    list1 = {}
    quotCount = 0
    for voroodi in voroodis:
        if voroodi == "!":
            notExistance = 1
            continue
        if voroodi == '"':
            if quotationMode == 0:
                quotationMode = 1
            else:
                quotationMode = 0
                for item in list(list1.keys()):
                    returnList.append(item)
            continue
        voroodi = my_normalizer.normalize(voroodi)
        voroodi = myStem.convert_to_stem(voroodi)
        if voroodi not in dictionary:
            j = 1
            continue
        word = dictionary[voroodi][1]
        if quotationMode == 1:
            list2 = list1
            list1 = {}
            for pos in word:
                if quotCount == 0:
                    list1[pos] = word[pos]
                else:
                    for item in list2:
                        if pos == item:
                            for index1 in word[pos]:
                                for index2 in list2[item]:
                                    if (index1 - 1) == index2:
                                        if pos in list1:
                                            list1[pos].append(index1)
                                        else:
                                            list1[pos] = [index1]
            quotCount = 1
        else:
            if notExistance == 0:
                for item in list(word.keys()):
                    returnList.append(item)
            else:
                for item in list(word.keys()):
                    returnNotList.append(item)
                notExistance = 0

    returnNotList = list(dict.fromkeys(returnNotList))
    if returnList == []:
        if j == 1:
            return "پرسمان شما یافت نشد!!!!!!"
        for i in range(12201):
            returnList.append(str(i))
    for item in returnNotList:
        for index in returnList:
            if item == index:
                returnList.remove(index)
    return returnList

dictionary = {}
my_normalizer = Normalizer()
myStem = FindStems()
punctuations = string.punctuation
stopWords = set(stopwords_list())
punctuations += ''.join(['،','؛','»','«','؟'])
makePositionalIndex(1)
print(dictionary["ماجدی"][1]['3'][0])
voroodis = input()
voroodis = word_tokenize(voroodis)
print(voroodis)
finalList = findQuery(voroodis)
finalList = [key for key, value in Counter(finalList).most_common()]
print(finalList)
# # print(int(listLen[0]))def sort_doc_id_s(doc_list):
# list1 = [key for key, value in Counter(list1).most_common()]
# print(len(list1))

# # list2.sort(key=lambda x: len(x.positions), reverse=True)
# for item in list1:
#     with open("IR_data_news_12k.json", "r") as file:
#         jsonFile = json.load(file)
#         print(jsonFile[item.id]["url"])
#         print(jsonFile[item.id]["title"])
#         file.close()
# print(list2[0].id)
