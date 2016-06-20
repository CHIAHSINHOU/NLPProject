#!/usr/bin/env python 
# -*- coding: utf-8 -*-
import re
import fileinput
import random
import codecs
from itertools import izip
from sqlite import bncTag
from collections import defaultdict
import nltk
from nltk.stem import WordNetLemmatizer

feq = defaultdict(lambda: defaultdict(lambda: 0))

def words(text): return re.findall('[A-Za-z]+', text)

def to_sent(tokens, to_correct=True):
    for token in tokens:
        if token.startswith('{+') and token.endswith('+}'):
            if to_correct:
                yield token[2:-2]
        elif token.startswith('[-') and token.endswith('-]'):
            if not to_correct:
                yield token[2:-2]
        else:
            yield token

def get_diff_index(list1, list2):

    if len(list1) > len(list2):
        l1 = list2
        l2 = list1
    else:
        l1 = list1
        l2 = list2
    for n, item2 in enumerate(l1):
        if item2 != l2[n]:
            return n;

    # return {'LC1RR':RR[(LC1, w)], 'RC1RR':RR[(w, RC1)], 'LC+RC': RR[(LC1,w)]+RR[(w, RC1)]}



if __name__ == '__main__':

    # words = 'This concert hall was too small to enter all of the audience .'.split()
    # tagged = bncTag(words)
    lemmatizer = WordNetLemmatizer()
    # print lemmatizer.lemmatize('better', pos='a')
    count = 0
    for line_no, line in enumerate(fileinput.input()):
        # print line_no
        try:
            line = line.decode('utf-8').strip().lower()
        except:
            continue
        # token: word, edit or consecutive edits
        tokens = re.findall("((((\[\-((?!\-\]).)*\-\])|(\{\+((?!\+\}).)*\+\})))+|[\w-]+|\S+)", line)
        tokens = [ elements[0] for elements in tokens ]
        # output the entry if at least 1 edit exists
        words_correct = words(' '.join(to_sent(tokens)))
        words_incorrect = words(' '.join(to_sent(tokens, False)))
        # print words_correct
        # print words_incorrect
        index = get_diff_index(words_correct, words_incorrect)
        correct_tagged = bncTag(words_correct)
        incorrect_tagged = bncTag(words_incorrect)
        if index != None:
            if correct_tagged[index] == 'a' and incorrect_tagged[index] == 'a':
                w1 = lemmatizer.lemmatize(words_incorrect[index], pos='a')
                w2 = lemmatizer.lemmatize(words_correct[index], pos='a')
                if w1 != w2:
                    feq[w1][w2] += 1
                    count +=1
                    if count > 100:
                        break

                # print '{}_{}'.format(
                #     lemmatizer.lemmatize(words_incorrect[index], pos='a').encode('unicode_escape'), 
                # lemmatizer.lemmatize(words_correct[index], pos='a').encode('unicode_escape'))

    for key, item in feq.items():
        for w, count in item.items():
            print '{}\t{}\t{}'.format(key.encode('unicode_escape'), w.encode('unicode_escape'), count) 


