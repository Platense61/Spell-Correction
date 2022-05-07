# REMY: you'll probably need to change the file locations so it works for windows.
# the exported files should be saved anyways, so it might not be worth running.
# I should have the rest of this finished by this evening.

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
    print("parsing count_2L...")

    bigrams = {}
    bigram = ""
    count = 0

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
    print("parsing aspell.dat...")
    aspellFormat("raw/incorrect_words/aspell.dat")

    # TODO: holbrook-tagged.dat
    print("parsing holbrook-tagged.dat...")
    # holbrook-tagged format : incorrect word encapsulated within 
    # <ERR targ='correct word'> 'incorrect word' </ERR>
    with open("raw/incorrect_words/holbrook-tagged.dat", 'r') as fp:
        while True:
            c = fp.read(1)
            if not c:
                print("end of file. Converting to CSV...")
                break

    print("parsing holbrook-missp.dat...")
    # holbrook-missp format : same as aspell
    # worth noting : first one is a little strange? open in word editor to see first 10 lines
    aspellFormat("raw/incorrect_words/holbrook-missp.dat")

    print("parsing wikipedia.dat...")
    # wikipedia format : same as aspell
    aspellFormat("raw/incorrect_words/wikipedia.dat")

    print("parsing missp.dat...")
    # missp format : same as aspell
    aspellFormat("raw/incorrect_words/missp.dat")

# TODO: aspell format
# decide if it should return data or go straight to csv
def aspellFormat(path):
    # aspell.dat format : correct word starts with a '$'
    # common misspellings follow 1 word/line until next '$' char
    with open(path, 'r') as fp:
        while True:
            c = fp.read(1)
            if not c:
                print("end of file. Converting to CSV...")
                break


def toCSV(path, field_names, data):
    # for key, value in data.items():
    #     print(key, " : ", value)
    with open(path, 'w') as csvfile:
        for key, value in data.items():
            csvfile.write("%s, %d\n" % (key, value))

    print("successfully outputted to csv...")


def main():
    # since each file has a different structure, each needs to be imported differently
    big()
    count2L()
    # incorrect_words()


if __name__ == "__main__":
    main()
    print("exiting...")


# def fromBigTxt():
#     global big
#     big = file('big.txt').read()
#     N = len(big)
#     s = set()
#     for i in xrange(6, N):
#         c = big[i]
#         if ord(c) > 127 and c not in s:
#             print i, c, ord(c), big[max(0, i-10):min(N, i+10)]
#             s.add(c)
#     print s
#     print [ord(c) for c in s]