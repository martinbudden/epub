#!/bin/env python
#coding=utf-8
# file: epub.py


#import re
import sys
import os.path
from jinja2 import Environment, PackageLoader
import zipfile


class epub():
	def __init__(self,bookdir):
		self.env = Environment(loader=PackageLoader('epub', 'templates'))
		self.sections = []
		self.bookdir = os.path.join(os.curdir,bookdir)
		if not os.path.isdir(self.bookdir):
			os.makedirs(self.bookdir)
		self.sections = []
		self.opffilename = "content.opf"
		self.ncxfilename = "toc.ncx"
		self.title = ""
		self.uuid = ""
		self.author = ""
		self.author_as = ""
		self.depth = "1"
		self.description = ""
		self.source = ""
		self.publisher = ""
		self.publication = ""
		self.published = ""
		self.rights = ""
		self.language = "en"
		self.chapterTranslation = "Chapter"
		self.xmlExt = ".xml"

	def set(self,title,author,author_as,published,source):
		self.title = title
		self.author = author
		self.author_as = author_as
		self.published = published
		self.source = source

	def setUuid(self,uuid):
		self.uuid = uuid

	def addSection(self,section):
		self.sections.append(section)

	def writeFile(self,dir,filename,content):
		filename = os.path.join(dir,filename)
		FILE = open(filename,"w")
		FILE.write(content)
		FILE.close()

	def writeMimeType(self):
		s = "application/epub+zip"
		self.writeFile(self.bookdir,"mimetype",s)

	def writeMetaInf(self):
		self.metainfdir = os.path.join(self.bookdir,"META-INF")
		if not os.path.isdir(self.metainfdir):
			os.makedirs(self.metainfdir)
		template = self.env.get_template("container.xml")
		s = template.render({'file':self.opffilename})
		self.writeFile(self.metainfdir,"container"+self.xmlExt,s)

	def writeStylesheets(self):
		self.cssdir = os.path.join(self.opsdir,"css")
		if not os.path.isdir(self.cssdir):
			os.makedirs(self.cssdir)
		for i in self.stylesheets:
			template = self.env.get_template(i)
			s = template.render()
			self.writeFile(self.cssdir,i,s);

	def writeImages(self):
		self.imagedir = os.path.join(self.opsdir,"images")
		if not os.path.isdir(self.imagedir):
			os.makedirs(self.imagedir)

	def writeOpf(self):
		# Open Packaging Format
		template = self.env.get_template("content.opf")
		print "self:",self
		s = template.render({'title':self.title,'uuid':self.uuid,'language':self.language,'author':self.author,'author_as':self.author_as,'description':self.description,'publisher':self.publisher,'source':self.source,'published':self.published,'ncxfile':self.ncxfilename,'rights':self.rights,'stylesheets':self.stylesheets,'sections':self.sections})
		self.writeFile(self.opsdir,self.opffilename,s);

	def writeNcx(self):
		# Navigation Center for XML
		template = self.env.get_template("toc.ncx")
		s = template.render({'uid':self.uuid,'depth':self.depth,'title':self.title,'author':self.author_as, 'sections':self.sections})
		self.writeFile(self.opsdir,self.ncxfilename,s);

	def writeTitle(self,filename):
		css = "titlepage.css"
		template = self.env.get_template("titlepage.xml")
		s = template.render({'title':self.title,'css':css,'author':self.author,'published':self.published,'source':self.source})
		self.writeFile(self.opsdir,filename,s);

	def writeChapter(self,section):
		css = "main.css"
		#if section['title'].find("section")==-1:
		#<span class="translation">{{ translation }}</span> <span class="count">{{ count }}</span>
		#extra = extra % {'translation':self.sectionTranslation,'count':section['count']}
		template = self.env.get_template("main.xml")
		s = template.render({'css':css,'id':section['id'],'class':section['class'],'title':section['title'],'text':section['text']})
		self.writeFile(self.opsdir,section['file']+self.xmlExt,s);

	def writeContent(self):
		for i in self.sections:
			if i['class'] == "title":
				self.writeTitle(i['file']+self.xmlExt)
			else:
				self.writeChapter(i)

	def writeOps(self):
		# Open Publication Structure
		self.opsdir = os.path.join(self.bookdir,"OPS")
		if not os.path.isdir(self.opsdir):
			os.makedirs(self.opsdir)
		self.stylesheets = ["page.css","titlepage.css","about.css","main.css"] #,"play.css"]
		self.writeOpf()
		self.writeNcx()
		self.writeStylesheets()
		#self.writeImages()
		self.writeContent()

	def writeEpub(self):
		self.writeMimeType()
		self.writeMetaInf()
		self.writeOps()

	def zipBook(self):
		myZipFile = zipfile.ZipFile(self.title+".epub","w")
		print "zipfile:",self.title+".epub"
		os.chdir(self.bookdir)
		for root,dirs,files in os.walk("."):
			for fileName in files:
				if fileName[0] != ".":
					myZipFile.write(os.path.join(root,fileName))
		myZipFile.close()
		os.chdir("..")

