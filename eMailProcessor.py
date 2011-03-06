'''
The mail module of the Life Parser Project.

Author          :                Naresh Pratap Singh
E-Mail          :                MAIL2NARESH@GMAIL.COM
Date            :                Jan 17 2011
Project Advisor :                Prof. Steven Skiena
'''
import errorStrings, debugTrace
import repositoryIface
import eMailParser
import siteConfig
import email
import os
import re
import sentimentPackage

class eMailProcessor:

    repoRoot                        = None
    repoType                        = None
    eMailRegEx                      = '[A-Z0-9-_.%+]+@[A-Z0-9.-]+\.[A-Z]{2,4}'

    eMailRegExInst                  = None

    # Enables debug traces for this module if set to True.
    debugEnabled                    = False

    errorStringsInst                = None
    debugTraceInst                  = None

    def __init__(self, repoRoot, repoType, debugEnabled = False):

        self.repoRoot               = repoRoot
        self.repoType               = repoType

        self.debugEnabled           = debugEnabled

        self.eMailRegExInst         = re.compile(self.eMailRegEx, re.IGNORECASE)
    
        self.errorStringsInst       = errorStrings.errorStrings()
        self.debugTraceInst         = debugTrace.debugTrace(self.debugEnabled)


    def processEMails(self, emailId):
        '''
            This function process eMails stored in the repository.
        '''
        repoInst                    = repositoryIface.repositoryIface(self.repoType, self.repoRoot, self.debugEnabled)
        mailParser                  = eMailParser.eMailParser() 
            
        '''
            Read the stored emails. Following steps are required:
            Connect to DataStore.
            Select user's DataStore.
            Open the output file in analysis directory.
            Enumerate all items.
            Fetch the items in a dictionary.
            Store the required data items.
            Disaonnect from datastore.
            Close the output file.
        '''     
        repoInst.doConnectToDataStore()
        repoInst.doSelectDataStore(emailId)
        
        if os.access(siteConfig.analysisDir, os.F_OK) is False:
            os.mkdir(siteConfig.analysisDir)

        sentFilePath                = os.path.join(siteConfig.analysisDir, emailId + siteConfig.analysisSentSuffix)
        recvFilePath                = os.path.join(siteConfig.analysisDir, emailId + siteConfig.analysisRecvSuffix)

        hSentFile                   = open(sentFilePath, 'w')
        hRecvFile                   = open(recvFilePath, 'w')
        sentimentInst               = sentimentPackage.sentimentPackage(self.debugEnabled)

        itemList                    = repoInst.doListItems()
        
        msgDict                     = mailParser.getMessageAsDict(repoInst.doFetchItem(itemList[0]))

        mailCount                   = len(itemList)

        for item in itemList:
            print 'Remaining ' + str(mailCount)
            try:
                msgDict                 = mailParser.getMessageAsDict(repoInst.doFetchItem(item))
                dirtyDate               = msgDict['Date'][0].replace("=20", ' ')
                commaIndex              = dirtyDate.find(',')
                goodDate                = dirtyDate[:commaIndex].strip() + dirtyDate[commaIndex:]
                sentimentValue          = sentimentInst.computeSentiment(msgDict ['Payload'])
                self.dumpRequiredOutput(hSentFile, hRecvFile, emailId, email.utils.parsedate_tz(goodDate), msgDict, sentimentValue [0], sentimentValue [1])
            except KeyError:
               self.debugTraceInst.doPrintTrace(errorStringsInst.getDictKeyMissingError(), sys.exc_info()[2])

            mailCount                   -= 1
        
        hSentFile.close()
        hRecvFile.close()


    def dumpRequiredOutput(self, hSentFile, hRecvFile, emailId, dateTime, msgHeader, positiveSentiment, negativeSentiment):
        '''
            This function extracts the interesting data from the emails
            and dumps it to output file.
        '''
        strDateTime                 = '%d/%d/%d\t%d:%d:%d'% (dateTime[1], dateTime[2], dateTime[0], dateTime[3], dateTime[4], dateTime[5])
        mailList                    = ''

        if msgHeader['From'][0].find(emailId) != -1:
            if msgHeader.has_key('To'):
                toList                  = self.eMailRegExInst.findall(msgHeader['To'][0])
                mailList                = '\t' + ' '.join(set(toList)) + '\t' + str(positiveSentiment) + '\t' + str(negativeSentiment)

            hSentFile.write(strDateTime + mailList + '\n') 
        else:
            if msgHeader.has_key('From'):
                fromList                = self.eMailRegExInst.findall(msgHeader['From'][0])
                mailList                = '\t' + ' '.join(set(fromList)) + '\t' + str(positiveSentiment) + '\t' + str(negativeSentiment)

            hRecvFile.write(strDateTime + mailList + '\n')
