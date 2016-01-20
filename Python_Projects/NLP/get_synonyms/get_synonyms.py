from nltk.corpus import wordnet as wn

word = 'pollution'

synonyms = set()
meanings = wn.synsets(word)
for meaning in meanings:
	lemma_names = meaning.lemma_names()
	for lemma_name in lemma_names:
		synonyms.add(lemma_name)

synonyms = list(synonyms)
print 'synonyms of word \"' + word + '\" include the following:'
print synonyms