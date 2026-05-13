import xml.etree.ElementTree as ET
import bz2
import string
import os
import json
import matplotlib.pyplot as plt
import math

class Corpus:

    def __init__(self, filepaths,
    cache_path="freq_table.json", 
    text_cache_path = "corpus_text.json", 
    onegram_cache_path="onegram_table.json",
    bigram_cache_path="bigram_table.json",
    trigram_cache_path="trigram_table.json",
    bigram_words_cache_path="bigram_words_table.json",
    trigram_words_cache_path="trigram_words_table.json", 
    quadgram_words_cache_path = "quadgram_words_table.json"):

        self.filepaths = filepaths  
        self.text_cache_path = text_cache_path
        self.text = self.load_or_build(self.text_cache_path, self.load_corpus)
        self.cache_path = cache_path
        self.onegram_cache_path = onegram_cache_path
        self.bigram_cache_path = bigram_cache_path
        self.trigram_cache_path = trigram_cache_path
        self.bigram_words_cache_path = bigram_words_cache_path
        self.trigram_words_cache_path = trigram_words_cache_path
        self.quadgram_words_cache_path = quadgram_words_cache_path

        self.frequencies = self.load_or_build(self.cache_path, self.load_frequency_table)
        self.onegrams = self.load_or_build(self.onegram_cache_path, self.load_onegram_table)
        self.bigrams = self.load_or_build(self.bigram_cache_path, self.load_bigram_table)
        self.trigrams = self.load_or_build(self.trigram_cache_path, self.load_trigram_table)
        self.bigram_words = self.load_or_build(self.bigram_words_cache_path, self.load_bigram_words_table)
        self.trigram_words = self.load_or_build(self.trigram_words_cache_path, self.load_trigram_words_table)
        self.quadgram_words = self.load_or_build(self.quadgram_words_cache_path, self.load_quadgram_words_table)

    def _load_cache(self, path):
        if os.path.exists(path):
            try:
                with open(path, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                os.remove(path)
        return None

    def _save_cache(self, data, path):
        with open(path, 'w') as f:
            json.dump(data, f)

    def _load_or_build_text(self):
        if os.path.exists(self.text_cache_path):
            with open(self.text_cache_path, 'r', encoding='utf-8') as f:
                return f.read()
        text = self.load_corpus()
        with open(self.text_cache_path, 'w', encoding='utf-8') as f:
            f.write(text)
        return text

    def load_or_build(self, cache_path, build_func):
        cached = self._load_cache(cache_path)
        if cached is not None:
            return cached
        table = build_func()
        self._save_cache(table, cache_path)
        return table

    def load_corpus(self):
        text = []
        for filepath in self.filepaths:
            if filepath.endswith(".bz2"):
                with bz2.open(filepath, 'rb') as f:
                    for event, elem in ET.iterparse(f, events=('end',)):
                        if elem.text and elem.text.strip():
                            text.append(elem.text.strip())
                        elem.clear()
            elif filepath.endswith(".txt"):
                with open(filepath, 'r', encoding='utf-8') as f:
                    text.append(f.read())
        return ' '.join(text)

    #auto complete
    def _tokenize(self):
        words = []
        for word in self.text.lower().split():
            clean = ''.join(ch for ch in word if ch in string.ascii_lowercase or ch == "'")
            clean = clean.strip("'")
            if clean:
                words.append(clean)
        return words

    def _build_vocab(self, words, vocab_size=50000):
        word_counts = {}
        for word in words:
            word_counts[word] = word_counts.get(word, 0) + 1
        vocab = set()
        for word, _ in sorted(word_counts.items(), key=lambda x: x[1], reverse=True)[:vocab_size]:
            vocab.add(word)
        return vocab

    #decrypt
    def load_frequency_table(self):
        counter = {}
        for letter in string.ascii_lowercase:
            counter[letter] = 1  # Laplace smoothing

        for ch in self.text.lower():
            if ch in string.ascii_lowercase:
                counter[ch] += 1

        total = sum(counter.values())
        table = {}
        for k, f in counter.items():  
            table[k] = math.log(f / total)  
        return table

    def load_onegram_table(self):
        counter = {}
        k = 1
        for a in string.ascii_lowercase:
            counter[a] = 1  #laplace

        for ch in self.text.lower():
            if ch in string.ascii_lowercase:
                counter[ch] += 1

        total = sum(counter.values())
        table = {}
        for k, f in counter.items():  
            table[k] = math.log(f / total)  
        return table

    def load_bigram_table(self):
        counter = {}
        k = 1
        for a in string.ascii_lowercase:
            for b in string.ascii_lowercase:
                counter[a+b] = k  #laplace

        text = self.text.lower()
        for i in range(len(text) - 1):
            a, b = text[i], text[i + 1]
            if a in string.ascii_lowercase and b in string.ascii_lowercase:
                counter[a+b] += 1

        total = sum(counter.values())
        table = {}
        for k, f in counter.items():  
            table[k] = math.log(f / total)  
        return table

    def load_trigram_table(self):
        counter = {}
        k = 1
        for a in string.ascii_lowercase:
            for b in string.ascii_lowercase:
                for c in string.ascii_lowercase:
                    counter[a+b+c] = k  #laplace

        text = self.text.lower()
        for i in range(len(text) - 2):
            a, b, c = text[i], text[i + 1], text[i + 2]
            if a in string.ascii_lowercase and b in string.ascii_lowercase and c in string.ascii_lowercase:
                counter[a+b+c] += 1

        total = sum(counter.values())
        table = {}
        for k, f in counter.items():  
            table[k] = math.log(f / total)  
        return table

    #auto complete igen
    def load_bigram_words_table(self, vocab_size=50000):
        words = self._tokenize()
        vocab = self._build_vocab(words, vocab_size)

        counter = {}
        for i in range(len(words) - 1):
            a, b = words[i], words[i + 1]
            if a in vocab and b in vocab:
                key = a + " " + b
                counter[key] = counter.get(key, 0) + 1

        total = sum(counter.values()) + len(counter)  #Laplace k smoothing med längden av counter
        table = {}
        for k, f in counter.items():  
            table[k] = math.log(f / total)  
        return table

    def load_trigram_words_table(self, vocab_size=50000):
        words = self._tokenize()
        vocab = self._build_vocab(words, vocab_size)

        counter = {}
        for i in range(len(words) - 2):
            a, b, c = words[i], words[i + 1], words[i + 2]
            if a in vocab and b in vocab and c in vocab:
                key = a + " " + b + " " + c
                counter[key] = counter.get(key, 0) + 1

        total = sum(counter.values()) + len(counter)  #laplace smoothing
        table = {}
        for k, f in counter.items():  
            table[k] = math.log(f / total)  
        return table

    def load_quadgram_words_table(self, vocab_size=50000):
        words = self._tokenize()
        vocab = self._build_vocab(words, vocab_size)

        counter = {}
        for i in range(len(words) - 3):
            a, b, c, d = words[i], words[i + 1], words[i + 2], words[i+3]
            if a in vocab and b in vocab and c in vocab and d in vocab:
                key = a + " " + b + " " + c + " " + d
                counter[key] = counter.get(key, 0) + 1

        total = sum(counter.values()) + len(counter)  #laplace smoothing
        table = {}
        for k, f in counter.items():  
            table[k] = math.log(f / total)  
        return table

    def plot_corpus(self):
        sorted_freq = sorted(self.frequencies.items(), key=lambda item: item[1], reverse=True)
        letters = []
        for letter, freq in sorted_freq:
            letters.append(letter)
        freqs = []
        for letter, freq in sorted_freq:
            freqs.append(freq)
        plt.bar(letters, freqs)
        plt.xlabel("Bokstav")
        plt.ylabel("Frekvens")
        plt.title('Bokstavsfrekvens för corpus')
        plt.show()
    
    def corpus_stats(self):
        words = self._tokenize()
        word_count = len(words)
        char_count = len(self.text)

        return char_count, word_count