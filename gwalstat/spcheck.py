from spellchecker import SpellChecker
import nltk

nltk.download('punkt')

def spelling_check(content):

    spell = SpellChecker()

    word_list = nltk.word_tokenize(content)

    misspelled = spell.unknown(word_list)

    error_list = []
    if(len(misspelled) > 0):
        for word in misspelled:
            #print("[TYPO Found] -> "+ word)
            error_list.append("[TYPO Found] -> "+ word)
    return error_list

print(spelling_check("this is a hello woald tast, which the tast would be failed"))
