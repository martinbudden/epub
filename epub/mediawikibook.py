#!/bin/env python
#coding=utf-8
# file: mediawiki.py

import sys
import re
import sys
import time
import httplib

from mwlib.dummydb import DummyDB
from mwlib.uparser import parseString
from mwlib.parser import show
from mwlib.xhtmlwriter import MWXHTMLWriter, preprocess
from mwlib.xhtmlwriter import validate as mwvalidate
try:
    import xml.etree.ElementTree as ET
except:
    from elementtree import ElementTree as ET
#from mwlib.xfail import xfail
from xml.sax import make_parser, SAXException
import xml.sax.handler

from epub import epub

MWXHTMLWriter.ignoreUnknownNodes = False

class MyWriter(MWXHTMLWriter):
    header = ""
    #css = ""
    def __init__(self,**kargs):
        #MWXHTMLWriter.__init__(self,**kargs)
        MWXHTMLWriter.__init__(self,None,None,"images/IMAGENAME",False)
        self.root = self.xmlbody = ET.Element("body")
        self.paratag = "p"
    def xwriteParagraph(self,obj):
        """
        currently the parser encapsulates almost anything into paragraphs,
        but XHTML1.0 allows no block elements in paragraphs.
        therefore we use the html-div-element. 

        this is a hack to let created documents pass the validation test.
        """
        e = ET.Element(self.paratag) # "div" or "p"
        #e.set("class","mwx.paragraph")
        return e



class ValidationError(Exception):
    def __init__(self,value):
        self.value = value
    def __str__(self):
        return repr(self.value)


def validate(xml):
    r = mwvalidate(xml)
    if len(r):
        print xml
        raise ValidationError,r

class WikiHandler(xml.sax.handler.ContentHandler):
	def __init__(self):
		self.stack = []
		self.elementIndex =0
		self.limit = 100000
		self.inElement = ""
		self.text = ""

	def startElement(self,name,attributes):
		self.elementIndex += 1
		if self.elementIndex > self.limit and self.limit > 0:
			raise SAXException('Reached limit count') # stop parsing
		self.stack.append(name);
		self.inElement = name

	def characters(self,data):
		if self.inElement == "rev":
			self.text += data.encode('utf-8')

	def endElement(self,name):
		self.stack.pop()

def parse_wediawiki_xml(text):
	handler = WikiHandler()
	try:
		xml.sax.parseString(text,handler)
	except SAXException:
		print "caught"
	return handler.text

def httpGet(host,uri):
	print "httpGet:",uri
	http = httplib.HTTP(host)

	# write header
	USER_AGENT = "httplib-example-1.py"
	http.putrequest("GET", uri)
	http.putheader("User-Agent", USER_AGENT)
	http.putheader("Host", host)
	http.putheader("Accept", "*/*")
	http.endheaders()

	# get response
	errcode, errmsg, headers = http.getreply()
	if errcode != 200:
		raise Error(errcode, errmsg, headers)

	file = http.getfile()
	return file.read()


def httpGetOld(host,uri):
	conn = httplib.HTTPConnection(host)
	conn.request("GET",uri)
	r1 = conn.getresponse()
	print r1.status,r1.reason
	text = r1.read()

def getXHTML(wikitext):
    wikitext = unicode(wikitext.decode("utf-8"))
    #wikitext.decode("utf-8").encode("ascii","xmlcharrefreplace")
    r = parseString(title="",raw=wikitext)
    preprocess(r)
    dbw = MyWriter()
    dbw.writeBook(r)
    text = dbw.asstring()
    text = re.sub('<p />','',text)
    text = re.sub('<p> ','<p>',text)
    text = re.sub(' </p>','</p>',text)
    text = re.sub('</p><p>','</p>\n<p>',text)
    text = re.sub(' <br /> &#160;&#160;&#160;&#160;&#160; ','</p>\n<p>',text)
    text = re.sub('&#160;&#160;&#160;&#160;&#160; ','<p>',text)
    text = re.sub('</dd><dd>','</dd>\n<dd>',text)
    text = re.sub('<body><div class="mwx.article"><h1 />','',text)
    text = re.sub('</div></body>','',text)
    return text

def removeNoPrint(text):
	text = re.sub("\{\{\w*\}\}","",text)
	text = re.sub("\{\{(?:[^\}]*)\}\}","",text)
	#text = re.sub('"',""",text)
	text = re.sub('={2,6}[\w\-: ]*={2,6}',"",text)
	return text

def mediaWikiToXHTML(text,references):
	paragraphs = re.split('\n\n+',text)
	s = ""
	for i in paragraphs:
		if i:
			m = re.match("(\s*===([^=]+)===\s+)",i)
			if m:
				s += "<h3>"+m.group(2)+"</h3>\n\n"
			else:
				m = re.match("\{\{reflist\}\}",i)
				if m:
					reftext = "<ol>\n"
					for i in references:
						reftext += "<li>"+i+"</li>\n"
					reftext += "</ol>\n\n"
					s += re.sub("\{\{reflist\}\}",reftext,text)
				else:
					s += "<p>"+i+"</p>\n\n"
	s = re.sub("<poem>",'<div class="verse">',s)
	s = re.sub("</poem>",'</div>',s)
	return s

def parse_wikisource_contents(text):
	"""
	Parse the text of a Wikisource contents page to ascertain the title, author and sections of a work.
	The sections are typically chapters of a book, but may be other subdivisions of a work.
	"""
	#print "--------------------------------------"
	#print "text:", text
	#print "--------------------------------------"
	info = {'title':"",'author':"",'author_as':"",'translator':"",'published':""}
	title = ""
	m = re.search("\s*title\s*=\s*(.*)",text)
	if m:
		title = m.group(1)
		title = re.sub("\[\[","",title)
		title = re.sub("\]\]","",title)
	info['title'] = title.strip()
	author = ""
	m = re.search("\s*author\s*=\s*(.*)",text)
	if m:
		author = m.group(1)
	info['author'] = author.strip()
	info['author_as'] = info['author']
	translator = ""
	m = re.search("\s*translator\s*=\s*(.*)",text)
	if m:
		translator = m.group(1)
	info['translator'] = translator.strip()
	sections = []
	for m in re.finditer("\s*\*\s*\[\[([^\]]*)\]\](.*)",text):
		cp = m.group(1)
		ct = cp + m.group(2)
		ct = re.sub("\{\{(?:[^\}]*)\}\}","",ct)
		pos = cp.find("|")
		if pos != -1:
			cp = cp[0:pos]
			ct = ct[pos+1:]
		pos = cp.find("/")
		if pos != -1:
			cp = cp[pos:]
		cp = re.sub(" ","_",cp)
		sections.append({'wikisubpage':cp.strip(),'title':ct.strip()})
		print "ch:",cp,ct
	info['sections'] = sections
	return info

def parse_mediawiki_book_contents(text):
	"""
	Parse the text of a mediawiki book contents page to ascertain the title, author and sections of a work.
	"""
	info = {'title':"",'author':"",'author_as':"",'published':""}
	title = ""
	m = re.search("\n==(.*)==\n",text)
	if m:
		title = m.group(1).strip()
	author = "Wikipedia"
	info['title'] = title
	info['author'] = author.strip()
	info['author_as'] = info['author']

	sections = []
	#sections.append({'wikisubpage':"Space",'title':"Space"})
	for m in re.finditer(":\[\[([^\]]*)\]\]",text):
		cp = m.group(1)
		ct = cp
		pos = cp.find("|")
		if pos != -1:
			cp = cp[0:pos]
			cp = re.sub(" ","_",cp)
			ct = ct[pos+1:]
		pos = cp.find("/")
		if pos != -1:
			cp = cp[pos:]
		cp = re.sub(" ","_",cp)
		sections.append({'wikisubpage':cp,'title':ct})
		#print "ch:",cp,ct
	info['sections'] = sections
	return info


def get_mediawiki_book(epub,host,title):
	"""
	Get a mediawiki book and put its contents into an epub object.
	"""
	wikipagetitle = re.sub(" ","_",title)
	print "wikipagetitle",wikipagetitle
	# http://en.wikipedia.org/wiki/Book:Space
	# http://en.wikipedia.org/wiki/Book:Computer_Networking
	# http://en.wikipedia.org/w/api.php?format=xml&action=query&prop=revisions&titles=Book:Computer_Networking&rvprop=content|timestamp|user|ids
	# http://en.wikipedia.org/wiki/Computer_networking
	# http://en.wikipedia.org/w/index.php?title=Computer_networking&action=render
	uriTemplate = "/w/api.php?format=xml&action=query&prop=revisions&titles=Book:%(title)s&rvprop=content|timestamp|user|ids"
	uri = uriTemplate % {'title':wikipagetitle}
	print "uri",uri
	text = httpGet(host,uri)
	print "text:",text
	info = parse_mediawiki_book_contents(text)
	info['source'] = "Wikisource"
	add_sections(info)
	return epub

def get_wikisource_work(epub,host,title):
	"""
	Get a Wikisource work (typically a book) and put its contents into an epub object.
	"""
	wikipagetitle = re.sub(" ","_",title)
	print "wikipagetitle:",wikipagetitle
	# http://en.wikisource.org/w/api.php?format=xml&action=query&prop=revisions&titles=Through_the_Looking-Glass,_and_What_Alice_Found_There&rvprop=content|timestamp|user|ids
	# http://en.wikisource.org/w/api.php?action=parse&page=Through_the_Looking-Glass,_and_What_Alice_Found_There
	# http://en.wikisource.org/w/index.php?title=Through_the_Looking-Glass,_and_What_Alice_Found_There&action=render
	# http://en.wikisource.org/w/index.php?title=Through_the_Looking-Glass,_and_What_Alice_Found_There/section_I&action=render
	# http://en.wikisource.org/w/api.php?format=xml&action=query&prop=revisions&titles=Through_the_Looking-Glass,_and_What_Alice_Found_There&rvprop=content|timestamp|user|ids


	uriTemplate = "/w/api.php?format=xml&action=query&prop=revisions&titles=%(title)s&rvprop=content|timestamp|user|ids"
	#uriTemplate = "/w/api.php?action=parse&page=%(title)s"
	#uriTemplate = "/w/api.php?action=expandtemplates&title=%(title)s"
	uri = uriTemplate % {'title':wikipagetitle}
	text = httpGet(host,uri)
	#print "text:",text
	#return
	print "uri",uri
	text = parse_wediawiki_xml(text)
	info = parse_wikisource_contents(text)
	info['source'] = "Wikisource"
	if len(info['sections']) == 0:
		add_section(epub,info,host,wikipagetitle,text)
	else:
		add_sections(epub,info,host,wikipagetitle)
	return epub

def add_sections(epub,info,host,wikipagetitle):
	epub.set(info['title'],info['author'],info['author_as'],info['published'],info['source'])
	# add the title page
	epub.addSection({'class':"title",'type':"cover",'id':"level1-title",'playorder':"1",'title':"Title",'file':"titlepage",'text':info['title']})
	sections = info['sections']

	uriTemplate = "/w/api.php?format=xml&action=query&prop=revisions&titles=%(title)s&rvprop=content|timestamp|user|ids"
	#uriTemplate = "/w/api.php?format=xml&action=parse&page=%(title)s"
	count = 1
	print "sections:",sections
	for i in sections:
		# get each section (typically a chapter) and add it to the epub object
		# each section is a separate wiki page
		if count > 3:
			break
		print "=========================="
		print "getting",i['title']
		uri = uriTemplate % {'title':wikipagetitle+i['wikisubpage']}
		print "uri",uri
		text = httpGet(host,uri)
		text = parse_wediawiki_xml(text)
		text = removeNoPrint(text)
		text = getXHTML(text)
		#text = mediaWikiToXHTML(text)
		epub.addSection({'class':"chapter",'type':"text",'id':"level1-s"+str(count),'playorder':str(count+1),'count':str(count),'title':i['title'],'file':"main"+str(count),'text':text})
		count += 1

def add_section(epub,info,host,wikipagetitle,text):
	# whole work is one wiki page, so split on headings
	# eg "Groundwork of the Metaphysics of Morals" at http://en.wikisource.org/wiki/Groundwork_of_the_Metaphysics_of_Morals

	epub.set(info['title'],info['author'],info['author_as'],info['published'],info['source'])
	# add the title page
	epub.addSection({'class':"title",'type':"cover",'id':"level1-title",'playorder':"1",'title':"Title",'file':"titlepage",'text':info['title']})
	print "zero sections"
	# reget the page, expanding the templates
	uriTemplate = "/w/api.php?format=xml&action=query&prop=revisions&titles=%(title)s&rvprop=content|timestamp|user|ids&rvexpandtemplates"
	uri = uriTemplate % {'title':wikipagetitle}
	text = httpGet(host,uri)
	print "uri",uri
	text = parse_wediawiki_xml(text)

	#print "text:",text
	refcount = 0
	references = []
	tt = ""
	start = 0
	end = len(text)
	for m in re.finditer("(<ref>([^<]*)</ref>)",text):
		#print "fffff:",m.group(1)
		references.append(m.group(2))
		refcount += 1
		tt += text[start:m.start(1)] + "<sup>["+ str(refcount)+"]</sup>"
		start = m.end(1)
		#tt += "["+ str(refcount)+"]"
		#print "tt:",tt
	tt += text[start:end]

	if tt != "":
		#print "ttx:",tt
		text = tt;
	start = 0
	end = len(text)
	chtitle = "main"
	count = 1
	for m in re.finditer("(\s*==([^=]+)==\s+)",text):
		print "s1,e1", m.start(1), m.end(1)
		#print "s2,e2", m.start(2), m.end(2)
		end = m.start(1)
		if start!=0:
			chtext = text[start:end]
			chtext = mediaWikiToXHTML(chtext,references)
			print "chtitle:",chtitle
			print "chtext:",chtext[0:40]
			epub.addSection({'class':"chapter",'type':"text",'id':"level1-chapter"+str(count),'playorder':str(count+1),'count':str(count),'title':chtitle,'file':"main"+str(count),'text':chtext})
			count += 1
		start = m.end(1)
		chtitle = m.group(2)
	chtext = text[start:]
	print "sx,ex",start,end
	print "chtextx:",chtitle,chtext
	chtext = mediaWikiToXHTML(chtext,references)
	epub.addSection({'class':"chapter",'type':"text",'id':"level1-chapter"+str(count),'playorder':str(count+1),'count':str(count),'title':chtitle,'file':"main"+str(count),'text':chtext})
	#text = parseMediaWikiXML(text)
	#text = removeNoPrint(text)
	#text = getXHTML(text)
	#epub.addSection({'class':"section",'type':"text",'id':"level1-section"+str(count),'playorder':str(playorder),'count':str(count),'title':"XXXX",'file':"main"+str(count),'text':text})

