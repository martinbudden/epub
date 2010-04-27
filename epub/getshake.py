#!/bin/env python
#coding=utf-8
# file: getshake.py

import re
import uuid
from optparse import OptionParser

import epub
from xml.sax import SAXException
import xml.sax.handler


class MyXMLHandler(xml.sax.handler.ContentHandler):
    def __init__(self, book):
        xml.sax.handler.ContentHandler.__init__(self)
        self.book = book
        self.stack = []
        self.element_index = 0
        self.limit = 100000
        self.in_element = ""
        self.text = ""
        self.chapter_text = ""
        self.act = 0
        self.scene = 0
        self.chapter_title = ""
        self.chapter_text = ""
        self.titles = {}
        self.in_section = ""

    def startElement(self, name, attributes):
        self.element_index += 1
        if self.element_index > self.limit and self.limit > 0:
            raise SAXException('Reached limit count')  # stop parsing
        self.stack.append(name)
        self.in_element = name
        if name == 'ACT':
            self.act += 1
            self.scene = 0
            self.in_section = name
        if name == 'SCENE':
            self.scene += 1
            self.in_section = name
        if name == 'PLAY' or name == 'PERSONAE':
            self.in_section = name
        if name == "SCENE" or name == "FM" or name == "PERSONAE":
            print "MMM", name
        tag = "<" + name + ">"
        if name != 'PLAY' and name != 'ACT':
            self.text += tag

    def characters(self, data):
        text = data.strip()
        text = re.sub("\n", "", text)
        self.text += text

    def endElement(self, name):
        self.stack.pop()
        tag = "</" + name + ">\n"
        #if name == 'LINE':
        #    tag = '</LINE><BR />\n'
        #else:
        #    tag = '</' + name + '>\n'
        if name == 'TITLE':
            title = self.text
            title = re.sub('<TITLE>', '', title);
            title = re.sub('<ACT>', '', title);
            title = re.sub('<SCENE>', '', title);
            title = re.sub('<PERSONAE>', '', title);
            self.titles[self.in_section] = title
            print 'title:', title
        if name != 'PLAY' and name != 'ACT':
            self.text += tag
        self.chapter_text += self.text
        title = ''
        if name == 'FM':
            title = self.titles['PLAY']
        if name == 'SCENE':
            title = self.titles['ACT'] + ', ' + self.titles['SCENE']
        if name == 'PERSONAE':
            title = self.titles[name]
        if name == 'SCENE' or name == 'FM' or name == 'PERSONAE':
            print "adding", title
            xmlid = "act" + str(self.act) + "-scene" + str(self.scene)
            if name == 'FM' or name == 'PERSONAE':
                xmlid = name
                print self.chapter_text
            self.chapter_title = title
            self.book.add_section({'id': xmlid, 'title': self.chapter_title,
                                   'text': self.chapter_text})
            self.chapter_text = ""
        #print self.text
        self.text = ""


def parse_xml(book, filename):
    handler = MyXMLHandler(book)
    parser = xml.sax.make_parser()
    parser.setContentHandler(handler)
    try:
        parser.parse(filename)
    except SAXException, inst:
        print "caught", inst
        print filename
    return handler.book


def main():
    parser = OptionParser()
    #parser.add_option("-f", "--file", dest="filename", help="write report to FILE", metavar="FILE")
    parser.add_option("-d", "--date", dest="date", help="published DATE", metavar="DATE")
    #parser.add_option("-q", "--quiet", action="store_false", dest="verbose", default=True, help="don't print status messages to stdout")

    (options, args) = parser.parse_args()
    uid = uuid.uuid4()
    #title = args[0]
    title = "Hamlet"
    author = "William Shakespeare"
    author_as = "Shakespeare, William"
    published = ""
    bookdir = title

    #bookdir = author + " - " + title
    book = epub.EPub(bookdir)
    book.set_uuid(uid)
    book.stylesheets = {'main': 'play.css', 'titlepage': "titlepage.css"}
    book.templates['main'] = 'mainplay.xml'
    book.dtdfilename = 'play.dtd'
    book.set(title, author, author_as, published, "Testsource")
    book.add_section({'id': "level1-title", 'title': "Title", 'text': title})
    filename = "../test/data/hamlet.xml"
    parse_xml(book, filename)
    book.write_epub()
    book.zip_epub()

if __name__ == "__main__":
    main()
