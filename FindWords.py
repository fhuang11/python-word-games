import nltk
import sys
import copy as cp
from nltk.corpus import wordnet
import timeit

# install nltk (first time only)
#nltk.download('words')

# words and letters
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
progress_interval = 1
current_progress = 0

# game parameters
default_max_repeated_letters = 2
default_max_word_length = 9
default_min_word_length = 4
found_words = []


def is_word(word_to_test, min_length=default_min_word_length):
    #if len(word_to_test) >= min_length and word_to_test in words.words():
    if len(word_to_test) >= min_length and word_to_test in wordnet.words():
        return True
    else:
        return False
# print(is_word("test"))
# print(is_word("exys"))


def check_word(word_array, min_word_length, debug, progress_bar):
    global tested_words_count, current_progress, found_words
    # check word
    word = ''.join(word_array)
    if is_word(word, min_word_length):
        found_words.append(word)
        if debug:
            print("word:", word)

    # monitor progress
    if not debug and progress_bar:
        tested_words_count += 1
        if (tested_words_count / possible_words) * 100 > (current_progress + progress_interval):
            current_progress += progress_interval
            sys.stdout.write("\rcurrent progress is " + str(current_progress) + "%")
            sys.stdout.flush()

def find_more_words_arrays(word_arrays, word_arrays_with_only_optional_letters,
                           mandatory_letter, optional_letters, letters, min_word_length, debug, progress_bar):
    new_word_arrays = []

    # add letter to end of existing word
    for word_array in word_arrays:
        for letter in letters:
            new_word_array = word_array + [letter]
            new_word_arrays.append(new_word_array)
            check_word(new_word_array, min_word_length, debug, progress_bar)

    # word with only optional letters except for mandatory letter at end
    new_word_arrays_with_only_optional_letters = []
    for word_array in word_arrays_with_only_optional_letters:
        for letter in optional_letters:
            new_word_array_without_mandatory_letter = word_array + [letter]
            new_word_arrays_with_only_optional_letters.append(new_word_array_without_mandatory_letter)
            new_word_array = new_word_array_without_mandatory_letter + [mandatory_letter]
            new_word_arrays.append(new_word_array)
            check_word(new_word_array, min_word_length, debug, progress_bar)

    return new_word_arrays, new_word_arrays_with_only_optional_letters

# find all possible words with mandatory letter and optional letters. Each letter can be used multiple times.
# note progress bar does not work in debug mode and is disabled
def start_find_words(mandatory_letter, optional_letters,
                     min_word_length=default_min_word_length, max_word_length=default_max_word_length,
                     debug=False, progress_bar=True):

    # sort letters by decreasing frequency
    #unsorted_letters = optional_letters + mandatory_letter
    #letters = ''.join(sorted(unsorted_letters, key=lambda x: letter_frequency[x], reverse=True))
    # print(letters)

    letters = optional_letters + mandatory_letter

    # track progress
    if progress_bar and not debug:
        global tested_words_count, current_progress, possible_words
        word_lengths = list(range(min_word_length, max_word_length+1))
        possible_words = 0
        for l in word_lengths:
            possible_words += l*(len(letters) ** (l-1))
        print("possible words:", possible_words)
        sys.stdout.write("current progress is 0%")
        sys.stdout.flush()
        tested_words_count = 0
        current_progress = 0

    # find words of all lengths starting with word of length 1 [t]
    # by recursively finding word_arrays of increasing length
    word_arrays = [[mandatory_letter]]
    word_arrays_with_only_optional_letters = [[]]
    for length in range(1, max_word_length):
        word_arrays, word_arrays_with_only_optional_letters = find_more_words_arrays(word_arrays,
            word_arrays_with_only_optional_letters, mandatory_letter, optional_letters, letters,
            min_word_length, debug, progress_bar)

    if progress_bar and not debug:
        sys.stdout.write("\rcurrent progress is 100%")
        sys.stdout.flush()
        print("")
    return found_words

def print_results(found_words, mandatory_letter, optional_letters):
    # print results
    print("There are " + str(len(found_words)) + " words with mandatory letter " + mandatory_letter +
          " and optional letters " + optional_letters + " are: ")
    # print words and definitions
    for word in found_words:
        try:
            print(word, "-", wordnet.synsets(word)[0].definition())
        except IndexError:
            print(word)
#print(wordnet.synsets("dog")[0].definition())

# test
#for long word 169826304 combinations
mandatory_letter="r"
optional_letters="tnacifo"
#found_words = start_find_words(mandatory_letter, optional_letters, debug=True)
#print_results(found_words, mandatory_letter, optional_letters)

mandatory_letter="r"
optional_letters="tnco"
found_words = start_find_words(mandatory_letter, optional_letters, max_word_length=5, debug=False)
print_results(found_words, mandatory_letter, optional_letters)
# timing for short word 3635 combinations about 8 seconds without printing results
print(timeit.timeit('start_find_words(mandatory_letter="r", optional_letters="tnco", max_word_length=6, progress_bar=False)',
              'from __main__ import start_find_words', number=10)/10)

