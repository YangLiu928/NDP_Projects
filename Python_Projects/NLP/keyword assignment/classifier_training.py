from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
import json
import numpy as np
from sklearn import svm
from sklearn.pipeline import Pipeline
from sklearn.externals import joblib
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.multiclass import OneVsRestClassifier
from sklearn.svm import SVC
import time

print 'loading training data'

training_set = joblib.load('training_set.pkl')
training_labels = joblib.load('training_labels.pkl')

print 'generating binarized labels'
binarizer = MultiLabelBinarizer()
binarized_training_labels = binarizer.fit_transform(training_labels)
shape = binarized_training_labels.shape
print 'shape of binarized labels is ' + str(shape[0]) + ' by ' + str(shape[1])


print 'tokenizing training text'
count_vect = CountVectorizer(stop_words = 'english', ngram_range = (1,1))
tokenized_texts = count_vect.fit_transform(training_set)

print 'generating TFIDF features for training text'
tfidf_transformer = TfidfTransformer()
texts_tfidf = tfidf_transformer.fit_transform(tokenized_texts)

print 'training classifier'
start_time = time.time()
classifier = OneVsRestClassifier(SVC(kernel='linear',probability=True))
classifier.fit(texts_tfidf,binarized_training_labels)
print 'time for training is ' + str((time.time()-start_time)) + 'seconds'


# SVM_Linear = Pipeline([
# 	('CountVectorizer',CountVectorizer(stop_words = 'english', ngram_range = (1,1))),
# 	('TfidfTransformer',TfidfTransformer()),
# 	('classifier',svm.LinearSVC())
# 	])

# SVM_Linear = SVM_Linear.fit(training_set,training_labels)

joblib.dump(classifier,'classifiers/OVR_linear_svm_classifier.pkl')
joblib.dump(count_vect,'count_vect.pkl')
joblib.dump(tfidf_transformer,'tfidf_transformer.pkl')
joblib.dump(binarizer,'binarizer.pkl')

