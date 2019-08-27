from spellchecker import SpellChecker
import nltk

nltk.download("punkt")


def spelling_check(content):

    spell = SpellChecker()
    result = {}

    word_list = nltk.word_tokenize(content)

    misspelled = spell.unknown(word_list)

    error_list = []

    if len(misspelled) > 0:

        for word in misspelled:
            # print("[TYPO Found] -> "+ word)
            error_list.append("[TYPO Found] -> " + word + "<br>")

            # Reform to html output
            content = content.replace(word, "<u>" + word + "</u>")

        result["error_list"] = error_list
        result["report"] = content
        return result
    else:
        return None


def gen_report(filepath, filename_list):

    output = {}
    comment_report = ""
    html_report = """
    <style>
    u {text-decoration: #f00 wavy underline;}
    </style>
    """

    for f in filename_list:
        print(filepath + "/" + f)

        check_file = open(filepath + "/" + f, "r")
        result = spelling_check(check_file.read())

        comment_report += f + "<br>"
        for typo in result["error_list"]:
            comment_report += typo
        comment_report += "<br>"

        html_report += f + "<br><br>"
        html_report += result["report"]
        html_report += "<br><br><br>"

    output["comment_report"] = comment_report
    output["html_report"] = html_report

    return output


# print(spelling_check("this is a tast, which the tast would be failed"))
