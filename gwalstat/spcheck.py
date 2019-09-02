from spellchecker import SpellChecker
import nltk


class SpCheck:
    def __init__(self, *args, **kwargs):
        nltk.download("punkt")
        self.spell = SpellChecker()

    def spelling_check(self, content):

        result = {}

        word_list = nltk.word_tokenize(content)

        misspelled = self.spell.unknown(word_list)

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

    def gen_report(self, filepath, filename_list):

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
            result = self.spelling_check(check_file.read())

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


# sp = SpCheck()
# print(sp.spelling_check("this is a tast, which the tast would be failed"))
