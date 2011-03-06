
'''
This module computes the sentiments based on input text.
It reads a list of sentiment depicting words from Sentiment database
and computes the sentiment value.

Author          :                Naresh Pratap Singh
E-Mail          :                MAIL2NARESH@GMAIL.COM
Date            :                Jan 17 2011
Project Advisor :                Prof. Steven Skiena
'''

import siteConfig
import errorStrings, debugTrace
import sys
import re

class sentimentPackage:

    sentimentFile                = siteConfig.sentimentMainFile
    sentimentDelim               = '|'
    sentimentDict                = {}

    debugEnabled                 = False
    errorStringsInst             = None
    debugTraceInst               = None

    def __init__(self, debugEnabled = False):
        try:
            self.debugEnabled       = debugEnabled
            self.errorStringsInst   = errorStrings.errorStrings()
            self.debugTraceInst     = debugTrace.debugTrace(self.debugEnabled)

            hSentimentFile          = open(self.sentimentFile)

            for line in hSentimentFile.readlines():
                items               = line.split(self.sentimentDelim)

                self.sentimentDict [items [0]]  = (items [1], items [2], int(items[3]))

            hSentimentFile.close()
        except:
            hSentimentFile.close()
            self.debugTraceInst.doPrintTrace(self.errorStringsInst.getResourceNotFoundError(), sys.exc_info() [1])

    def constructRegEx(self, word):
        return r'\b' + word + r'\b'

    def countWords(self, word, message):
        regEx                       = self.constructRegEx(word)
        regObj                      = re.compile(regEx)
       
        wordList                    = regObj.findall(message)

        if wordList != None:
            return len(wordList)
        else:
            return 0

    def computeSentiment(self, message):
        
        positiveSentiment           = 0
        negativeSentiment           = 0

        for key in self.sentimentDict.keys():
            wordCount               = self.countWords(key, message)

            if self.sentimentDict [key][2] == -1:
                negativeSentiment   += wordCount
            else:
                positiveSentiment   += wordCount

        return (positiveSentiment, negativeSentiment)

if __name__ == "__main__":
    sent                = sentimentPackage(True)
    print sent.computeSentiment("hi This is a test program xoxo")
