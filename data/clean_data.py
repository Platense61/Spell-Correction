# REMY: you'll probably need to change the file locations so it works for windows.
# the exported files should be saved anyways, so it might not be worth running.

# - PYTHON DICTIONARIES ARE IMPLEMENTED AS HASHTABLES (means O(1) lookup speeds (GOOD))
import csv


# parses big.txt
# dictionary where key:value is word:number of times seen
def big():
    # needs to only allow alphabetical characters, break on others.
    words = {}
    buffer = ""

    print("parsing big.txt...")
    with open("raw/big.txt", 'r') as fp:
        while True:
            c = fp.read(1)
            if not c:
                print("end of file. Converting to CSV...")
                break

            if c.isalpha():
                buffer += c
            else:
                if len(buffer) > 0: # if there is a word behind c
                    buffer = buffer.lower()
                    if buffer in words:
                        words[buffer] += 1
                    else:
                        words[buffer] = 1

                    buffer = ""

    # sorts dictionary by key
    words = dict(sorted(words.items(), reverse=True, key=lambda item: item[1]))
    toCSV('clean/word_freq.csv', ["word", "freq"], words)


# parses count_2l.txt
def count2L():
    bigrams = {}
    bigram = ""
    count = 0

    print("parsing count_2L...")
    with open("raw/bigram_freq/count_2l.txt", 'r') as fp:
        while True:
            line = fp.readline()
            if not line:
                print("end of file. Converting to CSV...")
                break

            bigram, count = line.split("\t")
            bigrams[bigram] = int(count)


    # sorts dictionary by key
    bigrams = dict(sorted(bigrams.items(), reverse=True, key=lambda item: item[1]))
    toCSV('clean/bigram_freq.csv', ["bigram", "freq"], bigrams)


# all incorrect_words (.dat) files
def incorrect_words():
    # TODO: holbrook-tagged.dat
    print("parsing holbrook-tagged.dat...")
    # holbrook-tagged format : incorrect word encapsulated within 
    # <ERR targ='correct word'> 'incorrect word' </ERR>
    holbrook_tagged_data = {}
    with open("raw/incorrect_words/holbrook-tagged.dat", 'r') as fp:
        while True:
            c = fp.read(1)
            if not c:
                print("end of file. Converting to CSV...")
                break

            if c == '<':
                # get the word
                word_found = False
                word = ""
                missp = ""
                while not word_found:
                    c = fp.read(1) # starts on E of '<EER targ='
                    word += c
                    if c == '>':
                        word_found = True
                
                # get the misspelling
                word_found = False
                while not word_found:
                    c = fp.read(1)
                    missp += c
                    if c == '<':
                        word_found = True

                word = word[9:len(word)-1].lower()
                missp = missp[1:len(missp)-2].lower()

                if word not in holbrook_tagged_data: # if the word hasn't been found yet
                    holbrook_tagged_data[word] = [missp]
                elif missp not in holbrook_tagged_data[word]: # if the misspelled version hasnt been recorded yet
                    holbrook_tagged_data[word].append(missp)

    print("parsing holbrook-missp.dat...")
    # holbrook-missp format : same as aspell
    # worth noting : first one is a little strange? open in word editor to see first 10 lines
    holbrook_missp_data = aspellFormat("raw/incorrect_words/holbrook-missp.dat")

    print("parsing aspell.dat...")
    aspell_data = aspellFormat("raw/incorrect_words/aspell.dat")

    print("parsing wikipedia.dat...")
    # wikipedia format : same as aspell
    wikipedia_data = aspellFormat("raw/incorrect_words/wikipedia.dat")

    print("parsing missp.dat...")
    # missp format : same as aspell
    missp_data = aspellFormat("raw/incorrect_words/missp.dat")

    # combine them into one dictionary
    master = combineDict(aspell_data, holbrook_missp_data)
    master = combineDict(master, wikipedia_data)
    master = combineDict(master, missp_data)
    master = combineDict(master, holbrook_tagged_data)

    toCSV('clean/incorrect_words.csv', ['word', 'wrong'], master)


def combineDict(dict1, dict2):
    for key, value in dict2.items():
        if key in dict1:
            dict1[key] += value
            # dict1[key] = list(dict.fromkeys(dict1[key])) # removes duplicates. Doesnt work properly.
        else:
            dict1[key] = value

    return dict1


# aspell format
# returns dict
def aspellFormat(path):
    # aspell.dat format : correct word starts with a '$'
    # common misspellings follow 1 word/line until next '$' char
    data = {}
    key = ""

    with open(path, 'r') as fp:
        while True:
            line = fp.readline()
            if not line:
                print("end of file. Converting to CSV...")
                break

            if line[0] == '$':
                key = line[1:len(line)].lower()
                if key not in data:
                    data[key] = []
            else:
                data[key].append(line[:len(line)-1].lower())
                    
    return data


def toCSV(path, field_names, data):
    # for key, value in data.items():
    #     print(key, " : ", value)
    with open(path, 'w') as csvfile:
        for key, value in data.items():
            if type(value) == int:
                csvfile.write("%s, %d\n" % (key, value))
            else:
                csvfile.write("%s, %s\n" % (key, value))

    print("successfully outputted to ", path)


def main():
    # since each file has a different structure, each needs to be imported differently
    big()
    count2L()
    incorrect_words()


if __name__ == "__main__":
    main()
    print("exiting...")
