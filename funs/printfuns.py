from funs.recfuns import countRecs, filterRecs, recs

def printWord(lst):
    for i in range(len(lst)):
        if(lst[i]) != ' ':
            print(lst[i], end=" ")
        else:
            print("_", end=" ")
    print("\n")

def printKnown(lst):
    if not lst:
        print("No confirmed letters right now :(")
        return
    print("We know that the word also has:")
    for el in lst:
        print("%s" % (el), end = " ")



def printWelcomeMessage(word):
    print("\n======== GET LIVE WORDLE RECOMMENDATIONS ========\n")
    print("  We will give you live wordle recommendations")
    print("  all you have to do is come up with a starting")
    print("  word!")
    print()
    print("  Need a good starting word? Try: %s" % (word))

def line():
    print("--------------------------------------------")