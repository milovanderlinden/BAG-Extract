# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__ = "miblon"
__date__ = "$Jun 11, 2011 3:46:27 PM$"

import zipfile
#import os
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


class BAGFileReader:
    def __init__(self, file):
        self.file = file
        self.init = True
        self.zip = zipfile.ZipFile(file)
    def process(self):
        #for dirpath, dirnames, filenames in os.walk(dir_to_scan):
        if zipfile.is_zipfile(self.file):
            self.readzipfile()
            #remove the file
            #os.remove(file)

    def readzipfile(self):
        tzip = self.zip
            
        for name in tzip.namelist():
            ext = name.split('.')

            if ext[1] == 'xml':
                print name
            elif ext[1] == 'zip':
                #print "Found zip"
                print name
                self.readzipstring(StringIO(tzip.read(name)))
            else:
                print "Found something useles"

    def readzipstring(self,name):
        tzip = zipfile.ZipFile(name, "r")

        for nested in tzip.namelist():
            #can we insert a record for the file?

            ext = nested.split('.')
            if ext[1] == 'xml':
                print nested
            elif ext[1] == 'zip':
                #print "Found zip"
                print nested
                self.readzipstring(StringIO(tzip.read(nested)))
            else:
                print "Found something useles"