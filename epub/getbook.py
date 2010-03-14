#!/bin/env python
#coding=utf-8
# file: getbook.py

import os
import os.path

from optparse import OptionParser
import uuid
import zipfile

from epub import epub
from mediawikibook import get_wikisource_work

def zipBook(title):
    myZipFile = zipfile.ZipFile(title+".epub","w")
    os.chdir(title)
    for root,dirs,files in os.walk("."):
        for fileName in files:
            if fileName[0] != ".":
                myZipFile.write(os.path.join(root,fileName))
    myZipFile.close()
    os.chdir("..")

def main():
	parser = OptionParser()
	#parser.add_option("-f","--file",dest="filename",help="write report to FILE",metavar="FILE")
	parser.add_option("-d","--date",dest="date",help="published DATE",metavar="DATE")
	#parser.add_option("-q","--quiet",action="store_false",dest="verbose",default=True,help="don't print status messages to stdout")

	(options,args) = parser.parse_args()
	#title = args[0]
	#title = "Treasure_Island"
	title = "Through the Looking-Glass, and What Alice Found There"
	title = "Great Expectations"
	#title = "Groundwork of the Metaphysics of Morals"
	bookdir = title
	book = epub(bookdir)
	host = "en.wikisource.org"
	get_wikisource_work(book,host,title)
	#title = "Space"
	#host = "en.wikipedia.org"
	#book = get_mediawiki_book(book,host,title)
	uid = uuid.uuid4()
	book.setUuid(uid)
	book.writeEpub()
	zipBook(title)

main()
