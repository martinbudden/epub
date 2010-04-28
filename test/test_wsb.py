"""
Test the wikisource book contents parsing.
"""

#from epub import epub
from epub import epub
#import epub.mediawikibook as mediawikibook
from epub import mediawikibook

def read_file(filename):
    """Read a file and return its contents."""
    FILE = open(filename, "r")
    text = FILE.read()
    FILE.close()
    #text = text.decode("utf-8")  # from utf-8 to unicode
    text = text.decode("mac_roman")  # from utf-8 to unicode
    return text


def add_sections(pub, sections, dirname):
    """
    Add sections to a work. Each section is from a MediaWiki page.
    """

    count = 1
    for i in sections:
        # get each section (typically a chapter) and add it to the epub object
        # each section is a separate wiki page
        textxml = read_file(dirname + i['wikisubpage'] + ".xml")
        text2 = mediawikibook.parse_mediawiki_xml(textxml)
        text = read_file(dirname + i['wikisubpage'] + ".txt")
        #print "====================="
        #print text.encode("utf-8")
        #print "---------------------"
        #print text2.encode("utf-8")
        #print "====================="
        #assert text == text2
        text = mediawikibook.remove_templates(text)
        pub.add_section({'class': "chapter", 'type': "text", 'id': "level1-s" + str(count),
            'playorder': str(count + 1), 'count': str(count), 'title': i['title'],
            'file': "main" + str(count), 'text': text})
        count += 1


def get_wikisource_work(pub, host, title):
    """
    Get a Wikisource work (typically a book) and put its contents into an epub object.
    """

    wikipagetitle = title
    uri_template = '/w/api.php?format=xml&action=query&prop=revisions' \
                   '&titles=%(title)s&rvprop=content|timestamp|user|ids'
    uri = uri_template % {'title': wikipagetitle}
    text = read_file(uri)
    print "uri", uri
    text = mediawikibook.parse_mediawiki_xml(text)
    info = mediawikibook.parse_wikisource_contents(text)
    info['source'] = "Wikisource"
    pub.set(info['title'], info['author'], info['author_as'], info['published'], info['source'])
    # add the title page
    pub.add_section({'title': "Title", 'text': info['title']})
    if len(info['sections']) == 0:
        mediawikibook.add_section(epub, host, wikipagetitle, text)
    else:
        mediawikibook.add_sections(epub, info['sections'], host, wikipagetitle)
    return epub


def test_Great_Expectations():
    """Test using data based on Great Expectations"""
    text = read_file("test/data/Great Expectations.txt")
    info = mediawikibook.parse_wikisource_contents(text)
    assert info['title'] == "Great Expectations"
    assert info['author'] == "Charles Dickens"
    sections = info['sections']
    assert sections[0] == {'wikisubpage': '/Chapter_I', 'title': 'Chapter I'}


def test_Through_the_Looking_Glass():
    """Test using data based on Through the Looking-Glass"""
    title = "Through the Looking-Glass, and What Alice Found There"
    bookdir = "epub/books/" + title
    pub = epub.EPub(bookdir)
    text = read_file("test/data/" + title + ".txt")
    #text = mediawikibook.parse_mediawiki_xml(text)
    info = mediawikibook.parse_wikisource_contents(text)
    assert info['title'] == "Through the Looking-Glass, and What Alice Found There"
    assert info['author'] == "Lewis Carroll"
    sections = info['sections']
    print sections
    assert sections[0] == {'wikisubpage': '/Preface',
                           'title': 'Poem: Child of the pure unclouded brow'}
    assert sections[1] == {'wikisubpage': '/Chapter_I',
                           'title': 'Chapter I: Looking-Glass House'}
    assert sections[2] == {'wikisubpage': '/Chapter_II',
                           'title': 'Chapter II: The Garden of Live Flowers'}
    sections = sections[0:2]
    info['source'] = "Wikisource"
    print "sss:", sections
    pub.set(info['title'], info['author'], info['author_as'], info['published'], info['source'])
    # add the title page
    pub.add_section({'title': "Title", 'text': info['title']})
    #add_sections(pub, sections, "test/data/" + title)
    add_sections(pub, sections, "test/data/" + "alice")
    pub.write_epub()
    pub.zip_epub()

    #assert False


def test_Treasure_Island():
    """Test using data based on Treasure Island"""
    text = read_file("test/data/Treasure Island.txt")
    info = mediawikibook.parse_wikisource_contents(text)
    assert info['title'] == "Treasure Island"
    assert info['author'] == "Robert Louis Stevenson"
    sections = info['sections']
    assert sections[0] == {'wikisubpage': '/Chapter_1',
                           'title': 'Chapter 1: The Old Sea-dog at the Admiral Benbow'}


def main():
    """
    Test the parsing of wikisource book contents pages.
    """

    test_Through_the_Looking_Glass()
    test_Great_Expectations()
    test_Treasure_Island()


if __name__ == "__main__":
    main()
