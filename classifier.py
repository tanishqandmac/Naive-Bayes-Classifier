import pickle
import nltk
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 

stop_words = set(stopwords.words('english')) 

def dictAddition(dictionary,string):
    tokens = nltk.word_tokenize(string.lower())
    for token in tokens:
        if token.lower() not in stop_words:
            if token not in dictionary:
                dictionary[token] = 1.0
            else:
                dictionary[token] += 1.0
    return dictionary

sentenceDictionary = []
SarcasmDict={}
notSarcasmDict={}
DictionaryAll = {}
bayesProbability_1 = 1
bayesProbability_0 = 1
SCount = 0.0
NCount = 0.0

f = open('trainedDataset.tsv')
for sentence in f:
    sentenceToken = sentence.split('\t')
    try:
        sentenceDictionary.append({'text':sentenceToken[2].encode('utf8'),'category':sentenceToken[1]})
        if(sentenceToken[1]=="0"):
            SCount+=1.0
        else:
            NCount+=1.0
    except:
        continue

'''
for k in sentenceDictionary:
    if k['category']=="0":
        notSarcasmDict = dictAddition(notSarcasmDict,k['text'])
    else:
        SarcasmDict = dictAddition(SarcasmDict,k['text'])

with open("sarcasmDict.pkl", "wb") as f:
    pickle.dump(SarcasmDict, f)

with open("NotSarcasmDict.pkl", "wb") as f:
    pickle.dump(notSarcasmDict, f)
'''

with open("sarcasmDict.pkl", "rb") as f:
    SarcasmDict = pickle.load(f)
DictionaryAll = SarcasmDict

with open("NotSarcasmDict.pkl", "rb") as f:
    notSarcasmDict = pickle.load(f)
DictionaryAll.update(notSarcasmDict)

testSentence = "if i had my license the only thing i'd use it for is mcdonalds at 3am #sarcasm"
tokens = nltk.word_tokenize(testSentence.lower())
tokenFiltered = []
for token in tokens:
    if token not in stop_words:
        tokenFiltered.append(token)

for token in tokenFiltered:
    try:
        bayesProbability_1 *= (1.0+SarcasmDict[token])/(len(SarcasmDict)+len(DictionaryAll))
        bayesProbability_0 *= (1.0+notSarcasmDict[token])/(len(notSarcasmDict)+len(DictionaryAll))
        
    except:
        bayesProbability_1 *= (1.0)/(len(SarcasmDict)+len(DictionaryAll))
        bayesProbability_0 *= (1.0)/(len(notSarcasmDict)+len(DictionaryAll))
   

    

bayesProbability_1 *= (SCount/SCount+NCount)
bayesProbability_0 *= (NCount/SCount+NCount)

print "Sarcastic Sentiment Analysis".center(50,"-")
print "Sentence: "+testSentence

if(bayesProbability_1>bayesProbability_0):
    print "Result: Sarcastic"
else:
    print "Result: Not Sarcastic"
print "\n"

print "Sarcasm Probability: "+ str(bayesProbability_1)
print "Non Sarcasm Probability: "+ str(bayesProbability_0)
print "\n"