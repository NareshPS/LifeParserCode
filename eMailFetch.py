'''
Author          :                Naresh Pratap Singh
E-Mail          :                MAIL2NARESH@GMAIL.COM
Date            :                Jan 18 2011
Project Advisor :                Prof. Steven Skiena
'''

import eMailProtocolIface
import debugTrace
import errorStrings

class eMailFetch:
    '''
        This class is used to fetch eMails from a given service provider
        using the specified protocol.
    '''
    
    eMailProtocol       = None
    serviceProvider     = None
    xoAuthString        = None
    protocolIfaceInst   = None
    debugEnabled        = False
    mailboxList         = None
    currentMailbox      = None
    
    defMailCount        = 30
    
    mailReqTypeDict     = {'FULL': '(RFC822)', 'HEADER': '(RFC822.HEADER)', 'TEXT': '(RFC822.TEXT)'}
    mailReqDelim        = '|'
    
    # debugTrace instance for trace logging.
    debugTraceInst      = None
    
    # errorStrings instance for fetching error message strings.
    errorStringsInst    = None

    def __init__(self, eMailProtocol, serviceProvider, xoAuthString, debugEnabled = False):
        '''
        Constructor
        '''
        
        self.debugEnabled           = debugEnabled
        self.eMailProtocol          = eMailProtocol
        self.serviceProvider        = serviceProvider
        self.xoAuthString           = xoAuthString
        
        self.debugTraceInst         = debugTrace.debugTrace(self.debugEnabled)
        self.errorStringsInst       = errorStrings.errorStrings()
        
    def doConnect(self):
        
        self.protocolIfaceInst      = eMailProtocolIface.eMailProtocolIface(self.eMailProtocol, self.serviceProvider, self.debugEnabled)
        
        self.protocolIfaceInst.doConnectToProvider()  
        self.protocolIfaceInst.doXOAuthAuthentication(self.xoAuthString)     
        
    
    def doDisconnect(self):
        self.currentMailbox         = None
        self.mailboxList            = None
        self.protocolIfaceInst.doDisconnect()
        
    def getMailboxList(self, bForceFetch = False):

        if self.mailboxList is None or bForceFetch is True or self.doShouldUpateCache() is True:
            return self.protocolIfaceInst.getMailboxList()
        
        return None
        
    def doSelectMailbox(self, mailBox):
        
        self.protocolIfaceInst.doSelectMailbox(mailBox)
        self.currentMailbox         = mailBox
        
        
    def getMails(self, startIdx = 0, mailCount = 0, searchCrit = 'ALL', searchAction = 'CONT', reqType = 'FULL'):
        
        if mailCount == 0 or mailCount > 100:
            mailCount   = self.defMailCount
            
        reqList                     = reqType.split(self.mailReqDelim)
        
        resultTuples                = []
        
        for reqType in reqList:
            resultTuples.append(self.protocolIfaceInst.getMails(startIdx, mailCount, searchCrit, searchAction, self.getReqTypeFromFlags(reqType)))
            
        return resultTuples
    
    def getReqTypeFromFlags(self, reqType):
        
        if reqType == 'FULL':
            return '(RFC822)'
        elif reqType == 'TEXT':
            return '(RFC822.TEXT)'        
        elif reqType == 'HEADER':
            return '(RFC822.HEADER)'
        
        return '(RFC822.HEADER)'
    def doShouldUpateCache(self):    
        return False  
