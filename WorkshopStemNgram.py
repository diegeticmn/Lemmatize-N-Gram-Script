#!/usr/bin/env python
# -*- coding: utf-8 -*-
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
from nltk import ngrams
from collections import Counter, OrderedDict
import string
from nltk.corpus import stopwords

#---------LEMMA AND NGRAM FREQUENCY PROGRAM--------#
# AUTHOR: Kevin Swanberg, University of Minnesota Duluth

# DATE: December 13th, 2017

# FUNCTION: This function takes an input text file, tokenizes the text and splits it into sentences
#           then takes the lemmas of the words in the sentences and finds the ngram frequencies of
#           the lemmas and outputs this to a text file with format (NGRAM) FREQ

# REQUIREMENTS: PYTHON 3.5 OR GREATER
#               NLTK

#Open input data - replace text file with your data (in the form of a text file in the same directory as this file)
with open('clientreports.txt', encoding='utf-8') as f:
    text=f.read().replace('\n', ' ')

# split the document into sentences and tokenize each sentence

class Splitter(object):

	#Load tokenizer for english, Tokenize each word
    def __init__(self):
        self.splitter = nltk.data.load('tokenizers/punkt/english.pickle')
        self.tokenizer = nltk.tokenize.TreebankWordTokenizer()

#Split into separate words - each outputted list is a sentence
    def split(self,text):

        # split into single sentence
        sentences = self.splitter.tokenize(text)
        # tokenization in each sentences
        tokens = [self.tokenizer.tokenize(sent) for sent in sentences]
        return tokens

#Convert Penn Treebank tags to Wordnet tags, whoop!
class LemmatizationWithPOSTagger(object):
    def __init__(self):
        pass
    def get_wordnet_pos(self,treebank_tag):

        if treebank_tag.startswith('J'):
            return wordnet.ADJ
        elif treebank_tag.startswith('V'):
            return wordnet.VERB
        elif treebank_tag.startswith('N'):
            return wordnet.NOUN
        elif treebank_tag.startswith('R'):
            return wordnet.ADV
        else:
            # As default pos in lemmatization is Noun
            return wordnet.NOUN

    def pos_tag(self,tokens):
        # Find POS tag for each word - outputs a list of tuples as [(Word, TAG), (Word, TAG)...]
        pos_tokens = [nltk.pos_tag(token) for token in tokens]

        # lemmatization using pos tag
        # convert into list of tuples as [('Word', 'Lemma', TAG), ('Word', 'Lemma', ['TAG'])
        pos_tokens = [ [(word, lemmatizer.lemmatize(word,self.get_wordnet_pos(pos_tag)), [pos_tag]) for (word,pos_tag) in pos] for pos in pos_tokens]
        return pos_tokens

#Initialize
lemmatizer = WordNetLemmatizer()
splitter = Splitter()
lemmatization_using_pos_tagger = LemmatizationWithPOSTagger()

#Make lowercase
text = text.lower()

#Remove punctuation
replace_punctuation = str.maketrans(string.punctuation, ' '*len(string.punctuation))
text = text.translate(replace_punctuation)

#Remove Stop Words
stop_words = set(stopwords.words('english'))
text = ' '.join([word for word in text.split() if word not in stop_words])

#split document into sentence followed by tokenization
tokens = splitter.split(text)

#lemmatize with pos tagger
lemma_pos_token = lemmatization_using_pos_tagger.pos_tag(tokens)
lemma_list = []

#Get just the lemmas
for i in lemma_pos_token:
	lemma = []
	for j in i:
		lemma.append(j[1])
	lemma_list.append(lemma)

#Initialize the counter
frequencies = Counter([])


#Iterates through sentences, finds ngrams and counts frequences
for i in lemma_list:
	trigrams = ngrams(i, 2) #Replace 3 with n for n-grams
	frequencies += Counter(trigrams)

#Write frequeinces to output file - output format is (NGRAM), FREQ
with open("output.txt", 'w') as file:
    for k,v in  frequencies.most_common():
        file.write( "{} ; {}\n".format(k,v) )
