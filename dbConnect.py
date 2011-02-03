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
import siteConfig

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

    def __init__(self, hostName, userName, password, defDB, debugEnabled = False):
        self.debugEnabled       = debugEnabled
        self.hostName           = hostName
        self.userName           = userName
        self.password           = password
        self.defDB              = defDB

        self.debugTraceInst     = debugTrace.debugTrace(self.debugEnabled)
        self.errorStringsInst   = errorStrings.errorStrings()

    def dbConnect(self):
        try:
            self.mySQLConn      = MySQLdb.connect(self.hostName, self.userName, self.password, self.defDB)
            self.connCursor     = self.mySQLConn.cursor (MySQLdb.cursors.DictCursor)
        except MySQLdb.Error, e:
            self.debugTraceInst.doPrintTrace(self.errorStringsInst.getConnectionFailedError() + ':' + e.args[ 1 ])

    def dbDisconnect(self):
        self.connCursor.close ()
        self.mySQLConn.close ()

    def fetchUserAccessToken(self, userName):
        
        queryString = "select oauthToken, oauthSecret from records where emailId='" + userName + "'"
        self.connCursor.execute(queryString)

        row         = self.connCursor.fetchone ()

        if row == None:
            self.debugTraceInst.doPrintTrace(self.errorStringsInst.getFailedRequestError())

        return row

    def setProgressInfo(self, emailId, inProgress = False):
       
        queryString = "update records set fetchDate=current_date(), inProgress=" + str(inProgress) + " where emailId='" + emailId + "'"
        self.connCursor.execute(queryString)

    def getProgressInfo(self, emailId):
       
        queryString = "select fetchDate, inProgress from records where emailId='" + emailId + "'"
        self.connCursor.execute(queryString)
        
        row         = self.connCursor.fetchone ()

        if row == None:
            self.debugTraceInst.doPrintTrace(self.errorStringsInst.getFailedRequestError())

        return row

    def fetchAllAccessTokens(self):
        
        queryString = "select emailId, oauthToken, oauthSecret from records"
        self.connCursor.execute(queryString)

        rows        = self.connCursor.fetchall ()

        if rows == None:
            self.debugTraceInst.doPrintTrace(self.errorStringsInst.getFailedRequestError())
        
        return rows

if __name__ == '__main__':
    dbConn      = dbConnect(siteConfig.dbHost, siteConfig.dbUser, siteConfig.dbPass, siteConfig.dbName)
    print dbConn.fetchAllAccessTokens()
