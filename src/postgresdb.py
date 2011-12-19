__author__ = "Matthijs van der Deijl"
__date__ = "$Dec 09, 2009 00:00:01 AM$"

"""
 Naam:         libDatabase.py
 Omschrijving: Generieke functies voor databasegebruik binnen BAG Extract+
 Auteur:       Matthijs van der Deijl

 Versie:       1.4
               - Deze database klasse is vanaf heden specifiek voor postgres/postgis
 Datum:        15 juni 2011

 Versie:       1.3
               - functie controleerTabellen toegevoegd
               - selectie van logregels gesorteerd op datum
 Datum:        9 december 2009

 Versie:       1.2
 Datum:        24 november 2009

 Ministerie van Volkshuisvesting, Ruimtelijke Ordening en Milieubeheer
"""
import psycopg2
import logger
from libBAGconfiguratie import *

class Database:
    def __init__(self, args):
        # Lees de configuratie uit BAG.conf
        self.args = args
        self.log = logger.LogHandler(args)
        if args.database:
            self.database = args.database
        else:
            self.database = configuratie.database
        if args.host:
            self.host = args.host
        else:
            self.host = configuratie.host

        if args.schema:
            self.schema = args.schema
        else:
            self.schema = configuratie.schema

        # default to public schema
        if not self.schema:
            self.schema = 'public'

        if args.username:
            self.user = args.username
        else:
            self.user = configuratie.user
        if args.port:
            self.port = args.port
        else:
            self.port = 5432
        if args.no_password:
            # Gebruik geen wachtwoord voor de database verbinding
            self.password = None
        else:
            if args.password:
                self.password = args.password
            else:
                self.password = configuratie.password

    def initialiseer(self, bestand):
        self.log.log('Probeer te verbinden...')
        self.verbind(True)

        self.log.log('database script uitvoeren...')
        try:
            script = open(bestand, 'r').read()
            self.cursor.execute(script)
            self.connection.commit()
            self.log.log('script uitgevoerd')
        except psycopg2.DatabaseError, e:
            print "fout: procedures :%s" % str(e)

    def verbind(self, initdb=False):
        try:
            self.connection = psycopg2.connect("dbname='%s' user='%s' host='%s' password='%s'" % (self.database,
                                                                                                  self.user,
                                                                                                  self.host,
                                                                                                 self.password));
            self.cursor = self.connection.cursor()

            if initdb:
                self.maak_schema()

            self.zet_schema()
            self.log.log("verbonden met database %s" % (self.database))
        except Exception, e:
            print("fout %s: kan geen verbinding maken met database %s" % (str(e), self.database))
            sys.exit()

    def maak_schema(self):
        # Public schema: no further action required
        if self.schema != 'public':
            # A specific schema is required create it and set the search path
            self.uitvoeren('''DROP SCHEMA IF EXISTS %s CASCADE;''' % self.schema)
            self.uitvoeren('''CREATE SCHEMA %s;''' % self.schema)
            self.connection.commit()

    def zet_schema(self):
        # Non-public schema set search path
        if self.schema != 'public':
            # Always set search path to our schema
            self.uitvoeren('SET search_path TO %s,public' % self.schema)
            self.connection.commit()

    def uitvoeren(self, sql, parameters=None):
        try:
            if parameters:
                self.cursor.execute(sql, parameters)
            else:
                self.cursor.execute(sql)
        except (psycopg2.IntegrityError, psycopg2.ProgrammingError), e:
            print "fout %s voor query: %s" % (str(e), str(self.cursor.mogrify(sql, parameters)))
            return self.cursor.rowcount
