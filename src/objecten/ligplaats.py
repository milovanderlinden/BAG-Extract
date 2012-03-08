from objecten.gerelateerdeadressen import Gerelateerdeadressen
from objecten.tijdvakgeldigheid import Tijdvakgeldigheid
from objecten.bron import Bron

class Ligplaats():
    """
    BAG Klasse Ligplaats
    Class voor het BAG-objecttype Ligplaats.
    """

    #__tablename__ = 'ligplaats'
    #identificatie = Column(Integer, primary_key=True)
    #aanduidingrecordinactief = Column(String(1))
    #aanduidingrecordcorrectie = Column(String(5))
    #officieel = Column(String(1))
    #inonderzoek = Column(String(1))
    #documentnummer = Column(String(20))
    #documentdatum = Column(String(8))
    #hoofdadres  = Column(String(16))
    #ligplaatsstatus = Column(String(80))
    #ligplaatsgeometrie = Column(String(1000000))
    #begindatum = Column(Date)
    #einddatum = Column(Date)
    #geometrie = Column(Geometry)

    def __init__(self, xmlnode, configuratie):
        self.config = configuratie
        self.tag = "bag_LVC:Ligplaats"
        self.naam = "ligplaats"
        self.type = 'LIG'
        
        mydb = self.config.get_database()
        for node in xmlnode.childNodes:
            if node.localName == 'gerelateerdeAdressen':
                self.gerelateerdeAdressen = Gerelateerdeadressen(node, self.config)
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
            if node.localName == 'ligplaatsStatus':
                self.status = mydb.getText(node.childNodes)
            if node.localName == 'ligplaatsGeometrie':
                for geometrie in node.childNodes:
                    # sla pure tekst nodes over
                    if geometrie.nodeType == node.TEXT_NODE:
                        continue
                    #self.config.logger.debug(gml)
                    self.geometrie = geometrie.toxml()

    def __repr__(self):
       return "<Ligplaats('%s','%s', '%s', '%s')>" % (self.identificatie, self.gerelateerdeAdressen, self.tijdvakgeldigheid, self.bron)
   
    def insert(self):
        self.sql = """INSERT INTO ligplaats (identificatie, aanduidingrecordinactief,
            aanduidingrecordcorrectie, officieel, inonderzoek, documentnummer, documentdatum, hoofdadres,
            ligplaatsstatus, begindatumtijdvakgeldigheid, einddatumtijdvakgeldigheid, geometrie) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s,ST_GeomFromGML(%s))"""
        self.valuelist = (self.identificatie, self.inactief, \
            self.correctie, self.officieel, self.inonderzoek, self.bron.documentnummer, self.bron.documentdatum, \
            self.gerelateerdeAdressen.hoofdadres, self.status, self.tijdvakgeldigheid.begindatum, \
            self.tijdvakgeldigheid.einddatum, self.geometrie)

    drop = "DROP TABLE IF EXISTS ligplaats CASCADE;"
        
    create = """CREATE TABLE ligplaats (
                    gid serial,
                    identificatie numeric(16,0),
                    aanduidingrecordinactief boolean,
                    aanduidingrecordcorrectie integer,
                    officieel boolean,
                    inonderzoek boolean,
                    documentnummer character varying(20),
                    documentdatum date,
                    hoofdadres numeric(16,0),
                    ligplaatsstatus character varying(80),
                    begindatumtijdvakgeldigheid timestamp without time zone,
                    einddatumtijdvakgeldigheid timestamp without time zone,
                    geometrie geometry,
                    PRIMARY KEY (gid),
                    CONSTRAINT enforce_dims_geometrie CHECK ((st_ndims(geometrie) = 3)),
                    CONSTRAINT enforce_geotype_geometrie CHECK (
                          ((geometrytype(geometrie) = 'POLYGON'::text) OR (geometrie IS NULL))),
                    CONSTRAINT enforce_srid_geometrie CHECK ((st_srid(geometrie) = 28992))
                );"""


