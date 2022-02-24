import nltk
from random import random
import sys

from funs import printfuns as printer
from funs import recfuns as r

# If you're runnng this you'll need to download the nltk corups of English words
# run nltk.download() in a python shell beforehand

word_list = [w for w in nltk.corpus.words.words('en') if len(w) == 5 and w.islower()]
words = set(word_list)

done = False
input_vals = [-1, -1, -1, -1, -1]
ans = [' ', ' ', ' ', ' ', ' ']
confirmed = {}
confirmed_not = []
recs = {}

def checkDone(word):
    for c in word:
        if c == ' ':
            return False
    return True

# Get a random word to suggest as starting word, print welcome message
starter = word_list[int(random()*len(word_list))]
printer.printWelcomeMessage(starter)

# Initialize the recommendations dictionary
r.initRecs()

mode = 0
if len(sys.argv) > 1:
    if sys.argv[1] == "-gui":
        mode = 1

if mode == 0:
    try:
        while not done:
            # Message prompt for inputting a word
            print("---------------------------------------------------")
            guess = input("Please input your guess: ")
            print("Please tell us how your word performed:")
            print("0 - not present\n1 - present, wrong location\n2 - present, right location\n")


            for i in range(5):

                # If the answer array is not filled in for this place (0-5)
                if (ans[i] == ' '):
                    input_vals[i] = int(input("%c - " % (guess[i])))

                # Else it is filled in, ie. we know the letter that goes there
                else:
                    print("%c - CONFIRMED" % ans[i])
                    continue
            
                # If the user confirms that this letter is in this location
                if input_vals[i] == 2:
                    ans[i] = guess[i]
                    if guess[i] in confirmed_not:
                        confirmed_not.pop(confirmed_not.index(guess[i]))
                    r.updateConf(2, guess[i], i)

                # If the user confirms this letter is present, but not in this location
                if input_vals[i] == 1:
                    if (guess[i] not in confirmed):
                        confirmed[guess[i]] = [i]
                    else:
                        confirmed[guess[i]].append(i)
                    r.updateConf(1, guess[i], i)
                    #print(confirmed)
                
                # If the user confirms that this letter is NOT present in the word
                if input_vals[i] == 0:
                    # If this is a double letter
                    if (guess[i] in ans):
                        # Remove recommendations that have double letters
                        r.removeDoubles(guess[i])
                    else:
                        r.updateConf(0, guess[i], i)
                    if (guess[i] not in confirmed_not):
                        confirmed_not.append(guess[i])
                    

            # If all of the characters have been confirmed
            if checkDone(ans):
                print("Congrats! You're all done")
                break

            printer.line()
            print("Alright, here's where we're at:")
            printer.printWord(ans)
            print("Here's the other letters we know are in the word\nsomewhere:")
            for c in confirmed:
                if c not in ans:
                    print(c, end = " ")
            print()
            printer.line()
            r.getRecommendations()
            r.printRecs()
    except KeyboardInterrupt:
        print("\n\nThanks for playing! Now shutting down...\n")
    finally:
        exit(0)

elif mode == 1:
    #tkinter time
    pass