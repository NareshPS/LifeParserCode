'''
The mail module of the LifeLogger Project.

Author          :                Naresh Pratap Singh
E-Mail          :                MAIL2NARESH@GMAIL.COM
Date            :                Jan 17 2011
Project Advisor :                Prof. Steven Skiena
'''

import siteConfig
import xoauth
import eMailService, eMailFetch, eMailParser
import errorStrings, debugTrace
import repositoryIface
import email, email.header
import os
import dbConnect
import time

#These values are provided by the service provider when registering the application.
gMailFetchDuration      = 24    
gMailProtocol           = 'IMAP'
gMailProvider           = 'GMAIL'
gMailRepoRoot           = siteConfig.repoRoot
gMailRepoType           = 'FILE'

errorStringsInst    = errorStrings.errorStrings()
debugTraceInst      = debugTrace.debugTrace(siteConfig.debugEnabled)

def downloadMails(emailId, accessTokenKey, accessTokenSecret, fetchDate):
    gMailFetch          = None
    gMailService        = None
    gMailXOAuthString   = None
    userIdentity        = emailId
    
    oAuthConsumer       = xoauth.OAuthEntity(siteConfig.consumerKey, siteConfig.consumerSecret)
    oAuthAccess         = xoauth.OAuthEntity(accessTokenKey, accessTokenSecret)
    
    gMailService        = eMailService.eMailService(userIdentity, oAuthConsumer, oAuthAccess, gMailProtocol, gMailProvider, siteConfig.debugEnabled)
    gMailXOAuthString   = gMailService.doGenerateXOAuthString()
    
    gMailRepoInst       = repositoryIface.repositoryIface(gMailRepoType, gMailRepoRoot, siteConfig.debugEnabled)
    gMailParserInst     = eMailParser.eMailParser() 
    
    
    if gMailXOAuthString is not None:
        gMailFetch      = eMailFetch.eMailFetch(gMailProtocol, gMailProvider, gMailXOAuthString, siteConfig.debugEnabled)
        
        #Connect to GMAIL Service Provider.
        gMailFetch.doConnect()
        
        #Select "All Mail" mailbox.
        gMailFetch.doSelectMailbox('[Gmail]/All Mail')
        
        '''
            Connect to DataStore.
        '''     
        gMailRepoInst.doConnectToDataStore()
        gMailRepoInst.doSelectDataStore(emailId)
        
        '''
            Fetch the mails. 
            The result is a tuple (Total number of mails, Fetched mail count, Fetched mail list).
        '''
        searchAction        = 'ALL'

        if fetchDate is not None:
            searchAction    = '(SINCE "' + fetchDate + '")'

        result              = gMailFetch.getMails(0, 1, searchAction, 'CONT', 'HEADER')[ 0 ]
        
        if result[ 0 ] != -1:
            totalMails      = result[ 0 ]
            
            remMails        = totalMails
            startIdx        = 0
            
            while remMails > 0:
                debugTraceInst.doPrintTrace('StartIdx: %d, remMails: %d'%(startIdx, remMails), True)

                result      = gMailFetch.getMails(startIdx, 0, searchAction, 'CONT', 'HEADER')

                remMails    -= result[ 0 ][ 1 ]
                startIdx    += result[ 0 ][ 1 ]
                
                '''
                    Write the fetched data to repository.
                    Currently, each mail header is stored in a separate file.
                    Only headers are being fetched and stored.
                '''
                for mailEntry in result[ 0 ][ 2 ]:
                    mailHeader      = email.message_from_string(mailEntry[ 1 ])
                    messageId       = email.header.decode_header(mailHeader[ 'Message-ID' ])[ 0 ][ 0 ]
                    cleanMessageId  = gMailParserInst.doCleanupForFilename(messageId)
                    entryName       = emailId + cleanMessageId + siteConfig.fileSuffix
                    
                    #Transform the message into a storage format.
                    gMailRepoInst.doUpdateItem(entryName, gMailParserInst.getMessageAsList(mailEntry[ 1 ]))
        else:
            debugTraceInst.doPrintTrace(errorStringsInst.getFetchFailedError())
        
        gMailRepoInst.doDisconnect()
        gMailFetch.doDisconnect()
        
    else:
        debugTraceInst.doPrintTrace(errorStringsInst.getXOAuthStringNoneError())

def dumpRequiredOutput(emailId, dateTime, msgHeader):
    '''
        This function extracts the interesting data from the emails
        and dumps it to output file.
    '''
    if os.access(siteConfig.analysisDir, os.F_OK) is False:
        os.mkdir(siteConfig.analysisDir)

    sentFilePath            = os.path.join(siteConfig.analysisDir, emailId + siteConfig.analysisSentSuffix)
    recvFilePath            = os.path.join(siteConfig.analysisDir, emailId + siteConfig.analysisRecvSuffix)

    hSentFile               = open(sentFilePath, 'a')
    hRecvFile               = open(recvFilePath, 'a')

    print msgHeader
    print dateTime

    strDateTime             = str(dateTime[1]) + '/' + str(dateTime[2]) + '/' \
                                + str(dateTime[0]) + '\t' + str(dateTime[3]) + ':' \
                                + str(dateTime[4]) + ':' + str(dateTime[5]) + '\n'

    if msgHeader['from'][0].find(emailId) != -1:
        hSentFile.write(strDateTime)
    else:
        hRecvFile.write(strDateTime)

    hSentFile.close()
    hRecvFile.close()

def processEMails(emailId):
    '''
        This function process eMails stored in the repository.
    '''
    gMailRepoInst       = repositoryIface.repositoryIface(gMailRepoType, gMailRepoRoot, siteConfig.debugEnabled)
    gMailParserInst     = eMailParser.eMailParser() 
        
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
    gMailRepoInst.doConnectToDataStore()
    gMailRepoInst.doSelectDataStore(emailId)

    itemList            = gMailRepoInst.doListItems()

    for item in itemList:
        msgHeader   = gMailParserInst.getMessageAsDict(gMailRepoInst.doFetchItem(item))
        dumpRequiredOutput(emailId, email.utils.parsedate_tz(msgHeader['date'][0]), msgHeader)
        break
        
        
if __name__ == '__main__':
    '''
        Issue Fetch requests every 2 hour.
    '''
    dbConn              = dbConnect.dbConnect(siteConfig.dbHost, siteConfig.dbUser, siteConfig.dbPass, siteConfig.dbName, True)

    while 1:
        dbConn.dbConnect()
        userInfoList        = dbConn.fetchAllAccessTokens()

        print 'Download Started at: %d'%(time.time())

        for userInfo in userInfoList:
            '''
                Set inProgress to True in database.
                Fetch Emails.
                Process EMails.
                Set inProgress to False in database.
            '''
            progressInfo        = dbConn.getProgressInfo(userInfo['emailId'])
            dbConn.setProgressInfo(userInfo['emailId'], True)
            strDateTime         = None

            if progressInfo['fetchDate'] is not None:
                dateTime        = progressInfo['fetchDate']
                month           = dateTime.strftime("%B")[0:3]
                year            = dateTime.strftime("%Y")
                day             = dateTime.strftime("%d")
                strDateTime     = day + '-' + month + '-' + year
            
#downloadMails(userInfo['emailId'], userInfo['oauthToken'], userInfo['oauthSecret'], strDateTime)
                processEMails(userInfo['emailId'])
            
            dbConn.setProgressInfo(userInfo['emailId'], False)
        
        dbConn.dbDisconnect()
        break
#time.sleep(gMailFetchDuration*60*60)        #Converting to seconds.
        break
