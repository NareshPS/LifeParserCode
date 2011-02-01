'''
This modules is used to parse the email messages
supplied in string formats.

Author          :                Naresh Pratap Singh
E-Mail          :                MAIL2NARESH@GMAIL.COM
Date            :                Jan 22 2011
Project Advisor :                Prof. Steven Skiena
'''

import debugTrace, errorStrings
import re

class eMailParser:
    
    unwantedCharList                    = ['/', '<', '>']
    replacementChar                     = ' '
    headerSeparatorChar                 = ':'
    headerNameRegEx                     = '[a-zA-Z\-]+:'
    
    regExInst                           = None

    debugEnabled                        = False
    # debugTrace instance for trace logging.
    debugTraceInst                      = None
    
    # errorStrings instance for fetching error message strings.
    errorStringsInst                    = None
    
    def __init__(self, debugEnabled = False):
        self.debugEnabled               = debugEnabled

        self.debugTraceInst             = debugTrace.debugTrace(self.debugEnabled)
        self.errorStringsInst           = errorStrings.errorStrings()

        self.regExInst                  = re.compile(self.headerNameRegEx)
        
    def getMessageAsList(self, stringMessage):
       
        messageLines                    = stringMessage.splitlines()
        numLines                        = len(messageLines)
        outMessageLines                 = []
        initMatchObj                    = self.regExInst.match(messageLines[0])

        if messageLines and initMatchObj is not None and initMatchObj.start() is not None:
            outListIdx                  = 0
            for index in range(numLines):
                if len(messageLines[index]) != 0:
                    matchObj            = self.regExInst.match(messageLines[index])
                    if matchObj is not None and matchObj.start() is not None:
                        outMessageLines.append(messageLines[index])
                        outListIdx      += 1
                    else:
                        outMessageLines[outListIdx - 1]     += messageLines[index]

        else:
            self.debugTraceInst.doPrintTrace(self.errorStringsInst.getInvalidRequestError())
        
        return outMessageLines
    
    def doConvertMessageToFileFormat(self, messageContents):
     
        #Append the number of lines in the contents.
        newContents                     = []
        newContents.append(str(len(messageContents)))
        
        for line in messageContents:
            newContents.append(line)
        
        return newContents

    def doConvertFileFormatToMessage(self, fileContents):
        
        if fileContents:
            numLines                        = len(fileContents)
            newContents                     = []
        
            for index in range(1, numLines):
                if len(fileContents[ index ]) > 0:
                    newContents.append(fileContents[ index ])
            
        return newContents

    def getMessageAsDict(self, messageContents):

        messageDict                         = {}

        if messageContents:
            for entry in messageContents:
                matchObj                    = self.regExInst.match(entry)

                if matchObj is not None and matchObj.start() is not None and matchObj.start() == 0:
                    keyName                 = entry[matchObj.start():matchObj.end()-1]

                    if messageDict.has_key(keyName) is False:
                        messageDict[keyName]    = []

                    messageDict[keyName].append(entry[matchObj.end():])
                else:
                    self.debugTraceInst.doPrintTrace(self.errorStringsInst.getInvalidRequestError()+':'+entry)
        else:
            self.debugTraceInst.doPrintTrace(self.errorStringsInst.getInvalidRequestError())
        
        return messageDict
    
    def doCleanupForFilename(self, fileName):
        
        newName                         = fileName
        
        for char in self.unwantedCharList:
            newName                     = newName.replace(char, self.replacementChar)
            
        return newName.strip()
