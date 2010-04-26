#!/bin/env python
#coding=utf-8
#file: epub.py


"""
Epub class to support writing publications in epub format.
"""

#import re
import os.path
from jinja2 import Environment, PackageLoader
import zipfile


class EPub():
    """
    Class to support writing publications in epub format.
    Has methods to set the publication's metadata and content,
    and to write out that content to .epub files.
    """

    def __init__(self, bookdir):
        self.env = Environment(loader=PackageLoader('epub', 'templates'))
        self.sections = []
        self.bookdir = os.path.join(os.curdir, bookdir)
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
        self.xml_ext = ".xml"
        self.opsdir = ""
        self.stylesheets = {'page': "page.css", 'titlepage': "titlepage.css", 'about': "about.css", 'main': "main.css"}

    def set(self, title, author, author_as, published, source):
        """Set the common attributes for the publication."""
        self.title = title
        self.author = author
        self.author_as = author_as
        self.published = published
        self.source = source

    def set_uuid(self, uuid):
        """Set the uuid for the publication."""
        self.uuid = uuid

    def add_section(self, section):
        """Add a section to the publication."""
        self.sections.append(section)

    def write_file(self, dirname, filename, content):
        """Utility function to write a file."""
        filename = os.path.join(dirname, filename)
        FILE = open(filename, "w")
        FILE.write(content.encode("utf-8"))
        FILE.close()

    def write_mime_type(self):
        """Write out the epub mimetype file."""
        self.write_file(self.bookdir, "mimetype", "application/epub+zip")

    def write_meta_inf(self):
        """Write the publication's meta information file."""
        metainfdir = os.path.join(self.bookdir, "META-INF")
        if not os.path.isdir(metainfdir):
            os.makedirs(metainfdir)
        template = self.env.get_template("container.xml")
        s = template.render({'file': self.opffilename})
        self.write_file(metainfdir, "container" + self.xml_ext, s)

    def write_stylesheets(self):
        """
        Write out the stylesheets for the publication, using the templates.
        """
        cssdir = os.path.join(self.opsdir, "css")
        if not os.path.isdir(cssdir):
            os.makedirs(cssdir)
        for i in self.stylesheets:
            template = self.env.get_template(self.stylesheets[i])
            s = template.render()
            self.write_file(cssdir, self.stylesheets[i], s)

    def write_images(self):
        """Write an empty image directory."""
        imagedir = os.path.join(self.opsdir, "images")
        if not os.path.isdir(imagedir):
            os.makedirs(imagedir)

    def write_opf(self):
        """Write the opf(Open Packaging Format) file."""
        template = self.env.get_template("content.opf")
        s = template.render({'title': self.title, 'uuid': self.uuid, 'language': self.language,
            'author': self.author, 'author_as': self.author_as, 'description': self.description,
            'publisher': self.publisher, 'source': self.source, 'published': self.published,
            'ncxfile': self.ncxfilename, 'rights': self.rights, 'stylesheets': self.stylesheets,
            'sections': self.sections})
        self.write_file(self.opsdir, self.opffilename, s)

    def write_ncx(self):
        """Write the ncx(Navigation Center for XML) file."""
        template = self.env.get_template("toc.ncx")
        s = template.render({'uid': self.uuid, 'depth': self.depth, 'title': self.title,
            'author': self.author_as, 'sections': self.sections})
        self.write_file(self.opsdir, self.ncxfilename, s)

    def write_title(self, filename):
        """Write the publication's titlepage."""
        css = self.stylesheets['titlepage']
        template = self.env.get_template("titlepage.xml")
        s = template.render({'title': self.title, 'css': css, 'author': self.author, 'published': self.published, 'source': self.source})
        self.write_file(self.opsdir, filename, s)

    def write_chapter(self, section):
        """Write a file for a chapter in the publication."""
        css = self.stylesheets['main']
        #if section['title'].find("section")==-1:
        #<span class="translation">{{ translation }}</span> <span class="count">{{ count }}</span>
        #extra = extra % {'translation': self.sectionTranslation, 'count': section['count']}
        template = self.env.get_template("main.xml")
        s = template.render({'css': css, 'id': section['id'], 'class': section['class'], 'title': section['title'], 'text': section['text']})
        self.write_file(self.opsdir, section['file'] + self.xml_ext, s)

    def write_content(self):
        """Iterate through the sections, writing each out appropriately."""
        for i in self.sections:
            if i['class'] == "title":
                self.write_title(i['file'] + self.xml_ext)
            else:
                self.write_chapter(i)

    def write_ops(self):
        """Write the ops(Open Publication Structure) file."""
        self.opsdir = os.path.join(self.bookdir, "OPS")
        if not os.path.isdir(self.opsdir):
            os.makedirs(self.opsdir)
        self.write_opf()
        self.write_ncx()
        self.write_stylesheets()
        #self.writeImages()
        self.write_content()

    def write_epub(self):
        """Write out the epub directory."""
        self.write_mime_type()
        self.write_meta_inf()
        self.write_ops()

    def zip_epub(self):
        """Zip up the epub directory contents into an .epub file"""
        zip_file = zipfile.ZipFile(self.title + '.epub', 'w')
        cwd = os.getcwd()
        os.chdir(self.bookdir)
        for root, dirs, files in os.walk('.'):
            for filename in files:
                if filename[0] != '.':
                    zip_file.write(os.path.join(root, filename))
        zip_file.close()
        os.chdir(cwd)
