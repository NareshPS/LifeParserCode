'''
This Library implements routines to connect and perform operations
on a SQL database.

Author          :                Naresh Pratap Singh
E-Mail          :                MAIL2NARESH@GMAIL.COM
Date            :                Jan 18 2011
Project Advisor :                Prof. Steven Skiena
'''
import MySQLdb
import debugTrace
import errorStrings

class dbConnect:

    mySQLConn                   = None
    connCursor                  = None
    hostName                    = None
    userName                    = None
    password                    = None
    defDB                       = None

    debugEnabled                = False

    debugTraceInst              = None
    errorStringsInst            = None

    def dbConnect(self, hostName, userName, password, defDB, debugEnabled = False):
        self.debugEnabled       = debugEnabled
        self.hostName           = hostName
        self.userName           = userName
        self.password           = password
        self.defDB              = defDB

        self.debugTraceInst     = debugTrace.debugTrace(self.debugEnabled)
        self.errorStringsInst   = errorStrings.errorStrings()

        try:
            self.mySQLConn          = MySQLdb.connect(hostName, userName, password, defDB)
            self.connCursor     = self.mySQLConn.cursor (MySQLdb.cursors.DictCursor)
        except MySQLdb.Error, e:
            self.debugTraceInst.doPrintTrace(self.errorStringsInst.getConnectionFailedError() + ':' + e.args[ 1 ])

    def dbDisconnect(self):
        self.connCursor.close ()
        self.mySQLConn.close ()

    def fetchUserAccessToken(self, userName):
        
        queryString = "select oauthToken, oauthSecret from records where emailId='" + userName + "'"

        row         = self.connCursor.fetchone ()

        if row == None:
            self.debugTraceInst.doPrintTrace(self.errorStringsInst.getFailedRequestError())

        return row

    def fetchAllAccessTokens(self):
        
        queryString = "select oauthToken, oauthSecret from records"

        rows        = self.connCursor.fetchall ()

        if row == None:
            self.debugTraceInst.doPrintTrace(self.errorStringsInst.getFailedRequestError())
        
        return rows

if __name__ == '__main__':
    print 'hi'
