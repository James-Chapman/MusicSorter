MusicSorter
===========

For usage see README.txt in src directory.


About
-----

I have a lot of duplicate MP3s and want to delete the lower quality file.
This was written to rename and restructure all my files in a way that
would make it easy to spot duplicates and then delete the lower quality
file. 

It iterates through a folder of MP3 files and moves and renames them into
a new folder and you typically end up with something like: 

new_folder/artist/album_type/(year) album/01 - 128 - song_title.mp3

new_folder/artist/album_type/(year) album/01 - 320 - song_title.mp3

You can easily see which file is the lower quality file and delete it.
While size is also a good indicator, it isn't always a true indicator
because VBR can result in a smaller yet higher quality file.





System requirements
-------------------

  * Python 2.7 (http://www.python.org/download/)




Usage
-----

  * Modify the config file first!
  * Now run 'python run.py' and read the available run time parameters.

Everything is logged to a logfile called MP3MusicSorter.log




CHANGELOG
---------

6 September 2013

  [x] Massive database improvements.
  [x] A lot of Windows file system related bug fixes.
  [x] Activity indicator during the sort_and_rename process. 


4 September 2013

  [x] Added SQLite DB queries to show tracks that have more than 1 file associated with it.
  [x] Added MP3Exception class.


1 September 2013

  [x] Initial project creation.




KNOWN ISSUES
------------

  [ ]






PROBLEMS
--------


The 2 libraries required for this app to run are bundled with it:
  
  * mutagen library
  * ConfigParser library  (may not work)

If the bundled ConfigParser library does not work you will need to add it to your python environment.
To do that, perform the following steps:

1.) Download ez_setup.py from https://bitbucket.org/pypa/setuptools/raw/bootstrap/ez_setup.py
2.) Open a command prompt and run
    'python ez_setup.py'
    
"pip" should now be installed in C:\Python27\Scripts
Run 'pip install ConfigParser'

The same with mutagen if it fails.



