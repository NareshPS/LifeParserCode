import daemon

import time
import glob
import logging
import logging.handlers

class LifeParserDaemon(daemon.Daemon):
    logger              = None

    def __init__(self):
        self.logger     = logging.getLogger('LifeParserLogger')
        self.logger.setLevel(logging.DEBUG)
        handler         = logging.handlers.RotatingFileHandler('/tmp/lifeparser.log', maxBytes=10000000, backupCount=5)
        self.logger.addHandler(handler)
        daemon.Daemon.__init__(self, '/tmp/pidfile')

    def run(self):
#fileName        =   '/tmp/lifeparser.log'
#       logging.basicConfig(filename=fileName, level=logging.DEBUG)
#       logging.debug('Go to log file')
        self.logger.debug('Testing Log')
        time.sleep(1000)

if __name__ == '__main__':
    lPD = LifeParserDaemon()
    lPD.start()

