from pathlib import Path
import pickle
import re
import timeit

# pip dependencies, should be in requirements.txt
import nltk
from nltk.corpus import reuters

def eliminate_words(words, guess, results):
    matching = []
    for word in words:
        for idx, char in enumerate(guess):
            #print(idx, char)
            if (results[idx] == "none" and char in word) or (results[idx] == "correct" and word[idx] != char) or (results[idx] == "wrong" and word[idx] == char) or (results[idx] == "wrong" and char not in word):
                break
            matching.append(word)

    return matching

def regex_eliminate_words(words, pattern, in_word, not_in_word):
    re_pattern = re.compile(pattern)
    matching = []

    for word in words:
        match = re_pattern.match(word) 
        in_word_match = not 0 in [char in word for char in in_word]
        not_in_word_match = 1 in [char in word for char in not_in_word]
        if (match and in_word_match) and not not_in_word_match:
            matching.append(word)

    return matching

def frequent_word_dist():
    print("Download 'reuters' corpus, please.")
    nltk.download()
    return nltk.FreqDist(reuters.words())

def trim_uncommon_words(words):
    freq_list = frequent_word_dist()
    common_words = set()
    for word in words:
        if word in freq_list:
            common_words.add(word)

    return common_words

def analyze_wordle(words):
    while len(words) > 1:
        guess = input("Enter guess:")
        results = []
        pattern = ""
        in_word = set()
        not_in_word = set()

        for letter in guess:
            user = input(letter + " is (c)orrect or (w)rong spot. Enter for not found")
            if user == 'c':
                pattern += letter
                in_word.add(letter)
                results.append("correct")
            elif user == 'w':
                pattern += f"[^{letter}]"
                in_word.add(letter)
                results.append("wrong")
            else:
                pattern += f"."
                not_in_word.add(letter)
                results.append("none")

        pattern = f"^{pattern}$"

        print(pattern)
        print(in_word)
        print(not_in_word)

        #if_words = eliminate_words(words, guess, results)
        words = regex_eliminate_words(words, pattern, in_word, not_in_word)

        # print("Wordlist from conditional implementation")
        # print(if_words)
        # print(len(if_words))
        #print(timeit.timeit(lambda: eliminate_words(words, guess, results), number=10000))
        
        print("Wordlist from regex implementation")
        print(words)
        print(len(words))
        #print(timeit.timeit(lambda: regex_eliminate_words(words, pattern, in_word, not_in_word), number=10000))

def get_words_len5(words):
    words_len5 = set()
    if not Path("words_len5.pickle").is_file():
        for word in words_alpha:
            if len(word.strip()) == 5:
                words_len5.add(word.strip())

        pickle.dump(words_len5, open("words_len5.pickle", "wb"))
    else:
        words_len5 = pickle.load(open("words_len5.pickle", "rb"))
    
    return words_len5

def get_words_common(words):
    if not Path("words_common.pickle").is_file():
        words_common = trim_uncommon_words(words_len5)
        pickle.dump(words_common, open("words_common.pickle", "wb"))
    else:
        words_common = pickle.load(open("words_common.pickle", "rb"))

    return words_common

words_alpha = open("words_alpha.txt", "r")
words = get_words_common(get_words_len5(words_alpha))

while(True):
    analyze_wordle(words.copy())

    if input("Exit? y/n") == "y":
        break
