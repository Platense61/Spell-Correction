import tkinter as tk
import os
import csv

#####
# - Need to put the path to your 'clean' folder on line 64
#   in importData()
#####

# global dictionaries
incorrect_words = {}    # key : value -> str : list -> correct word : incorrect spelling(s)
bi_freq = {}            # key : value -> str : int  -> bigram : frequency
word_freq = {}          # key : value -> str : int  -> word : frequency found in big.txt

word = ""

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
    btn_open = tk.Button(fr_buttons, text="Open")
    btn_save = tk.Button(fr_buttons, text="Get Text", command= lambda: retrieve_input(txt_edit))
    listbox = tk.Listbox(fr_buttons, height=4)

    btn_open.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
    btn_save.grid(row=1, column=0, sticky="ew", padx=5)
    listbox.grid(row = 2, column = 0, sticky = "ew")
    fr_buttons.grid(row=0, column=0, sticky="ns")
    txt_edit.grid(row=0, column=1, sticky="nsew")

    window.bind("<Key>", update_suggestions)
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
    
#This is an event listener. Listens for each character typed in our entry window.
#declared right above window.mainloop() above
def update_suggestions(event):
    global word
    if event.char == ' ': #If a space is detected word is printed and the global var word is set to empty string
        print(word)
        word = ""
    #This else statement is where the suggestion code will go. So far it contains the current word being typed (global called word)
    else:
        word = word + event.char


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
                word_freq[line[0]] = int(line[1])




if __name__ == "__main__":
    importData()
    main()
