'''
This package defines class for fetching GMail feeds.

Author          :                Naresh Pratap Singh
E-Mail          :                MAIL2NARESH@GMAIL.COM
Date            :                Jan 18 2011
Project Advisor :                Prof. Steven Skiena
'''

import xoauth
import debugTrace
import errorStrings

class eMailService:

    userIdentity        = None
    oAuthConsumer       = None
    oAuthAccess         = None
    eMailProtocol       = None
    xoAuthString        = None
    debugEnabled        = False
    eMailProtocol       = None
    serviceProvider     = None
    
    # debugTrace instance for trace logging.
    debugTraceInst      = None
    
    # errorStrings instance for fetching error message strings.
    errorStringsInst    = None
    
    def __init__(self, userIdentity, oAuthConsumer, oAuthAccess, eMailProtocol, serviceProvider, debugEnabled = False):
        self.userIdentity       = userIdentity
        self.oAuthConsumer      = oAuthConsumer
        self.oAuthAccess        = oAuthAccess
        self.debugEnabled       = debugEnabled
        self.eMailProtocol      = eMailProtocol
        self.serviceProvider    = serviceProvider
        
        self.debugTraceInst     = debugTrace.debugTrace(self.debugEnabled)
        self.errorStringsInst   = errorStrings.errorStrings()
        
    def doGenerateXOAuthString(self):
        
        if self.oAuthAccess is not None and self.oAuthConsumer is not None:
            self.xoAuthString    = xoauth.GenerateXOauthString(
                                      self.oAuthConsumer, 
                                      self.oAuthAccess, 
                                      self.userIdentity, 
                                      self.eMailProtocol,
                                      None, None, None
                                      )
            
#self.debugTraceInst.doPrintTrace('xoAuthString: ' + self.xoAuthString, True)
            return self.xoAuthString
        else:
            self.debugTraceInst.doPrintTrace(self.errorStringsInst.getKeySecretMissingError())
        
        return None
    
    def getXOAuthString(self):
        return self.xoAuthString
