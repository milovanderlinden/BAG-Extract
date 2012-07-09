from objecten.tijdvakgeldigheid import Tijdvakgeldigheid
from objecten.bron import Bron
class Woonplaats():
    """
    BAG Klasse Woonplaats
    Class voor het BAG-objecttype Woonplaats.
    """
    
    def __init__(self, xmlnode, configuratie):
        self.config = configuratie
        self.tag = "bag_LVC:Woonplaats"
        self.naam = "Woonplaats"
        self.type = 'WPL'
        
        mydb = self.config.get_database()
        for node in xmlnode.childNodes:
            if node.localName == 'woonplaatsNaam':
                self.naam = mydb.getText(node.childNodes)
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
            if node.localName == 'woonplaatsStatus':
                self.status = mydb.getText(node.childNodes)
            if node.localName == 'woonplaatsGeometrie':
                for geometrie in node.childNodes:
                    # sla pure tekst nodes over
                    if geometrie.nodeType == node.TEXT_NODE:
                        continue
                    import sys
                    self.geometrie = geometrie.toxml()
                    
    def __repr__(self):
       return "<Woonplaats('%s','%s', '%s')>" % (self.tag, self.naam, self.type)
    
    def insert(self):
        _sql = "INSERT INTO " + self.config.schema + ".woonplaats ("
        self.sql = _sql + """identificatie, aanduidingrecordinactief,
            aanduidingrecordcorrectie, officieel, inonderzoek, documentnummer, documentdatum, woonplaatsnaam,
            woonplaatsstatus, 
            begindatumtijdvakgeldigheid, einddatumtijdvakgeldigheid, geometrie) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s,ST_MULTI(ST_GeomFromGML(%s)))"""
        self.valuelist = (self.identificatie, self.inactief, \
            self.correctie, self.officieel, self.inonderzoek, self.bron.documentnummer, self.bron.documentdatum, \
            self.naam, self.status, self.tijdvakgeldigheid.begindatum, \
            self.tijdvakgeldigheid.einddatum, self.geometrie)
        #return self.sql, self.valuelist

    @staticmethod
    def drop(schema):
        return "DROP TABLE IF EXISTS " + schema + ".woonplaats CASCADE;"
    
    @staticmethod
    def create(schema):
        return """CREATE TABLE """ + schema + """.woonplaats (
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
                  woonplaatsnaam character varying(80),
                  woonplaatsstatus character varying(80),
                  geom_valid boolean default TRUE,
                  geometrie geometry,
                  PRIMARY KEY (gid),
                  CONSTRAINT enforce_dims_geometrie CHECK ((st_ndims(geometrie) = 2)),
                  CONSTRAINT enforce_geotype_geometrie CHECK (
                          ((geometrytype(geometrie) = 'MULTIPOLYGON'::text) OR (geometrie IS NULL))),
                  CONSTRAINT enforce_srid_geometrie CHECK ((st_srid(geometrie) = 28992))
                )WITH (
                        OIDS=TRUE
                );"""
