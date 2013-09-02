#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
'''
Created on 1 Sep 2013

@author: jchapman
'''
from MusicTrack import MusicTrack

#from mutagen.flac import FLAC
from mutagen.mp3 import MP3

import fnmatch
import os
import re
import shutil

class MP3MusicSorter(object):
    '''
    Class that does the sorting.
    '''
    def __init__(self, myos, dest_dir, directory_to_scan=None, logger=None):
        '''
        Constructor
        '''
        self.this_script = os.path.basename(__file__)
        self.this_class = self.__class__.__name__
        if myos.lower() == "windows":
            self.sep = "\\"
        else:
            self.sep = "/"
        self.music_dir_to_scan = directory_to_scan
        self.sorted_root_dir = dest_dir
        self.log = logger
        
    
    def iterateThroughFolder(self, directory_to_scan, pretend=True):
        '''
        Iterate through folder and perform id3 query against each file.
        '''
        self.music_dir_to_scan = directory_to_scan
        for root, dirnames, filenames in os.walk(self.music_dir_to_scan):
            for filename in fnmatch.filter(filenames, '*.mp3'):
                music_track = self.extractID3InfoFromFile(os.path.join(root, filename))
                #music_track.printMusicTrackData()
                if music_track.album == None:
                    self.log.logMsg('error', "%s has no album." % (music_track.filename))
                elif music_track.artist == None:
                    self.log.logMsg('error', "%s has no artist." % (music_track.filename))
                elif music_track.name == None:
                    self.log.logMsg('error', "%s has no name." % (music_track.filename))
                elif music_track.number == None:
                    self.log.logMsg('error', "%s has no track number." % (music_track.filename))
                else:
                    if pretend:
                        self.printMove(music_track)
                    if not pretend:
                        self.moveFile(music_track)


    def extractID3InfoFromFile(self, musicfile):
        '''
        @param musicfile: Filename of the file to parse for ID3 tag info. 
        Extract ID3 information from each file.
        @return: MusicTrack object
        '''
        try:
            f = MP3(musicfile)
        except Exception as e:
            self.log.logMsg('error', "processing: %s - %s" % (str(musicfile), str(e)))
        song = MusicTrack()
        song.filename = musicfile
        try:
            song.bitrate = f.info.bitrate / 1000
            song.length = f.info.length
            song.artist = f.tags.getall("TPE2")[0]
            if not song.artist:
                song.artist = f.tags.getall("TP2")[0]
            if not song.artist:
                song.artist = f.tags.getall("artist")[0]
            song.album = f.tags.getall("TALB")[0]
            if not song.album:
                song.album = f.tags.getall("TAL")[0]
            if not song.album:
                song.album = f.tags.getall("album")[0]
            name = str(f.tags.getall("TIT2")[0])
            if not name:
                name = str(f.tags.getall("TT2")[0])
            if not name:
                name = str(f.tags.getall("title")[0])
            song.name = re.sub(r'''[/{}<>%$£@:;#~*^¬]''', '_', name)
            number = str(f.tags.getall("TRCK")[0])
            if not number:
                number = str(f.tags.getall("TRK")[0])
            if not number:
                number = str(f.tags.getall("track")[0])
            song.number = number.split("/")[0].zfill(2)
            year = str(f.tags.getall("TDRC")[0])
            if year == "0000":
                year = str(f.tags.getall("TYER")[0])
            if year == "0000":
                year = str(f.tags.getall("TYE")[0])
            song.year = year.split("-")[0]
            #mb_info = f.tags.getall("TXXX")
        except Exception as e:
            self.log.logMsg('error', "Tag info missing from: %s - %s" % (str(musicfile), str(e)))
        try:
            song.music_brainz_artist_id = f.tags.getall("TXXX:ASIN")[0]
            song.music_brainz_album_artist_id = f.tags.getall("TXXX:MusicBrainz Album Artist Id")[0]
            song.music_brainz_album_id = f.tags.getall("TXXX:MusicBrainz Artist Id")[0]
            song.music_brainz_track_id = f.tags.getall("TXXX:ASIN")[0]
            song.music_brainz_album_type = f.tags.getall("TXXX:MusicBrainz Album Type")[0]
        except Exception as e:
            self.log.logMsg('warning', "Problem extracting musicbrainz data! - %s" % (str(e)))
        return song
        

    def moveFile(self, music_track):
        '''
        Moves the file to new destination based off information in the tag info
        @param music_track: 
        '''
        # /wherever/artist/album type/(year) album/01 - 320 - trackname.mp3
        destination_dir = self.setupDestinationDirString(music_track)
        final_file_dest = self.setupNewFilePathString(destination_dir, music_track)
        if not os.path.exists(destination_dir):
            try:
                os.makedirs(destination_dir)
            except Exception as e:
                self.log.logMsg('error', "Cannot create %s - %s" % (destination_dir, str(e)))
        self.log.logMsg('info', "%s --> %s" % (music_track.filename, final_file_dest))
        try:
            shutil.move(music_track.filename, final_file_dest) 
        except Exception as e:
            self.log.logMsg('error', "Error processing: %s - %s" % (music_track.filename, str(e)))
        
        
    def printMove(self, music_track):
        '''
        Pretends to move the file to new destination based off information in the tag info
        @param music_track: 
        '''
        # /wherever/artist/album type/(year) album/01 - 320 - trackname.mp3
        destination_dir = self.setupDestinationDirString(music_track)
        final_file_dest = self.setupNewFilePathString(destination_dir, music_track)
        self.log.logMsg('info', "%s --> %s" % (music_track.filename, final_file_dest), True)
        
        
    def setupDestinationDirString(self, music_track):
        '''
        Creates file path string based off the OS argument.
        @param music_track:  
        @return: destination_dir is the OS correct destination dir path
        '''
        destination_dir = "%s%s%s%s%s%s(%s) %s" % (self.sorted_root_dir, self.sep, music_track.artist, 
                                                   self.sep, music_track.music_brainz_album_type, 
                                                   self.sep, music_track.year, music_track.album)
        return destination_dir
        

    def setupNewFilePathString(self, destination_dir, music_track):
        '''
        Creates file name string based off the OS argument.
        @param destination_dir:
        @param music_track:  
        @return: final_file_path is the OS correct file path
        '''
        final_file_path = "%s%s%s - %s - %s.mp3" %(destination_dir, self.sep, music_track.number, 
                                                   music_track.bitrate, music_track.name)
        return final_file_path
    
    