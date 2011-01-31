'''
This library is used to print Debug messages.

Author          :                Naresh Pratap Singh
E-Mail          :                MAIL2NARESH@GMAIL.COM
Date            :                Jan 18 2011
Project Advisor :                Prof. Steven Skiena
'''
import traceback

class debugTrace:
    
    debugEnabled   = True
    
    def __init__(self, debugEnabled = True):
        self.debugEnabled       = debugEnabled
        
    def doPrintTrace(self, traceMessage, plainPrint = False):
        if self.debugEnabled is True:
            print traceMessage
            
            if plainPrint is not True:
                print 'Stack Trace: ',
                print traceback.print_stack()
        