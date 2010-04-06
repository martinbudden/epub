#!/bin/env python
#coding=utf-8
# file: getbook.py


import sys
from optparse import OptionParser
import uuid

from epub import epub
from mediawikibook import get_wikisource_work, get_mediawiki_book

def main():
	parser = OptionParser()
	#parser.add_option("-f","--file",dest="filename",help="write report to FILE",metavar="FILE")
	#parser.add_option("-d","--date",dest="date",help="published DATE",metavar="DATE")
	parser.add_option("-v", action="store_true", dest="verbose", default=False, help="print status messages to stdout")

	(options,args) = parser.parse_args()
	if len(args) == 0:
		title = "Treasure_Island"
	else:
		title = args[0]
	#title = "Through the Looking-Glass, and What Alice Found There"
	#title = "Great Expectations"
	#title = "Groundwork of the Metaphysics of Morals"
	title = "Fear and Trembling"
	#title = "Space"
	bookdir = title
	book = epub(bookdir)

	host = "en.wikisource.org"
	get_wikisource_work(book,host,title)

	#host = "en.wikipedia.org"
	#get_mediawiki_book(book,host,title)

	uid = uuid.uuid4()
	book.setUuid(uid)
	book.writeEpub()
	book.zipBook()


if __name__ == "__main__":
    main()
