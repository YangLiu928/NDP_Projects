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
	labels.append(entry['policy_area'])
	print 'processing entey #' + str(count)
	count +=1

joblib.dump(texts,'training_set.pkl')
joblib.dump(labels,'training_labels.pkl')