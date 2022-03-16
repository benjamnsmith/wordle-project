import nltk
from random import random
import sys
from tkinter import *
from tkinter import ttk

from funs import recfuns as r

# If you're runnng this you'll need to download the nltk corups of English words
# run nltk.download() in a python shell beforehand

word_list = [w for w in nltk.corpus.words.words('en') if len(w) == 5 and w.islower()]
words = set(word_list)

done = False
ans = [' ', ' ', ' ', ' ', ' ']
confirmed = {}
confirmed_not = []

def checkDone(word):
    for c in word:
        if c == ' ':
            return False
    return True


# Initialize the recommendations dictionary
r.initRecs()


guesses = 0
display_font = ('Andale Mono', 14)
root = Tk()
root.title("Wordle Recommendations")
root.geometry('700x500')

disp = Label(root, text="Welcome!\nPlease enter a word in the above\nbox to begin", font=display_font)
disp.grid(column=1,row=0)

buttons = []


def displayMessage(str):
    global disp

    disp.config(text=str)
    return
        
def setUp(container):
    play_area = ttk.Frame(container, padding=10)

    for i in range(6):
        for j in range(5):
            btn = Button(play_area, width=2, height=2, highlightbackground='black', state='disabled')
    
            btn['command'] = lambda arg=btn : updateButton(arg)
            btn.grid(column=j, row=i)
            buttons.append(btn)

    return play_area

def updateButton(btn):
    global buttons
    global guesses

    if buttons.index(btn) < guesses * 5:
        return
        
    colors = ['orange', 'green', 'black']
    try:
        next = colors[(colors.index(btn['highlightbackground']) + 1) % 3]
    except ValueError:
        next = 'orange'
    btn['highlightbackground'] = next


def moveOn():   
    global play_area
    global buttons
    global guesses
    global conf
    global g
    conf.config(state='disabled')

    num = 0
    for but in buttons:
        if buttons.index(but) < guesses * 5:
            continue
        if but['state'] == 'normal':

            letter = but['text'].lower()

            if but['highlightbackground'] == 'green':
                ans[num] = letter
                if letter in confirmed_not:
                    confirmed_not.pop(confirmed_not.index(letter))
                r.updateConf(2,letter, num)
                num += 1
            elif but['highlightbackground'] == 'orange':
                if letter not in confirmed:
                    confirmed[letter] = [num]
                else:
                    confirmed[letter].append(num)
                r.updateConf(1,letter, num)
                num += 1
            else:
                if letter in ans:
                    r.removeDoubles(letter)
                else:
                    r.updateConf(0,letter, num)
                    num += 1
                if letter not in confirmed_not:
                    confirmed_not.append(letter)
    if checkDone(ans):
        
        guesses += 1
        s = "Guess: " + str(guesses)

        g['text'] = s
        displayMessage("Congrats! You're all done\nTotal guesses: %d" % guesses)
        return
    r.getRecommendations()

    msg = r.recs4TK()
    global rec
    rec['text'] = msg

    guesses += 1
    s = "Guess: " + str(guesses)

    g['text'] = s

    if guesses == 6:
        displayMessage("Darn :(\nBetter luck next time")
        return
    else:
        displayMessage("Please enter a new word")
    return


def updatePlayArea(word):
    global play_area
    global guesses

    skips = guesses * 5
    letters = [letter for letter in word]
    iter = 0
    for but in buttons:
        if skips > 0:
            skips -= 1
            continue
        if but['state'] == 'disabled':
            but['text'] = letters[iter].upper()
            but['state'] = 'normal'
            iter += 1
            if iter == 5:
                break
    displayMessage("Please click each letter to\nlet me know how it performed")
    

    return

 
    
def getWord(event):
    global word

    guess = word.get()
    if len(guess) != 5:
        displayMessage("Please enter a five letter word")
        return -1
    word.delete(0,5)
    msg = "You entered: " + guess
    global conf
    conf.config(state='normal')
    displayMessage(msg)
    updatePlayArea(guess)

    return 0

def reset():
    r.initRecs()

    global buttons
    for btn in buttons:
        btn['state'] = 'disabled'
        btn['text'] = ''
        btn['highlightbackground'] = 'black'
    global confirmed
    confirmed = {}

    global confirmed_not
    confirmed_not = []

    global ans
    ans = [' ', ' ', ' ', ' ', ' ']

    global guesses
    guesses = 0

    global disp
    disp['text'] = 'Welcome!\nPlease enter a word in the above\nbox to begin'

    global rec
    starter = word_list[int(random()*len(word_list))]
    msg = "\nNeed a good starting word? Try: " + starter
    rec['text'] = msg
    
    

# GUESS DISPLAY
play_area = setUp(root)
play_area.grid(column=0, row=0)

# INPUT AREA
word = Entry(root, bd=5)
word.bind('<Return>', getWord)
word.grid(column=1, row=0, sticky=N, pady=15)    

# QUIT & CONFIRM BUTTONS, GUESS DISPLAY  
Button(root, text="Quit", command=root.destroy, font=display_font).grid(column=2, row=0, sticky=S)
conf = Button(root, text="Confirm", command=moveOn, state='disabled', font=display_font)
conf.grid(column=1, row=0, sticky=S)
g = ttk.Label(root, text="Guess: 0", padding=20, font=display_font)
g.grid(column=2, row=0, sticky=N)
again = Button(root, text="Play again", command=reset)
again.grid(column=3,row=0, sticky=S)


# RECOMMENDATION AREA THINGS
rec_area = Frame(root, padx=10, pady=10, highlightbackground="blue")
rec_area.columnconfigure(0,weight=3)
rec_area.grid(column=0, row=1)
l = Label(rec_area, text="Recommendations", font=display_font)
l.grid(column=0,row=0)


starter = word_list[int(random()*len(word_list))]
msg = "\nNeed a good starting word? Try: " + starter

rec = Label(rec_area, text=msg, justify='left', font=('Andale Mono', 14, 'bold'))
rec.grid(column=0,row=1)


root.mainloop()

'''
BROKEN
SHIVA (20000)
SKULL (20000)
STORM (20000)
SPEED (22202)
SPEND (22222)
'''