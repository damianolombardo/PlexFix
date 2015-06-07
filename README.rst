=========
 PlexFix
=========

This project is based upon a scrip that can be found `here <http://axisdata.com/FixPlexPosters>`_ which itself was a response to steps outlines by Nik Ansell which can be found `here. <https://nikansell.wordpress.com/2012/03/14/fixing-corrupt-plex-thumbnails/>`_ I wrote this to perform the steps of the original script independent of the system it is being executed on. However there is no guarantee this will work on anything but Windows.

The module created is based upon Sean Fisks `Python Project Template <https://github.com/seanfisk/python-project-template>`_ and there may still be elements remaining from it in the documentation, which I will do my best to remove when I have a chance.

Usage
=====

Either;
    `python plexfix 'show 1' 'show 2'`
or on windows
    `plexfix 'show 1' 'show 2'`

This will move the metadata associated with an item to a folder called tmp in the root directory of your system.
Then go to `Plex Media Manager <http://localhost:32400/web/index.html>`_ and manually refresh the item you have removed from Plex.

Project Setup
=============

This is my first published script and as such it is very simple in setup and use. As time progresses I will add features and setup steps.
There is still a need to manually refresh the database of the TV show/Movie which was corrupted, this should be changed when I add in the Plex API functionality.

Licenses
========

PlexFix licensed under the MIT/X11 license.


Issues
======

Please report any bugs or requests that you have using the GitHub issue tracker.

Development
===========
This is a work in progress, all development is performed whenever I get the programming buzz.


Authors
=======

* Damiano Lombardo
