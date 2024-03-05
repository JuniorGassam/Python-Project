import random
import json
def words_gen(str_pos, prob_cal, dict_words):
    prob_first_letter = [prob for prob in prob_cal if prob_cal[prob][0] > 0]
    current_list = []
    words = []
    current_word = ""
    end = False
    last_letters = ""

    for prob in prob_cal:
        if prob_cal[prob][0] > 0:
            prob_first_letter.append(prob)

    for _ in range(10):
        current_word += random.choice(prob_first_letter)
        while not end:
        # while not end:
            for j in range(1, len(prob_cal[current_word[-1]]) - 2):
                if prob_cal[current_word[-1]][j] > 0.000001:
                    current_list.append(str_pos[current_word[-1]][j - 1][1])
            current_word += random.choice(current_list)
            current_list = []

            last_letters = current_word[-2] + current_word[-1]

            if last_letters in two_end_letters(dict_words):
                end = True

        words.append(current_word)
        current_word = ""
        end = False

    return words

def create_alpha(dict_words):
    alpha = []
    is_in = False

    for word in dict_words:
        for char in word:
            for k in range(len(alpha)):
                if char == alpha[k]:
                    is_in = True
                    break
            if not is_in:
                alpha.append(char)
            is_in = False

    return alpha

def average_words_length_cal(dict_words):
    total_length = sum(len(word) for word in dict_words)
    average = total_length / len(dict_words)
    return round(average)

def prob_str_cal(alpha):
    str_pos = {}
    for char1 in alpha:
        for char2 in alpha:
            if char1 not in str_pos:
                str_pos[char1] = [(char1 + char2)]
            else:
                str_pos[char1].append((char1 + char2))

    return str_pos

def tab_prob(str_pos, dict_words, alpha):
    tab_prob = {}
    prob = 0
    prob_first = 0
    prob_end = 0
    n = 0
    m = 0
    l = 0

    for strs in str_pos:
        for str_value in str_pos[strs]:
            for word in dict_words:
                if str_value in word:
                    n += 1

                if word[0] == str_value[0]:
                    m += 1

                if word[-1] == str_value[0]:
                    l += 1

            prob_first = m / len(dict_words)
            prob = n / len(dict_words)
            prob_end = l / len(dict_words)

            if str_value[0] not in tab_prob:
                tab_prob[str_value[0]] = [prob_first, prob]
            else:
                tab_prob[str_value[0]].append(prob)

                if len(tab_prob[str_value[0]]) == (len(alpha) + 1):
                    tab_prob[str_value[0]].append(prob_end)

            prob = 0
            prob_first = 0
            prob_end = 0
            n = 0
            m = 0
            l = 0

    return tab_prob

def random_choice(lst):
    return random.choice(lst)

def two_end_letters(dict_words):
    return [(word[-2] + word[-1]) if len(word) >= 2 else word for word in dict_words]


def display_words(words):
    for word in words:
        print(word)


def save_prob_table_to_json(prob_table):
    with open('prob_table.json', 'w') as outfile:
        json.dump(prob_table, outfile)

def load_prob_table_from_json():
    try:
        with open('prob_table.json', 'r') as infile:
            prob_table = json.load(infile)
        return prob_table
    except FileNotFoundError:
        return None



# Utilisation des fonctions
# from data import dict_words
with open('data.txt', 'r', encoding='utf-8') as file:
    dict_words = file.read().splitlines()


prob_cal = load_prob_table_from_json()

dict_length = len(dict_words)
average_words_length = average_words_length_cal(dict_words)
alpha = create_alpha(dict_words)
str_pos = prob_str_cal(alpha)
if not prob_cal:
    prob_cal = tab_prob(str_pos, dict_words, alpha)
    save_prob_table_to_json(prob_cal)

words_generate = words_gen(str_pos, prob_cal, dict_words)
display_words(words_generate)