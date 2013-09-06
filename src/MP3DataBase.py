#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
'''
Created on 3 Sep 2013
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
        self.conn = sqlite3.connect("music.db")
        

    def _removeNonAscii(self, s): 
        '''
        Strip out non ascii characters from a string. SQLite gets unhappy if it finds chars that it can't read.
        '''
        return "".join(i for i in s if ord(i)<128)
    
    
    def _stripBadChars(self, s):
        '''
        Remove chars that could break a DB query.
        '''
        return re.sub(r'''['<>]''', '', self._removeNonAscii(str(s)))

        
    def createNewMusicTable(self):
        '''
        Create a new database in the music.db file
        '''
        cursor = self.conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS music(artist, album, track, bitrate, file)''')
        self.conn.commit()
    
        
    def insertTrack(self, music_track=MusicTrack()):
        '''
        Insert a track into our SQLite database
        '''
        artist   = self._stripBadChars(music_track.artist)
        album    = self._stripBadChars(music_track.album)
        track    = self._stripBadChars(music_track.name)
        filename = self._stripBadChars(music_track.filename)
        bitrate = music_track.bitrate
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO music VALUES (?, ?, ?, ?, ?)", (artist, album, track, bitrate, filename))
        self.conn.commit()

       
    def getDuplicates(self):
        '''
        Print out all the duplicates
        '''
        cursor = self.conn.cursor()
        cursor.execute("SELECT artist, album, track, bitrate, COUNT(file) AS filecount FROM music GROUP BY track ORDER BY COUNT(file),artist,track ASC")
        results = cursor.fetchall()
        return results
    
    
    def dropMusicTable(self):
        '''
        Drop the music table
        '''
        cursor = self.conn.cursor()
        cursor.execute('''DROP TABLE IF EXISTS music''')
        self.conn.commit()
        self.conn.close()
        
        