import urllib2
import json
'''
Get data consisting of probabilities of occurence of alphabets in English (source:Pavel Micka) and  1/3 million most frequent words with counts (source: Peter Norvig)
'''
def get_data():
    letter_probs=[] #list of letter probabilities
    f=open('letters.txt','r')
    for line in f.readlines():
        c,p=line.split()
        letter_probs.append((c,float(p)))
    letter_probs.sort(key=lambda x:x[1], reverse=True)
    d_words={} #dictionary of words with frequency grouped by length of words
    total_count=0
    g=open('count_1w.txt','r')
    for line in g.readlines():
        s,count=line.split()
        if len(s) not in d_words:
            d_words[len(s)]=[]
        d_words[len(s)].append((s.upper(),int(count)))
        total_count+=int(count)
    return letter_probs,d_words,total_count

def start(runs):
    req="http://gallows.hulu.com/play?code=panaik@ucsd.edu"
    wrong=0
    letter_probs,d_words,total_count=get_data()
    for i in xrange(runs):
        s=urllib2.urlopen(req).read()
        d=json.loads(s)
        token=d['token']
        correct_guesses=[]
        incorrect_guesses=[]
        remaining=3
        while d['status']=='ALIVE':
            state=d['state']
            guess=make_guess(state,incorrect_guesses,correct_guesses,letter_probs,d_words,total_count)
            print state
            resp="http://gallows.hulu.com/play?code=panaik@ucsd.edu&token="+token+"&guess="+guess
            s=urllib2.urlopen(resp).read()
            d=json.loads(s)
            if d['remaining_guesses']<remaining:
                incorrect_guesses.append(guess)
                remaining=d['remaining_guesses']
            else:
                correct_guesses.append(guess)
        if d['status']=='DEAD':
            wrong+=1
        print d['state']
    error=float(wrong)/runs
    return error

def get_guessed_cache(guessed_chars):
  guessedCharCache = [False for i in range(26)]

  for char in guessed_chars:
    guessedCharCache[get_char_index(char)] = True

  return guessedCharCache

def get_best_guess(state, candidates, total_count, letter_probs, guessedCharCache):
  chance = []

  # If no candidates, return using letter probs. Return the first (highest prob) unguessed char
  if len(candidates) == 0:
    for char, prob in letter_probs:
      if guessedCharCache[get_char_index(char)] == False:
        return (char, prob)

  #for c in a-z, if c is already guessed, then continue. Otherwise, p(c)=sum_over_words(p(c|w)*p(w))
  for c in range(0, 26):
    ch = chr(ord('A') + c)
    prob = 0

    # This character has already been guessed
    if guessedCharCache[c] == True:
      continue

    for word, cnt in candidates:
      if ch in word:
        prob += float(cnt)/len(candidates)

    chance.append((ch, prob))

  chance = sorted(chance, key = lambda x: x[1], reverse=True)
  return chance[0]

def get_char_index(char):
  return ord(char) - ord('A')

# Returns a list of candidate words and their counts
def get_matching_words(d_words, state, guessedCharCache):
  ln = len(state)
  words = d_words[ln]
  retWords = []

  for wordCountTuple in words:
    candidate = True
    word = wordCountTuple[0]

    for i, char in enumerate(word):
      if (state[i] != '_' and char != state[i]):
        #print ("Mismatch", state, word, char, i)
        candidate = False
        break

      if state[i] == '_' and guessedCharCache[get_char_index(char)] == True:
        #print ("Guessed ", state, word, char, i)
        candidate = False
        break

    if candidate:
      retWords.append(wordCountTuple)

  return retWords

def make_guess(state,incorrect_guesses,correct_guesses,letter_probs,d_words,total_count):
    words=state.split()
    best_guess=[] #list of best guesses and their probabilities for each word
    guessedCharCache = get_guessed_cache(incorrect_guesses + correct_guesses)

    for s in words:
        #print s
        candidates = get_matching_words(d_words, s, guessedCharCache)
        #print candidates
        best_guess.append(get_best_guess(s, candidates, total_count, letter_probs, guessedCharCache))

    best_guess.sort(key=lambda x:x[1], reverse=True) #guess highest probability
    return best_guess[0][0]
