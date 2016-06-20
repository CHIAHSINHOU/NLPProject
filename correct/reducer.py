#!/usr/bin/env python
# echo 'aaa bbb ccc\naaa bbb aaa' | python nc-map.py
from collections import defaultdict
import re
import fileinput
from collections import Counter
from nltk.corpus import wordnet as wn
from gensim.models import Word2Vec

def words(text): return re.findall('[A-Za-z]+', text)

feq = defaultdict(lambda: defaultdict(lambda: 0))

model = Word2Vec.load('word2vec.model')

for line in fileinput.input():
    wrong, correct, count = line.decode('unicode_escape').strip().split('\t')
    feq[wrong][correct] += int(count)

for wrong, item in feq.items():

	total = sum(item.values())
	for correct, count in item.items():
		feq[wrong][correct] = float(count)/total

for wrong, item in feq.items():
	for correct, count in item.items():
		
		try:
			sim = model.similarity(wrong, correct)
		except:
			feq[wrong][correct] = float(count)
			continue
		if sim > 0:
			count = float(count) + sim
		else:
			count = float(count)

		feq[wrong][correct] = count

	try:
		for correct, sim in model.most_similar(wrong, topn=5):
			c = words(correct)
			if c:
				feq[wrong][c[0]] += sim
	except:
		feq[wrong][wrong] = 1
		
	feq[wrong][wrong] = 1

	total = sum(item.values())


	for correct, count in item.items():
		feq[wrong][correct] = count/total

for wrong, item in feq.items():
	for correct, count in item.items():
		print '{}\t{} {}'.format(wrong.encode('utf-8'), correct.encode('utf-8'), count)




