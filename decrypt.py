import string
import math
import random 
import matplotlib.pyplot as plt

class Decrypt:

    def __init__(self, text, frequency_table_corpus, onegram_table, bigram_table, trigram_table):
        self.cipher =  {}
        self.best_mapping = None
        self.encrypted_message = self.monoalphabetic_substitution_chipfer(text)
        self.decrypted_message = ""  
        self.freq_table_corpus = frequency_table_corpus
        self.freq_table_message = {}
        self.onegram_table = onegram_table
        self.bigram_table = bigram_table
        self.trigram_table = trigram_table
        self.score = 0

    def monoalphabetic_substitution_chipfer(self, text):
        shuffled = list(string.ascii_lowercase)
        random.shuffle(shuffled)

        cipher = {}
        for i, letter in enumerate(string.ascii_lowercase):
            cipher[letter] = shuffled[i]
        
        self.cipher = cipher 

        res = ""
        for ch in text.lower():
            if ch in string.ascii_lowercase:
                res += cipher[ch]
            else:
                res += ch
        print(res)
        return res

    def message_frequency_table(self):
        counter = {} 
    
        #laplace k-smoothing. 1 verkar bäst? 
        k = 3
        for letter in string.ascii_lowercase:
            counter[letter] = k

        for letter in self.encrypted_message.lower():
            if letter in string.ascii_lowercase:
                counter[letter] += 1

        total = sum(counter.values())

        for letter, count in counter.items():
            self.freq_table_message[letter] = count / total

        return dict(self.freq_table_message)

    def frequency_analysis(self):
        sorted_freq_corpus = sorted(self.freq_table_corpus.items(), key=lambda item: item[1], reverse=True)
        sorted_freq_message = sorted(self.freq_table_message.items(), key=lambda item: item[1], reverse=True)

        #Om det inte skulle innehålla alla bokstäver av någon anledning
        corpus_letters = []
        for letter, freq in sorted_freq_corpus:
            corpus_letters.append(letter)

        message_letters = []
        for letter, freq in sorted_freq_message:
            message_letters.append(letter)

        #bijektion f: m --> c
        mapping = dict(zip(message_letters, corpus_letters))

        return mapping
    
    #till hill climbing
    def accept_mapping(self, mapping):
        res = ""
        for ch in self.encrypted_message:
            res += mapping.get(ch, ch)
        return res

    def score_function(self, text, n = 1): #N-GRAM
        score = 0
        text = text.lower()

        if n == 1:
            for i in range(len(text)):
                a = text[i]
                if a in string.ascii_lowercase:
                    score += self.onegram_table.get(a, -10)
        elif n == 2: 
            for i in range(len(text)-1):
                a,b = text[i], text[i+1]
                if a in string.ascii_lowercase and b in string.ascii_lowercase:
                        score += self.bigram_table.get(a+b, -10)
        elif n == 3:
            for i in range(len(text)-2):
                a,b,c = text[i], text[i+1], text[i+2]
                if a in string.ascii_lowercase and b in string.ascii_lowercase and c in string.ascii_lowercase:
                    score += self.trigram_table.get(a+b+c, -10)
        return score
    
    def hill_climbing(self, iterations=5001, T0=5, a=0.997, restarts = 20):
        best_guess = ""
        best_score = float('-inf')
        best_mapping = None

        for r in range (restarts):
            T_k = T0
            #initial gissning och score
            mapping = self.frequency_analysis()
            decrypted = self.accept_mapping(mapping)
            s_k = self.score_function(decrypted)

            for i in range(iterations):
                if i % 1000 == 0:
                    print(f"{i}, T_k={T_k}, score={s_k}")

                T_k = a**i * T0

                new_map = mapping.copy()
                b, c = random.sample(list(new_map.keys()), 2)
                new_map[b], new_map[c] = new_map[c], new_map[b]

                new_decrypted = self.accept_mapping(new_map)
                s_k_plus_one = self.score_function(new_decrypted)

                delta = s_k_plus_one - s_k

                if delta >= 0: #gör byte
                    mapping = new_map
                    s_k = s_k_plus_one
                    decrypted = new_decrypted
                else: #<= gör byte med sannolikhet p
                    p = math.exp(delta / T_k)
                    if random.random() < p: #[0,1]
                        mapping = new_map
                        s_k = s_k_plus_one
                        decrypted = new_decrypted
                
                if s_k > best_score:
                    best_score = s_k
                    best_guess = decrypted
                    best_mapping = mapping.copy()

        self.decrypted_message = best_guess
        self.score = best_score
        self.best_mapping = best_mapping
        return self.decrypted_message, self.score

    def evaluate_mapping(self):
        true_inverse = {enc.lower(): plain.lower() for plain, enc in self.cipher.items()}

        correct = 0
        mapping = {}
        for enc_letter in string.ascii_lowercase:
            predicted = self.best_mapping.get(enc_letter, '').lower()
            true = true_inverse.get(enc_letter, '')
            match = predicted == true
            if match:
                correct += 1
            mapping[enc_letter] = (predicted, true, match)

        return correct, mapping