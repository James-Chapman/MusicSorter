#!/usr/local/bin/python2.7
# encoding: utf-8
'''
Does what it says on the tin...
@author:     jchapman
'''

from MP3MusicSorter import MP3MusicSorter
from MP3Logger import MP3Logger
import sys
import os
import ConfigParser

this_script = os.path.basename(__file__)
name = "MP3MusicSorter"
help_message = '''

  Created by jchapman on 1 September 2013.
  
  Licensed under the Apache License 2.0
  http://www.apache.org/licenses/LICENSE-2.0
  
  Distributed on an "AS IS" basis without warranties
  or conditions of any kind, either express or implied.

USAGE

  %s pretend - Won't actually do anything, just a pretend run.
  %s sort_and_rename - This will cause files to be sorted and renamed.
''' % (this_script, this_script)

configFile = "%s.cfg" % (name)
if not os.path.exists(configFile):
    print("Can't find %s." % (configFile))
    sys.exit(1)

config = ConfigParser.ConfigParser()
config.read(configFile)
myos = config.get('MP3Tagger', 'os')
current_mp3_dir = config.get('MP3Tagger', 'current_mp3_dir')
sorted_mp3_dir = config.get('MP3Tagger', 'sorted_mp3_dir')
mp3_sort_format = config.get('MP3Tagger', 'mp3_sort_format')

MP3MusicSorter_logger = MP3Logger(name, "debug", "%s.log" % (name))


if __name__ == '__main__':
    arg = "None"
    sorter = MP3MusicSorter(myos, sorted_mp3_dir, logger=MP3MusicSorter_logger)
    try:
        arg = sys.argv[1]
    except:
        print(help_message)
        MP3MusicSorter_logger.closeLog()
    if arg == "pretend":
        try:
            sorter.iterateThroughFolder(current_mp3_dir, pretend=True)
        except KeyboardInterrupt:
            ### handle keyboard interrupt ###
            print("CTRL+C caught... Stopped!")
            MP3MusicSorter_logger.closeLog()
    elif arg == "sort_and_rename":
        sorter.iterateThroughFolder(current_mp3_dir, pretend=False)
        try:
            sorter.iterateThroughFolder(current_mp3_dir, pretend=True)
        except KeyboardInterrupt:
            ### handle keyboard interrupt ###
            print("CTRL+C caught... Stopped!")
            MP3MusicSorter_logger.closeLog()
    else:
        print(help_message)
    MP3MusicSorter_logger.closeLog()
    