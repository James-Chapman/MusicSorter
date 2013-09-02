'''
Created on 1 Sep 2013

@author: jchapman
'''
import logging

class MP3Logger:
    '''
    Logging class, sets up a logger and logs messages to logfile with level. Warning and above
    will always be printed to screen. Below that log messages are optional and default to not print.
    '''
    def __init__(self, name, level, logfile):
        '''
        Constructor
        '''
        self.logger = logging.getLogger(name)
        handler = logging.FileHandler(logfile)
        formatter = logging.Formatter('%(asctime)s %(name)s %(processName)s %(process)d %(levelname)s %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        if level == 'debug':
            self.logger.setLevel(logging.DEBUG)
        if level == 'info':
            self.logger.setLevel(logging.INFO)
        if level == 'warning':
            self.logger.setLevel(logging.WARNING)
        if level == 'error':
            self.logger.setLevel(logging.ERROR)
        if level == 'critical':
            self.logger.setLevel(logging.CRITICAL)
        

    def logMsg(self, level, message, print_it=False):
        """
        Takes message and log level as parameters. Log message to appropriate log level.
        """
        if level == 'debug':
            self.logger.debug(message)
            if print_it:
                print("[%s] %s" % (level.upper(), message))
        if level == 'info':
            self.logger.info(message)
            if print_it:
                print("[%s] %s" % (level.upper(), message))
        if level == 'warning':
            self.logger.warning(message)
            print("[%s] %s" % (level.upper(), message))
        if level == 'error':
            self.logger.error(message)
            print("[%s] %s" % (level.upper(), message))
        if level == 'critical':
            self.logger.critical(message)
            print("[%s] %s" % (level.upper(), message))


    def closeLog(self):
        """
        What it says on the tin.
        """
        logging.shutdown()
