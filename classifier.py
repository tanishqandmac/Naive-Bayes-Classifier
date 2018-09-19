import pickle
import nltk

sentenceDictionary = []
f = open('trainedDataset.tsv')
for sentence in f:
    sentenceToken = sentence.split('\t')
    sentenceDictionary.append({'text':sentenceToken[2],'category':sentenceToken[1]})

