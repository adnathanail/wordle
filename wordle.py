import os
import string
from typing import Dict, List, Set, Tuple

def get_initial_words() -> Dict[str, int]:
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

    words_by_frequency: Dict[str, int] = {}

    with open(os.path.join(__location__, 'google-books-common-words.txt')) as f:
        for row in f.readlines():
            word, frequency = row.split('\t')
            if len(word) == 5:
                words_by_frequency[word.lower()] = int(frequency)

    return words_by_frequency

def filter_words(
    known_letters: Set[str],
    known_not_letters: Set[str],
    known_not_words: Set[str],
    fixed_letters: List[Tuple[int, str]],
    fixed_not_letters: List[Tuple[int, str]],
    words_to_filter: Dict[str, int],
) -> Dict[str, int]:
    out: Dict[str, int] = {}

    for word, tally in words_to_filter.items():
        if word in known_not_words:
            continue
        good = True
        for letter in known_letters:
            if letter not in word:
                good = False
        for letter in known_not_letters:
            if letter in word:
                good = False
        for ind, letter in fixed_letters:
            if word[ind] != letter:
                good = False
        for (ind, letter) in fixed_not_letters:
            if word[ind] == letter:
                good = False
        if good:
            out[word] = tally

    return out

def get_letters_by_rank(words: Dict[str, int]) -> List[str]:
    letter_tallies: Dict[str, int] = {}

    for letter in string.ascii_lowercase:
        letter_tallies[letter] = 0

    for word in words:
        for char in word:
            letter_tallies[char.lower()] += 1

    return [item[0] for item in sorted(letter_tallies.items(), key=lambda x: x[1])]

def get_best_first_word(possible_words: Dict[str, int]) -> str:
    """Ranks by letter frequency, as opposed to word frequency, for an optimum first guess"""
    letters_by_rank = get_letters_by_rank(possible_words)

    best_word = ""
    best_word_score = 0

    for word in possible_words:
        score = 0
        already_scored_letters: Set[str] = set()
        for character in word:
            if character not in already_scored_letters:
                score += letters_by_rank.index(character)
                already_scored_letters.add(character)

        if score > best_word_score:
            best_word = word
            best_word_score = score
    return best_word

def get_best_word(possible_words: Dict[str, int]) -> str:
    best_word = ""
    best_word_score = 0

    for word, tally in possible_words.items():
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
    fixed_letters: List[Tuple[int, str]] = []
    fixed_not_letters: List[Tuple[int, str]] = []

    current_guess: str = get_best_first_word(current_words)

    while len(fixed_letters) < 5:
        print(f"\nTry '{current_guess}'\n")

        res = get_input(f"Was {current_guess} valid? (y/n): ", {"y", "n"})
        if res == "y":
            want_to_add_to_known_not_letters: Set[str] = set()
            for i in range(5):
                res = get_input(f"Result for '{current_guess[i]}' (b/g/y): ", {"b", "g", "y"})
                if res == "b":
                    want_to_add_to_known_not_letters.add(current_guess[i])
                elif res == "g":
                    known_letters.add(current_guess[i])
                    fixed_letters.append((i, current_guess[i]))
                elif res == "y":
                    known_letters.add(current_guess[i])
                    fixed_not_letters.append((i, current_guess[i]))
                else:
                    raise Exception("Enter b, g, or y")
            # Do this last as a letter can appear multiple times in a word, with different responses
            # E.g. WHICH with a response of GGBGB would add H to both known_letters and known_not_letters
            for letter in want_to_add_to_known_not_letters:
                if letter not in known_letters:
                    known_not_letters.add(letter)
        elif res == "n":
            known_not_words.add(current_guess)
        else:
            raise Exception("Enter y, or n")

        current_words = filter_words(known_letters, known_not_letters, known_not_words, fixed_letters, fixed_not_letters, current_words)
        current_guess = get_best_word(current_words)

    print("\nSUCCESS!!")

play()
