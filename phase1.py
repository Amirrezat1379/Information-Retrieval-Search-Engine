import json
from typing import Dict
from parsivar import Normalizer, Tokenizer, FindStems
from hazm import stopwords_list, word_tokenize
import string

# def estekhrajToken(newsList):
#     return thisList

class DocumentWord:
    def __init__(self, documentWord, token):
        self

class word:
    def __init__(self, token):
        self.counter = 0
        self.token = token
        self.documentWord = dict()
    
    def importWord(self, posotion, documentWord):
        self.counter += 1
        if documentWord not in saleh:
            print(malmal)

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
with open('IR_data_news_12k.json', 'r') as js_file:
    for jsonObj in js_file:
        js_data = json.loads(jsonObj)
        newsList.append(js_data)
        for i in js_data:
            thisList.append(i)
            tokens = []
            tok = []
            # print(i)
            content = js_data[i]['content']
            # print(content.translate(str.maketrans('', '', punctuations)))
            token_list = word_tokenize(my_normalizer.normalize(content.translate(str.maketrans('', '', punctuations))))
            for token in token_list:
                j += 1
                tok.append(token)
                tok.append(j)
                tokens.append(tok)
            j = 0
            thisList.append(tokens)
            print(i)
            print(tokens)
        
# myList = estekhrajToken(newsList)
print(thisList[0])
# print(myList)
