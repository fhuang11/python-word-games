import nltk, sys
import copy as cp
from nltk.corpus import words

# words and letters
nltk.download('words')
# letter frequency from Concise Oxford Dictionary (9th edition, 1995)
# https://www3.nd.edu/~busiforc/handouts/cryptography/letterfrequencies.html
letter_frequency = {'e': 11.1607, 'a': 8.4966, 'r': 7.5809, 'i': 7.5448, 'o': 7.1635, 't': 6.9509, 'n': 6.6544,
                    's': 5.7351,
                    'l': 5.4893, 'c': 4.5388, 'u': 3.6308, 'd': 3.3844, 'p': 3.1671, 'm': 3.0129, 'h': 3.0034,
                    'g': 2.4705,
                    'b': 2.0720, 'f': 1.8121, 'y': 1.7779, 'w': .12899, 'k': 1.1016, 'v': 1.0074, 'x': 0.2902,
                    'z': 0.2722,
                    'j': 0.1965, 'q': 0.1962}

# for progress tracker
possible_words = 0
tested_words_count = 0
progress_interval = 5
current_progress = 0

# game parameters
default_max_repeated_letters = 2
default_max_word_length = 9
default_min_word_length = 4
found_words = []


def is_word(word_to_test, min_length=default_min_word_length):
    if len(word_to_test) >= min_length and word_to_test in words.words():
        return True
    else:
        return False


# print(is_word("test"))
# print(is_word("exys"))


# def stop_looking_for_words(word, max_word_length=default_max_word_length):
#     if len(word) >= max_word_length:
#         return True;
#     else:
#         return False;

def check_word(word_array, debug):
    global tested_words_count, current_progress, found_words
    # check word
    #if debug: print("word array: ", word_array)
    word = ''.join(word_array)
    #if debug: print("word: ", word)
    if is_word(word):
        # print(word)
        # if word not in found_words:
        found_words.append(word)
    elif debug:
        print("not word:", word)

    # monitor progress
    if not debug:
        tested_words_count += 1
        if (tested_words_count / possible_words) * 100 > (current_progress + progress_interval):
            current_progress += progress_interval
            sys.stdout.write('\r')
            sys.stdout.write("current progress is " + str(current_progress) + "%")
            sys.stdout.flush()

# find all words with mandatory letter
def find_words_arrays(word_arrays, optional_letters, debug):
    for i in range(len(word_arrays[0])):
        new_word_arrays = []
        for word_array in word_arrays:
            if word_array[i] == ' ':
                for letter in optional_letters:
                    new_word_array = cp.deepcopy(word_array)
                    new_word_array[i] = letter
                    #if debug: print(new_word_array)
                    new_word_arrays.append(new_word_array)
                word_arrays = new_word_arrays
    return new_word_arrays


# find all possible words with mandatory letter and optional letters. Each letter can be used multiple times.
def start_find_words(mandatory_letter, optional_letters,
                     min_word_length=default_min_word_length, max_word_length=default_max_word_length,
                     debug=False):
    # sort letters by decreasing frequency
    #unsorted_letters = optional_letters + mandatory_letter
    #letters = ''.join(sorted(unsorted_letters, key=lambda x: letter_frequency[x], reverse=True))
    # print(letters)
    letters = optional_letters + mandatory_letter

    # track progress
    # sys.stdout.write("current progress is 0%")
    # sys.stdout.flush()
    global tested_words_count, current_progress, possible_words
    possible_words = max_word_length * (len(letters) ** (max_word_length - 1)) #TODO check formula
    tested_words_count = 0
    current_progress = 0

    # for each possible position of mandatory letter
    for length in range(min_word_length, max_word_length+1):
        blank_word = [' ']*length
        for mandatory_word_position in range(length):
            word_array = cp.deepcopy(blank_word)
            word_array[mandatory_word_position] = mandatory_letter
            word_arrays = find_words_arrays([word_array], optional_letters, debug)
            for word_array in word_arrays:
                check_word(word_array, debug)

    # print results
    if not debug:
        sys.stdout.write('\r')
        sys.stdout.write("current progress is 100%")
        sys.stdout.flush()
    print("")
    print("There are " + str(len(
        found_words)) + " words with mandatory letter " + mandatory_letter + " and optional letters " + optional_letters + " are: ")
    for real_word in found_words:
        print(real_word)


# test
# start_find_words(mandatory_letter="r", optional_letters="tnacifo")
#start_find_words(mandatory_letter="r", optional_letters="tnco", max_word_length=5, debug=True)
start_find_words(mandatory_letter="r", optional_letters="tnco", max_word_length=5)