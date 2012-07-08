class Pand():

    def __init__(self):
        self.id = None

    def __init__(self,xmlnode):
        self.tag = "bag_LVC:Pand"
        self.naam = "Pand"
        self.type = 'PND'
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
            if node.localName == 'pandstatus':
                self.status = getText(node.childNodes)
            if node.localName == 'bouwjaar':
                self.bouwjaar = getText(node.childNodes)
            if node.localName == 'pandGeometrie':
                for geometrie in node.childNodes:
                    # sla pure tekst nodes over
                    if geometrie.nodeType == node.TEXT_NODE:
                        continue

                    gml = geometrie.toxml()
                    self.geometrie = ogr.CreateGeometryFromGML(str(gml))

    def __repr__(self):
       return "<Pand('%s','%s', '%s', '%s')>" % (self.identificatie, self.status, self.tijdvakgeldigheid, self.bron)

    def insert(self):
        self.sql = """INSERT INTO pand (
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
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, ST_GeomFromText(%s, %s))"""
        self.valuelist = (self.identificatie, self.inactief, \
            self.correctie, self.officieel, self.inonderzoek, self.bron.documentnummer, self.bron.documentdatum, \
            self.status, self.bouwjaar, self.tijdvakgeldigheid.begindatum, \
            self.tijdvakgeldigheid.einddatum, str(self.geometrie.ExportToWkt()), '28992')
            
    drop = "DROP TABLE IF EXISTS pand CASCADE;"
     
    create = """CREATE TABLE pand (
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
                  pandstatus character varying(80),
                  bouwjaar numeric(4,0),
                  geom_valid boolean default TRUE,
                  geometrie geometry,
                  PRIMARY KEY (gid),
                  CONSTRAINT enforce_dims_geometrie CHECK ((st_ndims(geometrie) = 3)),
                  CONSTRAINT enforce_geotype_geometrie CHECK (
                          ((geometrytype(geometrie) = 'POLYGON'::text) OR (geometrie IS NULL))),
                  CONSTRAINT enforce_srid_geometrie CHECK ((st_srid(geometrie) = 28992))
                );"""

