"""
Test the xml conversion.
"""

#import epub.mediawikibook
from epub import mediawikibook


def test_xml():
    """Test reading a file that contains non-ascii data."""
    print "Testing alice preface"
    title = "Through the Looking-Glass, and What Alice Found There"
    title = "alice"
    filename = "test/data/" + title + "/Preface.txt"
    FILE = open(filename, "r")
    text = FILE.read()
    FILE.close()
    print "isinstance1", isinstance(text, unicode)
    text = text.decode("mac_roman")  # from latin-1 to unicode
    print "isinstance2", isinstance(text, unicode)
    #text = text.encode("latin-1")  # from unicode to latin-1


def main():
    """
    Test the reading of xml utf-8 files.
    """

    test_xml()


if __name__ == "__main__":
    main()
