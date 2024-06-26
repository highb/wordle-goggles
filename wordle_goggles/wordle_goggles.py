from pathlib import Path
import json
import re

import pdb

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

def get_frequent_word_dist():
    print("Download 'reuters' corpus, please.")
    nltk.download()
    return nltk.FreqDist(reuters.words())

def get_corpus_words():
    print("Download 'reuters' corpus, please.")
    nltk.download()
    return reuters.words()

def trim_uncommon_words(words):
    freq_list = get_frequent_word_dist()
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
        words = regex_eliminate_words(words, pattern, in_word, not_in_word)
        
        print(f"Wordlist ({len(words)} remain)")
        print(words)

def get_words_len5(words):
    if not Path("words_len5.json").is_file():
        words_len5 = []

        for word in words:
            word = str(word).strip().lower()
            if len(word) == 5:
                words_len5.append(word)

        print(words_len5)
        json.dump({'words': words_len5}, open("words_len5.json", "w"))

        return words_len5
    else:
        return json.load(open("words_len5.json", "r"))['words']
    

def get_words_common(words):
    if not Path("words_common.json").is_file():
        words_common = trim_uncommon_words(words)
        json.dump({'words': words_common}, open("words_common.json", "w"))
        return words_common
    else:
        return json.load(open("words_common.json", "r"))['words']


def get_words():
    if not Path("words.json").is_file():
        words_corpus = get_corpus_words()
        words = get_words_len5(words_corpus)
        json.dump({'words': words}, open("words.json", "w"))
        return words
    else:
        return json.load(open("words.json", "r"))['words']


def main():
    words = set(get_words())

    while(True):
        analyze_wordle(words.copy())

        if input("Exit? y/n") == "y":
            break
