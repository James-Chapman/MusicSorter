README
======

System requirements:

  * Python 2.7 (http://www.python.org/download/)


Usage:

  * Modify the config file first!
  * Now run 'python run.py' and read the available run time parameters.

Everything is logged to a logfile called MP3MusicSorter.log




CHANGELOG
=========

6 September 2013

  * Massive database improvements
  * A lot of Windows file system related bug fixes.


4 September 2013

  * Added SQLite DB queries to show tracks that have more than 1 file associated with it.
  * Added MP3Exception class.


1 September 2013

  * Initial project creation.





PROBLEMS
========


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



