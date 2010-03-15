#!/bin/env python
#coding=utf-8
# file: getbooktest.py

import epub

def writeBook():
	book = epub.epub("bookdir")
	book.set("Through the Looking Glass (And What Alice Found There)","Lewis Carroll","Carroll, Lewis", "1871","Wikisource")
	book.addSection({'class':"title",  'type':"cover",'id':"level1-title",   'playorder':"1",'title':"Title",'file':"titlepage",'text':"Through the Looking Glass (And What Alice Found There)"})
	book.addSection({'class':"chapter",'type':"text", 'id':"level1-chapter1",'playorder':"2",'count':"1", 'title':"Chapter 1 - Looking-Glass House",'file':"main1",'text':"<p>ch1 test text</p>"})
	book.addSection({'class':"chapter",'type':"text", 'id':"level1-chapter2",'playorder':"3",'count':"2",'title':"Chapter 2 - The Garden of Live Flowers",'file':"main2",'text':"<p>ch2 test text</p>"})
	book.addSection({'class':"chapter",'type':"text", 'id':"level1-chapter3",'playorder':"4",'count':"3",'title':"Chapter 3 - Looking-Glass Insects",'file':"main3",'text':"<p>ch3 test text</p>"})
	book.setUuid("a57c7564-3913-11de-8a9d-001cc0a62c0b")
	book.writeEpub()
	book.zipBook()

def getAndWriteBookTest():
	s="""
{{TextQuality|50%}}{{header2
 | title    = Through the Looking-Glass, and What Alice Found There
 | author   = Lewis Carroll
 | section  = 
 | previous = 
 | next     = 
 | notes    = '''''Through the Looking-Glass, and What Alice Found There''''' is a [[w:1871|1871]] children's book written by [[author:Lewis Carroll|Lewis Carroll]]. It is an indirect sequel to ''[[Alice's Adventures in Wonderland]]''. 
{{Wikipediarefb}}{{spoken}}
}}

===Contents===
*[[/Chapter I|Chapter I: Looking-Glass House]]
*[[/Chapter II|Chapter II: The Garden of Live Flowers]]
*[[/Chapter III|Chapter III: Looking-Glass Insects]]
*[[/Chapter IV|Chapter IV: Tweedledum and Tweedledee]]
*[[/Chapter V|Chapter V: Wool and Water]]
*[[/Chapter VI|Chapter VI: Humpty Dumpty]]
*[[/Chapter VII|Chapter VII: The Lion and the Unicorn]]
*[[/Chapter VIII|Chapter VIII: "It's My Own Invention!"]]
*[[/Chapter IX|Chapter IX: Queen Alice]] {{speaker|15}}
*[[/Chapter X|Chapter X: Shaking]]
*[[/Chapter XI|Chapter XI: Waking]]
*[[/Chapter XII|Chapter XII: Which Dreamed It?]]

===Chapter 4: Test===
test para 1

test para 2
"""

	#m = re.search("($|\n)\s*\*\[\[([^\]]*)",s)
	m = re.search("\s*title\s*=(.*)",s)
	if m:
		title = m.group(1)
		print "title",title
	m = re.search("\s*author\s*=(.*)",s)
	if m:
		author = m.group(1)
		print "author",author
	#p = re.compile("\s*\*\[\[([^\]]*)")
	#m = p.search(s)
	#while m:
	#	print "chapter",m.group(1)
	#	m = p.search(s,m.lastindex)
	for m in re.finditer("\s*\*\s*\[\[([^\]]*)", s):
		cp = m.group(1)
		ct = cp
		pos = cp.find("|")
		if pos != -1:
			cp = cp[0:pos]
			cp = re.sub(" ","_",cp)
			ct = ct[pos+1:]
		print "ch",cp,ct
	s = re.sub("\{\{\w*\}\}","",s)
	s = re.sub("\{\{(?:[^\}]*)\}\}","",s)
	s = re.sub("$\n*","",s)

def testParse():
	s="""
{{TextQuality|50%}}{{header2
 | title    = Through the Looking-Glass, and What Alice Found There
 | author   = Lewis Carroll
{{Wikipediarefb}}{{spoken}}
}}

===Chapter 4: Test===
test para 1: "hello there"
how are things

test para 2

some more text
"""
	s = mediaWikiToXHTML(s)
	print s

"""
{{saved_book}}

== Computer Networking ==
;Networking
:[[Computer networking]]
:[[Computer network]]
:[[Local area network]]
:[[Campus area network]]
:[[Metropolitan area network]]
:[[Wide area network]]
:[[Hotspot (Wi-Fi)]]
;OSI Model
:[[OSI model]]
:[[Physical Layer]]
:[[Media Access Control]]
:[[Logical Link Control]]
:[[Data Link Layer]]
:[[Network Layer]]
:[[Transport Layer]]
:[[Session Layer]]
:[[Presentation Layer]]
:[[Application Layer]]
;IEEE 802.1
:[[IEEE 802.1D]]
:[[Link Layer Discovery Protocol]]
:[[Spanning tree protocol]]
:[[IEEE 802.1p]]
:[[IEEE 802.1Q]]
:[[802.1w]]
:[[IEEE 802.1X]]
;IEEE 802.3
:[[Ethernet]]
:[[Link aggregation]]
:[[Power over Ethernet]]
:[[Gigabit Ethernet]]
:[[10 Gigabit Ethernet]]
:[[100 Gigabit Ethernet]]
;Standards
:[[IP address]]
:[[Transmission Control Protocol]]
:[[Internet Protocol]]
:[[IPv4]]
:[[IPv4 address exhaustion]]
:[[IPv6]]
:[[Dynamic Host Configuration Protocol]]
:[[Network address translation]]
:[[Simple Network Management Protocol]]
:[[Internet Protocol Suite]]
:[[Internet Control Message Protocol]]
:[[Internet Group Management Protocol]]
:[[Simple Mail Transfer Protocol]]
:[[Internet Message Access Protocol]]
:[[Lightweight Directory Access Protocol]]
;Routing
:[[Routing]]
:[[Static routing]]
:[[Link-state routing protocol]]
:[[Open Shortest Path First]]
:[[Routing Information Protocol]]
;IEEE 802.11
:[[IEEE 802.11]]
:[[IEEE 802.11 (legacy mode)]]
:[[IEEE 802.11a-1999]]
:[[IEEE 802.11b-1999]]
:[[IEEE 802.11g-2003]]
:[[IEEE 802.11n]]
;Other
:[[Twisted pair]]
:[[Optical fiber]]
:[[Optical fiber connector]]
:[[IEC connector]]

[[Category:Wikipedia:Books|Computer Networking]]
[[Category:Wikipedia:Books on computer science|Computer Networking]]
"""
writeBook()
print "sss"