class Woonplaats():
    def __init__(self, xmlnode):
        self.tag = "bag_LVC:Woonplaats"
        self.naam = "Woonplaats"
        self.type = 'WPL'
        for node in xmlnode.childNodes:
            if node.localName == 'woonplaatsNaam':
                self.naam = getText(node.childNodes)
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
            if node.localName == 'woonplaatsStatus':
                self.status = getText(node.childNodes)
            if node.localName == 'woonplaatsGeometrie':
                # zet de geometrie om naar echte geometrie (ogr) voordeel is dat je dit naar
                # shape, wkt, wkb etc. kunt exporteren
                #self.geometrie = gettext(node.childNodes)
                multigeom = ogr.Geometry( type= ogr.wkbMultiPolygon )
                for geometrie in node.childNodes:
                    # sla pure tekst nodes over
                    if geometrie.nodeType == node.TEXT_NODE:
                        continue

                    gml = geometrie.toxml()
                    simplegeom = ogr.CreateGeometryFromGML(str(gml))
                    if simplegeom.GetGeometryType() == 6: #multisurface!
                        multigeom = simplegeom
                    else:
                        multigeom.AddGeometryDirectly(simplegeom)
                self.geometrie = multigeom

    def __repr__(self):
       return "<Woonplaats('%s','%s', '%s')>" % (self.tag, self.naam, self.type)
    
    def insert(self):
        self.sql = """INSERT INTO woonplaats (identificatie, aanduidingrecordinactief,
            aanduidingrecordcorrectie, officieel, inonderzoek, documentnummer, documentdatum, woonplaatsnaam,
            woonplaatsstatus, 
            begindatum, einddatum, geometrie) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s,ST_GeomFromText(%s,%s))"""
        self.valuelist = (self.identificatie, self.inactief, \
            self.correctie, self.officieel, self.inonderzoek, self.bron.documentnummer, self.bron.documentdatum, \
            self.naam, self.status, self.tijdvakgeldigheid.begindatum, \
            self.tijdvakgeldigheid.einddatum, str(self.geometrie.ExportToWkt()), '28992')
        #return self.sql, self.valuelist

    drop = "DROP TABLE IF EXISTS woonplaats CASCADE;"
    
    create = """CREATE TABLE woonplaats (
                  gid serial,
                  identificatie numeric(16,0),
                  aanduidingrecordinactief boolean,
                  aanduidingrecordcorrectie integer,
                  officieel boolean,
                  inonderzoek boolean,
                  documentnummer character varying(20),
                  documentdatum date,
                  woonplaatsnaam character varying(80),
                  woonplaatsstatus character varying(80),
                  begindatumtijdvakgeldigheid timestamp without time zone,
                  einddatumtijdvakgeldigheid timestamp without time zone,
                  geom_valid boolean default TRUE,
                  geovlak geometry,
                  PRIMARY KEY (gid),
                  CONSTRAINT enforce_dims_geometrie CHECK ((st_ndims(geovlak) = 2)),
                  CONSTRAINT enforce_geotype_geometrie CHECK (
                          ((geometrytype(geovlak) = 'MULTIPOLYGON'::text) OR (geovlak IS NULL))),
                  CONSTRAINT enforce_srid_geometrie CHECK ((st_srid(geovlak) = 28992))
                )WITH (
                        OIDS=TRUE
                );"""
