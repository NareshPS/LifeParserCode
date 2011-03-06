'''
This class takes care of fetching/storing data to/from a data provider.
To switch to a different data provider, include the provider module in this file
and add the entry in dataStoreDict. Make sure the relevant interfaces are exposed in
the new provider module.
  
Author          :                Naresh Pratap Singh
E-Mail          :                MAIL2NARESH@GMAIL.COM
Date            :                Jan 21 2011
Project Advisor :                Prof. Steven Skiena
    
'''

import fsDataStore
import debugTrace, errorStrings
import eMailParser

class repositoryIface:
    '''
        This class takes care of fetching/storing data to/from a data provider.
    '''
    
    dataStoreInst                       = None
    dataStoreType                       = None
    dataStoreRoot                       = None
    dataStoreName                       = None
    delimitChar                         = '|'
    
    dataStoreDict                       = {'FILE': [ fsDataStore, 'fsDataStore', {'CONNECT': 'doConnect', 'AUTH': 'doAuthenticate', 
                                                       'LIST_STORES': 'doListStores', 'LIST_ITEMS': 'doListItems', 'SELECT': 'doSelect', 'SEARCH': 'doSearch', 
                                                       'FETCH': 'doFetch', 'UPDATE': 'doUpdate', 'DISC': 'doDisconnect'} ]}
    
    searchActionList                    = [ 'NEW', 'CONT' ]
    currentDataIdList                   = None
    
    debugEnabled                        = False
    # debugTrace instance for trace logging.
    debugTraceInst                      = None
    
    # errorStrings instance for fetching error message strings.
    errorStringsInst                    = None
    
    def __init__(self, dataStoreType, dataStoreRoot, debugEnabled = False):
        
        self.dataStoreType              = dataStoreType
        self.dataStoreRoot              = dataStoreRoot
        
        self.debugEnabled               = debugEnabled
        
        self.debugTraceInst             = debugTrace.debugTrace(self.debugEnabled)
        self.errorStringsInst           = errorStrings.errorStrings()
        
    def doConnectToDataStore(self):
        
        if self.dataStoreInst is None:
            if self.dataStoreDict.has_key(self.dataStoreType):
                dataStoreMod            = self.dataStoreDict[ self.dataStoreType ][ 0 ]
                dataStoreClass          = self.dataStoreDict[ self.dataStoreType ][ 1 ]
                self.dataStoreInst      = dataStoreMod.__getattribute__(dataStoreClass)(self.dataStoreRoot, self.debugEnabled)
                connectMethod           = self.dataStoreDict[ self.dataStoreType ][ 2 ][ 'CONNECT' ]
                return getattr(self.dataStoreInst, connectMethod)()
            else:
                self.debugTraceInst.doPrintTrace(self.errorStringsInst.getUnsupportedProtocolError())
        else:
            self.debugTraceInst.doPrintTrace(self.errorStringsInst.getAlreadyConnectedError())
            
        return False
    
    def doDisconnect(self):
        
        if self.dataStoreInst is not None:
            discMethod                  = self.dataStoreDict[ self.dataStoreType ][ 2 ][ 'DISC' ]
            getattr(self.dataStoreInst, discMethod)
            self.dataStoreInst          = None
        else:
            self.debugTraceInst.doPrintTrace(self.errorStringsInst.getNotConnectedError())
            

    def doListStores(self):
        
        if self.dataStoreInst is None:
            self.debugTraceInst.doPrintTrace(self.errorStringsInst.getNotConnectedError())
            return None
        
        listMethod                      = self.dataStoreDict[ self.dataStoreType ][ 2 ][ 'LIST_STORES' ]
        
        return getattr(self.dataStoreInst, listMethod)()
        
    def doListItems(self):
        
        if self.dataStoreInst is None:
            self.debugTraceInst.doPrintTrace(self.errorStringsInst.getNotConnectedError())
            return None
        
        listMethod                      = self.dataStoreDict[ self.dataStoreType ][ 2 ][ 'LIST_ITEMS' ]
        
        return getattr(self.dataStoreInst, listMethod)()
        
    
    def doSelectDataStore(self, dataStoreName):
        
        if self.dataStoreInst is None:
            self.debugTraceInst.doPrintTrace(self.errorStringsInst.getNotConnectedError())
            return None
            
        self.dataStoreName              = dataStoreName
        
        selectMethod                    = self.dataStoreDict[ self.dataStoreType ][ 2 ][ 'SELECT' ]
        
        return getattr(self.dataStoreInst, selectMethod)(dataStoreName)
    
    def doFetchItems(self, itemList):
        
        '''
            Takes a list of items to fetch as input.
            Returns a dictionary of item and their contents.
            The name of items form the key.
        '''
        if self.dataStoreInst is None:
            self.debugTraceInst.doPrintTrace(self.errorStringsInst.getNotConnectedError())
            return None
        
        fetchMethod                     = self.dataStoreDict[ self.dataStoreType ][ 2 ][ 'FETCH' ]
        retDict                         = {}
        
        for itemName in itemList:
            retDict[ itemName ]         = getattr(self.dataStoreInst, fetchMethod)(itemName, self.delimitChar)
            
        return retDict

    def doFetchItem(self, itemName):
        
        if self.dataStoreInst is None:
            self.debugTraceInst.doPrintTrace(self.errorStringsInst.getNotConnectedError())
            return None
        
        fetchMethod                     = self.dataStoreDict[ self.dataStoreType ][ 2 ][ 'FETCH' ]
        
        return eMailParser.eMailParser().doConvertFileFormatToMessage(getattr(self.dataStoreInst, fetchMethod)(itemName, self.delimitChar))
    
    def doSearchItems(self, pattern):
        
        if self.dataStoreInst is None:
            self.debugTraceInst.doPrintTrace(self.errorStringsInst.getNotConnectedError())
            return None
        
        searchMethod                    = self.dataStoreDict[ self.dataStoreType ][ 2 ][ 'SEARCH' ]
        
        return getattr(self.dataStoreInst, searchMethod)(pattern)
    
    def doUpdateItem(self, itemName, itemContents):
        
        if self.dataStoreInst is None:
            self.debugTraceInst.doPrintTrace(self.errorStringsInst.getNotConnectedError())
            return None
        
        updateMethod                    = self.dataStoreDict[ self.dataStoreType ][ 2 ][ 'UPDATE' ]
        newContents                     = eMailParser.eMailParser().doConvertMessageToFileFormat(itemContents)
        
        return getattr(self.dataStoreInst, updateMethod)(itemName, newContents, self.delimitChar)
