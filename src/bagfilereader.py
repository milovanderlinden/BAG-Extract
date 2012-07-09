"""
 Naam: bagfilereader.py
 Omschrijving: Inlezen van BAG-gerelateerde files of directories
 Auteur(s): Milo van der Linden Just van den Broecke
"""

import os
import sys

try:
    import zipfile
except:
    formatter = logging.Formatter('%(levelname)s - %(message)s')
    logging.critical("Python zipfile is vereist")
    sys.exit()

from xml.dom.minidom import parse
import csv

#from lxml import etree

#Onderstaand try/catch blok is vereist voor python2/python3 portabiliteit
try:
    from io import StringIO #Python3
    from io import BytesIO #Python3
except:
    try:
        from cStringIO import StringIO #probeer cStringIO, faster
    except:
        from StringIO import StringIO #StringIO, standaard

class BAGFilereader:
    def __init__(self, configuratie):
        self.config = configuratie

    def process(self):
        self.config.logger.debug("bagfilereader.process()")
        if not os.path.exists(self.config.extract):
            logging.critical(self.config.extract + " niet gevonden")
            sys.exit()

        # TODO: Verwerk een directory
        if os.path.isdir(self.config.extract) == True:
            self.readDir()
        elif zipfile.is_zipfile(self.config.extract):
            self.zip = zipfile.ZipFile(self.config.extract, "r")
            self.readzipfile()
        else:
            zipfilename = os.path.basename(self.config.extract).split('.')
            ext = zipfilename[1]
            if ext == 'xml':
                xml = self.parseXML(self.config.extract)
                self.processXML(zipfilename[0],xml)
            if ext == 'csv':
                fileobject = open(self.config.extract, "rb")
                objecten = self.processCSV(zipfilename[0], fileobject)
                # TODO: verwerken!

    def readDir(self):
        self.config.logger.debug("bagfilereader.readDir()")
        for each in os.listdir(self.config.extract):
            _file = os.path.join(self.config.extract, each)
            if zipfile.is_zipfile(_file):
                self.zip = zipfile.ZipFile(_file, "r")
                self.readzipfile()
            else:
                if os.path.isdir(_file) != True:
                    zipfilename = each.split('.')
                    if len(zipfilename) == 2:
                        ext = zipfilename[1]
                        if ext == 'xml':
                            self.config.logger.info("==> XML File: " + each)
                            xml = self.parseXML(_file)
                            self.processXML(zipfilename[0],xml)
                        if ext == 'csv':
                            self.config.logger.info("==> CSV File: " + each)
                            fileobject = open(_file, "rb")
                            objecten = self.processCSV(zipfilename[0],fileobject)
                            return objecten

    def readzipfile(self):
        self.config.logger.debug("bagfilereader.readzipfile(file)")
        tzip = self.zip
        self.config.logger.info("readzipfile content=" + str(tzip.namelist()))
        for naam in tzip.namelist():
            ext = naam.split('.')
            self.config.logger.info("readzipfile: " + naam)
            if len(ext) == 2:
                if ext[1] == 'xml':
                    try:
                        xml = self.parseXML(BytesIO(tzip.read(naam))) #Python3
                    except:
                        xml = self.parseXML(StringIO(tzip.read(naam)))
                    #xml = etree.parse (StringIO(tzip.read(naam)))
                    self.processXML(naam, xml)
                elif ext[1] == 'zip':
                    try:
                        self.readzipstring(BytesIO(tzip.read(naam))) #Python3
                    except:
                        self.readzipstring(StringIO(tzip.read(naam)))

                elif ext[1] == 'csv':
                    self.config.logger.info(naam)
                    try:
                        fileobject = BytesIO(tzip.read(naam)) #Python3
                    except:
                        fileobject = StringIO(tzip.read(naam))

                    objecten = self.processCSV(naam, fileobject)
                    return objecten
                else:
                    self.config.logger.warn("Negeer: " + naam)

    def readzipstring(self,naam):
        self.config.logger.debug("bagfilereader.readzipstring(naam)")
        # logging.info("readzipstring naam=" + naam)
        tzip = zipfile.ZipFile(naam, "r")
        # logging.info("readzipstring naam=" + tzip.getinfo().filename)

        for nested in tzip.namelist():
            self.config.logger.info("readzipstring: " + nested)
            ext = nested.split('.')
            if len(ext) == 2:
                if ext[1] == 'xml':
                    try:
                        xml = self.parseXML(BytesIO(tzip.read(nested)))
                    except:
                        xml = self.parseXML(StringIO(tzip.read(nested)))

                    #xml = etree.parse(StringIO(tzip.read(nested)))
                    self.processXML(nested, xml)
                elif ext[1] == 'csv':
                    #Log.log.info(nested)
                    try:
                        fileobject = BytesIO(tzip.read(nested))
                    except:
                        fileobject = StringIO(tzip.read(nested))

                    objecten = self.processCSV(nested, fileobject)
                    return objecten

                elif ext[1] == 'zip':
                    try:
                        self.readzipstring(BytesIO(tzip.read(nested)))
                    except:
                        self.readzipstring(StringIO(tzip.read(nested)))
                else:
                    self.config.logger.info("Negeer: " + nested)

    def parseXML(self,naam):
        self.config.logger.debug("bagfilereader.parseXML(naam)")
        #Log.log.startTimer("parseXML")
        xml = parse(naam)
        #Log.log.endTimer("parseXML")
        return xml

    def processXML(self, naam, xml):
        self.config.logger.debug("bagfilereader.processXML(naam, xml)")
        #self.config.logger.info("processXML: " + naam)
        xmldoc = xml.documentElement
        self.processDOM(xmldoc)
        xml.unlink()

    def processDOM(self, node):
        self.config.logger.debug("bagfilereader.processDOM(naam, xml)")
        
        from objecten.ligplaats import Ligplaats
        from objecten.standplaats import Standplaats
        from objecten.pand import Pand
        from objecten.nummeraanduiding import Nummeraanduiding
        from objecten.woonplaats import Woonplaats

        self.ligplaatsen = []
        self.verblijfsobjecten = []
        self.openbareRuimten = []
        self.nummeraanduidingen = []
        self.standplaatsen = []
        self.panden = []
        self.woonplaatsen = []
        
        mode = "Onbekend"

        if node.localName == 'BAG-Extract-Deelbestand-LVC':
            mode = 'Nieuw'
            #firstchild moet zijn 'antwoord'
            for childNode in node.childNodes:
                if childNode.localName == 'antwoord':
                    # Antwoord bevat twee childs: vraag en producten
                    antwoord = childNode
                    for child in antwoord.childNodes:
                        if child.localName == "vraag":
                            # TODO: Is het een idee om vraag als object ook af te
                            # handelen en op te slaan
                            vraag = child
                        elif child.localName == "producten":
                            producten = child
                            #Log.log.startTimer("objCreate")
                            for productnode in producten.childNodes:
                                if productnode.localName == 'LVC-product':
                                    for node in productnode.childNodes:
                                        if node.localName == 'Ligplaats':
                                            _obj = Ligplaats(node, self.config)
                                            self.ligplaatsen.append(_obj)
                                        elif node.localName == 'Woonplaats':
                                            _obj = Woonplaats(node, self.config)
                                            self.woonplaatsen.append(_obj)
                                        elif node.localName == 'Verblijfsobject':
                                            _obj = Verblijfsobject()
                                        elif node.localName == 'OpenbareRuimte':
                                            _obj = OpenbareRuimte()
                                        elif node.localName == 'Nummeraanduiding':
                                            _obj = Nummeraanduiding(node, self.config)
                                            self.nummeraanduidingen.append(_obj)
                                        elif node.localName == 'Standplaats':
                                            _obj = Standplaats(node,self.config)
                                            self.standplaatsen.append(_obj)
                                        elif node.localName == 'Pand':
                                            _obj = Pand(node, self.config)
                                            self.panden.append(_obj)    
                                           
                            mydb = self.config.get_database()
                            mydb.verbind()
                            
                            # TODO Momenteel worden de database acties geloopt en wordt elk individueel record gecommit.
                            # Ik denk erover om de commits te centraliseren en commitloops van bepaalde volumes te maken, b.v. een commitloop per duizend
                            # Dat maakt rollbacks ook eenvoudiger
                            for woonplaats in self.woonplaatsen:
                                woonplaats.insert()

                            mydb.bulk(self.woonplaatsen)

                            for ligplaats in self.ligplaatsen:
                                #array per bestand? Even kijken of het geheugen dat aan kan.
                                ligplaats.insert()

                            mydb.bulk(self.ligplaatsen)            

                            for nummeraanduiding in self.nummeraanduidingen:
                                nummeraanduiding.insert()
                                mydb.uitvoeren(nummeraanduiding.sql, nummeraanduiding.valuelist)

                            for standplaats in self.standplaatsen:
                                standplaats.insert()
                                mydb.uitvoeren(standplaats.sql, standplaats.valuelist)

                            for pand in self.panden:
                                pand.insert()
                                mydb.uitvoeren(pand.sql, pand.valuelist)

        elif node.localName == 'BAG-Mutaties-Deelbestand-LVC':
            mode = 'Mutatie'
            #firstchild moet zijn 'antwoord'
            for childNode in node.childNodes:
                if childNode.localName == 'antwoord':
                    # Antwoord bevat twee childs: vraag en producten
                    antwoord = childNode
                    for child in antwoord.childNodes:
                        if child.localName == "producten":
                            producten = child
                            #Log.log.startTimer("objCreate (mutaties)")
                            for productnode in producten.childNodes:
                                if productnode.localName == 'Mutatie-product' and productnode.childNodes:
                                    origineelObj = None
                                    nieuwObj = None
                                    for mutatienode in productnode.childNodes:
                                        if mutatienode.localName == 'Nieuw':
                                            #Log.log.info("Nieuw Object")
                                            self.bagObjecten.extend(
                                                BAGObjectFabriek.bof.BAGObjectArrayBijXML(mutatienode.childNodes))
                                        elif mutatienode.localName == 'Origineel':
                                            objs = BAGObjectFabriek.bof.BAGObjectArrayBijXML(mutatienode.childNodes)
                                            if len(objs) > 0:
                                                origineelObj = objs[0]
                                        elif mutatienode.localName == 'Wijziging':
                                            objs = BAGObjectFabriek.bof.BAGObjectArrayBijXML(mutatienode.childNodes)

                                            if len(objs) > 0:
                                                nieuwObj = objs[0]
                                                if nieuwObj and origineelObj:
                                                    nieuwObj.origineelObj = origineelObj
                                                    self.bagObjecten.append(nieuwObj)
                                                    #Log.log.info("Wijziging Object")
                                                    origineelObj = None
                                                    nieuwObj = None

        else:
            BAGConfig.logger.warn("kan node niet verwerken: " + node.localName)
            return


    def processCSV(self,naam, fileobject):
        self.config.logger.debug("bagfilereader.processCSV(naam, fileobject)")
        self.config.logger.info(naam)
        # TODO: zorg voor de verwerking van het geparste csv bestand
        # Maak er gemeente_woonplaats objecten van overeenkomstig de nieuwe
        # tabel woonplaats_gemeente

        # TODO: Dirty version hack. Er blijkt in python2 ook een TextIOWrapper te zitten, maar deze veroorzaakt
        #       encoding issues die ik zo snel niet kreeg opgelost. Zo dan maar:
        if sys.version_info[0] == 3:
            from io import TextIOWrapper
            myReader = csv.reader(TextIOWrapper(fileobject,'iso-8859-15'), delimiter=';', quoting=csv.QUOTE_NONE)
        elif sys.version_info[0] == 2:
            myReader = csv.reader(fileobject, delimiter=';', quoting=csv.QUOTE_NONE)

        objecten = []
        cols = next(myReader)
        for record in myReader:
            if record[0]:
                if cols[0] == 'Woonplaats':
                    from objecten.gemeentewoonplaats import Gemeentewoonplaats
                    _obj = Gemeentewoonplaats(record, self.config)
                    
                elif cols[1] == 'Gemcodel':
                    _obj = Gemeenteprovincie(record)
    
                if _obj:
                    objecten.append(_obj)
                else:
                    self.config.logger.warn("Geen object gevonden voor " + str(record))
                    
        # Verwerk het bestand, lees gemeente_woonplaatsen in de database
        self.config.logger.info("%s objecten gevonden in bestand" % str(len(objecten)))
        mydb = self.config.get_database()
        mydb.verbind()
        mydb.connection.set_client_encoding('LATIN1')
        
        for object in objecten:
            object.insert()
            mydb.uitvoeren(object.sql, object.valuelist)
        mydb.connection.commit()

