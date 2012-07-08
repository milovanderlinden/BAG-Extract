from objecten.gerelateerdewoonplaats import Gerelateerdewoonplaats
from objecten.gerelateerdeopenbareruimte import Gerelateerdeopenbareruimte
from objecten.tijdvakgeldigheid import Tijdvakgeldigheid
from objecten.bron import Bron

class Nummeraanduiding():

    def __init__(self, xmlnode, configuratie):
        self.config = configuratie
        self.tag = "bag_LVC:Nummeraanduiding"
        self.naam = "Nummeraanduiding"
        self.type = 'NUM'

        self.huisletter = None
        self.huisnummertoevoeging = None
        self.postcode = None
        self.gerelateerdewoonplaats = Gerelateerdewoonplaats(None,self.config)
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
            if node.localName == 'huisnummer':
                self.huisnummer = mydb.getText(node.childNodes)
            if node.localName == 'huisletter':
                self.huisletter = mydb.getText(node.childNodes)
            if node.localName == 'huisnummertoevoeging':
                self.huisnummertoevoeging = mydb.getText(node.childNodes)
            if node.localName == 'postcode':
                self.postcode = mydb.getText(node.childNodes)
            if node.localName == 'nummeraanduidingStatus':
                self.status = mydb.getText(node.childNodes)
            if node.localName == 'typeAdresseerbaarObject':
                self.typeAdresseerbaarObject = mydb.getText(node.childNodes)
            if node.localName == 'gerelateerdeOpenbareRuimte':
                self.gerelateerdeopenbareruimte = Gerelateerdeopenbareruimte(node, self.config)
            if node.localName == 'gerelateerdeWoonplaats':
                self.gerelateerdewoonplaats = Gerelateerdewoonplaats(node, self.config)

    def __repr__(self):
       return "<Nummeraanduiding('%s', '%s', '%s')>" % (self.identificatie, self.tijdvakgeldigheid, self.bron)

    def insert(self):
        self.sql = """INSERT INTO """ + self.config.schema + """.nummeraanduiding (
            identificatie,
            aanduidingrecordinactief,
            aanduidingrecordcorrectie,
            officieel,
            inonderzoek,
            documentnummer,
            documentdatum,
            huisnummer,
            huisletter,
            huisnummertoevoeging,
            postcode,
            nummeraanduidingstatus,
            typeadresseerbaarobject,
            gerelateerdeopenbareruimte,
            gerelateerdewoonplaats,
            begindatumtijdvakgeldigheid,
            einddatumtijdvakgeldigheid)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        self.valuelist = (self.identificatie, self.inactief, \
            self.correctie, self.officieel, self.inonderzoek, \
            self.bron.documentnummer, self.bron.documentdatum, \
            self.huisnummer, self.huisletter, self.huisnummertoevoeging, \
            self.postcode, self.status, self.typeAdresseerbaarObject, \
            self.gerelateerdeopenbareruimte.identificatie, \
            self.gerelateerdewoonplaats.identificatie, self.tijdvakgeldigheid.begindatum, \
            self.tijdvakgeldigheid.einddatum)

    @staticmethod
    def drop(schema):
        return "DROP TABLE IF EXISTS " + schema + ".nummeraanduiding CASCADE;"
    
    @staticmethod
    def create(schema):
        return """CREATE TABLE """ + schema + """.nummeraanduiding (
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
                  huisnummer numeric(5,0),
                  huisletter character varying(1),
                  huisnummertoevoeging character varying(4),
                  postcode character varying(6),
                  nummeraanduidingstatus character varying(80),
                  typeadresseerbaarobject character varying(20),
                  gerelateerdeopenbareruimte numeric(16,0),
                  gerelateerdewoonplaats numeric(16,0),
                  PRIMARY KEY (gid)
                );"""
