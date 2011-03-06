'''
This library is used to print Debug messages.

Author          :                Naresh Pratap Singh
E-Mail          :                MAIL2NARESH@GMAIL.COM
Date            :                Jan 18 2011
Project Advisor :                Prof. Steven Skiena
'''
import traceback
import sys

class debugTrace:
    
    debugEnabled   = True
    
    def __init__(self, debugEnabled = True):
        self.debugEnabled       = debugEnabled
        
    def doPrintTrace(self, traceMessage, traceObj = None, plainPrint = False):
        if self.debugEnabled is True:
            print traceMessage
            
            if plainPrint is not True:
                print 'Stack Trace: ',
                
                if traceObj is not None:
                    print traceback.print_exc(traceObj)
                else:
                    print traceback.print_exc()
