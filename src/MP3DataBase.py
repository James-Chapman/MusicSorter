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
        self.conn = sqlite3.connect(":memory:")
        #self.conn = sqlite3.connect("music.db")
        

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
        
        
    def createNewArtistTable(self):
        '''
        Create a new database in the music.db file
        '''
        cursor = self.conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS artist(id INTEGER PRIMARY KEY AUTOINCREMENT, artist_name TEXT)''')
        self.conn.commit()
        
        
    def createNewAlbumTable(self):
        '''
        Create a new database in the music.db file
        '''
        cursor = self.conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS album(id INTEGER PRIMARY KEY AUTOINCREMENT, artist_id INT, album_name TEXT)''')
        self.conn.commit()


    def createNewTrackTable(self):
        '''
        Create a new database in the music.db file
        '''
        cursor = self.conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS track(id INTEGER PRIMARY KEY AUTOINCREMENT, artist_id INT, album_id INT, track_num INT, track_name TEXT, bitrate INT, filename TEXT)''')
        self.conn.commit()
        
        
    def dropAllTables(self):
        '''
        Drops all tables in the database
        '''
        cursor = self.conn.cursor()
        cursor.execute('''DROP TABLE IF EXISTS artist''')
        cursor.execute('''DROP TABLE IF EXISTS album''')
        cursor.execute('''DROP TABLE IF EXISTS track''')
        self.conn.commit()
        self.conn.close()


    def getArtistId(self, artist_name):
        '''
        Get the artist ID from the artist table
        '''
        cursor = self.conn.cursor()
        cursor.execute("SELECT id FROM artist WHERE artist_name = ?", (artist_name, ))
        result_row = cursor.fetchone()
        if not result_row:
            artist_id = self.insertArtist(artist_name)
        else:
            artist_id = result_row[0]
        return artist_id
            
            
    def insertArtist(self, artist_name):
        '''
        Insert artist into artist table and return id
        '''
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO artist (artist_name) VALUES (?)", (artist_name, ))
        return cursor.lastrowid
    
    
    def getAlbumId(self, artist_id, album_name):
        '''
        Get the album ID from the album table
        '''
        cursor = self.conn.cursor()
        cursor.execute("SELECT id FROM album WHERE artist_id = ? AND album_name = ?", (artist_id, album_name))
        result_row = cursor.fetchone()
        if not result_row:
            retval = self.insertAlbum(artist_id, album_name)
        else:
            retval = result_row[0]
        return retval
            
            
    def insertAlbum(self, artist_id, album_name):
        '''
        Insert album into album table and return id
        '''
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO album (album_name) VALUES (?)", (album_name, ))
        return cursor.lastrowid
        
    
    def insertTrack(self, music_track=MusicTrack()):
        '''
        Insert a track into our SQLite database
        '''
        artist   = self._stripBadChars(music_track.artist)
        album    = self._stripBadChars(music_track.album)
        track    = self._stripBadChars(music_track.name)
        number   = int(music_track.number)
        filename = self._stripBadChars(music_track.filename)
        bitrate = music_track.bitrate
        cursor = self.conn.cursor()
        artist_id = self.getArtistId(artist)
        album_id = self.getAlbumId(artist_id, album)

        cursor.execute("INSERT INTO track (artist_id, album_id, track_num, track_name, bitrate, filename) VALUES (?, ?, ?, ?, ?, ?)", (artist_id, album_id, number, track, bitrate, filename))
        self.conn.commit()
        
        
    def getDuplicates(self):
        '''
        Print out all the duplicates
        '''
        cursor = self.conn.cursor()
        cursor.execute("SELECT a1.artist_name, a2.album_name, t.track_num, t.track_name, t.bitrate, count(t.filename) FROM track AS t LEFT JOIN artist a1 ON a1.id = t.artist_id LEFT JOIN album a2 ON a2.id = t.album_id GROUP BY t.track_name ORDER BY COUNT(t.filename),a1.artist_name,t.track_name ASC")
        results = cursor.fetchall()
        return results
        for row in results:
            print("%s   %s   %s   %s   %s   %s" % (row[0], row[1], row[2], row[3], row[4], row[5]))
    
    

        
        