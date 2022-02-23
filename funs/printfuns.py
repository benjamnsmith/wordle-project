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
                print("Here are my recommendations:")
                message = True
            print(r, end = " ")
            iter += 1
            if iter % 9 == 0:
                print()
                iter = 0
    print()