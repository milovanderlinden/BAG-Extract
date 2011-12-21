__author__ = "Milo van der Linden"
__date__ = "$Dec 21, 2011 00:00:01 AM$"

"""
 Naam:         oracledb.py
 Omschrijving: functies voor databasegebruik binnen BAG Extract+
               Voor oracle gelden wat andere randvoorwaarden:
               - elke user komt standaard binnen in zijn eigen schema
               - Je verbindt niet met een database, maar met een sid,
                 dat moet getest worden.

 Versie:       0.1
               - Voor oracle 11g

 Datum:        21 december 2011
"""
import cx_Oracle
import logger
from libBAGconfiguratie import *

class Database:
    def __init__(self, args):
        # Lees de configuratie uit BAG.conf
        self.args = args
        self.log = logger.LogHandler(args)
        if args.sid:
            self.sid = args.sid
        else:
            self.sid = configuratie.sid
        if args.host:
            self.host = args.host
        else:
            self.host = configuratie.host
        if args.port:
            self.port = args.port
        else:
            self.port = configuratie.port
        # default to default port 1521
        if not self.port
            self.port = 1521

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
        except cx_Oracle.DatabaseError, e:
            print "fout: procedures :%s" % str(e)

    def verbind(self, initdb=False):
        try:
            self.dsn = cx_Oracle.makedsn(self.host,self.port,self.sid)
            self.connection = cx_Oracle.Connection(self.user, self.password, self.dsn));
            self.cursor = self.connection.cursor()

            if initdb:
                self.maak_schema()

            self.zet_schema()
            self.log.log("verbonden met sid %s" % (self.sid))
        except Exception, e:
            print("fout %s: kan geen verbinding maken met sid %s" % (str(e), self.sid))
            sys.exit()

    def uitvoeren(self, sql, parameters=None):
        try:
            if parameters:
                self.cursor.execute(sql, parameters)
            else:
                self.cursor.execute(sql)
        except (cx_Oracle.IntegrityError, cx_Oracle.ProgrammingError), e:
            print "fout %s voor query: %s" % (str(e), str(self.cursor.mogrify(sql, parameters)))
            return self.cursor.rowcount
