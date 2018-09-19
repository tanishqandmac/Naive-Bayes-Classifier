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

def datasetDictCreation(filename):
    SCount = 0.0
    NCount = 0.0
    f = open(filename)
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
    return sentenceDictionary,SCount,NCount

def separateDictionaryCreation(notSarcasmDict,SarcasmDict,sentenceDictionary):
    for k in sentenceDictionary:
        if k['category']=="0":
            notSarcasmDict = dictAddition(notSarcasmDict,k['text'])
        else:
            SarcasmDict = dictAddition(SarcasmDict,k['text'])
    return SarcasmDict,notSarcasmDict

def pickleLoad(filename):
    with open(filename, "rb") as f:
        filetype = pickle.load(f)
    return filetype

def pickleUnload(filename,filetype):
    with open(filename, "wb") as f:
        pickle.dump(filetype, f)

def bayesianClassification(testSentence,SarcasmDict,notSarcasmDict,SCount,NCount):
    bayesProbability_1 = 1
    bayesProbability_0 = 1
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

    return bayesProbability_1,bayesProbability_0

#Variable Declaration
sentenceDictionary = []
SarcasmDict={}
notSarcasmDict={}
DictionaryAll = {}
SCount = 0.0
NCount = 0.0
filename = 'trainedDataset.tsv'

#Dataset to Dictionary Mapping
sentenceDictionary,SCount,NCount = datasetDictCreation(filename)

#Model Creation (If not Created)
'''
SarcasmDict,notSarcasmDict = separateDictionaryCreation(notSarcasmDict,SarcasmDict,sentenceDictionary)
pickleUnload("sarcasmDict.pkl",SarcasmDict)
pickleUnload("NotSarcasmDict.pkl",notSarcasmDict)
'''

#Downloading Models
SarcasmDict = pickleLoad("Model/sarcasmDict.pkl")
notSarcasmDict = pickleLoad("Model/NotSarcasmDict.pkl")
DictionaryAll = SarcasmDict
DictionaryAll.update(notSarcasmDict)

#Sentence Classification
testSentence = "if i had my license the only thing i'd use it for is mcdonalds at 3am #sarcasm"
bayesProbability_1,bayesProbability_0 = bayesianClassification(testSentence,SarcasmDict,notSarcasmDict,SCount,NCount)

#Output
print "\n"
print "Sarcastic Sentiment Analysis".center(50,"-")
print "\n"
print "Sentence: "+testSentence
if(bayesProbability_1>bayesProbability_0):
    print "Result: Sarcastic"
else:
    print "Result: Not Sarcastic"
print "\n"
print "Sarcastic Probability: "+ str(bayesProbability_1)
print "Non Sarcastic Probability: "+ str(bayesProbability_0)
print "\n"
