import nltk
from random import random

import funs

# If you're runnng this you'll need to download the nltk corups of English words
# run nltk.download() in a python shell beforehand

word_list = [w for w in nltk.corpus.words.words('en') if len(w) == 5 and w.islower()]
words = set(word_list)

done = False
goal = [-1, -1, -1, -1, -1]
ans = [' ', ' ', ' ', ' ', ' ']
confirmed = {}
confirmed_not = []
recs = {}

def checkDone(word):
    for c in word:
        if c == ' ':
            return False
    return True

starter = word_list[int(random()*len(word_list))]

print("\n========= GET LIVE WORDLE RECOMMENDATIONS =========\n")
print("  We will give you live wordle recommendations")
print("  all you have to do is come up with a starting")
print("  word!")
print()
print("  Need a good starting word? Try: %s" % (starter))

funs.initRecs()
try:
    while not done:
        print("---------------------------------------------------")
        guess = input("Please input your guess: ")
        print("Please tell us how your word performed:")
        print("0 - not present\n1 - present, wrong location\n2 - present, right location\n")
        for i in range(5):
            if (ans[i] == ' '):
                goal[i] = int(input("%c - " % (guess[i])))
            else:
                print("%c - CONFIRMED" % ans[i])
                continue
            if goal[i] == 2:
                ans[i] = guess[i]
                if guess[i] in confirmed_not:
                    confirmed_not.pop(confirmed_not.index(guess[i]))
            if goal[i] == 1:
                if (guess[i] not in confirmed):
                    confirmed[guess[i]] = [i]
                else:
                    confirmed[guess[i]].append(i)
                print(confirmed)
            if goal[i] == 0:
                if ((guess[i] not in confirmed_not) and (guess[i] not in confirmed)):
                    confirmed_not.append(guess[i])
        if checkDone(ans):
            print("Congrats! You're all done")
            break
        print("---------------------------------------------------")
        print("Alright, here's where we're at:")
        funs.printWord(ans)
        print("Here's the other letters we know are in the word\nsomewhere:")
        for c in confirmed:
            if c not in ans:
                print(c, end = " ")
        print("\n---------------------------------------------------")
        funs.getRecommendations(confirmed)
        funs.printRecs()
except KeyboardInterrupt:
    print("\n\nThanks for playing! Now shutting down...\n")
finally:
    exit(0)