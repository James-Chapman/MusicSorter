MusicSorter
===========

I have a lot of duplicate MP3s and want to delete the lower quality file.
This was written to rename and restructure all my files in a way that
would make it easy to spot duplicates and then delete the lower quality
file. 

Iterates through a folder of MP3 files and moves and renames them into
a new folder and you typically end up with something like: 

new_folder/artist/album_type/(year) album/01 - 128 - song_title.mp3
new_folder/artist/album_type/(year) album/01 - 320 - song_title.mp3

You can easily see which file is the lower quality file and delete it.
While size is also a good indicator, it isn't always a true indicator
because VBR can result in a smaller yet higher quality file.
