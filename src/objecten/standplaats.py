class Standplaats():
    def __init__(self,xmlnode):
        self.tag = "bag_LVC:Standplaats"
        self.naam = "standplaats"
        self.type = 'LIG'
        for node in xmlnode.childNodes:
            if node.localName == 'gerelateerdeAdressen':
                self.gerelateerdeAdressen = GerelateerdeAdressen(node)
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
            if node.localName == 'standplaatsStatus':
                self.status = getText(node.childNodes)
            if node.localName == 'standplaatsGeometrie':
                for geometrie in node.childNodes:
                   # sla pure tekst nodes over
                    if geometrie.nodeType == node.TEXT_NODE:
                        continue
                    gml = geometrie.toxml()
                    self.geometrie = ogr.CreateGeometryFromGML(str(gml))

    def __repr__(self):
       return "<Ligplaats('%s','%s', '%s', '%s')>" % (self.identificatie, self.gerelateerdeAdressen, self.tijdvakgeldigheid, self.bron)

    def insert(self):
        self.sql = """INSERT INTO standplaats (identificatie, aanduidingrecordinactief,
            aanduidingrecordcorrectie, officieel, inonderzoek, documentnummer, documentdatum, hoofdadres,
            standplaatsstatus, begindatum, einddatum, geometrie) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s,ST_GeomFromText(%s,%s))"""
        self.valuelist = (self.identificatie, self.inactief, \
            self.correctie, self.officieel, self.inonderzoek, self.bron.documentnummer, self.bron.documentdatum, \
            self.gerelateerdeAdressen.hoofdadres, self.status, self.tijdvakgeldigheid.begindatum, \
            self.tijdvakgeldigheid.einddatum, str(self.geometrie.ExportToWkt()), '28992')
    drop = "DROP TABLE IF EXISTS standplaats CASCADE;"
    
    create = """CREATE TABLE standplaats (
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
                  geom_valid boolean default TRUE,
                  geovlak geometry,
                  PRIMARY KEY (gid),
                  CONSTRAINT enforce_dims_geometrie CHECK ((st_ndims(geovlak) = 3)),
                  CONSTRAINT enforce_geotype_geometrie CHECK (
                          ((geometrytype(geovlak) = 'POLYGON'::text) OR (geovlak IS NULL))),
                  CONSTRAINT enforce_srid_geometrie CHECK ((st_srid(geovlak) = 28992))
                );"""

