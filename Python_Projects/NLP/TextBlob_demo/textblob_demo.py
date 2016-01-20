from textblob import TextBlob

text = [
	'bad',
	'terrible',
	'good',
	'fabulous',
	'great',
	'computer',
	'the food is good',
	'the food is bad',
	'the food is not good',
	'the food is not bad',
	'the food is not so good',
	'the food is not too bad',
	'the weather is nice',
	'it\'s freezing today'
	]


for word in text:
	print word + ' (' + str(TextBlob(word).sentiment.polarity) + ')'
