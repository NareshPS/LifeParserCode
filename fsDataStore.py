'''
This class is used to store/retrieve in files.

Author          :                Naresh Pratap Singh
E-Mail          :                MAIL2NARESH@GMAIL.COM
Date            :                Jan 21 2011
Project Advisor :                Prof. Steven Skiena
'''

import debugTrace, errorStrings
import os

class fsDataStore:
    '''
        This class is used to store/retrieve in files.
    '''
    
    fsRoot                          = None
    fsDataDir                       = None
    longPathPrefix                  = '\\\\?\\'
    
    debugEnabled                    = False
    
    def __init__(self, fsRoot, debugEnabled = False):
        
        self.fsRoot                     = os.path.abspath(fsRoot)          
        
        self.debugEnabled               = debugEnabled
        
        self.debugTraceInst             = debugTrace.debugTrace(self.debugEnabled)
        self.errorStringsInst           = errorStrings.errorStrings()
        
    def doConnect(self):
        
        if os.path.exists(self.fsRoot) is False:
            self.debugTraceInst.doPrintTrace(self.errorStringsInst.getInvalidConfigError())
            return False
        
        return True
    
    def doDisconnect(self):
        
        self.fsRoot                     = None
        
    def doList(self):
        
        if self.fsDataDir is None:
            self.debugTraceInst.doPrintTrace(self.errorStringsInst.getEarlyRequestError())
            return None
        
        pathInfo                        = os.listdir(self.fsRoot)    
        dirList                         = []
        
        for item in pathInfo:
            if os.path.isdir(os.path.join(self.fsRoot, item)):
                dirList.append(item)
 
        return dirList
    
    def doSelect(self, dataDir):
        
        self.fsDataDir                  = dataDir   
        fullPath                        = os.path.join(self.fsRoot, self.fsDataDir)
        
        if os.path.exists(fullPath) is False:
            os.mkdir(fullPath)
            
    def doFetch(self, fileName):
        
        if self.fsDataDir is None:
            self.debugTraceInst.doPrintTrace(self.errorStringsInst.getEarlyRequestError())
            return None
        
        filePath                        = os.path.join(self.fsRoot, self.fsDataDir, fileName)
        
        if os.path.exists(filePath):
            #Read File If Exists
            fileHandle                  = open(filePath, 'r')
            fileContents                = fileHandle.readlines()
            fileHandle.close()
            
            return fileContents
        else:
            self.debugTraceInst.doPrintTrace(self.errorStringsInst.getResourceNotFoundError())
            
        return None
    
    def doSearch(self, pattern):
        
        if self.fsDataDir is None:
            self.debugTraceInst.doPrintTrace(self.errorStringsInst.getEarlyRequestError())
            return None
    
    def doUpdate(self, fileName, fileContents, delimitChar, shouldAppend = False):
        
        if self.fsDataDir is None:
            self.debugTraceInst.doPrintTrace(self.errorStringsInst.getEarlyRequestError())
            return None
        
        filePath                        = os.path.join(self.fsRoot, self.fsDataDir, fileName)
        filePath                        = self.longPathPrefix + filePath  
        
        if shouldAppend is True:
            #Open with append permissions
            fileHandle                  = open(filePath, 'a')
        else:
            #Create New File
            fileHandle                      = open(filePath, 'w')
        
        for line in fileContents:
            fileHandle.write(line)
            fileHandle.write(delimitChar)
            
        fileHandle.close()
            
        return None