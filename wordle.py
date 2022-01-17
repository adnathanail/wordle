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

def get_letters_by_rank(words):
    letter_tallies = {}

    for letter in string.ascii_lowercase:
        letter_tallies[letter] = 0

    for word in words:
        for char in word:
            letter_tallies[char.lower()] += 1

    return [item[0] for item in sorted(letter_tallies.items(), key=lambda x: x[1])]

def get_best_word(letters_by_rank, possible_words):
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

words_we_care_about = get_initial_words()
ranked_letters = get_letters_by_rank(words_we_care_about)
print(get_best_word(ranked_letters, words_we_care_about))