'''
This module provides interface for connection to a mail server using the specified protocol

Author          :                Naresh Pratap Singh
E-Mail          :                MAIL2NARESH@GMAIL.COM
Date            :                Jan 18 2011
Project Advisor :                Prof. Steven Skiena
'''

import imaplib
import serviceProviders
import debugTrace, errorStrings
import re

class eMailProtocolIface:
    
    eMailProtocol               = None
    serviceProvider             = None
    debugEnabled                = False
    
    #Service Provider Instance
    serviceProviderInst         = None 
    
    #Connection Handle
    connectionHandle            = None
    
    eMailMechanism              = 'XOAUTH'
    pyModuleDict                = {'IMAP': [ imaplib, {'CONNECT': 'IMAP4_SSL', 'AUTH': 'authenticate', 
                                                       'LIST': 'list', 'SELECT': 'select', 'SEARCH': 'search', 
                                                       'FETCH': 'fetch', 'CLOSE': 'close', 'LOGOUT': 'logout'} ]}
    
    searchActionList            = [ 'NEW', 'CONT' ]
    currentMsgIdList            = None
    
    # debugTrace instance for trace logging.
    debugTraceInst              = None
    
    # errorStrings instance for fetching error message strings.
    errorStringsInst            = None
    
    def __init__(self, eMailProtocol, serviceProvider, debugEnabled = False):
        
        self.eMailProtocol          = eMailProtocol
        self.serviceProvider        = serviceProvider
        self.debugEnabled           = debugEnabled
        
        self.serviceProviderInst    = serviceProviders.serviceProviders()
        
        self.debugTraceInst         = debugTrace.debugTrace(self.debugEnabled)
        self.errorStringsInst       = errorStrings.errorStrings()
        
    def doConnectToProvider(self):
        
        if self.connectionHandle is not None:
            self.debugTraceInst.doPrintTrace(self.errorStringsInst.getAlreadyConnectedError())
            return
        
        hostname                    = self.serviceProviderInst.getHostName(self.eMailProtocol, self.serviceProvider)
        connectMethod               = self.pyModuleDict[ self.eMailProtocol ][ 1 ][ 'CONNECT' ]
        self.connectionHandle       = self.pyModuleDict[ self.eMailProtocol ][ 0 ].__getattribute__(connectMethod)(hostname)
        
    def doDisconnect(self):
        
        if self.connectionHandle is not None:
            closeMethod             = self.pyModuleDict[ self.eMailProtocol ][ 1 ][ 'CLOSE' ]
            logoutMethod            = self.pyModuleDict[ self.eMailProtocol ][ 1 ][ 'LOGOUT' ]
            
            getattr(self.connectionHandle, closeMethod)()
            getattr(self.connectionHandle, logoutMethod)()
            
            #Reset Variables
            self.connectionHandle   = None
            self.currentMsgIdList   = None
        else:
            self.debugTraceInst.doPrintTrace(self.errorStringsInst.getNotConnectedError())
            
    
    def doXOAuthAuthentication(self, xoAuthString):
        
        authMethod                  = self.pyModuleDict[ self.eMailProtocol ][ 1 ][ 'AUTH' ]
        #self.connectionHandle.authenticate(self.eMailMechanism, lambda x: xoAuthString)
        getattr(self.connectionHandle, authMethod)(self.eMailMechanism, lambda x: xoAuthString)
        
    def getMailboxList(self):
        
        if self.connectionHandle is None:
            self.debugTraceInst.doPrintTrace(self.errorStringsInst.getNotConnectedError())
            return None
        
        listMethod                  = self.pyModuleDict[ self.eMailProtocol ][ 1 ][ 'LIST' ]
        mailboxList                 = getattr(self.connectionHandle, listMethod)()
        
        mailboxRegex                = re.compile('"(.*?)"')
        
        absMailboxList              = []
        
        for item in mailboxList[ 1 ]:
            regexOutput             = mailboxRegex.findall(item)
            mailboxName             = self.getAbsoluteMailbox(regexOutput[ 0 ], regexOutput[ 1 ])
            absMailboxList.append(mailboxName)
            
        return absMailboxList
        
    def doSelectMailbox(self, mailBox):
        
        if self.connectionHandle is not None:
            selectMethod            = self.pyModuleDict[ self.eMailProtocol ][ 1 ][ 'SELECT' ]
            getattr(self.connectionHandle, selectMethod)(mailBox)
        else:
            self.debugTraceInst.doPrintTrace(self.errorStringsInst.getNotConnectedError())
    
    def getAbsoluteMailbox(self, root, mailboxPath):
        '''
            Construct full path. Typically of the form "/[GMAIL]/All Mails".
            Strip the beginning "/" to get the path relative to "/".
            Return this Path.
        '''
        fullPath                    = root + mailboxPath
        
        if fullPath[ 0 ] == '/':
            return fullPath[1:]
        else:
            return fullPath
        
    def getMails(self, startIdx, mailCount, searchCrit, searchAction, reqType):
        
        errorTuple                  = (-1, 0, 0)
        
        if self.connectionHandle is None:
            self.debugTraceInst.doPrintTrace(self.errorStringsInst.getNotConnectedError())
            return None
        
        if self.doValidateSearchAction(searchAction) is False:
            return errorTuple
        
        if self.currentMsgIdList is None or searchAction == self.searchActionList[ 0 ]:         
            searchMethod                = self.pyModuleDict[ self.eMailProtocol ][ 1 ][ 'SEARCH' ]
            reqStatus, searchRes        = getattr(self.connectionHandle, searchMethod)(None, searchCrit)
            msgIdList                   = searchRes[ 0 ].split()            
            numMessages                 = len(msgIdList)
            self.currentMsgIdList       = (numMessages, msgIdList)
        
        endIdx                          = startIdx + mailCount
        msgIdStr                        = ','.join(self.currentMsgIdList[ 1 ][ startIdx:endIdx ])
        
        fetchMethod                     = self.pyModuleDict[ self.eMailProtocol ][ 1 ][ 'FETCH' ]
        reqStatus, mailData             = getattr(self.connectionHandle, fetchMethod)(msgIdStr, reqType)
        
        retMailData                     = []
        numEntries                      = len(mailData)
        
        
        for index in range(0, numEntries, 2):
            retMailData.append(mailData[ index ])
            
        return (len(self.currentMsgIdList[ 1 ]), len(mailData)/2, retMailData) 
    
    def doValidateSearchAction(self, searchAction):
        ''' 
            Validates the Search Action from the searchActionList
        '''
        try:
            index                   = self.searchActionList.index(searchAction)
        except ValueError:
            return False
        
        return True
    
    def getPyMailModuleItem(self):
        
        if self.eMailProtocol is not None and self.pyModuleDict.has_key(self.eMailProtocol) is True:
            return self.pyModuleDict[ self.eMailProtocol ]
        
        return None