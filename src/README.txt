-- README --

System requirements to run:

* Python 2.7 (http://www.python.org/download/)
* mutagen library (bundled)
* ConfigParser library (bundled, but may not work).

To run the app do:

* Modify the config file first!

* run.py show_duplicates - Will print out a list of Artists and Track Titles 
                           that have more than 1 file associated with each Title.

* run.py pretend         - This will display what it's going to do if the sort_and_rename
                           option is passed in.

* run.py sort_and_rename - This will rename and restructure your mp3 into the 
                           following structure:
                           artist/album_type/(year) album_name/01 - bitrate - track_title.mp3

Everything is logged to a logfile called MP3MusicSorter.log






-- CHANGELOG --

  4 September 2013

* Added SQLite DB queries to show tracks that have more than 1 file associated with it.
* Added MP3Exception class.



  1 September 2013

* Initial project creation.








-- PROBLEMS --

If the bundled ConfigParser library does not work you will need to add it to your python environment.
To do that, perform the following steps:

1.) Download ez_setup.py from https://bitbucket.org/pypa/setuptools/raw/bootstrap/ez_setup.py
2.) Open a command prompt and run
    python ez_setup.py
    
"pip" should now be installed in C:\Python27\Scripts
Run "pip install ConfigParser"

The same with mutagen if it fails.