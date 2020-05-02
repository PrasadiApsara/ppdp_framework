import tweepy
from tweepy import API
from tweepy import Cursor
from tweepy import Stream
import spacy
import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt
import re
import csv
import nltk
from textblob import TextBlob
from sklearn.tree import DecisionTreeClassifier
from sklearn.feature_extraction import DictVectorizer
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score
from datetime import datetime


class PPDP():
    def features(self, sentence, index, postags, doc):
        """ sentence: [w1, w2, ...], index: the index of the word """
        #print("before postag" + datetime.now().strftime("%H:%M:%S"))
        #postags = nltk.pos_tag(sentence)
        #print("after postag" + datetime.now().strftime("%H:%M:%S"))
        #nlp = spacy.load("en_core_web_sm")
        #str = " "
        #doc = nlp(str.join(sentence))
        #print("after spacy" + datetime.now().strftime("%H:%M:%S"))
        #spacy_tag = ""
        #for x in doc.ents:
        #    if x.text == sentence[index]:
        #        spacy_tag = matching_terms[0].label_
        #        print(spacy_tag)
        #        break
        spacy_tag = ""
        result = filter(lambda x: x.text == sentence[index], doc.ents)
        matched = list(result)
        if(len(matched) > 0):
            spacy_tag = matched[0].label_
            print(spacy_tag)
            print(sentence[index])
        return {
            'word': self.remov_punct(sentence[index]),
            'is_first': index == 0,
            'is_last': index == len(sentence) - 1,
            'is_capitalized': len(sentence[index]) > 1 and sentence[index][0].upper() == sentence[index][0],
            'is_all_caps': sentence[index].upper() == sentence[index],
            'is_all_lower': sentence[index].lower() == sentence[index],
            'prefix-1': '' if len(sentence[index]) < 1 else sentence[index][0],
            'prefix-2': '' if len(sentence[index]) < 1 else sentence[index][:2],
            'prefix-3': '' if len(sentence[index]) < 1 else sentence[index][:3],
            'suffix-1': '' if len(sentence[index]) < 1 else sentence[index][-1],
            'suffix-2': '' if len(sentence[index]) < 1 else sentence[index][-2:],
            'suffix-3': '' if len(sentence[index]) < 1 else sentence[index][-3:],
            'prev_word': '' if index == 0 else sentence[index - 1],
            'next_word': '' if index == len(sentence) - 1 else sentence[index + 1],
            'has_hyphen': '-' in sentence[index],
            'is_numeric': sentence[index].isdigit(),
            'capitals_inside': sentence[index][1:].lower() != sentence[index][1:],
            'pos_tag': postags[index][1],
            'named_entity': spacy_tag
        }

    def untag(self, tagged_sentence):
        return [w for w, t in tagged_sentence]

    def remov_punct(self, withpunct):
        punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
        without_punct = ""
        char = 'nan'
        for char in withpunct:
            if char not in punctuations:
                without_punct = without_punct + char
        return(without_punct)

    def transform_to_dataset(self, tagged_sentences):
        print("start transforming")
        X, y = [], []
        count = 0
        nlp = spacy.load("en_core_web_sm")
 
        for tagged in tagged_sentences:
            count = count + 1
            print(count)
            postags = nltk.pos_tag(self.untag(tagged))
            str = " "
            doc = nlp(str.join(self.untag(tagged)))
            for index in range(len(tagged)):
                X.append(self.features(self.untag(tagged), index, postags, doc))
                y.append(tagged[index][1])
 
        return X, y

    def transform_to_dataset_crf(self, tagged_sentences):
        X, y = [], []
 
        for tagged in tagged_sentences:
            X.append([self.features(self.untag(tagged), index) for index in range(len(tagged))])
            y.append([tagged[index][1] for index in range(len(tagged))])
 
        return X, y

    def pos_tag(self, sentence, clf):
        nlp = spacy.load("en_core_web_sm")
        postags = nltk.pos_tag(sentence)
        str = " "
        doc = nlp(str.join(sentence))
        tags = clf.predict([self.features(sentence, index, postags, doc) for index in range(len(sentence))])
        return zip(sentence, tags)

    def sanitize(self, token):
        word = token[0]
        tag = token[1]
        if tag == "DI":
                word = "*****"
        elif tag == "QIGENDER":
                word = "<Gender>"
        elif tag == "QIAGE":
            if word.isnumeric() and int(word) > 0 :
                age = int(word)
                ageLowerBound = age - 5
                ageUpperBound = age + 5
                word = str(ageLowerBound) + "-"+ str(ageUpperBound)
                print(word)
        elif tag == "QIRACE":
            word = "<Race>"
        elif tag == "QIJOB":
            word = "<Job>"
        elif tag == "QIREGION":
            word = "<Region>"
        elif tag == "QIRELIGION":
            word = "<Religion>"
        elif tag == "QILANG":
            word = "<Language>"
        elif tag == "QIMARITAL":
            word = "<Any>"
        return word

    def remove_pattern(self, input_txt, pattern):
        r = re.findall(pattern, input_txt)
        for i in r:
            input_txt = re.sub(i, '', input_txt)
        
        return input_txt

    def hashtag_extract(self, x):
        hashtags = []
        # Loop over the words in the tweet
        for i in x:
            ht = re.findall(r"#(\w+)", i)
            hashtags.append(ht)

        return hashtags

