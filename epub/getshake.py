#!/bin/env python
#coding=utf-8
# file: getshake.py

import sys
import os
import os.path
import re
import sys
import time
import uuid
from optparse import OptionParser
import httplib
import zipfile

from ebook import ebook
from xml.sax import make_parser, SAXException
import xml.sax.handler

class MyXMLHandler(xml.sax.handler.ContentHandler):
	def __init__(self):
		self.stack = []
		self.elementIndex =0
		self.limit = 100000
		self.inElement = ""
		self.text = ""
		self.chapterText = ""

	def setBook(self,filename,uid):
		self.count = 1
		self.playorder = 1
		self.act = 0
		self.scene = 0
		author = "William Shakespeare"
		title = "Hamlet"
		author_as = "Shakespeare, William"
		published = ""
		bookdir = title

		#bookdir = author + " - " + title
		self.book = ebook(bookdir)
		self.book.set(uid,title,author,author_as,published,"Testsource")
		self.book.addChapter({'class':"title",'type':"cover",'id':"level1-title",'playorder':"1",'title':"Title",'file':"titlepage",'text':title})


	def startElement(self,name,attributes):
		self.elementIndex += 1
		if self.elementIndex > self.limit and self.limit > 0:
			raise SAXException('Reached limit count') # stop parsing
		self.stack.append(name);
		self.inElement = name
		if name=="ACT":
			self.act += 1
			self.scene = 0
		if name=="SCENE":
			self.scene += 1
		if name=="SCENE" or name=="FM" or name=="PERSONAE":
			print "MMM", name
		tag = "<"+name+">"
		tag = tag.encode("utf-8")
		#print tag
		if name!="PLAY":
			self.text += tag


	def characters(self,data):
		text = data.encode('utf-8').strip()
		text = re.sub("\n","",text)
		self.text += text

	def endElement(self,name):
		self.stack.pop()
		tag = "</"+name+">\n"
		tag = tag.encode("utf-8")
		if name!="PLAY":
			self.text += tag
		self.chapterText += self.text
		if name=="SCENE" or name=="FM" or name=="PERSONAE":
			print "nn", name
			xmlid = "act"+str(self.act)+"-scene"+str(self.scene)
			if name=="FM" or name=="PERSONAE":
				xmlid = name
				print self.chapterText
			xmlid = xmlid.encode("utf-8")
			self.chapterTitle = "test chapter title"
			self.book.addChapter({'class':"chapter",'type':"text",'id':xmlid,'playorder':str(self.playorder),'count':str(self.count),'title':self.chapterTitle,'file':"main"+str(self.count),'text':self.chapterText})
			self.chapterText = ""
			self.count += 1
			self.playorder += 1
		#print self.text
		self.text = ""

def parseXML(filename,uid):
	handler = MyXMLHandler()
	handler.setBook(filename,uid)
	parser = xml.sax.make_parser()
	parser.setContentHandler(handler)
	try:
		parser.parse(filename)
	except SAXException:
		print "caught"
		print filename
	return handler.book

def getXMLBook(filename,uid):
	return parseXML(filename,uid)


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
	uid = uuid.uuid4()
	title = "hamlet"
	#title = args[0]
	filename = "hamlet.xml"
	book = getXMLBook(filename,uid)
	book.writeBook()
	zipBook(book.title)

main()