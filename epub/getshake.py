#!/bin/env python
#coding=utf-8
# file: getshake.py

import os.path
import re
import uuid
from optparse import OptionParser

from ebook import ebook
from xml.sax import SAXException
import xml.sax.handler


class MyXMLHandler(xml.sax.handler.ContentHandler):
    def __init__(self):
        xml.sax.handler.ContentHandler.__init__(self)
        self.stack = []
        self.elementIndex = 0
        self.limit = 100000
        self.inElement = ""
        self.text = ""
        self.chapterText = ""
        self.act = 0
        self.count = 1
        self.scene = 0
        self.playorder = 1
        self.chapter_title = ""
        self.chapter_text = ""

    def set_book(self, filename, uid):
        author = "William Shakespeare"
        title = "Hamlet"
        author_as = "Shakespeare, William"
        published = ""
        bookdir = title

        #bookdir = author + " - " + title
        self.book = ebook(bookdir)
        self.book.set(uid, title, author, author_as, published, "Testsource")
        self.book.add_chapter({'class': "title", 'type': "cover", 'id': "level1-title", 'playorder': "1", 'title': "Title", 'file': "titlepage", 'text': title})

    def startElement(self, name, attributes):
        self.elementIndex += 1
        if self.elementIndex > self.limit and self.limit > 0:
            raise SAXException('Reached limit count')  # stop parsing
        self.stack.append(name)
        self.inElement = name
        if name == "ACT":
            self.act += 1
            self.scene = 0
        if name == "SCENE":
            self.scene += 1
        if name == "SCENE" or name == "FM" or name == "PERSONAE":
            print "MMM", name
        tag = "<" + name + ">"
        tag = tag.encode("utf-8")
        #print tag
        if name != "PLAY":
            self.text += tag

    def characters(self, data):
        text = data.encode('utf-8').strip()
        text = re.sub("\n", "", text)
        self.text += text

    def endElement(self, name):
        self.stack.pop()
        tag = "</" + name + ">\n"
        tag = tag.encode("utf-8")
        if name != "PLAY":
            self.text += tag
        self.chapter_text += self.text
        if name == "SCENE" or name == "FM" or name == "PERSONAE":
            print "nn", name
            xmlid = "act" + str(self.act) + "-scene" + str(self.scene)
            if name == "FM" or name == "PERSONAE":
                xmlid = name
                print self.chapterText
            xmlid = xmlid.encode("utf-8")
            self.chapter_title = "test chapter title"
            self.book.add_chapter({'class': "chapter", 'type': "text", 'id': xmlid, 'playorder': str(self.playorder), 'count': str(self.count), 'title': self.chapter_title, 'file': "main" + str(self.count), 'text': self.chapter_text})
            self.chapter_text = ""
            self.count += 1
            self.playorder += 1
        #print self.text
        self.text = ""


def parse_xml(filename, uid):
    handler = MyXMLHandler()
    handler.set_book(filename, uid)
    parser = xml.sax.make_parser()
    parser.setContentHandler(handler)
    try:
        parser.parse(filename)
    except SAXException:
        print "caught"
        print filename
    return handler.book


def get_xml_book(filename, uid):
    return parse_xml(filename, uid)


def main():
    parser = OptionParser()
    #parser.add_option("-f", "--file", dest="filename", help="write report to FILE", metavar="FILE")
    parser.add_option("-d", "--date", dest="date", help="published DATE", metavar="DATE")
    #parser.add_option("-q", "--quiet", action="store_false", dest="verbose", default=True, help="don't print status messages to stdout")

    (options, args) = parser.parse_args()
    uid = uuid.uuid4()
    title = "hamlet"
    #title = args[0]
    filename = "hamlet.xml"
    book = get_xml_book(filename, uid)
    book.write_book()
    book.zip_book()

if __name__ == "__main__":
    main()
