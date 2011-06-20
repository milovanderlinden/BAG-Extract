__author__ = "Matthijs van der Deijl"
__date__ = "$Jun 11, 2011 3:46:27 PM$"
#------------------------------------------------------------------------------
# Naam:         Objecten.py
# Omschrijving: Classes voor de BAG-objecten
#
# Per BAG-objecttype (woonplaats, openbareruimte, nummeraanduiding,
# ligplaats, standplaats, verblijfsobject, pand) is er een aparte class
# met functionaliteit voor het lezen uit XML, het schrijven in de database
# en het lezen uit de database. Ook bevat elke BAG-objectype-class functies
# voor het initialiseren van de database (maken van tabellen, indexen en
# views).
# De BAG-objecttype-classes zijn afgeleid van de basisclass BAGobject.
# Hierin is een BAG-object een verzameling van BAG-attributen met elk
# hun eigen eigenschappen.
#
# Auteurs:       Matthijs van der Deijl, Milo van der Linden
#
# Versie:       1.8
#
# Versie:       1.7
#               - objecttype LPL vervangen door LIG
#               - objecttype SPL vervangen door STA
# Datum:        11 maart 2011
#
# Versie:       1.6
#               - Veldlengte voor tekstwaarde van geometrie verhoogt naar 1000000
# Datum:        8 oktober 2010
#
# Versie:       1.3
#               - Tag voor VerkorteOpenbareRuimteNaam verbeterd
#               - GeomFromText vervangen door GeomFromEWKT
#                 (dit voorkomt Warnings in de database logging)
#               - Functie controleerTabel toegevoegd
#               - Primaire index op tabel uniek gemaakt
#               - Ophalen van waardes uit database met leestekens verbeterd
# Datum:        28 december 2009
#
# Versie:       1.2
# Datum:        24 november 2009
#
# Ministerie van Volkshuisvesting, Ruimtelijke Ordening en Milieubeheer
#------------------------------------------------------------------------------

from osgeo import ogr #apt-get install python-gdal
import datetime
import time
#from sqlalchemy.ext.declarative import declarative_base
#Base = declarative_base()
# TODO: Testen met sqlalchemy en impact bepalen
class Base:
    def __init__(self):
        self.id = None


# Geef de waarde van een textnode in XML
def getText(nodelist):
    """
    Voeg de inhoud van XML textnodes samen tot een string
    """
    rc = ""
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc = rc + node.data
    return rc

def getDate(node):
    """
    Maak een datum object van een XML datum/tijd
    BAG Datum/tijd is in het formaat JJJJMMDDUUMMSSmm
    Deze functie genereert een datum van de BAG:DatumTijd
    """
    _text = getText(node.childNodes)
    if len(_text) == 16:
        bagdatumtijd = _text[:-2]
        return datetime.datetime(*time.strptime(bagdatumtijd, "%Y%m%d%H%M%S")[0:6])
    elif len(_text) == 8:
        bagdatumtijd = _text
        return datetime.datetime(*time.strptime(bagdatumtijd, "%Y%m%d")[0:6])

def getTimestamp(node):
    """
    Maak een datum/tijd object van een XML datum/tijd
    BAG Datum/tijd is in het formaat JJJJMMDDUUMMSSmm
    Deze functie genereert een timestamp van de BAG:DatumTijd
    """
    _text = getText(node.childNodes)
    if len(_text) == 16:
        bagdatumtijd = _text[:-2]
        return datetime.datetime(*time.strptime(bagdatumtijd, "%Y%m%d%H%M%S")[0:6])
    elif len(_text) == 8:
        bagdatumtijd = _text
        return datetime.datetime(*time.strptime(bagdatumtijd, "%Y%m%d")[0:6])

    #tmp_datetime = gettext(node.childNodes).split('+')
    #return datetime.datetime(*time.strptime(tmp_datetime[0], "%Y-%m-%dT%H:%M:%S")[0:6])

class Tijdvakgeldigheid():
    """
    BAG sub-klasse.
    """
    def __init__(self,xmlnode):
        self.tag = "bag_LVC:tijdvakgeldigheid"
        self.naam = "tijdvakgeldigheid"
        self.type = ''
        self.einddatum = None
        self.begindatum = None
        for node in xmlnode.childNodes:
            if node.localName == 'begindatumTijdvakGeldigheid':
                self.begindatum = getDate(node)
            if node.localName == 'einddatumTijdvakGeldigheid':
                self.einddatum = getDate(node)
    def __repr__(self):
       return "<Tijdvakgeldigheid('%s','%s')>" % (self.begindatum, self.einddatum)

class GerelateerdPand():
    """
    BAG sub-klasse.
    """
    def __init__(self,xmlnode):
        self.tag = "bag_LVC:gerelateerdPand"
        self.naam = "gerelateerdPand"
        self.type = ''
        for node in xmlnode.childNodes:
            if node.localName == 'identificatie':
                self.identificatie = getText(node.childNodes)
    def __repr__(self):
       return "<GerelateerdPand('%s')>" % (self.identificatie,)

class GerelateerdeOpenbareRuimte():
    """
    BAG sub-klasse.
    """
    def __init__(self,xmlnode):
        self.tag = "bag_LVC:gerelateerdeOpenbareRuimte"
        self.naam = "gerelateerdeOpenbareRuimte"
        self.type = ''
        for node in xmlnode.childNodes:
            if node.localName == 'identificatie':
                self.identificatie = getText(node.childNodes)
    def __repr__(self):
       return "<GerelateerdeOpenbareRuimte('%s')>" % (self.identificatie,)

class GerelateerdeWoonplaats():
    """
    BAG sub-klasse.
    """
    def __init__(self,xmlnode=None):
        if xmlnode:
            self.tag = "bag_LVC:gerelateerdeWoonplaats"
            self.naam = "gerelateerdeWoonplaats"
            self.type = ''
        if xmlnode:
            for node in xmlnode.childNodes:
                if node.localName == 'identificatie':
                    self.identificatie = getText(node.childNodes)
        else:
            self.identificatie = None

    def __repr__(self):
        return "<GerelateerdeWoonplaats('%s')>" % (self.identificatie,)

class GerelateerdeAdressen():
    """
    BAG sub-klasse.
    Collectie van gerelateerde adressen
    """
    def __init__(self,xmlnode):
        self.tag = "bag_LVC:gerelateerdeAdressen"
        self.naam = "gerelateerdeAdressen"
        self.type = ''
        for node in xmlnode.childNodes:
            if node.localName == 'hoofdadres':
                for adresElement in node.childNodes:
                    if adresElement.localName == 'identificatie':
                        self.hoofdadres = getText(adresElement.childNodes)
    def __repr__(self):
       return "<GerelateerdeAdressen('%s')>" % (self.hoofdadres,)

class Bron():
    """
    BAG sub-klasse.
    """
    def __init__(self,xmlnode):
        self.tag = "bag_LVC:bron"
        self.naam = "bron"
        self.type = ''
        for node in xmlnode.childNodes:
            if node.localName == 'documentdatum':
                self.documentdatum = getDate(node)
            if node.localName == 'documentnummer':
                self.documentnummer = getText(node.childNodes)
    def __repr__(self):
       return "<Bron('%s','%s')>" % (self.documentdatum, self.documentnummer)

class OpenbareRuimte(Base):
    """
    BAG Klasse OpenbareRuimte
    Class voor het BAG-objecttype OpenbareRuimte.
    """

    def __init__(self,xmlnode):
        self.tag = "bag_LVC:OpenbareRuimte"
        self.naam = "OpenbareRuimte"
        self.type = 'OPR'
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
            if node.localName == 'openbareRuimteNaam':
                self.naam = getText(node.childNodes)
            if node.localName == 'openbareruimteStatus':
                #let op! kleine r van ruimte, is dit een fout in de xml?
                self.status = getText(node.childNodes)
            if node.localName == 'openbareRuimteType':
                self.type = getText(node.childNodes)
            if node.localName == 'gerelateerdeWoonplaats':
                self.gerelateerdeWoonplaats = GerelateerdeWoonplaats(node)
    def __repr__(self):
       return "<OpenbareRuimte('%s','%s', '%s', '%s')>" % (self.identificatie, self.naam, self.tijdvakgeldigheid, self.bron)

    def insert(self):
        self.sql = """INSERT INTO openbareruimte (
            identificatie,
            aanduidingrecordinactief,
            aanduidingrecordcorrectie,
            officieel,
            inonderzoek,
            documentnummer,
            documentdatum,
            openbareruimtenaam,
            openbareruimtestatus,
            openbareruimtetype,
            gerelateerdewoonplaats,
            begindatum,
            einddatum)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        self.valuelist = (self.identificatie, self.inactief, \
            self.correctie, self.officieel, self.inonderzoek, \
            self.bron.documentnummer, self.bron.documentdatum, \
            self.naam, self.type, self.status, self.gerelateerdeWoonplaats.identificatie,self.tijdvakgeldigheid.begindatum, self.tijdvakgeldigheid.einddatum)
            
class Nummeraanduiding(Base):
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

class Standplaats(Base):
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

class Pand(Base):
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
            begindatum,
            einddatum,
            geometrie)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, ST_GeomFromText(%s, %s))"""
        self.valuelist = (self.identificatie, self.inactief, \
            self.correctie, self.officieel, self.inonderzoek, self.bron.documentnummer, self.bron.documentdatum, \
            self.status, self.bouwjaar, self.tijdvakgeldigheid.begindatum, \
            self.tijdvakgeldigheid.einddatum, str(self.geometrie.ExportToWkt()), '28992')

class Ligplaats(Base):
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

    def __init__(self,xmlnode):
        self.tag = "bag_LVC:Ligplaats"
        self.naam = "ligplaats"
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
            if node.localName == 'ligplaatsStatus':
                self.status = getText(node.childNodes)
            if node.localName == 'ligplaatsGeometrie':
                for geometrie in node.childNodes:
                    gml = geometrie.toxml()
                    self.geometrie = ogr.CreateGeometryFromGML(str(gml))

    def __repr__(self):
       return "<Ligplaats('%s','%s', '%s', '%s')>" % (self.identificatie, self.gerelateerdeAdressen, self.tijdvakgeldigheid, self.bron)
   
    def insert(self):
        self.sql = """INSERT INTO ligplaats (identificatie, aanduidingrecordinactief,
            aanduidingrecordcorrectie, officieel, inonderzoek, documentnummer, documentdatum, hoofdadres,
            ligplaatsstatus, begindatum, einddatum, geometrie) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s,ST_GeomFromText(%s,%s))"""
        self.valuelist = (self.identificatie, self.inactief, \
            self.correctie, self.officieel, self.inonderzoek, self.bron.documentnummer, self.bron.documentdatum, \
            self.gerelateerdeAdressen.hoofdadres, self.status, self.tijdvakgeldigheid.begindatum, \
            self.tijdvakgeldigheid.einddatum, str(self.geometrie.ExportToWkt()), '28992')

#--------------------------------------------------------------------------------------------------------
# Class         Verblijfsobject
# Omschrijving  Class voor het BAG-objecttype Verblijfsobject.
#--------------------------------------------------------------------------------------------------------
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
                    gml = geometrie.toxml()
                    _geom = ogr.CreateGeometryFromGML(str(gml))
                    if _geom.GetGeometryName() <> 'POINT': #polygon!
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

#--------------------------------------------------------------------------------------------------------
# Class         Woonplaats
# Omschrijving  Class voor het BAG-objecttype Woonplaats.
#--------------------------------------------------------------------------------------------------------
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

class GemeenteWoonplaats(Base):
    """
    Klasse Gemeente
    """

    def __init__(self,record):
        # TODO: De csv is niet volledig gevuld, controleer of een record wel het minimaal aantal objecten bevat.
        # Woonplaats;Woonplaats code;Ingangsdatum WPL;Einddatum WPL;Gemeente;Gemeente code;
        # Ingangsdatum nieuwe gemeente;Aansluitdatum;Bijzonderheden;Nieuwe code Gemeente;
        #Gemeente beeindigd per;Behandeld;        Laatste WPL code:;3513
        if len(record) > 8:
            self.tag = "gem_LVC:GemeenteWoonplaats"
            self.naam = "gemeente_woonplaats"
            self.type = 'G_W'
            self.woonplaatsnaam = record[0]
            self.woonplaatscode = record[1]
            self.begindatum_woonplaats = record[2]
            self.einddatum_woonplaats = record[3]
            self.gemeentenaam = record[4]
            self.gemeentecode = record[5]
            self.begindatum_gemeente = record[6]
            self.aansluitdatum_gemeente = record[7]
            self.bijzonderheden = record[8]
            self.gemeentecode_nieuw = record[9]
            self.einddatum_gemeente = record[10]
            self.behandeld = record[11]

    def __repr__(self):
       return "<GemeenteWoonplaats('%s','%s', '%s')>" % (self.naam, self.woonplaatscode, self.gemeentecode)

    def insert(self):
        self.sql = """INSERT INTO gemeente_woonplaats (
            woonplaatsnaam,
            woonplaatscode,
            begindatum_woonplaats,
            einddatum_woonplaats,
            gemeentenaam,
            gemeentecode,
            begindatum_gemeente,
            aansluitdatum_gemeente,
            bijzonderheden,
            gemeentecode_nieuw,
            einddatum_gemeente,
            behandeld)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        self.valuelist = (self.woonplaatsnaam, self.woonplaatscode, self.begindatum_woonplaats, \
            self.einddatum_woonplaats,self.gemeentenaam, self.gemeentecode, self.begindatum_gemeente, \
            self.aansluitdatum_gemeente, self.bijzonderheden, self.gemeentecode_nieuw, self.einddatum_gemeente, \
            self.behandeld)

