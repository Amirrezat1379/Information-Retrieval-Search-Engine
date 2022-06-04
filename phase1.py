from collections import Counter
import json
from xml.dom.xmlbuilder import DocumentLS
import matplotlib.pyplot as plt
from parsivar import FindStems
from hazm import *
import string
import numpy as np
from numpy.linalg import norm
import arabic_reshaper
from bidi.algorithm import get_display
from scipy import spatial

# IR_data_news_12k

def convert(text):
    reshaped_text = arabic_reshaper.reshape(text)
    converted = get_display(reshaped_text)
    return converted

def makePositionalIndex(deleteStopWords=True, stemWords=True):
    wordCount = 0
    tokenCount = 0
    wordList = []
    tokenList = []
    popop = 0
    with open('IR_data_news_12k.json', 'r') as js_file:
        for jsonObj in js_file:
            js_data = json.loads(jsonObj)
            documentLen = len(js_data)
            for i in js_data:
                content = js_data[i]['content']
                token_list = word_tokenize(my_normalizer.normalize(content.translate(str.maketrans('', '', punctuations))))
                dictionaryLen.append(len(token_list))
                for position, token in enumerate(token_list):
                    if deleteStopWords == True:
                        if token not in stopWords:
                            wordCount += 1
                            if (stemWords == True):
                                token = myStem.convert_to_stem(token)
                            if token in dictionary:
                                dictionary[token][0] += 1
                                if i in dictionary[token][1]:
                                    dictionary[token][1][i][0] = 1 + np.log10(1 + (np.power(10, dictionary[token][1][i][0] - 1)))
                                    dictionary[token][1][i].append(position)
                                else:
                                    dictionary[token][1][i] = [1]
                                    dictionary[token][1][i].append(position)
                                    dictionary[token][2] = np.log10(documentLen / ((documentLen / np.power(10, dictionary[token][2])) + 1))
                            else:
                                tokenCount += 1
                                dictionary[token] = []
                                dictionary[token].append(1)
                                dictionary[token].append({})
                                dictionary[token][1][i] = [1]
                                dictionary[token][1][i].append(position)
                                dictionary[token].append(np.log10(documentLen))
                    else:
                        wordCount += 1
                        if (stemWords == True):
                            token = myStem.convert_to_stem(token)
                        if token in dictionary:
                            dictionary[token][0] += 1
                            dictionary[token][1][i][1] += 1
                            if i in dictionary[token][1]:
                                dictionary[token][1][i][0] = 1 + np.log10(1 + np.power(10, dictionary[token][1][i][0] - 1))
                                dictionary[token][1][i].append(position)
                            else:
                                dictionary[token][1][i] = [1]
                                dictionary[token][1][i].append(position)
                                dictionary[token][2] = np.log10(documentLen / ((documentLen / np.power(10, dictionary[token][2])) + 1))
                        else:
                            tokenCount += 1
                            dictionary[token] = []
                            dictionary[token].append(1)
                            dictionary[token].append({})
                            dictionary[token][1][i] = [1]
                            dictionary[token][1][i].append(position)
                            dictionary[token].append(np.log10(documentLen))
                if i == "500" or i == "1000" or i == "1500" or i == "2000":
                    wordList.append(np.log10(wordCount))
                    tokenList.append(np.log10(tokenCount))
    js_file.close()
    print(popop)
    return wordList, tokenList, tokenCount, wordCount

def calculateQueryTfIdf(query):
    queryDictionary = {}
    queryTfIdf = []
    for word in query:
        if word not in queryDictionary:
            queryDictionary[word] = query.count(word)
    for word in queryDictionary:
        queryTfIdf.append((1 + np.log10(queryDictionary[word])) * dictionary[word][2])
    return queryTfIdf

def calculateDocumentTfIdf(query, championList):
    queryDictionary = {}
    documentTfIdf = {}
    count = []
    i = 0
    for word in query:
        if word not in queryDictionary:
            queryDictionary[word] = query.count(word)
            count.append(0)
    for word in queryDictionary:
        if i == 0:
            for document in championList:
                if document in dictionary[word][1]:
                    documentTfIdf[document] = [dictionary[word][1][document][0] * dictionary[word][2] / dictionaryLen[int(document)]]
                else:
                    documentTfIdf[document] = [0]
                # documentTfIdf[document].append(0)
        else:
            for document in championList:
                if document in dictionary[word][1]:
                    documentTfIdf[document].append(dictionary[word][1][document][0] * dictionary[word][2] / dictionaryLen[int(document)])
                else:
                    documentTfIdf[document].append(0)

        i += 1
    return documentTfIdf

def calculateCosine(query, document):
    if len(query) == 1:
        return document[0]
    return np.dot(query,document)/(norm(query)*norm(document))

def createChampionList(query, k):
    championList = []
    for word in query:
        thisChampion = []
        for document in dictionary[word][1]:
            thisChampion.append([document, dictionary[word][1][document][0]])
        thisChampion.sort(key=lambda x: x[1], reverse=True)
        for i in range(min(len(thisChampion), k)):
            championList.append(thisChampion[i][0])
    championList = [key for key, value in Counter(championList).most_common()]
    return championList

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
            j = 0
            return "پرسمان شما یافت نشد!!!!!!"
        for i in range(12201):
            returnList.append(str(i))
    for item in returnNotList:
        for index in returnList:
            if item == index:
                returnList.remove(index)
    return returnList

dictionary = {}
dictionaryLen = []
my_normalizer = Normalizer()
myStem = FindStems()
punctuations = string.punctuation
stopWords = set(stopwords_list())
punctuations += ''.join(['،','؛','»','«','؟'])
wordList, tokenList, tokenCount, wordCount = makePositionalIndex()
print(tokenCount, wordCount)
# plt.plot(tokenList, wordList)
# UP = 0
# DOWN = 0
# for i in range(len(tokenList)):
#     UP += (tokenList[i] - np.mean(tokenList)) * (wordList[i]  - np.mean(wordList))
#     DOWN += (tokenList[i] - np.mean(tokenList)) ** 2
# b1 = UP / DOWN
# b0 = np.mean(wordList) - b1 * np.mean(tokenList)
# plt.plot(tokenList, [b0 + b1 * i for i in tokenList])
# # plt.show()
# freq = []
# lenght = []
# i = 0
# for index in dictionary:
#     i += 1
#     freq.append(np.log10(int(dictionary[index][0])))
#     lenght.append(np.log10(i))
# freq.sort(reverse=True)
# plt.plot(lenght, freq)
# plt.show()
while(True):
    totalCosine = []
    print("Enter your query:")
    voroodis = input()
    if voroodis == "end":
        break
    voroodis = word_tokenize(my_normalizer.normalize(voroodis))
    newVoroodis = []
    for voroodi in voroodis:
        voroodi = myStem.convert_to_stem(voroodi)
        newVoroodis.append(voroodi)
    voroodis = newVoroodis
    championList = createChampionList(voroodis, 10)
    queryTfIdf = calculateQueryTfIdf(voroodis)
    documentTfIdf = calculateDocumentTfIdf(voroodis, championList)
    # finalList = findQuery(voroodis)
    # finalList = [key for key, value in Counter(finalList).most_common()]
    # for item in finalList:
    # print(queryTfIdf)
    # print(documentTfIdf)
    for document in documentTfIdf:
        thisCosine = []
        thisCosine.append(document)
        thisCosine.append(calculateCosine(queryTfIdf, documentTfIdf[document]))
        totalCosine.append(thisCosine)
    totalCosine.sort(key=lambda x: x[1], reverse=True)
    with open('IR_data_news_12k.json', 'r') as js_file:
        data = json.load(js_file)
        # print(data["0"])
        for i in range(min(5, len(totalCosine))):
            print(data[totalCosine[i][0]]['url'])
            print(data[totalCosine[i][0]]['title'])
    # print(totalCosine)
    # championList(totalCosine, 10)
    # with open('readme.json', 'r') as file:
    #     js_file = json.load(file)
    #     for item in finalList:
    #         print(item)
    #         print(js_file[item]["url"])
    #         print(js_file[item]["title"])
    #         i += 1
    #         if i == 5:
    #             break
