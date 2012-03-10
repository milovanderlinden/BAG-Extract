from objecten.tijdvakgeldigheid import Tijdvakgeldigheid
from objecten.bron import Bron

class Pand():

    def __init__(self, xmlnode, configuratie):
        self.config = configuratie
        self.tag = "bag_LVC:Pand"
        self.naam = "Pand"
        self.type = 'PND'
        
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
            if node.localName == 'pandstatus':
                self.status = mydb.getText(node.childNodes)
            if node.localName == 'bouwjaar':
                self.bouwjaar = mydb.getText(node.childNodes)
            if node.localName == 'pandGeometrie':
                for geometrie in node.childNodes:
                    # sla pure tekst nodes over
                    if geometrie.nodeType == node.TEXT_NODE:
                        continue
                    self.geometrie = geometrie.toxml()

    def __repr__(self):
       return "<Pand('%s','%s', '%s', '%s')>" % (self.identificatie, self.status, self.tijdvakgeldigheid, self.bron)

    def insert(self):
        self.sql = """INSERT INTO """ + self.config.schema + """.pand (
            identificatie,
            aanduidingrecordinactief,
            aanduidingrecordcorrectie,
            officieel,
            inonderzoek,
            documentnummer,
            documentdatum,
            pandstatus,
            bouwjaar,
            begindatumtijdvakgeldigheid,
            einddatumtijdvakgeldigheid,
            geometrie)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, ST_GeomFromGML(%s))"""
        self.valuelist = (self.identificatie, self.inactief, \
            self.correctie, self.officieel, self.inonderzoek, self.bron.documentnummer, self.bron.documentdatum, \
            self.status, self.bouwjaar, self.tijdvakgeldigheid.begindatum, \
            self.tijdvakgeldigheid.einddatum, self.geometrie)
            
    @staticmethod
    def drop(schema):
        return "DROP TABLE IF EXISTS " + schema + ".pand CASCADE;"
     
    @staticmethod
    def create(schema):
        return """CREATE TABLE """ + schema + """.pand (
                  gid serial,
                  identificatie numeric(16,0),
                  aanduidingrecordinactief boolean,
                  aanduidingrecordcorrectie integer,
                  officieel boolean,
                  inonderzoek boolean,
                  documentnummer character varying(20),
                  documentdatum date,
                  pandstatus character varying(80),
                  bouwjaar numeric(4,0),
                  begindatumtijdvakgeldigheid timestamp without time zone,
                  einddatumtijdvakgeldigheid timestamp without time zone,
                  geometrie geometry,
                  PRIMARY KEY (gid),
                  CONSTRAINT enforce_dims_geometrie CHECK ((st_ndims(geometrie) = 3)),
                  CONSTRAINT enforce_geotype_geometrie CHECK (
                          ((geometrytype(geometrie) = 'POLYGON'::text) OR (geometrie IS NULL))),
                  CONSTRAINT enforce_srid_geometrie CHECK ((st_srid(geometrie) = 28992))
                );"""

