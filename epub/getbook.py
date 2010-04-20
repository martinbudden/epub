#!/bin/env python
#coding=utf-8
# file: getbook.py

"""
Get a book and write it to an epub file.
"""

from optparse import OptionParser
import uuid

from epub import epub
from mediawikibook import get_wikisource_work, get_mediawiki_book


def process_options(arglist=None):
    """
    Process options passed either via arglist or via command line args.
    """

    parser = OptionParser(arglist)
    #parser.add_option("-f","--file",dest="filename",help="write report to FILE",metavar="FILE")
    #parser.add_option("-d","--date",dest="date",help="published DATE",metavar="DATE")
    parser.add_option("-v", action="store_true", dest="verbose", default=False,
                      help="print status messages to stdout")

    (options, args) = parser.parse_args()
    return options, args


def main():
    """
    Parse options and write epub file.
    """

    options, args = process_options()
    if len(args) == 0:
        title = "Treasure_Island"
    else:
        title = args[0]
    title = "Through the Looking-Glass, and What Alice Found There"
    #title = "Great Expectations"
    #title = "Groundwork of the Metaphysics of Morals"
    #title = "Fear and Trembling"
    #title = "Space"
    bookdir = title
    book = epub(bookdir)

    host = "en.wikisource.org"
    get_wikisource_work(book, host, title)

    #host = "en.wikipedia.org"
    #get_mediawiki_book(book, host, title)

    uid = uuid.uuid4()
    book.set_uuid(uid)
    book.write_epub()
    book.zip_book()


if __name__ == "__main__":
    main()
