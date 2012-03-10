from objecten.gerelateerdeadressen import Gerelateerdeadressen
from objecten.tijdvakgeldigheid import Tijdvakgeldigheid
from objecten.bron import Bron

class Standplaats():
    def __init__(self, xmlnode, configuratie):
        self.config = configuratie
        self.tag = "bag_LVC:Standplaats"
        self.naam = "standplaats"
        self.type = 'STA'
        
        mydb = self.config.get_database()
        for node in xmlnode.childNodes:
            if node.localName == 'gerelateerdeAdressen':
                self.gerelateerdeAdressen = Gerelateerdeadressen(node, self.config)
            if node.localName == 'bron':
                self.bron = Bron(node, self.config)
            if node.localName == 'tijdvakgeldigheid':
                self.tijdvakgeldigheid = Tijdvakgeldigheid(node, self.config)
            if node.localName == 'identificatie':
                self.identificatie =  mydb.getText(node.childNodes)
            if node.localName == 'aanduidingRecordInactief':
                self.inactief =  mydb.getBoolean(node.childNodes)
            if node.localName == 'aanduidingRecordCorrectie':
                self.correctie =  mydb.getText(node.childNodes)
            if node.localName == 'officieel':
                self.officieel =  mydb.getBoolean(node.childNodes)
            if node.localName == 'inOnderzoek':
                self.inonderzoek =  mydb.getBoolean(node.childNodes)
            if node.localName == 'standplaatsStatus':
                self.status = mydb.getText(node.childNodes)
            if node.localName == 'standplaatsGeometrie':
                for geometrie in node.childNodes:
                   # sla pure tekst nodes over
                    if geometrie.nodeType == node.TEXT_NODE:
                        continue
                    self.geometrie = geometrie.toxml()

    def __repr__(self):
       return "<Standplaats('%s','%s', '%s', '%s')>" % (self.identificatie, self.gerelateerdeAdressen, self.tijdvakgeldigheid, self.bron)

    def insert(self):
        self.sql = """INSERT INTO """ + self.config.schema + """.standplaats (identificatie, aanduidingrecordinactief,
            aanduidingrecordcorrectie, officieel, inonderzoek, documentnummer, documentdatum, hoofdadres,
            standplaatsstatus, begindatumtijdvakgeldigheid, einddatumtijdvakgeldigheid, geometrie) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s,ST_GeomFromGml(%s))"""
        self.valuelist = (self.identificatie, self.inactief, \
            self.correctie, self.officieel, self.inonderzoek, self.bron.documentnummer, self.bron.documentdatum, \
            self.gerelateerdeAdressen.hoofdadres, self.status, self.tijdvakgeldigheid.begindatum, \
            self.tijdvakgeldigheid.einddatum, self.geometrie)

    @staticmethod    
    def drop(schema):
        return "DROP TABLE IF EXISTS " + schema + ".standplaats CASCADE;"
    
    @staticmethod    
    def create(schema):
        return  """CREATE TABLE """ + schema + """.standplaats (
                  gid serial,
                  identificatie numeric(16,0),
                  aanduidingrecordinactief boolean,
                  aanduidingrecordcorrectie integer,
                  officieel boolean,
                  inonderzoek boolean,
                  documentnummer character varying(20),
                  documentdatum date,
                  hoofdadres numeric(16,0),
                  standplaatsstatus character varying(80),
                  begindatumtijdvakgeldigheid timestamp without time zone,
                  einddatumtijdvakgeldigheid timestamp without time zone,
                  geometrie geometry,
                  PRIMARY KEY (gid),
                  CONSTRAINT enforce_dims_geometrie CHECK ((st_ndims(geometrie) = 3)),
                  CONSTRAINT enforce_geotype_geometrie CHECK (
                          ((geometrytype(geometrie) = 'POLYGON'::text) OR (geometrie IS NULL))),
                  CONSTRAINT enforce_srid_geometrie CHECK ((st_srid(geometrie) = 28992))
                );"""

