from sqlite import search_correct
from sqlite import bncTag
from linggle_api import search_count
import re
from gensim.models import Word2Vec
import os

model = Word2Vec.load(os.path.dirname(__file__)+'/word2vec.model')

def words(text): return re.findall('[A-Za-z]+|[^ A-Za-z]+', text)
def word(text): return re.findall('[A-Za-z]+', text)
def findAdjNoun(w, tags):
	if 'a' in tags:
		index = tags.index('a')
		for i, t in enumerate(tags[index+1:]):
			if t == 'n':
				return w[index], w[i+index+1]
		for i, t in reversed(list(enumerate(tags[:index]))):
			if t == 'n':
				return w[index], w[i]
	return None, None

def adjCorrect(text):

	w = words(text.lower())
	# print w
	tags = bncTag(w)
	# print tags
	adj, noun = findAdjNoun(w, tags)
	# print adj, noun
	score = []
	if adj != None:
		correct = search_correct(adj)
		correctMap = {x[0]:x[1] for x in correct}
		if correctMap == {}:
			try:
				for correct, sim in model.most_similar(adj, topn=5):
					c = word(correct.lower())
					if c:
						correctMap[correct] = sim
			except:
				correctMap[adj] = 1
			correctMap[adj] = 1
		candidate = correctMap.keys()
		# print candidate
		# print correctMap
		counts = search_count(candidate, noun)
		# print counts
		for text, count in counts:
			text = text.split()
			score.append((text[0], count * correctMap[text[0]]))
		score.sort(key = lambda x:x[1], reverse=True)

	return adj, score

if __name__ == '__main__':

	text = 'it is a large issue'
	adj, score = adjCorrect(text)
	print "text: {}\nadj: {}".format(text, adj)
	print "candidate:"
	for correct, s in score[:5]:
		print correct, s





