#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
'''
Created on 1 Sep 2013

@author: jchapman
'''
from MP3DataBase import MP3DataBase
from MusicTrack import MusicTrack
from mutagen.id3 import COMM, ID3
from mutagen.mp3 import MP3
import MP3Exception
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
        
        
    def _extractBasicInfo(self, song, mp3_audio_file):
        '''
        Extract bitrate and length from audio file.
        '''
        try:
            song.bitrate = mp3_audio_file.info.bitrate / 1000
            song.length = mp3_audio_file.info.length
        except Exception as e:
            self.log.logMsg('error', "error reading file info: %s - %s" % (str(song.filename), str(e)))
        return song
    
    
    def _extractArtist(self, song, mp3_audio_file):
        '''
        Extract Artist from tags.
        '''
        try:
            song.artist = mp3_audio_file.tags.getall("TPE2")[0]
        except Exception as e:
            pass
        if not song.artist:
            try:
                song.artist = mp3_audio_file.tags.getall("TP2")[0]
            except Exception as e:
                pass
        if not song.artist:
            try:
                song.artist = mp3_audio_file.tags.getall("artist")[0]
            except Exception as e:
                self.log.logMsg('error', "No Artist tag found for: %s" % (str(song.filename)))
        return song
        
        
    def _extractAlbum(self, song, mp3_audio_file):
        '''
        Extract Album Name from tags.
        '''
        try:
            song.album = mp3_audio_file.tags.getall("TALB")[0]
        except Exception as e:
            pass
        if not song.album:
            try:
                song.album = mp3_audio_file.tags.getall("TAL")[0]
            except Exception as e:
                pass
        if not song.album:
            try:
                song.album = mp3_audio_file.tags.getall("album")[0]
            except Exception as e:
                self.log.logMsg('error', "No Album tag found for: %s" % (str(song.filename)))
        return song
        
        
    def _extractTitle(self, song, mp3_audio_file):
        '''
        Extract Track Title from tags.
        '''
        name = None
        try:
            name = str(mp3_audio_file.tags.getall("TIT2")[0])
        except Exception as e:
            pass
        if not name:
            try:
                name = str(mp3_audio_file.tags.getall("TT2")[0])
            except Exception as e:
                pass
        if not name:
            try:
                name = str(mp3_audio_file.tags.getall("title")[0])
            except Exception as e:
                self.log.logMsg('error', "No Title tag found for: %s" % (str(song.filename)))
        try:
            song.name = re.sub(r'''[/{}<>%$Â£@:;#~*^Â¬]''', '_', name)
        except Exception as e:
            self.log.logMsg('error', "No Artist tag found for: %s" % (str(song.filename)))
        return song
        
        
    def _extractTrackNumber(self, song, mp3_audio_file):
        '''
        Extract Track Number from tags.
        '''
        number = None
        try:
            number = str(mp3_audio_file.tags.getall("TRCK")[0])
        except Exception as e:
            pass
        if not number:
            try:
                number = str(mp3_audio_file.tags.getall("TRK")[0])
            except Exception as e:
                pass
        if not number:
            try:
                number = str(mp3_audio_file.tags.getall("track")[0])
            except Exception as e:
                self.log.logMsg('error', "No Track Number tag found for: %s" % (str(song.filename)))
        try:
            song.number = number.split("/")[0].zfill(2)
        except:
            self.log.logMsg('error', "Can't split track number for: %s" % (str(song.filename)))
        return song
        
        
    def _extractYear(self, song, mp3_audio_file):
        '''
        Extract Release Year from tags.
        '''
        year = "0000"
        try:
            year = str(mp3_audio_file.tags.getall("TDRC")[0])
        except Exception as e:
            pass
        if year == "0000":
            try:
                year = str(mp3_audio_file.tags.getall("TYER")[0])
            except Exception as e:
                pass
        if year == "0000":
            try:
                year = str(mp3_audio_file.tags.getall("TYE")[0])
            except Exception as e:
                pass
        try:
            song.year = year.split("-")[0]
        except:
            self.log.logMsg('error', "Can't split year for: %s" % (str(song.filename)))    
        return song
            
        
    def _extractMusicBrainzData(self, song, mp3_audio_file):
        '''
        Extract MusicBrainz info from tags.
        '''
        try:
            song.music_brainz_artist_id = mp3_audio_file.tags.getall("TXXX:ASIN")[0]
            song.music_brainz_album_artist_id = mp3_audio_file.tags.getall("TXXX:MusicBrainz Album Artist Id")[0]
            song.music_brainz_album_id = mp3_audio_file.tags.getall("TXXX:MusicBrainz Artist Id")[0]
            song.music_brainz_track_id = mp3_audio_file.tags.getall("TXXX:ASIN")[0]
            song.music_brainz_album_type = mp3_audio_file.tags.getall("TXXX:MusicBrainz Album Type")[0]
        except Exception as e:
            self.log.logMsg('warning', "Problem extracting musicbrainz data! - %s" % (str(e)), False)
        return song
        
        
    def _setupDestinationDirString(self, music_track):
        '''
        Creates file path string based off the OS argument.
        @param music_track:  
        @return: destination_dir is the OS correct destination dir path
        '''
        destination_dir = "%s%s%s%s%s%s(%s) %s" % (self.sorted_root_dir, self.sep, music_track.artist, 
                                                   self.sep, music_track.music_brainz_album_type, 
                                                   self.sep, music_track.year, music_track.album)
        return destination_dir
        

    def _setupNewFilePathString(self, destination_dir, music_track):
        '''
        Creates file name string based off the OS argument.
        @param destination_dir:
        @param music_track:  
        @return: final_file_path is the OS correct file path
        '''
        final_file_path = "%s%s%s - %s - %s.mp3" %(destination_dir, self.sep, music_track.number, 
                                                   music_track.bitrate, music_track.name)
        return final_file_path
    
        
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
                #music_track.printMusicTrackData()
                if music_track.album == None:
                    self.log.logMsg('error', "Skipping file: %s - no album found." % (music_track.filename))
                elif music_track.artist == None:
                    self.log.logMsg('error', "Skipping file: %s - no artist found." % (music_track.filename))
                elif music_track.name == None:
                    self.log.logMsg('error', "Skipping file: %s - no title found." % (music_track.filename))
                elif music_track.number == None:
                    self.log.logMsg('error', "Skipping file: %s - no track number found." % (music_track.filename))
                else:
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
        try:
            music_track = self._extractBasicInfo(music_track, mp3_audio_file)
            music_track = self._extractArtist(music_track, mp3_audio_file)
            music_track = self._extractAlbum(music_track, mp3_audio_file)
            music_track = self._extractTitle(music_track, mp3_audio_file)
            music_track = self._extractTrackNumber(music_track, mp3_audio_file)
            music_track = self._extractYear(music_track, mp3_audio_file)
            music_track = self._extractMusicBrainzData(music_track, mp3_audio_file)
            return music_track
        except Exception as e:
            self.log.logMsg('error', "fail: %s - %s" % (str(musicfile), str(e)))


    def updateTagsToV24(self, music_track):
        '''
        Attempts to upgrade the mp3 ID3 tags prior to the move/rename.
        '''
        audiofile = ID3(music_track)
        audiofile.update_to_v24()
        audiofile.save()
        self.log.logMsg('debug', "Tags updated to v2.4 for %s" % (str(music_track)))
        
        
    def addComment(self, music_track):
        '''
        Add a comment to the mp3 file.
        '''
        audiofile = ID3(music_track)
        audiofile.add(COMM(encoding=3, lang="eng", desc="Comment", text=u"http://linux-101.org"))
        audiofile.save()
        self.log.logMsg('debug', "Comment added to %s" % (str(music_track)))


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
        
        

    