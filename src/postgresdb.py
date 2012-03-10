"""
 Naam: postgresdb.py
 Omschrijving: Database driver voor postgres
 Auteur(s): Matthijs van der Deijl, Milo van der Linden, Just van den Broecke
"""

import sys
import os
import logging
import datetime
import time
import xml.dom.minidom as dom

try:
   import psycopg2
except:
    formatter = logging.Formatter('%(levelname)s - %(message)s')
    logging.critical("Python psycopg2 is niet geinstalleerd")
    sys.exit()

class Database:

    def __init__(self, configuratie):
        self.config = configuratie

    def initialiseer(self, bestand):
        self.config.logger.debug("postgresdb.initialiseer()")
        self.verbind()

        try:
            self.config.logger.info("Database script wordt gelezen")
            script = open(bestand, 'r').read()
            self.cursor.execute(script)
            self.connection.commit()
            self.config.logger.info("Database script uitgevoerd")
        except psycopg2.DatabaseError:
            e = sys.exc_info()[1]
            self.config.logger.critical("'%s' tijdens het inlezen van '%s'" % (str(e), str(bestand)))
            sys.exit()

    def getBoolean(self, nodelist):
        rc = ""
        for node in nodelist:
            if node.nodeType == node.TEXT_NODE:
                rc = rc + node.data

        if rc == 'N':
            return 'FALSE'
        elif rc == 'J':
            return 'TRUE'
        else:
            return None

    def getText(self, nodelist):
        """
        Voeg de inhoud van XML textnodes samen tot een string
        """
        rc = ""
        for node in nodelist:
            if node.nodeType == node.TEXT_NODE:
                rc = rc + node.data
        return rc

    def getDate(self, node):
        """
        Maak een datum object van een XML datum/tijd
        BAG Datum/tijd is in het formaat JJJJMMDDUUMMSSmm
        Deze functie genereert een datum van de BAG:DatumTijd
        """
        self.config.logger.debug(node)
        if type(node) == str:
            # TODO Momenteel alleen voor de gemeente_woonplaats csv
            _text = node
            if len(_text) > 0:
                if len(_text) == 10:
                    return datetime.datetime(*time.strptime(_text, "%d-%m-%Y")[0:6])
                elif len(_text) == 8:
                    return datetime.datetime(*time.strptime(_text, "%Y%m%d")[0:6])
            else:
                return None

        elif node is None:
            return None

        else:
            # TODO check inbouwen op nodetype en of aan alle voorwaarden wordt voldaan
            _text = self.getText(node.childNodes)
            self.config.logger.debug(_text)
            if len(_text) == 16:
                bagdatumtijd = _text[:-2]
                _dt = datetime.datetime(*time.strptime(bagdatumtijd, "%Y%m%d%H%M%S")[0:6])
                self.config.logger.debug(_dt)
                return _dt
                
            elif len(_text) == 8:
                bagdatumtijd = _text
                _dt = datetime.datetime(*time.strptime(bagdatumtijd, "%Y%m%d")[0:6])
                self.config.logger.debug(_dt)
                return _dt

            else:
                return None
                

    def getTimestamp(self, node):
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

    def maak_database(self):
        self.config.logger.debug("postgresdb.maak_database()")
        
        from objecten.ligplaats import Ligplaats
        from objecten.nummeraanduiding import Nummeraanduiding
        from objecten.openbareruimte import Openbareruimte
        from objecten.pand import Pand
        from objecten.standplaats import Standplaats
        from objecten.verblijfsobject import Verblijfsobject
        from objecten.woonplaats import Woonplaats
        from objecten.verblijfsobjectgebruiksdoel import Verblijfsobjectgebruiksdoel
        from objecten.verblijfsobjectpand import Verblijfsobjectpand
        from objecten.adresseerbaarobjectnevenadres import Adresseerbaarobjectnevenadres
        from objecten.gemeentewoonplaats import Gemeentewoonplaats
        from objecten.gemeenteprovincie import Gemeenteprovincie
        
        self.verbind()
 
        self.cursor.execute(Ligplaats.drop(self.config.schema))
        self.cursor.execute(Nummeraanduiding.drop)
        self.cursor.execute(Openbareruimte.drop)
        self.cursor.execute(Pand.drop)
        self.cursor.execute(Standplaats.drop)
        self.cursor.execute(Verblijfsobject.drop)
        self.cursor.execute(Woonplaats.drop)
        self.cursor.execute(Verblijfsobjectgebruiksdoel.drop)
        self.cursor.execute(Verblijfsobjectpand.drop)
        self.cursor.execute(Adresseerbaarobjectnevenadres.drop)
        self.cursor.execute(Gemeentewoonplaats.drop(self.config.schema))
        self.cursor.execute(Gemeenteprovincie.drop)
        
        self.cursor.execute(Ligplaats.create(self.config.schema))
        self.cursor.execute(Nummeraanduiding.create)
        self.cursor.execute(Openbareruimte.create)
        self.cursor.execute(Pand.create)
        self.cursor.execute(Standplaats.create)
        self.cursor.execute(Verblijfsobject.create)
        self.cursor.execute(Woonplaats.create)
        self.cursor.execute(Verblijfsobjectgebruiksdoel.create)
        self.cursor.execute(Verblijfsobjectpand.create)
        self.cursor.execute(Adresseerbaarobjectnevenadres.create)
        self.cursor.execute(Gemeentewoonplaats.create(self.config.schema))
        self.cursor.execute(Gemeenteprovincie.create)
        self.cursor.execute("select probe_geometry_columns();")
        self.connection.commit()
        

    def verbind(self):
        self.config.logger.debug("postgresdb.verbind()")
        try:

            self.config.logger.info('Verbinding maken met ' + self.config.database)
            self.connection = psycopg2.connect("dbname='%s' user='%s' host='%s' password='%s'" % (self.config.database,
                                                                                                  self.config.user,
                                                                                                  self.config.host,
                                                                                                 self.config.password))
            self.cursor = self.connection.cursor()
            self.config.logger.info("Verbonden")
            self.zet_schema()
        except Exception:

            e = sys.exc_info()[1]
            self.config.logger.critical("Verbinden mislukt: %s" % (str(e)))
            # TODO: Bepalen of hier connecties en cursors moeten worden gesloten
            sys.exit()

    def zet_schema(self):
        self.config.logger.debug("postgresdb.zet_schema()")
        if self.config.schema != 'public':
            try:
                self.cursor.execute('SET search_path TO %s,public' % self.config.schema)

            except Exception:

                self.connection.rollback()
                self.config.logger.warning('Schema %s bestaat nog niet en wordt gemaakt' % self.config.schema)

                try:

                    self.cursor.execute('CREATE SCHEMA %s;' % self.config.schema)
                    self.cursor.execute('SET search_path TO %s,public' % self.config.schema)
                    self.config.logger.info("Schema %s is aangemaakt" % self.config.schema)

                except Exception:

                    self.connection.rollback()
                    e = sys.exc_info()[1]
                    self.config.logger.error("Schema %s kon niet worden gemaakt: %s" % (self.config.schema, str(e)))

    def uitvoeren(self, sql, parameters=None):
        try:
            if parameters:
                #self.config.logger.debug("postgresdb.uitvoeren(%s, %s)" % (sql, parameters))
                self.cursor.execute(sql, parameters)
            else:
                #self.config.logger.debug("postgresdb.uitvoeren(%s)" % sql)
                self.cursor.execute(sql)

            self.connection.commit()

        except Exception:
            self.connection.rollback()
            e = sys.exc_info()[1]
            self.config.logger.error("%s" % str(e))


    def file_uitvoeren(self, sqlfile):
        self.config.logger.debug("postgresdb.file_uitvoeren(%s)" % sqlfile)
        try:
            self.config.logger.info("Script %s wordt uitgevoerd" % sqlfile)
            self.verbind()
            f = open(sqlfile, 'r')
            sql = f.read()
            self.uitvoeren(sql)
            self.connection.commit()
            f.close()

        except (Exception):

            self.connection.rollback()
            e = sys.exc_info()[1]
            self.config.logger.critical("ik kan dit script niet uitvoeren vanwege deze fout: %s" % (str(e)))
