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
import os, sys, traceback
import dbConnect
import time
import eMailProcessor

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

            try:
            
                while remMails > 0:
                    debugTraceInst.doPrintTrace('StartIdx: %d, remMails: %d'%(startIdx, remMails), sys.exc_info()[2], True)

                    result      = gMailFetch.getMails(startIdx, 0, searchAction, 'CONT', 'FULL')

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
                        gMailRepoInst.doUpdateItem(entryName, mailEntry[ 1 ])
            except:
                debugTraceInst.doPrintTrace(errorStringsInst.getFailedRequestError(), sys.exc_info()[2])
        else:
            debugTraceInst.doPrintTrace(errorStringsInst.getFetchFailedError())
        
        gMailRepoInst.doDisconnect()
        gMailFetch.doDisconnect()
        
    else:
        debugTraceInst.doPrintTrace(errorStringsInst.getXOAuthStringNoneError())

def handleWebRequest(emailId):
    
    if emailId is not None:
        dbConn          = dbConnect.dbConnect(siteConfig.dbHost, siteConfig.dbUser, siteConfig.dbPass, siteConfig.dbName, True)
        mailProcessor   = eMailProcessor.eMailProcessor(gMailRepoRoot, gMailRepoType, siteConfig.debugEnabled)
        dbConn.dbConnect()

        userInfo        = dbConn.fetchUserAccessToken(emailId)
        '''
            Set inProgress to True in database.
            Fetch Emails.
            Process EMails.
            Set inProgress to False in database.
        '''
        progressInfo        = dbConn.getProgressInfo(emailId)

        if progressInfo['inProgress'] == 0 or progressInfo['inProgress'] is None:
#           dbConn.setProgressInfo(emailId, True)
            strDateTime         = None

            if progressInfo['fetchDate'] is not None:
                dateTime        = progressInfo['fetchDate']
                month           = dateTime.strftime("%B")[0:3]
                year            = dateTime.strftime("%Y")
                day             = dateTime.strftime("%d")
                strDateTime     = day + '-' + month + '-' + year
            
            try:
#downloadMails(emailId, userInfo['oauthToken'], userInfo['oauthSecret'], strDateTime)
                mailProcessor.processEMails(emailId)
            except:
                debugTraceInst.doPrintTrace(errorStringsInst.getFailedRequestError(), sys.exc_info()[2])
            
#dbConn.setProgressInfo(emailId, False, 100)
            
        dbConn.dbDisconnect()

        
if __name__ == '__main__':
    
    '''
        Check if the request is triggered from the Web.
        If so, hand it over to appropriate handler.
    '''
    if len(sys.argv) >1:
        handleWebRequest(sys.argv[1])
    else:
        '''
            Issue Fetch requests every 24 hour.
        '''
        dbConn              = dbConnect.dbConnect(siteConfig.dbHost, siteConfig.dbUser, siteConfig.dbPass, siteConfig.dbName, True)
        mailProcessor       = eMailProcessor.eMailProcessor(gMailRepoRoot, gMailRepoType, siteConfig.debugEnabled)

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
                
                if progressInfo['inProgress'] == 0:
                    dbConn.setProgressInfo(userInfo['emailId'], True)
                    strDateTime         = None

                    if progressInfo['fetchDate'] is not None:
                        dateTime        = progressInfo['fetchDate']
                        month           = dateTime.strftime("%B")[0:3]
                        year            = dateTime.strftime("%Y")
                        day             = dateTime.strftime("%d")
                        strDateTime     = day + '-' + month + '-' + year
                   
                    try:
# downloadMails(userInfo['emailId'], userInfo['oauthToken'], userInfo['oauthSecret'], strDateTime)
                        mailProcessor.processEMails(userInfo['emailId'])
                    except:
                        debugTraceInst.doPrintTrace(errorStringsInst.getFailedRequestError())
                    
                    dbConn.setProgressInfo(userInfo['emailId'], False, 100)
            
            dbConn.dbDisconnect()
#time.sleep(gMailFetchDuration*60*60)        #Converting to seconds.
            break
