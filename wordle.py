import os
from typing import Dict, List, Set, Union

def get_initial_words() -> Dict[str, int]:
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

    words_by_frequency: Dict[str, int] = {}

    with open(os.path.join(__location__, 'google-books-common-words.txt')) as f:
        for row in f.readlines():
            word, frequency = row.split('\t')
            if len(word) == 5:
                words_by_frequency[word.lower()] = int(frequency)
        print(words_by_frequency["which"])

    return words_by_frequency

def filter_words(known_letters: Set[str], known_not_letters: Set[str], known_not_words: Set[str], fixed_letters: List[Union[str, None]], words_to_filter: Dict[str, int]) -> Dict[str, int]:
    out: Dict[str, int] = {}

    for word, tally in words_to_filter.items():
        print(word, tally)
        if word in known_not_words:
            continue
        print(word, tally)
        good = True
        for letter in known_letters:
            if letter not in word:
                good = False
        print(good)
        for letter in known_not_letters:
            if letter in word:
                good = False
        print(good)
        for ind, letter in enumerate(fixed_letters):
            if letter is not None and word[ind] != letter:
                good = False
        print(good)
        if good:
            out[word] = tally

    return out

def get_best_word(possible_words: Dict[str, int]) -> str:

    best_word = ""
    best_word_score = 0

    for word, tally in possible_words.items():
        if word == "which":
            print(tally, word)
        if tally > best_word_score:
            best_word_score = tally
            best_word = word

    return best_word

def get_input(prompt: str, allowed_values: Set[str]) -> str:
    result = input(prompt)
    while result not in allowed_values:
        print("Invalid value\n")
        result = input(prompt)
    return result

def play():
    current_words = get_initial_words()
    known_letters: Set[str] = set()
    known_not_letters: Set[str] = set()
    known_not_words: Set[str] = set()
    fixed_letters: List[Union[str, None]] = [None, None, None, None, None]

    while None in fixed_letters:
        print(known_letters, known_not_letters, known_not_words, fixed_letters)
        current_guess = get_best_word(current_words)
        print(f"\nTry '{current_guess}'\n")

        res = get_input(f"Was {current_guess} valid? (y/n): ", {"y", "n"})
        if res == "y":
            for i in range(5):
                res = get_input(f"Result for '{current_guess[i]}' (b/g/y): ", {"b", "g", "y"})
                if res == "b":
                    known_not_letters.add(current_guess[i])
                elif res == "g":
                    known_letters.add(current_guess[i])
                    fixed_letters[i] = current_guess[i]
                elif res == "y":
                    known_letters.add(current_guess[i])
                else:
                    raise Exception("Enter b, g, or y")
        elif res == "n":
            known_not_words.add(current_guess)
        else:
            raise Exception("Enter y, or n")

        current_words = filter_words(known_letters, known_not_letters, known_not_words, fixed_letters, current_words)

    print("\nSUCCESS!!")

# play()

current_words = get_initial_words()
# print(filter_words({'c', 'w', 'h'}, {'i', 'h'}, set(), ['w', 'h', None, 'c', None], current_words))
print(filter_words({'c', 'w', 'h'}, set(), set(), [None, None, None, None, None], current_words))