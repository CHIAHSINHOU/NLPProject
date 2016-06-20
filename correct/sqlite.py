import fileinput
import sqlite3
from itertools import izip
import os

conn = sqlite3.connect(os.path.dirname(__file__)+'/adjCorrect.db')

RELATION_TABLE_SCHEMA = ('CREATE TABLE Relation('
                    "wrong TEXT, "
                    'correct TEXT, '
                    'probability REAL, '
                    'PRIMARY KEY (wrong, correct)'
                    ');')

WORDLEMMA_TABLE_SCHEMA = ('CREATE TABLE WordLemma('
                    "word TEXT, "
                    'lemma TEXT, '
                    'tag TEXT, '
                    'probability REAL, '
                    'PRIMARY KEY (word, lemma, tag)'
                    ');')


def get_connection():

    conn = sqlite3.connect(os.path.dirname(__file__)+'/adjCorrect.db')
    conn.text_factory = str
    return conn

def parse_adj_relation(fileName):
    for line in fileinput.input(fileName):
        wrong, correct = line.strip().split('\t')
        correct, prob = correct.split(' ')
        yield (wrong, correct, float(prob))

def parse_bnc_word_lemma():
    for line in fileinput.input('bnc.word.lemma.pos.txt'):
        lemma, word, tag, count, total, prob = line.split()
        # data parsing
        lemma, word, tag, count, total, prob = lemma[1:-1], word[1:-1], tag[1:-1], float(count), float(total), float(prob)
        # ignore foreign word (tag = F)
        if tag == 'F': continue
        yield (word, lemma, tag, prob)


def init_db(word_lemmas, relations):
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("DROP TABLE IF EXISTS Relation;")
        cur.execute("DROP TABLE IF EXISTS WordLemma;")
        # create table
        cur.execute(RELATION_TABLE_SCHEMA)
        cur.execute(WORDLEMMA_TABLE_SCHEMA)
        # insert data
        cur.executemany('INSERT INTO Relation VALUES (?,?,?)', relations)
        cur.executemany('INSERT INTO WordLemma VALUES (?,?,?,?)', word_lemmas)

def search_correct(word):
    with get_connection() as conn:
        cur = conn.cursor()
        cmd = 'SELECT correct,probability FROM Relation WHERE wrong=? ORDER BY probability DESC;'
        return cur.execute(cmd, (word,))

def search_tag(word):
    with get_connection() as conn:
        cur = conn.cursor()
        cmd = 'SELECT tag FROM WordLemma WHERE word=? ORDER BY probability DESC;'
        for res in cur.execute(cmd, (word,)):
            return res[0]

def bncTag(words):
    tagged = [ str(search_tag(w.strip().lower())) for w in words ]
    return tagged

if __name__ == '__main__':
    # bnc word lemma data
    relations = list()
    for i in xrange(10):
        relations += list(parse_adj_relation('wtf/reducer-0'+str(i)))
    for i in xrange(6):
        relations += list(parse_adj_relation('wtf/reducer-1'+str(i)))
    word_lemmas = list(parse_bnc_word_lemma())
    # insert data into sqlite3 db
    init_db(word_lemmas, relations)
    # tag example
    word = 'small'
    res = search_correct(word)
    for correct, prob in res:
        print '{}\t{}'.format(correct, prob)
    words = 'This concert hall was too small to enter all of the audience .'.split()
    tagged = bncTag(words)
    print ' '.join('%s/%s' % wordTag for wordTag in izip(words, tagged))
