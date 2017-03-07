#! python3

import os
import time
import re
import docx
import PyPDF2

def gives_file_text(fileObj):
    if str(fileObj).lower().endswith('.txt'):
        return str(fileObj.read())

    elif str(fileObj).lower().endswith('.docx'):
        doc = docx.Document(fileObj)
        fullText = []
        for para in doc.paragraphs:
            fullText.append(para.text)
            fileString = '\n'.join(fullText)
        return fileString

    elif str(fileObj).lower().endswith('.pdf'):
        pdfReader = PyPDF2.PdfFileReader(fileObj)
        fullText = []
        for pageNum in range(pdfReader.numPages):
            pageObj = pdfReader.getPage(pageNum)
            fullText.append(pageObj.extractText())
        fileString = '\n'.join(fullText)
        return fileString
    
    else:
        return 'Wrong file format!'


class CheckedText:
    def __init__(self, string):
        self.text = string
        self.lowercase_after_dot_wrong = self.checks_lowercase_after_dot(string)[0]
        self.lowercase_after_dot_probably_wrong = self.checks_lowercase_after_dot(string)[1]
        self.repeated_words = self.checks_repeated_words(string)
        self.multiple_spaces = self.checks_multiple_spaces(string)
        self.incorrect_words = self.checks_incorrect_words(string)
        self.missing_comma = self.checks_missing_comma(string)

    def checks_lowercase_after_dot(self, string):    
        """Checks for lowercase letters after dot in string."""
        exceptFileList = ['np.', 'Np.', 'etc.', 'zob.',
                          'br.','ryc.', 'dot.', 'woj.',
                          'r.', 'tzw.','prof.', 'dz.']

        dotLetterRegex = re.compile(r'(\w+\.)\s(\w+)')
        result = dotLetterRegex.findall(string)

        probablyWrong = []
        wrong = []

        for answerTuple in result:
            if answerTuple[1][0].islower() and answerTuple[0] in exceptFileList:
                probablyWrong.append(answerTuple)
            if answerTuple[1][0].islower() and answerTuple[0] not in exceptFileList:
                wrong.append(answerTuple)

        finalResult = []
        finalResult.append(wrong)
        finalResult.append(probablyWrong)
        return finalResult

    def checks_repeated_words(self, string):
        """Checks if any word is repeated."""
        repeatedRegex = re.compile(r'(\w+)\s(\w+)')
        oddWordsPairs = repeatedRegex.findall(string)

        result = []
        for answerTuple in oddWordsPairs:

            # This checks only pairs of every odd word in text with next one,
            # as the result file looks like this:
            # [('this', 'checks'), ('only', 'pairs'), ('in', 'tuples')]

            if answerTuple[0] == answerTuple[1]:
                result.append(answerTuple)

            # This checks also every even word in text with next one.
            # So it checks (see last example) 'checks' with 'only',
            # 'pairs' with 'in' untill the last tuple in list.

            index = oddWordsPairs.index(answerTuple)

            # This condition to stop "out of range" error at the end of the list.
            if oddWordsPairs.index(answerTuple) != len(oddWordsPairs) - 1:
                if answerTuple[1] == oddWordsPairs[index + 1][0]:
                    result.append((answerTuple[1], oddWordsPairs[index + 1][0]))
        return result

    def checks_multiple_spaces(self, string):
        """Checks if there are double or more spaces in text."""
        spacesRegex = re.compile(r'(\w+)( {2,})(\w+)')
        result = spacesRegex.findall(string)
        return result
    
    def checks_incorrect_words(self, string):
        """Checks if in text were used incorrect words."""
        # Creating list of incorrect words from an external file.
        wordsFile = open('incorrectWords.txt')
        wordsList = wordsFile.readlines()
        wrongWordsList = []
        for word in wordsList:
            if word.endswith('\n'):
                word = word[:-1]
            wrongWordsList.append(word)
        result = []
        for word in wrongWordsList:
            if word in string:
                result.append(word)
        return result
    
    def checks_missing_comma(self, string):
        """Checks if there is no missing coma before certain words."""
        commaWordsList = ['że', 'ale', 'lecz', 'zatem', 'toteż', 'więc']
        result = []
        for word in commaWordsList:
            commaRegex = re.compile(r'[^ ,]+ ' + word + ' ')
            regResult = commaRegex.findall(string)
            # If statement in the next line because for each word in list,
            # findall still returns an empty list if there is no result of
            # reg search.
            if len(regResult) != 0: result.append(regResult)   
        return result
