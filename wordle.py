import string

def get_initial_words():
    words = []

    with open("/usr/share/dict/words") as f:
        for row in f.readlines():
            words.append(row.replace("\n", ""))

    out = []

    for word in words:
        if len(word) == 5:
            if word[0].islower():
                out.append(word)

    return out

def filter_words(known_letters, known_not_letters, known_not_words, fixed_letters, words_to_filter):
    out = []

    for word in words_to_filter:
        if word in known_not_words:
            continue
        good = True
        for letter in known_letters:
            if letter not in word:
                good = False
        for letter in known_not_letters:
            if letter in word:
                good = False
        for ind, letter in enumerate(fixed_letters):
            if letter is not None and word[ind] != letter:
                good = False
        if good:
            out.append(word)

    return out

def get_letters_by_rank(words):
    letter_tallies = {}

    for letter in string.ascii_lowercase:
        letter_tallies[letter] = 0

    for word in words:
        for char in word:
            letter_tallies[char.lower()] += 1

    return [item[0] for item in sorted(letter_tallies.items(), key=lambda x: x[1])]

def get_best_word(possible_words):
    letters_by_rank = get_letters_by_rank(possible_words)

    best_word = ""
    best_word_score = 0

    for word in possible_words:
        score = 0
        already_scored_letters = set()
        for character in word:
            if character not in already_scored_letters:
                score += letters_by_rank.index(character)
                already_scored_letters.add(character)

        if score > best_word_score:
            best_word = word
            best_word_score = score
    return best_word

def get_input(prompt, allowed_values):
    result = input(prompt)
    while result not in allowed_values:
        print("Invalid value\n")
        result = input(prompt)
    return result

def play():
    current_words = get_initial_words()
    known_letters = set()
    known_not_letters=set()
    known_not_words=set()
    fixed_letters=[None, None, None, None, None]

    while None in fixed_letters:
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

play()