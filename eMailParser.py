'''
This modules is used to parse the email messages
supplied in string formats.

Author          :                Naresh Pratap Singh
E-Mail          :                MAIL2NARESH@GMAIL.COM
Date            :                Jan 22 2011
Project Advisor :                Prof. Steven Skiena
'''

class eMailParser:
    
    unwantedCharList                    = ['/', '<', '>']
    replacementChar                     = ' '
    def __init__(self):
        pass
        
    def getMessageAsList(self, stringMessage):
        
        messageLines                    = stringMessage.splitlines()
        outMessageLines                 = []
        
        for line in messageLines:
            
            if len(line) != 0:
                outMessageLines.append(line)
        
        return outMessageLines
    
    def doConvertMessageToFileFormat(self, messageContents):
        
        #Append the number of lines in the contents.
        newContents                     = []
        newContents.append(str(len(messageContents)))
        
        for line in messageContents:
            newContents.append(line)
            
        return newContents
    
    def doCleanupForFilename(self, fileName):
        
        newName                         = fileName
        
        for char in self.unwantedCharList:
            newName                     = newName.replace(char, self.replacementChar)
            
        return newName.strip()
        
        