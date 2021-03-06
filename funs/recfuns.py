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
    global ans
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

def getRecommendations():
    global confirmed_not
    global confirmed
    global ans


    pass_zero(confirmed_not)

    pass_one(confirmed)
    pass_two()
    pass_three(confirmed)

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

    global confirmed
    global confirmed_not
    global goal
    global ans

    confirmed = {}
    confirmed_not = []
    goal = [-1, -1, -1, -1, -1]
    ans = [' ', ' ', ' ', ' ', ' ']

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

def updateConf(case, letter, val):
    if case == 0:
        try:
            goal[val] = 0
            if ((letter not in confirmed_not) and (letter not in confirmed)):
                confirmed_not.append(letter)
        except Exception as e:
            print(e)
            print(goal)
            print(val)
    if case == 1:
        goal[val] = 1
        if (letter not in confirmed):
            confirmed[letter] = [val]
        else:
            confirmed[letter].append(val)
    if case == 2:
        ans[val] = letter
        goal[val] = 2
        if letter in confirmed_not:
            confirmed_not.pop(confirmed_not.index(letter))

def removeDoubles(double_letter):
    global recs
    for word in recs:
        # This might be wrong for edge case word has three of the same letter
        if len(word.split(double_letter)) > 2:
            recs[word] = -1 

def printRecs():
    global recs

    here = recs.copy()
    if countRecs(here) > 20:
        here = filterRecs()
    message = False
    iter = 0
    for r in here:
        if recs[r] > 0:
            if not message:
                print("I have %d recommendations for you:\n" % countRecs(recs))
                message = True
            print(r, end = " ")
            iter += 1
            if iter % 8 == 0:
                print()
                iter = 0
    print()

def printAlpha():
    global recs
    here = recs.copy()

    try:

        sorted = list(here.items()).sort()
        for elem in sorted:
            if recs[elem] > 0:
                if not message:
                    print("Here are my recommendations:")
                    message = True
                print(elem, end = " ")
                iter += 1
                if iter % 9 == 0:
                    print()
                    iter = 0
    except Exception as e:
        print(e)

def recs4TK():
    global recs

    here = recs.copy()

    ret = ""
    lst = []
    iter = 0
    for r in here:
        if here[r] > 0:
            lst.append(r)
    lst.sort()
    for word in lst:
        ret += word + "  "
        iter += 1
        if iter % 5 == 0:
            ret += "\n"
    return ret

    


''' 
Something else is broken:
bough (01100)
scour(00221)
trout(02220)
proud(22222)

Maybe not, proud just isn't in the word list??
'''