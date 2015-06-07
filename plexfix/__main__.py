from os import environ, path, makedirs, sep
from platform import system
from shutil import move
import sqlite3
from hashlib import sha1
from sys import argv

root = path.abspath(sep)
if system() == 'Windows':
    LOCALAPPDATA = environ['LOCALAPPDATA']
elif system() == 'Linux':
    LOCALAPPDATA = environ['PLEX_HOME']
elif system() == 'Darwin':
    LOCALAPPDATA = '~/Library/Application Support'
else:
    print('Unsupported System; Exiting')
    exit()
DBDIR = path.join(LOCALAPPDATA, "Plex Media Server", "Plug-in Support", "Databases")
MDDIR = path.join(LOCALAPPDATA, "Plex Media Server", "Metadata")


def plexfix(searchstring):
    """
    Search Plex database for a specific item and remove its metadata.
    Args:
        :param searchstring: Name of item to be searched, should be a close to the actual name as possible
        :type searchstring: str

    Returns:
        :return: None

    References:
        [1] https://nikansell.wordpress.com/2012/03/14/fixing-corrupt-plex-thumbnails/
        [2] http://axisdata.com/FixPlexPosters
    """

    if searchstring == '':
        print('Usage: plexfix(showname)')
        exit()
    conn = sqlite3.connect(path.join(DBDIR, "com.plexapp.plugins.library.db"))

    sql_string = "SELECT title, guid FROM metadata_items WHERE title LIKE '{}'".format(searchstring)
    results = list(conn.execute(sql_string))
    print('Searching for: {}'.format(searchstring))
    if len(results) == 1:
        showname = results[0][0]
        showid = results[0][1]
        showsum = sha1(showid.encode('utf-8')).hexdigest()
        showchar = showsum[0]
        showdir = showsum[1:]
        print("Title: {}".format(showname))
        moviepath = path.join(MDDIR, "Movies", showchar, showdir) + '.bundle'
        tvpath = path.join(MDDIR, "TV Shows", showchar, showdir) + '.bundle'
        plexposterbundles = path.join(root, 'tmp', 'plexposterbundles')
        if path.isdir(moviepath):
            bundlefile = moviepath
            bundledest = path.join(plexposterbundles, 'Movies')
        elif path.isdir(tvpath):
            bundlefile = tvpath
            bundledest = path.join(plexposterbundles, 'TV')
        else:
            print('No bundle file')
            return

        if path.isdir(bundlefile):
                if not path.isdir(bundledest):
                    if not path.isdir(path.join('tmp', 'plexposterbundles')):
                        makedirs(path.join('tmp', 'plexposterbundles'))
                    makedirs(bundledest)
                move(bundlefile, bundledest)
                print("""Bundle found and moved to "{}"
        Now go to Plex Media Manager and choose "Fix Incorrect Match"
        and then "Update Selection" for this title.""".format(bundledest))
    elif len(results) > 1:
        print('Multiple Entries Found')
        for i in results:
            print(i[0])
            print('Try a more specific search')

    else:
        print('No entries found -- please try a different search string.')




if __name__ == '__main__':
    for arg in argv[1:]:
        plexfix(arg)
