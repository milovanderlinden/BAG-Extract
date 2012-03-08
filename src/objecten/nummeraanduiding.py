class Nummeraanduiding():
    def __init__(self,xmlnode):
        self.tag = "bag_LVC:Nummeraanduiding"
        self.naam = "Nummeraanduiding"
        self.type = 'NUM'
        self.huisletter = None
        self.huisnummertoevoeging = None
        self.gerelateerdeWoonplaats = GerelateerdeWoonplaats()
        self.postcode = None
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
            if node.localName == 'huisnummer':
                self.huisnummer = getText(node.childNodes)
            if node.localName == 'huisletter':
                self.huisletter = getText(node.childNodes)
            if node.localName == 'huisnummertoevoeging':
                self.huisnummertoevoeging = getText(node.childNodes)
            if node.localName == 'postcode':
                self.postcode = getText(node.childNodes)
            if node.localName == 'nummeraanduidingStatus':
                self.status = getText(node.childNodes)
            if node.localName == 'typeAdresseerbaarObject':
                self.typeAdresseerbaarObject = getText(node.childNodes)
            if node.localName == 'gerelateerdeOpenbareRuimte':
                self.gerelateerdeOpenbareRuimte = GerelateerdeOpenbareRuimte(node)
            if node.localName == 'gerelateerdeWoonplaats':
                self.gerelateerdeWoonplaats = GerelateerdeWoonplaats(node)

    def __repr__(self):
       return "<Nummeraanduiding('%s', '%s', '%s')>" % (self.identificatie, self.tijdvakgeldigheid, self.bron)

    def insert(self):
        self.sql = """INSERT INTO nummeraanduiding (
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
            begindatum,
            einddatum)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        self.valuelist = (self.identificatie, self.inactief, \
            self.correctie, self.officieel, self.inonderzoek, \
            self.bron.documentnummer, self.bron.documentdatum, \
            self.huisnummer, self.huisletter, self.huisnummertoevoeging, \
            self.postcode, self.status, self.typeAdresseerbaarObject, \
            self.gerelateerdeOpenbareRuimte.identificatie, \
            self.gerelateerdeWoonplaats.identificatie, self.tijdvakgeldigheid.begindatum, \
            self.tijdvakgeldigheid.einddatum)

    drop = "DROP TABLE IF EXISTS nummeraanduiding CASCADE;"
    
    create = """CREATE TABLE nummeraanduiding (
                  gid serial,
                  identificatie numeric(16,0),
                  aanduidingrecordinactief boolean,
                  aanduidingrecordcorrectie integer,
                  officieel boolean,
                  inonderzoek boolean,
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
                  begindatumtijdvakgeldigheid timestamp without time zone,
                  einddatumtijdvakgeldigheid timestamp without time zone,
                  PRIMARY KEY (gid)
                );"""
