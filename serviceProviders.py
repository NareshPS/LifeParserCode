'''
This class returns suitable hostname for requested service provider and specified protocol.

Author          :                Naresh Pratap Singh
E-Mail          :                MAIL2NARESH@GMAIL.COM
Date            :                Jan 18 2011
Project Advisor :                Prof. Steven Skiena
'''

import debugTrace
import errorStrings

class serviceProviders:
    
    debugEnabled        = False
    
    # debugTrace instance for trace logging.
    debugTraceInst      = None
    
    # errorStrings instance for fetching error message strings.
    errorStringsInst    = None
    
    hostNameDict        = {'GMAIL:IMAP': 'imap.googlemail.com'}
    
    def __init__(self, debugEnabled = False):
        self.debugEnabled       = debugEnabled
        
        self.debugTraceInst     = debugTrace.debugTrace(self.debugEnabled)
        self.errorStringsInst   = errorStrings.errorStrings()
    
    def getHostName(self, eMailProtocol, serviceProvider):
        
        if eMailProtocol is None or serviceProvider is None:
            self.debugTraceInst.doPrintTrace(self.errorStringsInst.getUnsupportedProtocolError())
        else:
            dictKey         = serviceProvider + ':' + eMailProtocol
            if self.hostNameDict.has_key(dictKey):
                return self.hostNameDict[ dictKey ]
            else:
                self.debugTraceInst.doPrintTrace(self.errorStringsInst.getUnsupportedProtocolError()) 
            
        return None
            
        