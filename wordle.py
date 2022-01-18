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

def filter_words(known_letters, known_not_letters, known_not_words, fixed_letters, words_to_filter):
    out = []

    print(known_not_words)

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

words_we_care_about = get_initial_words()
ranked_letters = get_letters_by_rank(words_we_care_about)
# print(get_best_word(ranked_letters, words_we_care_about))

known = {"r", "s", "e"}
known_not_letters = {"a", "t", "o", "p", "u"}
fixed = [None, None, None, None, "e"]
not_words = ["arose", "aster", "hirse"]

words_we_care_about = filter_words(
    known_letters={"r", "s", "e"},
    known_not_letters={"a", "t", "o", "p", "u"},
    known_not_words={"arose", "aster", "hirse"},
    fixed_letters=[None, None, None, None, "e"],
    words_to_filter=words_we_care_about
)
ranked_letters = get_letters_by_rank(words_we_care_about)
print(get_best_word(ranked_letters, words_we_care_about))