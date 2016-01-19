from nltk import word_tokenize
import nltk
from nltk.stem import WordNetLemmatizer


lemmatizer = WordNetLemmatizer()
porter = nltk.PorterStemmer()

word = 'pollute'
word= lemmatizer.lemmatize(word)
word = porter.stem(word)

text = 'pollution was caused by pollutants. water contamination is one example of pollution.'
text = word_tokenize(text)

for index in range(0,len(text)):
	text[index] = porter.stem(lemmatizer.lemmatize(text[index]))

count = 0
for text_word in text:
	if word == text_word:
		count +=1

print count


