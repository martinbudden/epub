"""
Test the meaidwikibook contents parsing.
"""

import unittest

import mediawikibook

def test_Through_the_Looking_Glass():
	filename = "../test/data/Through the Looking-Glass, and What Alice Found There.txt"
	FILE = open(filename,"r")
	text = FILE.read()
	FILE.close()
	info = mediawikibook.parse_wikisource_contents(text)
	assert info['title'] == "Through the Looking-Glass, and What Alice Found There"
	assert info['author'] == "Lewis Carroll"
	sections = info['sections']
	assert sections[0] == {'wikisubpage': '/Preface', 'title': 'Poem: Child of the pure unclouded brow'}

def test_Great_Expectations():
	filename = "../test/data/Great Expectations.txt"
	FILE = open(filename,"r")
	text = FILE.read()
	FILE.close()
	info = mediawikibook.parse_wikisource_contents(text)
	assert info['title'] == "Great Expectations"
	assert info['author'] == "Charles Dickens"
	sections = info['sections']
	assert sections[0] == {'wikisubpage': '/Chapter_I', 'title': 'Chapter I'}

def test_Treasure_Island():
	filename = "../test/data/Treasure Island.txt"
	FILE = open(filename,"r")
	text = FILE.read()
	FILE.close()
	info = mediawikibook.parse_wikisource_contents(text)
	assert info['title'] == "Treasure Island"
	assert info['author'] == "Robert Louis Stevenson"
	sections = info['sections']
	assert sections[0] == {'wikisubpage': '/Chapter_1', 'title': 'Chapter 1: The Old Sea-dog at the Admiral Benbow'}

test_Through_the_Looking_Glass()
test_Great_Expectations()
test_Treasure_Island()

