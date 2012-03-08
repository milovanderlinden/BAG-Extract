class Verblijfsobject():
    def __init__(self,xmlnode):
        self.tag = "bag_LVC:Verblijfsobject"
        self.naam = "Verblijfsobject"
        self.type = 'VBO'
        self.correctie = None
        self.gebruiksdoel = None
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
                self.correcte = getText(node.childNodes)
            if node.localName == 'officieel':
                self.officieel = getText(node.childNodes)
            if node.localName == 'inOnderzoek':
                self.inonderzoek = getText(node.childNodes)
            if node.localName == 'verblijfsobjectStatus':
                self.status = getText(node.childNodes)
            if node.localName == 'gebruiksdoelVerblijfsobject':
                self.gebruiksdoel = getText(node.childNodes)
            if node.localName == 'oppervlakteVerblijfsobject':
                self.oppervlakte = getText(node.childNodes)
            if node.localName == 'gerelateerdPand':
                self.gerelateerdPand = GerelateerdPand(node)
            if node.localName == 'verblijfsobjectGeometrie':
                # zet de geometrie om naar echte geometrie (ogr) voordeel is dat je dit naar
                # shape, wkt, wkb etc. kunt exporteren
                #self.geometrie = gettext(node.childNodes)
                for geometrie in node.childNodes:
                    # sla pure tekst nodes over
                    if geometrie.nodeType == node.TEXT_NODE:
                        continue

                    gml = geometrie.toxml()
                    _geom = ogr.CreateGeometryFromGML(str(gml))
                    if _geom.GetGeometryName() != 'POINT': #polygon!
                        #Gebruik de centroide van de geometry
                        vlak = _geom
                        #Nu a
                        _punt = _geom.Centroid()
                        punt = ogr.Geometry(ogr.wkbPoint25D)
                        punt.AddPoint(_punt.GetX(),_punt.GetY(),0)
                    else: # We gaan uit van punt
                       vlak = None
                       punt = _geom
                self.punt = punt
                self.vlak = vlak

    def __repr__(self):
       return "<Verblijfsobject('%s','%s', '%s')>" % (self.tag, self.naam, self.type)

    def insert(self):
        if self.vlak:
            #tegen mijn principe, maar kan nu even niet anders...
            vlakval = self.vlak.ExportToWkt()
        else:
            vlakval = None

        self.sql = """INSERT INTO verblijfsobject (identificatie, aanduidingrecordinactief,
            aanduidingrecordcorrectie, officieel, inonderzoek, documentnummer, documentdatum, hoofdadres,
            gerelateerdpand, gebruiksdoel,
            verblijfsobjectstatus, oppervlakteverblijfsobject,
            begindatum, einddatum, punt, vlak) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s,ST_GeomFromText(%s,%s),ST_GeomFromText(%s,%s))"""
        self.valuelist = (self.identificatie, self.inactief, \
            self.correctie, self.officieel, self.inonderzoek, self.bron.documentnummer, self.bron.documentdatum, \
            self.gerelateerdeAdressen.hoofdadres, self.gerelateerdPand.identificatie, self.gebruiksdoel, self.status, self.oppervlakte, self.tijdvakgeldigheid.begindatum, \
            self.tijdvakgeldigheid.einddatum, str(self.punt.ExportToWkt()), '28992', vlakval,'28992')

    drop = "DROP TABLE IF EXISTS verblijfsobject CASCADE;"
    create = """CREATE TABLE verblijfsobject (
                  gid serial,
                  identificatie numeric(16,0),
                  aanduidingrecordinactief boolean,
                  aanduidingrecordcorrectie integer,
                  officieel boolean,
                  inonderzoek boolean,
                  documentnummer character varying(20),
                  documentdatum date,
                  hoofdadres numeric(16,0),
                  verblijfsobjectstatus character varying(80),
                  oppervlakteverblijfsobject numeric(6,0),
                  begindatumtijdvakgeldigheid timestamp without time zone,
                  einddatumtijdvakgeldigheid timestamp without time zone,
                  geom_valid boolean default TRUE,
                  geopunt geometry,
                  geovlak geometry,
                  PRIMARY KEY (gid),
                  CONSTRAINT enforce_dims_punt CHECK ((st_ndims(geopunt) = 3)),
                  CONSTRAINT enforce_geotype_punt CHECK (
                          ((geometrytype(geopunt) = 'POINT'::text) OR (geopunt IS NULL))),
                  CONSTRAINT enforce_srid_punt CHECK ((st_srid(geopunt) = 28992)),

                  CONSTRAINT enforce_dims_vlak CHECK ((st_ndims(geovlak) = 3)),
                  CONSTRAINT enforce_geotype_vlak CHECK (
                          ((geometrytype(geovlak) = 'POLYGON'::text) OR (geovlak IS NULL))),
                  CONSTRAINT enforce_srid_vlak CHECK ((st_srid(geovlak) = 28992))
                );"""
