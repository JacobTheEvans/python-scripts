import re, collections
"""
Dictionary taken from /usr/share/dict/ in ubuntu linux.
Functions words,train,edits1,know_edits1,know_edits2,know,correct
all taken from http://norvig.com/spell-correct.html.
"""

NWORDS = train(words(file('dict/dictionary.txt').read()))

alphabet = 'abcdefghijklmnopqrstuvwxyz'

def words(text): return re.findall('[a-z]+', text.lower()) 

def train(features):
    model = collections.defaultdict(lambda: 1)
    for f in features:
        model[f] += 1
    return model

def edits1(word):
   splits     = [(word[:i], word[i:]) for i in range(len(word) + 1)]
   deletes    = [a + b[1:] for a, b in splits if b]
   transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b)>1]
   replaces   = [a + c + b[1:] for a, b in splits for c in alphabet if b]
   inserts    = [a + c + b     for a, b in splits for c in alphabet]
   return set(deletes + transposes + replaces + inserts)

def known_edits2(word):
    return set(e2 for e1 in edits1(word) for e2 in edits1(e1) if e2 in NWORDS)

def known(words): return set(w for w in words if w in NWORDS)

def correct(word):
    candidates = known([word]) or known(edits1(word)) or known_edits2(word) or [word]
    return max(candidates, key=NWORDS.get)

def loadDict():
	f = open("dict/dictionary.txt")
	data = f.read().split("%%%%%%%%%%%%%%%")
	result = {}
	for i in data:
		result[i[1][0]] = i
	return result
	
def check(word):
	words = loadDict()
	try:
		check_list = words[word[0]]
		if word in check_list:
			return True
		else:
			return False
	except KeyError:
		return False

def process(text):
	result = {}
	for i in text.split(" "):
		punctuation = ["!",".","?"]
		isPunc = False

		for punc in punctuation:
			if punc in i:
				i = i.replace(punc, "")

		if check(i) == False:
			result[i] = check(i.lower())
		else:
			result[i] = check(i)
	return result
