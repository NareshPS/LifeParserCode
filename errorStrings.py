'''
This module contains a list of error strings used by the program.

Author          :                Naresh Pratap Singh
E-Mail          :                MAIL2NARESH@GMAIL.COM
Date            :                Jan 17 2011
Project Advisor :                Prof. Steven Skiena

'''

class errorStrings:
    
    errorUnsupportedProtocol        = 'Unsupported Protocol'
    errorKeySecretMissing           = 'Consumer/Access Key/Secret missing'
    errorNotConnected               = 'Not Connected'
    errorAlreadyConnected           = 'Already Connect. Please disconnect and try again.'
    errorFetchFailed                = 'Failed to fetch mails.'
    errorXOAuthStringNone           = 'XOAuth String is None'
    errorNotImplemented             = 'Function/Method/Module not Implemented'
    errorInvalidConfig              = 'Invalid Configuration Error'
    errorInvalidRequest             = 'Invalid Request.'
    errorEarlyRequest               = 'Missing initialization perhaps'
    errorResourceNotFound           = 'Resource Not Found'
    errorFailedRequest              = 'Specified Request Failed'
    errorConnectionFailed           = 'Connection Failed'
     
    def __init__(self):
        pass
    
    def getUnsupportedProtocolError(self):
        return self.errorUnsupportedProtocol
    
    def getKeySecretMissingError(self):
        return self.errorKeySecretMissing
    
    def getNotConnectedError(self):
        return self.errorNotConnected
    
    def getAlreadyConnectedError(self):
        return self.errorAlreadyConnected
    
    def getFetchFailedError(self):
        return self.errorFetchFailed
    
    def getXOAuthStringNoneError(self):
        return self.errorXOAuthStringNone
    
    def getNotImplementedError(self):
        return self.errorNotImplemented
    
    def getInvalidConfigError(self):
        return self.errorInvalidConfig
    
    def getInvalidRequestError(self):
        return self.errorInvalidRequest
    
    def getEarlyRequestError(self):
        return self.errorEarlyRequest
    
    def getResourceNotFoundError(self):
        return self.errorResourceNotFound

    def getFailedRequestError(self):
        return self.errorFailedRequest

    def getConnectionFailedError(self):
        return self.errorConnectionFailed
