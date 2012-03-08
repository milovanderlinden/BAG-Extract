import datetime
import time
import xml.dom.minidom as dom

class Openbareruimte():
    """
    BAG Klasse Openbareruimte
    Class voor het BAG-objecttype Openbareruimte.
    """
    
    def __init__(self,xmlnode):
        self.tag = "bag_LVC:OpenbareRuimte"
        self.naam = "OpenbareRuimte"
        self.type = 'OPR'
        for node in xmlnode.childNodes:
            if node.localName == 'bron':
                self.bron = Bron(node)
            if node.localName == 'tijdvakgeldigheid':
                self.tijdvakgeldigheid = Tijdvakgeldigheid(node)
            if node.localName == 'identificatie':
                self.identificatie = getText(node.childNodes)
            if node.localName == 'aanduidingRecordInactief':
                self.inactief = getText(node.childNodes)
            if node.localName == 'aanduidingRecordCorrectie':
                self.correctie = getText(node.childNodes)
            if node.localName == 'officieel':
                self.officieel = getText(node.childNodes)
            if node.localName == 'inOnderzoek':
                self.inonderzoek = getText(node.childNodes)
            if node.localName == 'openbareRuimteNaam':
                self.naam = getText(node.childNodes)
            if node.localName == 'openbareruimteStatus':
                #let op! kleine r van ruimte, is dit een fout in de xml?
                self.status = getText(node.childNodes)
            if node.localName == 'openbareRuimteType':
                self.type = getText(node.childNodes)
            if node.localName == 'gerelateerdeWoonplaats':
                self.gerelateerdewoonplaats = Gerelateerdewoonplaats(node)

    def __repr__(self):
       return "<OpenbareRuimte('%s','%s', '%s', '%s')>" % (self.identificatie, self.naam, self.tijdvakgeldigheid, self.bron)

    def insert(self):
        self.sql = """INSERT INTO openbareruimte (
            identificatie,
            aanduidingrecordinactief,
            aanduidingrecordcorrectie,
            officieel,
            inonderzoek,
            documentnummer,
            documentdatum,
            openbareruimtenaam,
            openbareruimtestatus,
            openbareruimtetype,
            gerelateerdewoonplaats,
            begindatum,
            einddatum)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        self.valuelist = (self.identificatie, self.inactief, \
            self.correctie, self.officieel, self.inonderzoek, \
            self.bron.documentnummer, self.bron.documentdatum, \
            self.naam, self.type, self.status, self.gerelateerdeWoonplaats.identificatie,self.tijdvakgeldigheid.begindatum, self.tijdvakgeldigheid.einddatum)
    
    drop = "DROP TABLE IF EXISTS openbareruimte CASCADE;"
        
    create = """CREATE TABLE openbareruimte (
                    gid serial,
                    identificatie numeric(16,0),
                    aanduidingrecordinactief boolean,
                    aanduidingrecordcorrectie integer,
                    officieel boolean,
                    inonderzoek boolean,
                    documentnummer character varying(20),
                    documentdatum date,
                    openbareruimtenaam character varying(80),
                    openbareruimtestatus character varying(80),
                    openbareruimtetype character varying(40),
                    gerelateerdewoonplaats numeric(16,0),
                    verkorteopenbareruimtenaam character varying(80),
                    begindatumtijdvakgeldigheid timestamp without time zone,
                    einddatumtijdvakgeldigheid timestamp without time zone,
                    PRIMARY KEY (gid)
                );"""

