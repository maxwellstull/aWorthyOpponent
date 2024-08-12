import random
import time
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

def comps_per(start_time, ctr):
    print("Computations per sec: ", ctr / (time.time() - start_time))

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
    letters = ['Q', 'T', 'G', 'T', 'O', 'U', 'J', 'S', 'S', 'S', 'I', 'N', 'E', 'N', 'P', 'I', 'N', 'U', 'E', 'J']
    print("Draw: ", letters)
    bank = letterbank(letters)

    dictionary_uncropped = None
    with open("resources/dictionary.txt","r") as fp:
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
    answers = []
    hundreds = []
    sloppy = True
    if(sloppy):
        start = time.time()
        hundred = time.time()
        for word_0 in dictionary_lengths[word_order[0]]:
            for word_1 in dictionary_lengths[word_order[1]]:
                if not bank.test([word_0, word_1]):
                    continue
                for word_2 in dictionary_lengths[word_order[2]]:
                    if not bank.test([word_0, word_1, word_2]):
                        continue
                    for word_3 in dictionary_lengths[word_order[3]]:
                        if not bank.test([word_0, word_1, word_2, word_3]):
                            continue
                        for word_4 in dictionary_lengths[word_order[4]]:
                            if bank.test([word_0, word_1, word_2, word_3, word_4]):
                                print("Valid:", word_0, word_1, word_2, word_3, word_4)
                                answers.append([word_0, word_1, word_2, word_3, word_4])
                                if(len(answers) % 100 == 0):
                                    print("Time per 100: ", time.time() - hundred)
                                    hundreds.append(time.time() - hundred)
                                    hundred = time.time()
        print("Valid answers: ", len(answers))
        print("Calculation time: ", time.time() - start)
        print("Hundreds: ", hundreds)
    else: # dynamic programming / "elegant" solution
        # Instead of testing every time to see if 5 words are valid n^5*n^2, this will create a giant dictionary of 
        #   all words that don't work with eachother as it computes
        # Dictionary will be more RAM intensive but drastically less computationally expensive as the dictionary is built, because
        #   we wont have to check if 5 words are valid if we know that "WRUNG" and "DANCER" are invalid together and those words are in that list.
        #   This will still be a mess of for loops, but it should execute faster for finding all solutions. It's also worth noting that 
        #   the intelligence will not include the first word, since it will only ever be seen once.
        legal_combos = {}
        answers = []
        start = time.time()
        hundred = time.time()
        hundreds = []
        for word0 in dictionary_lengths[word_order[0]]:
           # print(word0)
            if word0 not in legal_combos:
                legal_combos[word0] = {}
            for word1 in dictionary_lengths[word_order[1]]:
                #print(word1)
                if not bank.test([word0, word1]):
                    continue
                if word1 not in legal_combos:
                    legal_combos[word1] = {}
                for word2 in dictionary_lengths[word_order[2]]:
                    #print(word2)
                    if word2 not in legal_combos[word0]:
                        legal_combos[word0][word2] = bank.test([word0, word2])
                    if legal_combos[word0][word2] == False:
                        continue
                    if word2 not in legal_combos[word1]:
                        legal_combos[word1][word2] = bank.test([word1, word2])
                    if legal_combos[word1][word2] == False: 
                        continue

                    if word2 not in legal_combos:
                        legal_combos[word2] = {}
                    for word3 in dictionary_lengths[word_order[3]]:
#                        print(word3)
                        if word3 not in legal_combos[word0]:
                            legal_combos[word0][word3] = bank.test([word0, word3])
                        if legal_combos[word0][word3] == False:
                            continue
                        if word3 not in legal_combos[word1]:
                            legal_combos[word1][word3] = bank.test([word1, word3])
                        if legal_combos[word1][word3] == False:
                            continue
                        if word3 not in legal_combos[word2]:
                            legal_combos[word2][word3] = bank.test([word2, word3])
                        if legal_combos[word2][word3] == False:
                            continue

                        if word3 not in legal_combos:
                            legal_combos[word3] = {}
                        for word4 in dictionary_lengths[word_order[4]]:
                            if word4 not in legal_combos[word0]:
                                legal_combos[word0][word4] = bank.test([word0, word4])
                            if legal_combos[word0][word4] == False:
                                continue
                            if word4 not in legal_combos[word1]:
                                legal_combos[word1][word4] = bank.test([word1, word4])
                            if legal_combos[word1][word4] == False:
                                continue
                            if word4 not in legal_combos[word2]:
                                legal_combos[word2][word4] = bank.test([word2, word4])
                            if legal_combos[word2][word4] == False:
                                continue
                            if word4 not in legal_combos[word3]:
                                legal_combos[word3][word4] = bank.test([word3, word4])
                            if legal_combos[word3][word4] == False:
                                continue

                            if bank.test([word0, word1, word2, word3, word4]):
                                print("Valid: ", word0, word1, word2, word3, word4)
                                answers.append([word0, word1, word2, word3, word4])
                                if(len(answers) % 100 == 0):
                                    print("Time per 100: ", time.time() - hundred)
                                    hundreds.append(time.time() - hundred)
                                    hundred = time.time()

        print("Valid: ", len(answers))
        print("Calculation time: ", time.time() - start)
        print("Hundreds:", hundreds)



if __name__=="__main__":
    main()