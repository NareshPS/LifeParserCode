import daemon
import time
import logging

class LifeParserDaemon(daemon.Daemon):
    def __init__(self):
        daemon.Daemon.__init__(self, '/tmp/pidfile')

    def run(self):
        time.sleep(1000)
        print 'hi'


if __name__ == '__main__':
    fileName    =   'lifeparser.log'
    lPD = LifeParserDaemon()
    lPD.start()
    loggin.basicConfig(filename=fileName, level=logging.DEBUG)
    logging.debug('Go to log file')

