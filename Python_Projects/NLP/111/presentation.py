import cPickle as pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
import json
from sklearn.naive_bayes import MultinomialNB
import numpy as np
from sklearn.linear_model import SGDClassifier

NB = pickle.load(open('NB_classifier.p','rb'))
SVM = pickle.load(open('SVM.p','rb'))

