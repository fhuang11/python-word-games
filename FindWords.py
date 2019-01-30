import nltk, math
from nltk.corpus import words

# words and letters
nltk.download('words')
# letter frequency from Concise Oxford Dictionary (9th edition, 1995)
# https://www3.nd.edu/~busiforc/handouts/cryptography/letterfrequencies.html
letter_frequency = {'e':11.1607, 'a':8.4966,'r':7.5809, 'i':7.5448, 'o':7.1635, 't':6.9509,'n':6.6544, 's':5.7351,
                    'l':5.4893, 'c':4.5388, 'u':3.6308, 'd':3.3844, 'p':3.1671, 'm':3.0129, 'h':3.0034, 'g':2.4705,
                    'b':2.0720, 'f':1.8121, 'y':1.7779, 'w':.12899, 'k':1.1016, 'v':1.0074, 'x':0.2902, 'z':0.2722,
                    'j':0.1965, 'q':0.1962}

# for progress tracker
possible_words = 0
progress_interval = 5

# game parameters
default_max_word_length=9
default_min_length=4
found_words = []

def is_word(word_to_test, min_length=default_min_length):
    if len(word_to_test)>=min_length and word_to_test in words.words():
        return True
    else:
        return False
#print(is_word("test"))
#print(is_word("exys"))


def stop_looking_for_words(word, max_word_length=default_max_word_length):
    if len(word)>=max_word_length:
        return True;
    else:
        return False;

# recursive method used by start_find_words
def find_words(word, letters,
               max_word_length):
    # monitor progress
    global tested_words_count, current_progress, found_words
    tested_words_count += 1
    if (tested_words_count/possible_words)*100 > (current_progress + progress_interval):
        current_progress += progress_interval
        print("current progress is " + str(current_progress) + "%")

    # check word
    if is_word(word):
        print(word)
        if word not in found_words:
            found_words.append(word)
#    else:
#        print("    not word: " + word)

    if not stop_looking_for_words(word, max_word_length):
        for letter in letters:
            # add letter to end of word
            new_word = word + letter
            find_words(new_word, letters, max_word_length)
            # add letter to front of word
            new_word = letter + word
            find_words(new_word, letters, max_word_length)

# find all possible words with mandatory letter and optional letters. Each letter can be used multiple times.
def start_find_words(mandatory_letter, optional_letters,
                     max_word_length=default_max_word_length):

    # sort letters by decreasing frequency
    unsorted_letters = optional_letters + mandatory_letter
    letters = ''.join(sorted(unsorted_letters, key=lambda x: letter_frequency[x], reverse=True))
    print(letters)

    #track progress
    global tested_words_count, current_progress, possible_words
    possible_words = 1
    for i in range(max_word_length-1):
        possible_words += 2*possible_words*len(letters)
    tested_words_count = 0
    current_progress = 0

    find_words(mandatory_letter, optional_letters,
               max_word_length)

    # print results
    print("current progress is 100%")
    print("")
    print("The words with mandatory letter " + mandatory_letter + " and optional letters " + optional_letters + " are: ")
    for real_word in found_words:
        print(real_word)

# test
#start_find_words(mandatory_letter="r", optional_letters="tnacifo")
start_find_words(mandatory_letter="r", optional_letters="tnco", max_word_length=5)