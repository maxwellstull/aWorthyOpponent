import random

class letterbank():
    def __init__(self, letters):
        self.letters = sorted(list(letters), key=lambda k: scores[k], reverse=True)
        self.counts= {}
        for letter in self.letters:
            if letter not in self.counts:
                self.counts[letter] = 1
            else:
                self.counts[letter] += 1
    def is_in_bank(self, word):
        temp_counts = {key:value for key, value in self.counts.items()}
        for letter in word:
            if letter not in temp_counts or temp_counts[letter] == 0:
                return False
            temp_counts[letter] -= 1
        return True
    
    def test(self, word_list):
        temp_counts = {key:value for key, value in self.counts.items()}
        for word in word_list:
            for letter in word:
                if temp_counts[letter] == 0:
                    return False
                temp_counts[letter] -= 1
        return True
    
    

scores = {
    "A":3,
    "B":9,
    "C":9,
    "D":6,
    "E":3,
    "F":12,
    "G":6,
    "H":12,
    "I":3,
    "J":24,
    "K":15,
    "L":3,
    "M":9,
    "N":3,
    "O":3,
    "P":3,
    "Q":30,
    "R":3,
    "S":3,
    "T":3,
    "U":3,
    "V":12,
    "W":12,
    "X":24,
    "Y":12,
    "Z":30   
}
weights = {
    "A":11,
    "B":4,
    "C":3,
    "D":6,
    "E":16,
    "F":3,
    "G":5,
    "H":4,
    "I":10,
    "J":2,
    "K":2,
    "L":6,
    "M":3,
    "N":9,
    "O":10,
    "P":3,
    "Q":2,
    "R":8,
    "S":6,
    "T":8,
    "U":6,
    "V":3,
    "W":3,
    "X":1,
    "Y":3,
    "Z":1,   
}

def draw_letters(count=20):
    letters = list(weights.keys())
    probs = [weights[letter] for letter in letters]
    draw = random.choices(letters, weights=probs, k=count)
    return draw

def main():
#    letters = "MWDEWRSNJUISRYLAAIPI"
    letters = draw_letters()

    # Test if random letters comply (for instance, we can get 2 x's randomly but we can only draw 1)
    all_letters = []
    for letter, amnt in weights.items():
        for _ct in range(0, amnt):
            all_letters.append(letter)
    all_bank = letterbank(all_letters)
    if not all_bank.is_in_bank(letters):
        print("Invalid draw: ", letters)
        return
    

    # The actual stuff
    print("Draw: ", letters)
    bank = letterbank(letters)

    dictionary_uncropped = None
    with open("sandbox/dictionary.txt","r") as fp:
        dictionary_uncropped = fp.read().splitlines()

    dictionary_cropped = []
    for word in dictionary_uncropped:
        if len(word) <= 6 and len(word) >= 2:
            dictionary_cropped.append(word)

    
    dictionary_startswith = {letter:[] for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"}
    dictionary_contains = {letter:[] for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"}
    dictionary_lengths = {2:[], 3:[], 4:[], 5:[], 6:[]}

    dictionary = []

    for word in dictionary_cropped:
        if not bank.is_in_bank(word):
            continue
        dictionary.append(word)
        dictionary_startswith[word[0]].append(word)
        dictionary_lengths[len(word)].append(word)
        for letter in word:
            dictionary_contains[letter].append(word)
    
    word_order = sorted(list(dictionary_lengths), key=lambda k: len(dictionary_lengths[k]))
    print(word_order)

    # Here we get... sloppy
    for word_0 in dictionary_lengths[word_order[0]]:
#        print(word_0)
        for word_1 in dictionary_lengths[word_order[1]]:
            if not bank.test([word_0, word_1]):
                continue
#            print('\t',word_1)
            for word_2 in dictionary_lengths[word_order[2]]:
                if not bank.test([word_0, word_1, word_2]):
                    continue
#                print('\t\t',word_2)
                for word_3 in dictionary_lengths[word_order[3]]:
                    if not bank.test([word_0, word_1, word_2, word_3]):
                        continue
                    for word_4 in dictionary_lengths[word_order[4]]:
#                        print("Trying:", word_0, word_1, word_2, word_3, word_4)
                        if bank.test([word_0, word_1, word_2, word_3, word_4]):
                            print("Valid:", word_0, word_1, word_2, word_3, word_4)

if __name__=="__main__":
    main()