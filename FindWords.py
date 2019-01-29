import nltk
from nltk.corpus import words

nltk.download('words')

default_max_word_length=10
default_min_length=4

def is_word(word_to_test, min_length=default_min_length):
    if word_to_test in words.words() and len(word_to_test)>=min_length:
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
def find_words(word, optional_letters,
               max_word_length):
    if is_word(word):
        print(word)
#    else:
#        print("    not word: " + word)

    if not stop_looking_for_words(word, max_word_length):
        for letter in optional_letters:
            # add letter to end of word
            new_word = word + letter
            find_words(new_word, optional_letters, max_word_length)
            # add letter to front of word
            new_word = letter + word
            find_words(new_word, optional_letters, max_word_length)

# find all possible words with mandatory letter and optional letters. Each letter can be used multiple times.
def start_find_words(mandatory_letter, optional_letters,
                     max_word_length=default_max_word_length):
    find_words(mandatory_letter, optional_letters,
               max_word_length)

# test
start_find_words(mandatory_letter="r", optional_letters="tnacifo")