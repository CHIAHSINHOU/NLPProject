import requests
import urllib

def parseData(rowdict):
    def extract_word(word):
        return word.replace('<strong>', '').replace('</strong>', '').strip()
    return (' '.join(map(extract_word, rowdict['phrase'])), float(rowdict['count']))

def linggleit(query):
    # print query
    url = 'http://linggle.com/query/{}'.format(urllib.quote(query, safe=''))
    r = requests.get(url)
    if r.status_code == 200:
        # return map(parseData, r.json())
        # solve duplication problem
        res = dict()
        for ngram, count in map(parseData, r.json()):
            if ngram not in res:
                res[ngram] = count
        return sorted(res.items(), key=lambda x: x[-1], reverse=True)

def gen_query(candidate, noun):
    return '/'.join(candidate)+' '+noun

def search_count(candidate, noun):
    return linggleit(gen_query(candidate, noun))

if __name__ == "__main__":
    res = search_count(['large', 'big'], 'issue')
    print res[0]
    print '\n'.join( '\t'.join( str(y) for y in x ) for x in res )