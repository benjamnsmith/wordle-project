import nltk
from random import random
import sys
from tkinter import *
from tkinter import ttk


# If you're runnng this you'll need to download the nltk corups of English words
# run nltk.download() in a python shell beforehand

word_list = [w for w in nltk.corpus.words.words('en') if len(w) == 5 and w.islower()]
words = set(word_list)

word = word_list[int(random()*len(word_list))]

ans = [' ', ' ', ' ', ' ', ' ']

def checkDone(word):
    for c in word:
        if c == ' ':
            return False
    return True


guesses = 0
display_font = ('Andale Mono', 14)
root = Tk()
root.title("Let's Play Wordle!")
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
            btn = Button(play_area, width=2, height=2, bg='gray', state='disabled')
            btn.grid(column=j, row=i)
            buttons.append(btn)

    return play_area



def updatePlayArea(_word):
    global play_area
    global guesses
    global word
    global word_

    skips = guesses * 5
    letters = [letter for letter in _word]
    iter = 0
    for but in buttons:
        if skips > 0:
            skips -= 1
            continue
        if but['state'] == 'disabled':
            cur_letter = letters[iter]
            but['text'] = letters[iter].upper()
            but['state'] = 'normal'
            if cur_letter == word[iter]:
                but['highlightbackground'] = 'green'
            elif cur_letter in word:
                but['highlightbackground'] = 'orange'
            iter += 1
        if _word == word:
            displayMessage("Congrats!")
            word_['state'] = 'disabled'
        if iter == 5:
            break
    

    return

 
    
def getWord(event):
    global word_

    guess = word_.get()
    if len(guess) != 5:
        displayMessage("Please enter a five letter word")
        return -1
    word_.delete(0,5)
    msg = "You entered: " + guess
    displayMessage(msg)
    updatePlayArea(guess)

    return 0

    

# GUESS DISPLAY
play_area = setUp(root)
play_area.grid(column=0, row=0)

# INPUT AREA
word_ = Entry(root, bd=5)
word_.bind('<Return>', getWord)
word_.grid(column=1, row=0, sticky=N, pady=15)    

# QUIT & CONFIRM BUTTONS, GUESS DISPLAY  
Button(root, text="Quit", command=root.destroy, font=display_font).grid(column=2, row=0, sticky=S)
g = ttk.Label(root, text="Guess: 0", padding=20, font=display_font)
g.grid(column=2, row=0, sticky=N)
word_display = Label(root, text=word, pady=40)
word_display.grid(column=2,row=0)


root.mainloop()