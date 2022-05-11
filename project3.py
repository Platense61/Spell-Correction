from collections import OrderedDict
import time
import tkinter as tk
import os
import csv
from tkinter import filedialog as fd

#####
#   - findSuggestions(word) now works relatively efficiently.
#       - currently prints all known words within 2 common changes
#   - REMOVED ASPELL.DAT FROM THE INCORRECT WORD LIST IN ORDER TO TEST AGAINST
#       - "correct word appeared in top 5 81.77339901477832% of the time
#         correct word was first suggestion 41.87192118226601% of the time
#         Took 46 min and 14 sec" - with code segment on line 247 - 250
#       - general trouble with names
#
# IDEAS:
#   - we should either multithread the typing and wordSuggestions so the typing doesn't freeze,
#     or underline unknown words where you have to click on it to get suggestions
#####

# global dictionaries
incorrect_words = {}    # key : value -> str : list -> correct word : incorrect spelling(s)
all_incorrect_spellings = []
all_incorrect_str = ""
bi_freq = {}            # key : value -> str : int  -> bigram : frequency
word_freq = {}          # key : value -> str : int  -> word : frequency found in big.txt
word_freq_str = ""

word = ""
letters = "abcdefghijklmnopqrstuvwxyz"
begin_part = time.time()
begin_full = begin_part

# for testing
file_opened = False
correct_word = ""
total = 531 # for aspell.dat
correct = 0
count = 0
fully_correct = 0
progress = 0

def main():
    ###
    #This function had to be put inside main, because i could not access widget property with bind listener outside of main scope
    # So far it will underline any word not in word_freq{} (from big.txt)
    ###
    def detect_misspell(event):
        global word, word_freq

        # needs to update the internal 'word' if a backspace key is found
        if event.keycode == 855638143: # the keycode for backspace
            word = word[:len(word)-1]

        elif event.char == ' ' or event.keycode == 603979789: #If a space or enter key is detected word is printed and the global var word is set to empty string
            print(word)
            if word in word_freq:
                print("Found")

            else:
                # print("Not in words")
                txt_edit.tag_add('underline', "end-"+str(len(word)+2)+"chars", "end-2c")
                findSuggestions(word)
                
                #txt_edit.tag_config('highlight', foreground='red')
            word = ""
        #This else statement is where the suggestion code will go. So far it contains the current word being typed (global called word)
        else:
            word = word + event.char
            guessWord(word)

###############################################################
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
    txt_edit.tag_config('underline', underline = True)
    fr_buttons = tk.Frame(window)
    btn_open = tk.Button(fr_buttons, text="Open", command = openFile)
    btn_save = tk.Button(fr_buttons, text="Get Text", command= lambda: retrieve_input(txt_edit))
    listbox = tk.Listbox(fr_buttons, height=4)

    btn_open.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
    btn_save.grid(row=1, column=0, sticky="ew", padx=5)
    listbox.grid(row = 2, column = 0, sticky = "ew")
    fr_buttons.grid(row=0, column=0, sticky="ns")
    txt_edit.grid(row=0, column=1, sticky="nsew")

    window.bind("<Key>", detect_misspell)
    window.mainloop()


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


def openFile():
    global file_opened, correct_word
    filename = fd.askopenfilename(
        title='Open a file',
        initialdir=os.getcwd(),
        filetypes=(('All files', '*.*'),('text files', '*.txt'),('data files', '*.dat'))
    )
    print(filename) # prints the FULL path to a txt file

    # iterate through a dummy file printing words
    # connect this to the getSuggestions(word) function and eventually combine it with a probability function

    #filename = 'data/raw/incorrect_words/aspell.dat'
    file_opened = True
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

    print("FINISHED")
    print(correct, "out of", total)
    print("correct word appeared in top 5 " + str((correct/count)*100) + "% of the time")
    print("correct word was first suggestion " + str((fully_correct/count)*100) + "% of the time")

    end = time.time()
    print("Took " +  str(int((end - begin_full)/60)) + " min and " + str(int((end-begin_full)%60)) + " sec.")
    print(correct, fully_correct, total, count, progress, file_opened)


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
        guessWord(word)


def guessWord(word):
    guesses = []

    print(word)
    if word in word_freq_str:
        # for key, value in incorrect_words.items():
        #     if any(word in sub_str for sub_str in value):
        #         guesses.append(key)
        guesses = [guess for guess in word_freq.keys() if word in guess]

    guesses.sort(key=getWordFreq, reverse=True)
    guesses_pruned = guesses[:5]
    guesses_pruned.sort(key=len)
    print("top guesses:", guesses_pruned)


def findSuggestions(word):
    global begin_part
    begin_part = time.time()

    word_splits = generateSplits(word)
    one_char_errors = genCommonErrors(word_splits)
    two_char_errors = one_char_errors

    for new_word in one_char_errors:
        if new_word != None: # last new_word is None, not sure
            splits = generateSplits(new_word)
            errors = genCommonErrors(splits)

            two_char_errors = list(OrderedDict.fromkeys(two_char_errors + errors))

    two_char_errors = [k for k in two_char_errors if isKnown(k) and k != word]

    # print("potential replacements for " + word)
    # print(two_char_errors, len(two_char_errors))
    print("word look-up took " + str(time.time() - begin_part) + " seconds")

    # sorts by frequency 
    two_char_errors.sort(key=getWordFreq, reverse=True)

    # move element to the front if it's a common misspelling
    if word in all_incorrect_spellings:
        for key, value in incorrect_words.items():
            if word in value:
                two_char_errors.insert(0, key)

    if len(two_char_errors) >= 5:
        print("Suggestions for " + word + ":\n", two_char_errors[:5])
    else:
        print("Suggestions for " + word + ":\n", two_char_errors)

    updatePercent(word, two_char_errors)
    # print(progress, total)
    print(str(int((progress/total)*100)) + "% done.")


def updatePercent(word, wordList):
    global total, correct, progress, fully_correct, count
    if file_opened and len(wordList) > 0:
        if correct_word in wordList:
            correct += 1
        if correct_word == wordList[0]:
            fully_correct += 1

        progress += 1
        count += 1


def getWordFreq(word):
    if isKnown(word): return word_freq[word]
    return 0


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
        path_to_clean = 'data\\clean\\'

    importAll(path_to_clean)
    print("imported .csv's...")


def importAll(path):
    global incorrect_words, bi_freq, word_freq, all_incorrect_spellings, all_incorrect_str, word_freq_str
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
                all_incorrect_spellings.append(value)

            incorrect_words[key] = values

    all_incorrect_str = '\t'.join(all_incorrect_spellings)

    with open(path + 'bigram_freq.csv', 'r') as fp:
        for line in csv.reader(fp):
            bi_freq[line[0]] = int(line[1])

    with open(path + 'word_freq.csv', 'r') as fp:
        for line in csv.reader(fp):
            # print(line[0], line[1])
            word_freq[line[0]] = int(line[1])
            
    word_freq_str = '\t'.join(word_freq.keys())


if __name__ == "__main__":
    importData()
    main()
