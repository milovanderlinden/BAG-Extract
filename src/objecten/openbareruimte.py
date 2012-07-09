from objecten.gerelateerdewoonplaats import Gerelateerdewoonplaats
from objecten.tijdvakgeldigheid import Tijdvakgeldigheid
from objecten.bron import Bron

class Openbareruimte():
    """
    BAG Klasse Openbareruimte
    Class voor het BAG-objecttype Openbareruimte.
    """
    
    def __init__(self, xmlnode, configuratie):
        self.config = configuratie
        self.tag = "bag_LVC:OpenbareRuimte"
        self.naam = "OpenbareRuimte"
        self.type = 'OPR'
        
        mydb = self.config.get_database()
        for node in xmlnode.childNodes:
            if node.localName == 'bron':
                self.bron = Bron(node, self.config)
            if node.localName == 'tijdvakgeldigheid':
                self.tijdvakgeldigheid = Tijdvakgeldigheid(node, self.config)
            if node.localName == 'identificatie':
                self.identificatie = mydb.getText(node.childNodes)
            if node.localName == 'aanduidingRecordInactief':
                self.inactief = mydb.getBoolean(node.childNodes)
            if node.localName == 'aanduidingRecordCorrectie':
                self.correctie = mydb.getText(node.childNodes)
            if node.localName == 'officieel':
                self.officieel = mydb.getBoolean(node.childNodes)
            if node.localName == 'inOnderzoek':
                self.inonderzoek = mydb.getBoolean(node.childNodes)
            if node.localName == 'openbareRuimteNaam':
                self.naam = mydb.getText(node.childNodes)
            if node.localName == 'openbareruimteStatus':
                #let op! kleine r van ruimte, is dit een fout in de xml?
                self.status = mydb.getText(node.childNodes)
            if node.localName == 'openbareRuimteType':
                self.type = mydb.getText(node.childNodes)
            if node.localName == 'gerelateerdeWoonplaats':
                self.gerelateerdewoonplaats = Gerelateerdewoonplaats(node, self.config)

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
            begindatumtijdvakgeldigheid,
            einddatumtijdvakgeldigheid)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        self.valuelist = (self.identificatie, self.inactief, \
            self.correctie, self.officieel, self.inonderzoek, \
            self.bron.documentnummer, self.bron.documentdatum, \
            self.naam, self.type, self.status, self.gerelateerdewoonplaats.identificatie,self.tijdvakgeldigheid.begindatum, self.tijdvakgeldigheid.einddatum)
    
    @staticmethod
    def drop(schema):
        return "DROP TABLE IF EXISTS " + schema + ".openbareruimte CASCADE;"
        
    @staticmethod
    def create(schema):
        return """CREATE TABLE """ + schema + """.openbareruimte (
                    gid serial,
                    identificatie numeric(16,0),
                    aanduidingrecordinactief boolean,
                    aanduidingrecordcorrectie integer,
                    officieel boolean,
                    inonderzoek boolean,
                    begindatumtijdvakgeldigheid timestamp without time zone,
                    einddatumtijdvakgeldigheid timestamp without time zone,
                    documentnummer character varying(20),
                    documentdatum date,
                    openbareruimtenaam character varying(80),
                    openbareruimtestatus character varying(80),
                    openbareruimtetype character varying(40),
                    gerelateerdewoonplaats numeric(16,0),
                    verkorteopenbareruimtenaam character varying(80),
                    PRIMARY KEY (gid)
                );"""

