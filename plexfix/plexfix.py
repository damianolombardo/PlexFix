from os import environ, path, makedirs, sep
from platform import system
from shutil import move
import sqlite3
from hashlib import sha1
from sys import argv, exit
import getopt

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


def main(argv):
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

    opts, args = getopt.getopt(argv, "ht:d", ["help", "type="])

    mediatype = None

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print('''Usage: plexfix [options] Media Title
Options:
    -t, --type:
        s, series = deletes metadata for a an entire series.
        m, movie = deletes metadata for a movie
    -h, --help:
        Prints this help file
    -d:
        debug NOT IMPLEMENTED''')
            exit()
        elif opt == "-d":
            raise NotImplementedError
            # global _debug
            # _debug = 1
        elif opt in ("-t", "--type"):
            mediatype = arg

    searchstring = " ".join(args)

    conn = sqlite3.connect(path.join(DBDIR, "com.plexapp.plugins.library.db"))

    if mediatype is None:
        sql_string = "SELECT title, guid FROM metadata_items WHERE title LIKE '{}'".format(searchstring)
    elif mediatype.lower() in ["s", "series"]:
        # do the series search
        sql_string = "SELECT title, guid FROM metadata_items WHERE title LIKE '{}' AND metadata_type LIKE 2".format(
            searchstring)
    elif mediatype.lower() in ["m", "movie"]:
        # do the movie thing
        sql_string = "SELECT title, guid FROM metadata_items WHERE title LIKE '{}' AND metadata_type LIKE 1".format(
            searchstring)
    else:
        raise Exception

    def result_execute(result):
        title = result[0]
        guid = result[1]
        showsum = sha1(guid.encode('utf-8')).hexdigest()
        showchar = showsum[0]
        showdir = showsum[1:]
        print("Title: {}, GUID:{}".format(title, guid))
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

    # sql_string = "SELECT title, guid FROM metadata_items WHERE title LIKE '{}'".format(searchstring)
    result = list(conn.execute(sql_string))
    print('Searching for: {}'.format(searchstring))
    if len(result) == 1:
        result_execute(result[0])

    elif len(result) > 1:
        print('Multiple Entries Found')
        for i in result:
            print(i[0])
            print('Try a more specific search')

    else:
        print('No entries found -- please try a different search string.')


if __name__ == '__main__':
    main(argv[1:])
