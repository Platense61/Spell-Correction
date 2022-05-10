from collections import OrderedDict
import time
import tkinter as tk
from tkinter import filedialog as fd
import os
import csv

#####
#   - findSuggestions(word) now works relatively efficiently.
#       - currently prints all known words within 2 common changes
#   - REMOVED WIKIPEDIA.DAT FROM THE INCORRECT WORD LIST IN ORDER TO TEST AGAINST
#
# TO DO: 
#   - need to take in a file for the spell correction to work on in order to get a % correct
#   - need a probability function that takes a potential word, and the current word and returns between 0 - 1
#
# IDEAS:
#   - we should either multithread the typing and wordSuggestions so the typing doesn't freeze,
#     or underline unknown words where you have to click on it to get suggestions
#####

# global dictionaries
incorrect_words = {}    # key : value -> str : list -> correct word : incorrect spelling(s)
bi_freq = {}            # key : value -> str : int  -> bigram : frequency
word_freq = {}          # key : value -> str : int  -> word : frequency found in big.txt

word = ""
letters = "abcdefghijklmnopqrstuvwxyz"
begin = time.time()

def main():
    window = tk.Tk()
    window.title("Text Editor")

    window_w = 900
    window_h = 600

    screen_w = window.winfo_screenwidth()
    screen_h = window.winfo_screenheight()
    center_x = int(screen_w/2 - window_w/2)
    center_y = int(screen_h/2 - window_h/2)

    # centers the window
    window.geometry(f'{window_w}x{window_h}+{center_x}+{center_y}')
    window.resizable(True, True)

    window.rowconfigure(0,minsize=900,weight=1)
    window.columnconfigure(1, minsize=900, weight=1)

    txt_edit = tk.Text(window)
    fr_buttons = tk.Frame(window)
    btn_open = tk.Button(fr_buttons, text="Open", command = openFile)
    btn_save = tk.Button(fr_buttons, text="Get Text", command= lambda: retrieve_input(txt_edit))
    listbox = tk.Listbox(fr_buttons, height=4)

    btn_open.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
    btn_save.grid(row=1, column=0, sticky="ew", padx=5)
    listbox.grid(row = 2, column = 0, sticky = "ew")
    fr_buttons.grid(row=0, column=0, sticky="ns")
    txt_edit.grid(row=0, column=1, sticky="nsew")

    window.bind("<Key>", update_suggestions)
    window.mainloop()


def openFile():
    # filename = fd.askopenfilename(
    #     title='Open a file',
    #     initialdir=os.getcwd(),
    #     filetypes=(('text files', '*.txt'),('data files', '*.dat'),('All files', '*.*'))
    # )
    # print(filename) # prints the FULL path to a txt file

    # iterate through a dummy file printing words
    # connect this to the getSuggestions(word) function and eventually combine it with a probability function

    # works as is on mac, might need to use the conditional in importData() if it doesn't work on windows
    filename = 'data/raw/incorrect_words/wikipedia.dat'
    correct_word = ""
    buffer = ""
    with open(filename) as fp:
        while True:
            char = fp.read(1)
            if not char:
                print("eof")
                break

            if char == '$':
                correct_word = ""
                while True:
                    char = fp.read(1)
                    if not char.isalpha() and char != '$':
                        break
                    correct_word += char

            elif not char.isalpha():
                if not isKnown(buffer):
                    print(buffer, "->", correct_word)
                    findSuggestions(buffer)
                buffer = ""

            else:
                buffer += char


# This function grabs all text in editor upon clicking the get text button and outputs to command line
def retrieve_input(txt_edit):
    inputValue=txt_edit.get("1.0","end-1c")
    #Following replace lines remove punctuations from the words. Useful for when we do operations on words.
    inputValue = inputValue.replace("!","")
    inputValue = inputValue.replace("?","")
    inputValue = inputValue.replace(".","")
    inputValue = inputValue.replace(",","")
    my_split = inputValue.split()
    print(my_split)
    print(inputValue)


#This is an event listener. Listens for each character typed in our entry window.
#declared right above window.mainloop() above
def update_suggestions(event):
    global word

    # needs to update the internal 'word' if a backspace key is found
    if event.keycode == 855638143: # the keycode for backspace
        word = word[:len(word)-1]

    elif event.char == ' ' or event.keycode == 603979789: #If a space or enter key is detected word is printed and the global var word is set to empty string
        print(word)
        if not isKnown(word):
            findSuggestions(word)
        word = ""
    #This else statement is where the suggestion code will go. So far it contains the current word being typed (global called word)
    else:
        word = word + event.char


def findSuggestions(word):
    global begin
    begin = time.time()

    word_splits = generateSplits(word)
    one_char_errors = genCommonErrors(word_splits)
    two_char_errors = one_char_errors

    for new_word in one_char_errors:
        if new_word != None: # last new_word is None, not sure
            splits = generateSplits(new_word)
            errors = genCommonErrors(splits)

            two_char_errors = list(OrderedDict.fromkeys(two_char_errors + errors))

    two_char_errors = [k for k in two_char_errors if isKnown(k) and k != word]

    print("potential replacements for " + word)
    print(two_char_errors, len(two_char_errors))

    print("word look-up took " + str(time.time() - begin) + " seconds")
    # TODO: should cross reference if a potential word shows up in the incorrect words list
    #       along with the above, give different weights to different common mistakes

def genCommonErrors(word_splits):
    pos_deletes = deletionList(word_splits)
    pos_swaps = swapList(word_splits)
    pos_replacements = replaceList(word_splits)
    pos_inserts = insertionList(word_splits)

    master = pos_deletes + pos_swaps + pos_replacements + pos_inserts
    return list(OrderedDict.fromkeys(master))


# should this inlcude sets where the entire word is in one section? Currently will
def generateSplits(word):
    splits = []
    for i in range(len(word)+1):
        splits.append( (word[:i], word[i:]) )
    return list(OrderedDict.fromkeys(splits))

    
# deletion
def deletionList(set):
    list = []
    for L, R in set:
        if len(L) > 0 and len(R) > 0:
            list.append(L + R[1:])
    return list

# swapping of two adjacent letters
def swapList(set):
    list = []
    for L, R in set:
        if len(L) > 0 and len(R) > 0:
            list.append(L[:len(L)-1] + R[0] + L[len(L)-1] + R[1:])
    return list
    

# replace a letter
def replaceList(set):
    list = []
    for L, R in set:
        if len(L) > 0 and len(R) > 0:
            for char in letters:
                list.append(L + char +  R[1:])
    return list


# insert every letter into every set tuple
def insertionList(set):
    list = []
    for L, R in set:
        for char in letters:
            list.append(L + char + R)
    return list


# returns t or f if the word is in our makeshift dictionary of all words
def isKnown(word):
    return word in word_freq.keys()


def importData():
    if os.name == 'posix': # mac
        path_to_clean = 'data/clean/'

    if os.name == 'nt': # windows
        pass

    importAll(path_to_clean)
    print("imported .csv's...")


def importAll(path):
    global incorrect_words, bi_freq, word_freq
    key = ""
    value = ""
    values = []

    with open(path + 'incorrect_words.csv', 'r') as fp:
        for line in csv.reader(fp):
            key = line[0]
            values = []
            # print(key)
            for i in range(1, len(line)):
                value = line[i]
                # print('\t',line[i])
                if value[0] == '[':
                    value = value[1:]
                if value[len(value)-1] == ']':
                    value = value[:len(value)-1]
                value = value[1:len(value)-1]
                values.append(value)

            incorrect_words[key] = values

        with open(path + 'bigram_freq.csv', 'r') as fp:
            for line in csv.reader(fp):
                bi_freq[line[0]] = int(line[1])

        with open(path + 'word_freq.csv', 'r') as fp:
            for line in csv.reader(fp):
                # print(line[0], line[1])
                word_freq[line[0]] = int(line[1])


if __name__ == "__main__":
    importData()
    main()
