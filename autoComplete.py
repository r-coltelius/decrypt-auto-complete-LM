from corpus import Corpus
import random

class AutoComplete:

    def __init__(self, corpus: Corpus):
        self.bigram_words = corpus.bigram_words
        self.trigram_words = corpus.trigram_words
        self.quadgram_words = corpus.quadgram_words

    def predict_bi(self, word1, word2):
        word1, word2 = word1.lower(), word2.lower()

        w1w2 = word1 + " " + word2
        potentials = {}
        for trigram_key, trigram_log_prob in self.trigram_words.items():
            if trigram_key.startswith(w1w2):
                trigram_key = trigram_key.split(" ")[2]

                bigram_log_prob = self.bigram_words.get(w1w2, -10)
                potentials[trigram_key] = trigram_log_prob - bigram_log_prob

        if not potentials:
            return random.choice(["the", "a", "is", "in", "it", "of", "and", "to", "was", "that"])
        
        potentials = sorted(potentials.items(), key = lambda x : x[1], reverse = True)
        if len(potentials) > 1:
            rand = random.randint(0, 0)
            return potentials[rand][0]
        elif len(potentials) == 1:
            return potentials[0][0]
    
    def predict_tri(self, word1, word2, word3):
        word1, word2, word3 = word1.lower(), word2.lower(), word3.lower()

        w1w2w3 = word1 + " " + word2 + " " + word3
        potentials = {}
        for quadgram_key, quadgram_log_prob in self.quadgram_words.items():
            if quadgram_key.startswith(w1w2w3):
                quadgram_key = quadgram_key.split(" ")[3]

                trigram_log_prob = self.trigram_words.get(w1w2w3, -10)
                potentials[quadgram_key] = quadgram_log_prob - trigram_log_prob

        if not potentials:
            return self.predict_bi(word2, word3)

        potentials = sorted(potentials.items(), key = lambda x : x[1], reverse = True)
        if len(potentials) > 1:
            rand = random.randint(0, 0)
            return potentials[rand][0]
        elif len(potentials) == 1:
            return potentials[0][0]