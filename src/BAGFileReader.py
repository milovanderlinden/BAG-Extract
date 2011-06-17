__author__ = "Milo van der Linden"
__date__ = "$Jun 11, 2011 3:46:27 PM$"

import zipfile
import logger
import orm
import os
from xml.dom.minidom import parse
#from lxml import etree
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
        # TODO: Verwerk een directory
        if os.path.isdir(self.file) == True:
            self.readDir()
        elif zipfile.is_zipfile(self.file):
            self.zip = zipfile.ZipFile(self.file, "r")
            self.readzipfile()
        else:
            zipfilename = os.path.basename(self.file).split('.')
            ext = zipfilename[1]
            #controleer of het dan een xml bestand is
            if ext == 'xml':
                xml = parse(self.file)
                #xml = etree.parse (self.file)
                self.processXML(zipfilename[0],xml)

    def readDir(self):
        for each in os.listdir(self.file):
            _file = os.path.join(self.file, each)
            if zipfile.is_zipfile(_file):
                self.zip = zipfile.ZipFile(_file, "r")
                self.readzipfile()
            else:
                if os.path.isdir(_file) <> True:
                    zipfilename = each.split('.')
                    if len(zipfilename) == 2:
                        ext = zipfilename[1]
                        if ext == 'xml':
                            print each
                            xml = parse(_file)
                            #xml = etree.parse (_file)
                            self.processXML(zipfilename[0],xml)

    def readzipfile(self):
        tzip = self.zip
        for naam in tzip.namelist():
            ext = naam.split('.')
            if ext[1] == 'xml':
                self.log.log(naam)
                xml = parse(StringIO(tzip.read(naam)))
                #xml = etree.parse (StringIO(tzip.read(naam)))
                self.processXML(naam, xml)
            elif ext[1] == 'zip':
                self.log.log(naam)
                self.readzipstring(StringIO(tzip.read(naam)))
            else:
                self.log.log(naam)

    def readzipstring(self,naam):
        tzip = zipfile.ZipFile(naam, "r")

        for nested in tzip.namelist():
            ext = nested.split('.')
            if ext[1] == 'xml':
                self.log.log(nested)
                xml = parse(StringIO(tzip.read(nested)))
                #xml = etree.parse(StringIO(tzip.read(nested)))
                self.processXML(nested, xml)
            elif ext[1] == 'zip':
                self.log.log(nested)
                self.readzipstring(StringIO(tzip.read(nested)))
            else:
                self.log.log(nested)

    def processXML(self,naam, xml):
        self.log.log(naam)
        xmldoc = xml.documentElement
        #xmldoc = xml.getroot()
        #de orm bepaalt of het een extract of een mutatie is
        self.orm.getDocument(xmldoc)
        #self.log.log(document)
        xml.unlink()
        