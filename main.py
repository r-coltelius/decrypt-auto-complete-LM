import bz2
from corpus import Corpus
from autoComplete import AutoComplete
from decrypt import Decrypt
import string
from nltk.corpus import gutenberg as gtb
from nltk.corpus import reuters as rts
import random
import os
import matplotlib.pyplot as plt

class Main:
        def download_nltk(library, file_name, acronym): #exempel: reuters, reuters.txt, rts
            download(library)
            with open(file_name, 'w', encoding='utf-8') as f:
                for fileid in acronym.fileids():
                    f.write(acronym.raw(fileid))
        
        @staticmethod
        def print_messages(text, decrypted_message, score):
            print(text)

            print(f'decrypted message: ', decrypted_message)
            print(f'text length: ', len(text))
            print(f'word count in text: ', len(text.split()))
            print(f'best score: ', score)

        def plot_message(text):
            counter = {}
            for letter in string.ascii_lowercase:
                counter[letter] = 0
    
            for ch in text.lower():
                if ch in string.ascii_lowercase:
                    counter[ch] += 1

            freq_table = sorted(counter.items(), key=lambda item: item[1], reverse=True)
            total = sum(count for _, count in freq_table)  

            letters = [letter for letter, _ in freq_table]
            freqs = [count / total for _, count in freq_table]  

            plt.bar(letters, freqs)
            plt.xlabel("Bokstav")
            plt.ylabel("Relativ frekvens")
            plt.title('Bokstavsfrekvens för text')
            plt.show()

        @staticmethod
        def SPEAK_ROBOT_BI(A, word1, word2):
            user_input = ""
            while word1 is None or word2 is None:
                user_input = input("Start a sentence using two words: ")
            first_word = word1
            message = word1 + " " + word2

            for i in range(15):
                prediction = A.predict_bi(word1, word2)
                message += " "
                message += prediction
                if (i == 14):
                    if first_word == "is" or first_word == "are" or first_word == "how" or first_word == "can" or first_word == "why":
                        message += "?"
                    else: 
                        message += "."
                os.system('cls' if os.name == 'nt' else 'clear')
                print(message)
                prev_predicition = word1
                word1 = word2                    
                word2 = prediction

        @staticmethod
        def SPEAK_ROBOT_TRI(A, word1, word2, word3):
            user_input = ""
            while word1 is None or word2 is None or word3 is None:
                user_input = input("Start a sentence using three words: ")
            first_word = word1.lower()
            message = word1 + " " + word2 + " " + word3

            for i in range(15):
                prediction = A.predict_tri(word1, word2, word3)
                message += " "
                if prediction: 
                    message += prediction
                else:
                    prediction = A.predict_bi(word2, word3)
                    message += prediction

                if (i == 14):
                    if first_word == "is" or first_word == "are" or first_word == "how" or first_word == "can" or first_word == "why":
                        message += "?"
                    else :
                        message += "."
                os.system('cls' if os.name == 'nt' else 'clear')
                print(message)
                prev_predicition = word1
                word1 = word2    
                word2 = word3                
                word3 = prediction

        @staticmethod
        def main():
            mode = 0 #0 = decrypt, 1 = auto complete
            mode2 = 3 #2 = bigram, 3 = trigram
            #download_nltk(reuters, "reuters.txt", rts) ta bort dream, corpus
            C = Corpus(["gutenberg.txt", "dream-en-open.xml.bz2", "reuters.txt"])

            if mode == 0: #decrypt med scorefunktion (hill climb)
                chars_in_corpus, words_in_corpus = C.corpus_stats()
                print('Characters in corpus: ', chars_in_corpus)
                print('Words in corpus: ', words_in_corpus)
                C.plot_corpus()
                text = rts.raw('training/5467') #'training/5467' 3038, training/5487' 545, training/2207 155/2
                Main.plot_message(text)
                D = Decrypt(text, C.frequencies, C.onegrams, C.bigrams, C.trigrams)
                D.message_frequency_table()
                decrypted_message, score = D.hill_climbing()
                Main.print_messages(text, decrypted_message, score)
                correct, mapping = D.evaluate_mapping()
                print('corret letters: ', correct)
                print('mapping: ', mapping)

            elif mode == 1: #auto complete med betingad sannolikhet 
                A = AutoComplete(C)

                if mode2 == 2:
                    user_input = input("Start a sentence using two words: ")
                    word1, word2 = user_input.split(" ", 1)

                    Main.SPEAK_ROBOT_BI(A, word1, word2)
                elif mode2 == 3:
                    user_input = input("Start a sentence using three words: ")
                    word1, word2, word3 = user_input.split(" ", 2)

                    Main.SPEAK_ROBOT_TRI(A, word1, word2, word3)

if __name__ == '__main__':
    Main.main()