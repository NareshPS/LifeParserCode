'''
The mail module of the LifeLogger Project.

Author          :                Naresh Pratap Singh
E-Mail          :                MAIL2NARESH@GMAIL.COM
Date            :                Jan 17 2011
Project Advisor :                Prof. Steven Skiena
'''

import config
import xoauth
import eMailService, eMailFetch, eMailParser
import errorStrings, debugTrace
import repositoryIface
import email, email.header
import os
import dbConnect

#These values are provided by the service provider when registering the application.
consumerKey             = 'quine.algorithm.cs.sunysb.edu'
consumerSecret          = 'XWegMGJIOcnVYaigti7kLw21'
debugEnabled            = True
fileSuffix              = '.lifelogger'

def downloadFiles():
    debugEnabled        = True
    gMailFetch          = None
    gMailService        = None
    gMailXOAuthString   = None
    gMailProtocol       = 'IMAP'
    gMailProvider       = 'GMAIL'
    gMailRepoRoot       = '/home/naresh/LifeParser/Data/GMail_DataStore'
    gMailRepoType       = 'FILE'
    userIdentity        = config.user
    
    oAuthConsumer       = xoauth.OAuthEntity(consumerKey, consumerSecret)
    oAuthAccess         = xoauth.OAuthEntity(config.access_token[ 'key' ], config.access_token[ 'secret' ])
    
    gMailService        = eMailService.eMailService(userIdentity, oAuthConsumer, oAuthAccess, gMailProtocol, gMailProvider, debugEnabled)
    gMailXOAuthString   = gMailService.doGenerateXOAuthString()
    
    gMailRepoInst       = repositoryIface.repositoryIface(gMailRepoType, gMailRepoRoot, debugEnabled)
    gMailParserInst     = eMailParser.eMailParser() 
    
    errorStringsInst    = errorStrings.errorStrings()
    debugTraceInst      = debugTrace.debugTrace(debugEnabled)
    
    if gMailXOAuthString is not None:
        gMailFetch      = eMailFetch.eMailFetch(gMailProtocol, gMailProvider, gMailXOAuthString, debugEnabled)
        
        #Connect to GMAIL Service Provider.
        gMailFetch.doConnect()
        
        #Select "All Mail" mailbox.
        gMailFetch.doSelectMailbox('[Gmail]/All Mail')
        
        '''
            Connect to DataStore.
        '''     
        gMailRepoInst.doConnectToDataStore()
        gMailRepoInst.doSelectDataStore(config.user)
        
        '''
            Fetch the mails. 
            The result is a tuple (Total number of mails, Fetched mail count, Fetched mail list).
        '''
        result          = gMailFetch.getMails(0, 1, 'ALL', 'CONT', 'HEADER')[ 0 ]
        
        if result[ 0 ] != -1:
            totalMails      = result[ 0 ]
            
            remMails        = totalMails
            startIdx        = 0
            
            while remMails > 0:
                debugTraceInst.doPrintTrace('StartIdx: %d, remMails: %d'%(startIdx, remMails), True)
                result      = gMailFetch.getMails(startIdx, 0, 'ALL', 'CONT', 'HEADER')
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
                    entryName       = config.user + cleanMessageId + fileSuffix
                    
                    #Transform the message into a storage format.
                    gMailRepoInst.doUpdateItem(entryName, gMailParserInst.getMessageAsList(mailEntry[ 1 ]))
        else:
            debugTraceInst.doPrintTrace(errorStringsInst.getFetchFailedError())
        
        gMailRepoInst.doDisconnect()
        gMailFetch.doDisconnect()
        
    else:
        debugTraceInst.doPrintTrace(errorStringsInst.getXOAuthStringNoneError())
        
if __name__ == '__main__':
#downloadFiles()
    dbConn      = dbConnect.dbConnect(config.dbHost, config.dbUser, config.dbPass, config.dbName, True)
    print dbConn.fetchUserAccessToken()
