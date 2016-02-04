import cPickle as pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
import json
from sklearn.naive_bayes import MultinomialNB
import numpy as np
from sklearn.linear_model import SGDClassifier
from nltk import word_tokenize          
from nltk.stem import WordNetLemmatizer 

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
pickle.dump(texts_tfidf,open('feature_vectors.p','wb'))
pickle.dump(labels,open('labels.p','wb'))


length = len(labels)
border = int(length*0.9)
training_data = texts_tfidf[:border]
training_labels = labels[:border]
testing_data = texts_tfidf[border:]
testing_label = labels[border:]

NB_classifier = MultinomialNB().fit(training_data, training_labels)

pickle.dump(NB_classifier,open('NB_classifier.p','wb'))


SVM = SGDClassifier(loss='hinge', penalty='l2',alpha=1e-3, n_iter=5, random_state=42).fit(training_data, training_labels)
pickle.dump(SVM,open('SVM.p','wb'))

predicted = NB_classifier.predict(testing_data)
print "accuracy = " + str(np.mean(predicted == testing_label)) 

predicted = SVM.predict(testing_data)
print "accuracy = " + str(np.mean(predicted == testing_label)) 