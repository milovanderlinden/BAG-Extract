# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__ = "miblon"
__date__ = "$Jun 11, 2011 3:46:27 PM$"

import zipfile
import logger
import orm
import os

#import datetime
#import time
#import xml.dom.minidom
#import psycopg2
#import ConfigParser
#import sys
#import logging
#import logging.handlers
try:
  from cStringIO import StringIO
except:
  from StringIO import StringIO
from xml.dom.minidom import parse

class BAGFileReader:
    def __init__(self, file, args):
        self.args = args
        self.file = file
        self.init = True
        self.log = logger.LogHandler(args)
        self.orm = orm.Orm(args)

    def process(self):
        if zipfile.is_zipfile(self.file):
            self.zip = zipfile.ZipFile(self.file)
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
                #self.log.log(xml)
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
                #self.log.log(xml)
            elif ext[1] == 'zip':
                self.log.log(nested)
                self.readzipstring(StringIO(tzip.read(nested)))
            else:
                self.log.log(nested)

    def processXML(self,file, xml):
    #try:
        #lees het root object om de inhoud te bepalen
        #wandel vervolgens door de boom
        rootObj = xml.documentElement
        document = self.orm.getDocument(rootObj) #bepaal of het een extract of een mutatie is
        self.log.log(document)
        xml.unlink()
    #except Exception, e:
        #self.log.log("*** FOUT *** Fout in verwerking xml-bestand '%s':\n %s" %(file, e))
        #print Exception.message
        #print e
        