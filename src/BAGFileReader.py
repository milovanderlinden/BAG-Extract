__author__ = "Milo van der Linden"
__date__ = "$Jun 11, 2011 3:46:27 PM$"

import zipfile
import logger
import orm
import os
from xml.dom.minidom import parse

try:
  from cStringIO import StringIO
except:
  from StringIO import StringIO

class BAGFileReader:
    def __init__(self, file, args):
        self.args = args
        self.file = file
        self.init = True
        self.log = logger.LogHandler(args)
        self.orm = orm.Orm(args)

    def process(self):
        if zipfile.is_zipfile(self.file):
            self.zip = zipfile.ZipFile(self.file, "r")
            self.readzipfile()
        else:
            zipfilename = os.path.basename(self.file).split('.')
            ext = zipfilename[1]
            #controleer of het dan een xml bestand is
            if ext == 'xml':
                xml = parse(self.file)
                self.processXML(zipfilename[0],xml)


    def readzipfile(self):
        tzip = self.zip
        for name in tzip.namelist():
            ext = name.split('.')
            if ext[1] == 'xml':
                self.log.log(name)
                xml = parse(StringIO(tzip.read(name)))
                self.processXML(name, xml)
            elif ext[1] == 'zip':
                self.log.log(name)
                self.readzipstring(StringIO(tzip.read(name)))
            else:
                self.log.log(name)

    def readzipstring(self,name):
        tzip = zipfile.ZipFile(name, "r")

        for nested in tzip.namelist():
            ext = nested.split('.')
            if ext[1] == 'xml':
                self.log.log(nested)
                xml = parse(StringIO(tzip.read(nested)))
                self.processXML(nested, xml)
            elif ext[1] == 'zip':
                self.log.log(nested)
                self.readzipstring(StringIO(tzip.read(nested)))
            else:
                self.log.log(nested)

    def processXML(self,file, xml):
        print file
        rootObj = xml.documentElement
        #de orm bepaalt of het een extract of een mutatie is
        document = self.orm.getDocument(rootObj) 
        self.log.log(document)
        xml.unlink()
        