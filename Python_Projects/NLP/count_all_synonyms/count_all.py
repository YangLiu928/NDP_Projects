from nltk.corpus import wordnet as wn
from nltk import word_tokenize
import nltk

def _get_synonyms(word):
	# return [word]
	synonyms = set()
	meanings = wn.synsets(word)
	for meaning in meanings:
		lemma_names = meaning.lemma_names()
		for lemma_name in lemma_names:
			synonyms.add(lemma_name)
	synonyms = list(synonyms)
	return synonyms


def get_count(word, text):
	porter = nltk.PorterStemmer()
	synonyms = _get_synonyms(word)
	for index in range(0,len(synonyms)):
		synonyms[index] = porter.stem(synonyms[index])
	print synonyms

	text = word_tokenize(text)
	for index in range(0,len(text)):
		text[index] = porter.stem(text[index])
	# print text

	count = 0
	for text_word in text:
		if text_word in synonyms:
			count +=1

	return count

if __name__ == '__main__':
	word = 'pollute'
	text = 'pollution was caused by pollutants. water contamination is one example of pollution.'
	print get_count(word, text)