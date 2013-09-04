'''
Created on 4 Sep 2013

@author: jchapman
'''

class MP3Exception(Exception):
    '''
    Exception to be raised when we error.
    '''


    def __init__(self, error_message):
        '''
        Constructor
        '''
        self.error_message = error_message
        
    def __str__(self):
        '''
        String representation of object
        '''
        return self.error_message