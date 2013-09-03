'''
Created on 3 Sep 2013

@author: jchapman
'''
from MusicTrack import MusicTrack
import re
import sqlite3


class MP3DataBase(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.conn = sqlite3.connect(":memory:")
        

        
    def createNewMusicTable(self):
        '''
        Create a new database in the music.db file
        '''
        cursor = self.conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS music(artist, album, track, bitrate, file)''')
        self.conn.commit()
        #self.conn.close()
        
        
    def removeNonAscii(self, s): return "".join(i for i in s if ord(i)<128)
        
    def insertTrack(self, music_track=MusicTrack()):
        '''
        Insert a track into our SQLite database
        '''
        
        artist   = re.sub(r'''['<>]''', '_', self.removeNonAscii(str(music_track.artist)))
        album    = re.sub(r'''['<>]''', '_', self.removeNonAscii(str(music_track.album)))
        track    = re.sub(r'''['<>]''', '_', self.removeNonAscii(str(music_track.name)))
        filename = re.sub(r'''['<>]''', '_', self.removeNonAscii(str(music_track.filename)))
        bitrate = music_track.bitrate
        #filename = re.sub(r'[^\x00-\x7F]', '_', music_track.filename)
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO music VALUES ('%s','%s','%s','%s', '%s')" % (artist, album, track, bitrate, filename))
        self.conn.commit()
        #self.conn.close()

       
    def getDuplicates(self):
        '''
        Print out all the duplicates
        '''
        cursor = self.conn.cursor()
        cursor.execute("SELECT artist, album, track, bitrate, file FROM music")
        results = cursor.fetchall()
        #self.conn.close()
        #print results
        for row in results:
            print row
        return results
    
    
    def dropMusicTable(self):
        '''
        Drop the music table
        '''
        cursor = self.conn.cursor()
        cursor.execute('''DROP TABLE IF EXISTS music''')
        self.conn.commit()
        self.conn.close()
        
        