import nltk
word_list = [w for w in nltk.corpus.words.words('en') if len(w) == 5 and w.islower()]
words = set(word_list)

confirmed = {}
confirmed_not = []
recs = {}
goal = [-1, -1, -1, -1, -1]
ans = [' ', ' ', ' ', ' ', ' ']

# ZERO PASS
# Remove words that have letters we know are not in the word
# ie. if we know the word does not contain a 't', remove all words with 't'
def pass_zero(anti):
    global recs
    for rec in recs:
        for letter in anti:
            if letter in rec:
                recs[rec] = -1

# FIRST PASS
# Remove words that don't have confirmed letters
# ie. If we know the word has an 'h', remove all words without an 'h'
def pass_one(confirmed):
    global recs
    global num_recs

    for rec in recs:
        for conf in confirmed:
            if conf not in rec:
                recs[rec] = -1

# SECOND PASS
# Remove words that don't have for-certain letters in the right location
# ie. if we know the word has an 'e' in position 2, remove words that don't have an 'e' as the second letter
def pass_two():
    global recs
    global goal
    global num_recs

    for rec in recs:
        for i in range(len(goal)):
            if goal[i] == 2: # IF A LETTER IN THIS SPOT IS CONFIRMED TO BE CORECT LOCATION
                if rec[i] != ans[i]: # if the confirmed location letter is not in the same place in the recommendation
                    recs[rec] = -1
    

# THIRD PASS
# Remove words that have confirmed letters in the wrong location
# ie. if we know there is not an 'h' in position 4, remove all words that have an 'h' there
def pass_three(confirmed):
    global recs

    for rec in recs:
        for letter in confirmed:
            places = len(confirmed[letter])
            for i in range(places):
                curlist = confirmed[letter]
                if rec[curlist[i]] == letter:
                    recs[rec] = -1

def getRecommendations(letters):
    global recs
    global confirmed_not

    pass_zero(confirmed_not)
    

    pass_one(letters)


    pass_two()


    pass_three(letters)

def countRecs(dic):
    total = 0

    for el in dic:
        if dic[el] == 1:
            total += 1
    return total

def initRecs():
    global recs
    for w in words:
        recs[w] = 1

def filterRecs():
    global recs

    tmp = recs.copy()

    # 13 least common letters in te alphabet, from least frequent (q) to more frequent (m)
    least_common = ['q', 'j', 'z', 'x', 'v', 'k', 'w', 'y', 'f', 'b', 'g', 'h', 'm', 'p', 'd', 'u', 'c', 'l', 's', 'n', 't', 'o', 'i', 'r', 'a', 'e']

    while countRecs(tmp) > 20:
        for letter in least_common:
            for rec in tmp:
                if letter in rec:
                    tmp[rec] -= 1
    return tmp