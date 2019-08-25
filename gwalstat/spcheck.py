from spellchecker import SpellChecker
import nltk

nltk.download("punkt")

def spelling_check(content):

    spell = SpellChecker()
    html_report = ""
    result = {}

    word_list = nltk.word_tokenize(content)

    misspelled = spell.unknown(word_list)

    error_list = []

    if len(misspelled) > 0:
  
        html_report += "<style> u {text-decoration: #f00 wavy underline;}</style>"


        for word in misspelled:
            # print("[TYPO Found] -> "+ word)
            error_list.append("[TYPO Found] -> " + word)

            # Reform to html output
            content = content.replace(word, "<u>" + word + "</u>")

        result["error_list"] = error_list
        result["report"] = html_report + content
        return result
    else:
        return None


#print(spelling_check("this is a tast, which the tast would be failed"))
