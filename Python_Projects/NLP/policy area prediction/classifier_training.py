from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
import json
import numpy as np
from sklearn import svm
from sklearn.pipeline import Pipeline
from sklearn.externals import joblib

training_set = joblib.load('training_set.pkl')
training_labels = joblib.load('training_labels.pkl')

SVM_Linear = Pipeline([
	('CountVectorizer',CountVectorizer(stop_words = 'english', ngram_range = (1,1))),
	('TfidfTransformer',TfidfTransformer()),
	('classifier',svm.LinearSVC())
	])

SVM_Linear = SVM_Linear.fit(training_set,training_labels)

joblib.dump(SVM_Linear,'classifiers/linear_svm_classifier.pkl')