#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
'''
Created on 1 Sep 2013
'''

from MP3DataBase import MP3DataBase
from MusicTrack import MusicTrack
from mutagen.easyid3 import EasyID3
from mutagen.id3 import COMM, ID3, TPE2
from mutagen.mp3 import MP3
import MP3Exception
import fnmatch
import os
import re
import shutil
import sys

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
        self.PRINT_DEBUG = False
        
        
    def _extractBitrate(self, mp3_audio_file):
        '''
        Extract bitrate and length from audio file.
        '''
        bitrate = mp3_audio_file.info.bitrate / 1000
        self.log.logMsg('debug', "Bitrate: %s" % (bitrate), self.PRINT_DEBUG)
        return bitrate
    
    
    def _extractLength(self, mp3_audio_file):
        '''
        Extract bitrate and length from audio file.
        '''
        length = mp3_audio_file.info.length
        self.log.logMsg('debug', "Length: %s" % (length), self.PRINT_DEBUG)
        return length

    
    def _extractTagDataFromFile(self, tags, mp3_audio_file):
        '''
        Searches for tags in an MP3() file.
        '''
        for tag in tags:
            retval = mp3_audio_file.tags.getall(tag)
            if retval:
                self.log.logMsg('debug', "Tag found: %s - %s" % (tag, retval[0]), self.PRINT_DEBUG)
                return retval[0]
        #print(mp3_audio_file.tags.getall("TXXX"))
        return None
    
    
    def _extractArtist(self, mp3_audio_file):
        '''
        Extract Artist from tags.
        '''
        retval = self._extractTagDataFromFile(["TPE2","TPE1","TP2","TP1"], mp3_audio_file)
        self.log.logMsg('debug', "Artist: %s" % (retval), self.PRINT_DEBUG)
        return retval
        
        
    def _extractAlbum(self, mp3_audio_file):
        '''
        Extract Album Name from tags.
        '''
        retval = self._extractTagDataFromFile(["TALB","TAL","album"], mp3_audio_file)
        self.log.logMsg('debug', "Album: %s" % (retval), self.PRINT_DEBUG)
        return retval

        
    def _extractTitle(self, mp3_audio_file):
        '''
        Extract Track Title from tags.
        '''
        retval = self._extractTagDataFromFile(["TIT2","TT2","title"], mp3_audio_file)
        self.log.logMsg('debug', "Title: %s" % (retval), self.PRINT_DEBUG)
        return retval
        
        
    def _extractTrackNumber(self, mp3_audio_file):
        '''
        Extract Track Number from tags.
        '''
        retval = self._extractTagDataFromFile(["TRCK","TRK","track"], mp3_audio_file)
        if not retval:
            retval = "00/00"
        retval = str(retval).split('/')[0].zfill(2)
        self.log.logMsg('debug', "Track: %s" % (retval), self.PRINT_DEBUG)
        return retval
        
        
    def _extractYear(self, mp3_audio_file):
        '''
        Extract Release Year from tags.
        '''
        retval = self._extractTagDataFromFile(["TDRC","TYER","TYE"], mp3_audio_file)
        if not retval:
            retval = "0000-00-00"
        retval = str(retval).split('-')[0]
        self.log.logMsg('debug', "Year: %s" % (retval), self.PRINT_DEBUG)
        return retval
            
    
    def _extractMusicBrainzAlbumType(self, mp3_audio_file):
        '''
        Extract MusicBrainz info from tags.
        '''
        retval = self._extractTagDataFromFile(["TXXX:MusicBrainz Album Type"], mp3_audio_file)
        if not retval:
            retval = "unknown"
        self.log.logMsg('debug', "MusicBrainz Album Type: %s" % (retval), self.PRINT_DEBUG)
        return retval
    
    
    def _setupDestinationDirString(self, music_track):
        '''
        Creates file path string based off the OS argument.
        @param music_track:  
        @return: destination_dir is the OS correct destination dir path
        '''
        destination_dir = "%s%s%s%s%s%s(%s) %s" % (self.sorted_root_dir, self.sep,
                                                   self._subBadChars(str(music_track.artist)), self.sep, 
                                                   music_track.music_brainz_album_type, self.sep,
                                                   music_track.year, self._stripBadChars(str(music_track.album)))
        self.log.logMsg('debug', "Destination dir: %s" % (destination_dir), self.PRINT_DEBUG)
        return destination_dir
        

    def _setupNewFilePathString(self, destination_dir, music_track):
        '''
        Creates file name string based off the OS argument.
        @param destination_dir:
        @param music_track:  
        @return: final_file_path is the OS correct file path
        '''
        final_file_path = "%s%s%s - %s - %s.mp3" %(destination_dir, self.sep, music_track.number, 
                                                   music_track.bitrate, self._subBadChars(str(music_track.name)))
        self.log.logMsg('debug', "Final file path: %s" % (final_file_path), self.PRINT_DEBUG)
        return final_file_path
    
    
    def _checkForMissingInfo(self, music_track):
        '''
        Check music track for missing fields.
        '''
        anything_missing = False
        if music_track.album == None: anything_missing = True
        if music_track.artist == None: anything_missing = True
        if music_track.name == None: anything_missing = True
        if music_track.number == None: anything_missing = True
        return anything_missing
    
    
    def _removeNonAscii(self, str_in): 
        '''
        Strip out non ascii characters from a string. SQLite gets unhappy if it finds chars that it can't read.
        '''
        return "".join(char for char in str_in if ord(char)<128)
    
    
    def _stripBadChars(self, str_in):
        '''
        Remove chars that could break a DB query.
        '''
        return re.sub(r'''['<>;{}~*&#|/]''', '', str_in)
    
    
    def _subBadChars(self, str_in):
        '''
        Remove chars that could break a DB query.
        '''
        return re.sub(r'''['<>;{}~*&#|/]''', '_', str_in)
    
        
    def iterateThroughFolder(self, directory_to_scan, action="duplicates"):
        '''
        Iterate through folder and perform id3 query against each file.
        '''
        self.music_dir_to_scan = directory_to_scan
        if action == "getDuplicates":
            self.db = MP3DataBase()
            self.db.createNewMusicTable()
        for root, dirnames, filenames in os.walk(self.music_dir_to_scan):
            for filename in fnmatch.filter(filenames, '*.mp3'):
                music_track = self.extractID3InfoFromFile(os.path.join(root, filename))
                self.addComment(music_track.filename)
                if action == "upgradeTags":
                    self.updateTagsToV24(music_track.filename)
                    sys.exit()
                missing_fields = self._checkForMissingInfo(music_track)
                if not missing_fields:
                    if action == "pretend":
                        self.printMove(music_track)
                    elif action == "restructure":
                        #self.updateTagsToV24(music_track)
                        #self.addComment(music_track)
                        self.moveFile(music_track)
                    elif action == "getDuplicates":
                        self.db.insertTrack(music_track)
                    else:
                        raise MP3Exception("Unrecognised action parameter in %s.iterateThroughFolder()" % (self.this_class))
                else:
                    self.log.logMsg('error', "Skipping file because key info is missing: %s" % (music_track.filename))
        if action == "getDuplicates":
            db_data = self.db.getDuplicates()
            for row in db_data:
                if int(row[4]) > 1:
                    print(str(row[4]).ljust(6) + str(row[0]).ljust(40) + str(row[2]).ljust(40))
            self.db.dropMusicTable()
        

    def extractID3InfoFromFile(self, musicfile):
        '''
        @param musicfile: Filename of the file to parse for ID3 tag info. 
        Extract ID3 information from each file.
        @return: MusicTrack object
        '''
        mp3_audio_file = None
        try:
            mp3_audio_file = MP3(musicfile)
        except Exception as e:
            self.log.logMsg('error', "fail: %s - %s" % (str(musicfile), str(e)))
        music_track = MusicTrack()
        music_track.filename = musicfile
        music_track.bitrate  = self._extractBitrate(mp3_audio_file)
        music_track.length   = self._extractLength(mp3_audio_file)
        music_track.artist   = self._extractArtist(mp3_audio_file)
        music_track.album    = self._extractAlbum(mp3_audio_file)
        music_track.name     = self._extractTitle(mp3_audio_file)
        music_track.number   = self._extractTrackNumber(mp3_audio_file)
        music_track.year     = self._extractYear(mp3_audio_file)
        music_track.music_brainz_album_type = self._extractMusicBrainzAlbumType(mp3_audio_file)
        return music_track

            
    def extractAllTagData(self, musicfile):
        '''
        Extract MusicBrainz info from tags.
        '''
        #mp3_audio_file = None
        try:
            mp3_audio_file = MP3(musicfile)
            print(mp3_audio_file)
            easymp3_audio_file = EasyID3(musicfile)
            print(easymp3_audio_file)
        except Exception as e:
            self.log.logMsg('error', "fail: %s - %s" % (str(musicfile), str(e)))
        #tag_data = mp3_audio_file.tags.getall("")
        #return tag_data


    def updateTagsToV24(self, music_track):
        '''
        Attempts to upgrade the mp3 ID3 tags prior to the move/rename.
        '''
        audiofile = ID3(music_track)
        audiofile.update_to_v24()
        audiofile.save()
        self.log.logMsg('info', "Tags updated to v2.4 for %s" % (str(music_track)), True)
        
        
    def addComment(self, music_file):
        '''
        Add a comment to the mp3 file.
        '''
        audiofile = ID3(music_file)
        audiofile.add(COMM(encoding=3, lang="eng", desc="Comment", text=u"MP3MusicSorter"))
        audiofile.save()
        self.log.logMsg('debug', "Comment added to %s" % (str(music_file)), self.PRINT_DEBUG)
        
        
    def newArtistTag(self, music_file, artist_string):
        '''
        Add a new artist tag to the mp3 file.
        '''
        audiofile = ID3(music_file)
        audiofile.add(TPE2(encoding=3, text=u"%s" % (artist_string)))
        audiofile.save()
        self.log.logMsg('debug', "Artist tag added to %s" % (str(music_file)), self.PRINT_DEBUG)
        
        
    def moveFile(self, music_track):
        '''
        Moves the file to new destination based off information in the tag info
        @param music_track: 
        '''
        # /wherever/artist/album type/(year) album/01 - 320 - trackname.mp3
        destination_dir = self._setupDestinationDirString(music_track)
        final_file_dest = self._setupNewFilePathString(destination_dir, music_track)
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
        destination_dir = self._setupDestinationDirString(music_track)
        final_file_dest = self._setupNewFilePathString(destination_dir, music_track)
        self.log.logMsg('info', "%s --> %s" % (music_track.filename, final_file_dest), True)
        
        

    