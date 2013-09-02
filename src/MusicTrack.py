#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
'''
Created on 1 Sep 2013

@author: jchapman
'''

class MusicTrack(object):
    '''
    MusicTrack class is just a properties/object data structure class.
    '''
    def __init__(self):
        '''
        Constructor
        '''
        self.filename = None
        self.artist = None
        self.album  = None
        self.name   = None
        self.number = None
        self.year   = "0000"
        self.length = None
        self.bitrate = None
        self.comment = "http://linux-101.org"
        self.music_brainz_artist_id = None
        self.music_brainz_album_id  = None
        self.music_brainz_track_id  = None
        self.music_brainz_album_artist_id = None
        self.music_brainz_album_type = "unknown"
        
         
    def printMusicTrackData(self):
        '''
        Print all data we have for a track
        '''
        print("artist:  %s" % (self.artist))
        print("album:   %s" % (self.album))
        print("number:  %s" % (self.number))
        print("name:    %s" % (self.name))
        print("year:    %s" % (self.year))
        print("length:  %s" % (self.length))
        print("bitrate: %s" % (self.bitrate))
        print("comment: %s" % (self.comment))
        print("music_brainz_artist_id: %s" % (self.music_brainz_artist_id))
        print("music_brainz_album_id: %s" % (self.music_brainz_album_id))
        print("music_brainz_track_id: %s" % (self.music_brainz_track_id))
        print("music_brainz_album_artist_id: %s" % (self.music_brainz_album_artist_id))
        print("music_brainz_album_type: %s" % (self.music_brainz_album_type))
        print("")