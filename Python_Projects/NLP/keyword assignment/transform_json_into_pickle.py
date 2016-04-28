import json
from sklearn.externals import joblib

# load the training data
with open ('data.json') as input:
	raw_data = json.load(input)


texts = []
labels = []
count = 1
for entry in raw_data:
	texts.append(entry['summary'])
	labels.append(entry['keywords'])
	print 'processing entey #' + str(count)
	count +=1
	# print labels

joblib.dump(texts[:1000],'training_set.pkl')
joblib.dump(labels[:1000],'training_labels.pkl')

# print labels