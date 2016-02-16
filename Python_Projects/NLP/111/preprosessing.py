import cPickle as pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
import json
from sklearn.naive_bayes import MultinomialNB
import numpy as np
from sklearn.linear_model import SGDClassifier
from nltk import word_tokenize          
from nltk.stem import WordNetLemmatizer 
from sklearn import cross_validation
from sklearn.naive_bayes import GaussianNB
from sklearn import svm


# class LemmaTokenizer(object):
#     def __init__(self):
#         self.wnl = WordNetLemmatizer()
#     def __call__(self, doc):
#         return [self.wnl.lemmatize(t) for t in word_tokenize(doc)]



with open ('data.json') as input:
	raw_data = json.load(input)



texts = []
labels = []
count = 1
for entry in raw_data:
	texts.append(entry['summary'])
	labels.append(entry['policy_area'])
	print 'processing entey #' + str(count)
	count +=1

# tokenization and stop words removal
count_vect = CountVectorizer(stop_words = 'english')
tokenized_texts = count_vect.fit_transform(texts)

# tfidf feature vector extraction
tfidf_transformer = TfidfTransformer()
texts_tfidf = tfidf_transformer.fit_transform(tokenized_texts)

# storing processed data locally with pickle
# pickle.dump(texts_tfidf,open('feature_vectors.p','wb'))
# pickle.dump(labels,open('labels.p','wb'))


# length = len(labels)
# border = int(length*0.9)
# training_data = texts_tfidf[:border]
# training_labels = labels[:border]
# testing_data = texts_tfidf[border:]
# testing_label = labels[border:]





NB = MultinomialNB()
NB_scores = cross_validation.cross_val_score(NB, texts_tfidf, labels, cv=5)
print NB_scores






# pickle.dump(NB_classifier,open('NB_classifier.p','wb'))


SVM = SGDClassifier(loss='hinge', penalty='l2',alpha=1e-3, n_iter=5, random_state=42)

SVM_scores = cross_validation.cross_val_score(SVM, texts_tfidf, labels, cv=5)
print SVM_scores


# GNB = GaussianNB()
# GNB_scores = cross_validation.cross_val_score(GNB, texts_tfidf.toarray(), labels, cv=5)
# print GNB_scores

SVM_Linear = svm.LinearSVC()
SVM_Linear_scores = cross_validation.cross_val_score(SVM_Linear, texts_tfidf.toarray(), labels, cv=5)
print SVM_Linear_scores


# pickle.dump(SVM,open('SVM.p','wb'))





# predicted = NB_classifier.predict(testing_data)
# print "accuracy = " + str(np.mean(predicted == testing_label)) 

# predicted = SVM.predict(testing_data)
# print "accuracy = " + str(np.mean(predicted == testing_label)) 