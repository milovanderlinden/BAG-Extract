# Naam:         libDatabase.py
# Omschrijving: Generieke functies voor databasegebruik binnen BAG Extract+
# Auteur:       Matthijs van der Deijl
#
# Versie:       1.3
#               - functie controleerTabellen toegevoegd
#               - selectie van logregels gesorteerd op datum
# Datum:        9 december 2009
#
# Versie:       1.2
# Datum:        24 november 2009
#
# Ministerie van Volkshuisvesting, Ruimtelijke Ordening en Milieubeheer
#------------------------------------------------------------------------------
import psycopg2
from libBAGconfiguratie import *
from libLog import *

class Database:
    def __init__(self, args):
        # Lees de configuratie uit BAG.conf
        self.args = args
        #print args
        if args.database:
            self.database = args.database
        else:
            self.database = configuratie.database
        if args.host:
            self.host = args.host
        else:
            self.host = configuratie.host
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
        print 'Probeer te verbinden...'
        self.verbind()
        print 'database script uitvoeren...'
        try:
            script  = open(bestand,'r').read()
            self.cursor.execute(script)
            self.connection.commit()
            print 'script uitgevoerd'
        except psycopg2.DatabaseError, e:
            print "fout: procedures :%s" % str(e)
            
    def verbind(self):
        try:
            self.connection = psycopg2.connect("dbname='%s' user='%s' host='%s' password='%s'" %(self.database,
                                                                                                 self.user,
                                                                                                 self.host,
                                                                                                 self.password));
            self.cursor = self.connection.cursor()
            if self.args.verbose:
                print("verbonden met database %s" %(self.database))
        except Exception, e:
            print str(e)
            print("fout: kan geen verbinding maken met database %s" %(self.database))
            sys.exit()
    # Maak van de datum/tijdstip string in de BAG een datumwaarde voor in de database 
    def datum(self, tekst):
        # TODO: Echte datum functie toepassen.
        if tekst == '':
            return "2299-12-31"
        else:
            return "%c%c%c%c-%c%c-%c%c" %(tekst[0],tekst[1],tekst[2],tekst[3],tekst[4],tekst[5],tekst[6],tekst[7])

    # Geef de waarde in de vorm waarin het kan worden ingevoegd in de database
    def string(self, tekst):
        # TODO: Controleren of deze functie obsolete kan worden als psycopg2 goed wordt gebruikt!
        # Vervang een ' in een string door ''
        # Vervang een \n door een spatie
        # Vervang een \ door \\
        return tekst.replace("'", "''").replace("\n", " ").replace("\\", "\\\\")

    def maakObject(self, soort, naam, dropSQL, createSQL, parameters=None):
        # Probeer eerst het oude object weg te gooien. 
        try:
            self.connection.set_isolation_level(0)
            self.cursor.execute(dropSQL)
            if args.verbose:
                print "%s %s verwijderd" %(soort, naam)
        except:
            pass

        # Maak het object nieuw aan.
        try:
            self.connection.set_isolation_level(0)
            if parameters:
                print createSQL
                print parameters
                self.cursor.mogrify(createSQL, parameters)
                self.cursor.execute(createSQL, parameters)
            else:
                self.cursor.execute(createSQL)
                
            log("%s %s nieuw aangemaakt" %(soort, naam))
            self.connection.commit()
            return True
        except (psycopg2.Error,), foutmelding:
            log("*** FOUT *** Kan %s %s niet maken:\n %s" %(soort, naam, foutmelding))
            return False
        
    def maakTabel(self, naam, createSQL, parameters=None):
        if parameters:
            return self.maakObject("Tabel", naam, "DROP TABLE %s CASCADE" %(naam), createSQL, parameters)
        else:
            return self.maakObject("Tabel", naam, "DROP TABLE %s CASCADE" %(naam), createSQL)

    def maakView(self, naam, createSQL):
        return self.maakObject("View", naam, "DROP VIEW %s" %(naam), createSQL)

    def maakIndex(self, naam, createSQL):
        return self.maakObject("Index", naam, "DROP INDEX %s" %(naam), createSQL)

    def insert(self, sql, identificatie, parameters=None):
        try:
            if parameters:
                self.cursor.execute(sql, parameters)
            else:
                self.cursor.execute(sql)
        except (psycopg2.IntegrityError,), foutmelding:
            log("* Waarschuwing * Object %s niet opgeslagen: %s" %(identificatie, str(foutmelding)))
        except (psycopg2.Error,), foutmelding:
            log("*** FOUT *** Object %s niet opgeslagen: %s - %s" %(identificatie, str(foutmelding), sql))
        self.connection.commit()

    def execute(self, sql, parameters=None):
        try:
            if parameters:
                self.cursor.execute(sql, parameters)
            else:
                self.cursor.execute(sql)
            self.connection.commit()
            return self.cursor.rowcount
        except (psycopg2.Error,), foutmelding:
            # TODO: rollback uitvoeren bij INSERT!
            log("*** FOUT *** Kan SQL-statement '%s' niet uitvoeren:\n %s" %(sql, foutmelding))
            return False

    def select(self, sql, parameters=None):
        try:
            if parameters:
                self.cursor.execute(sql,parameters)
            else:
                self.cursor.execute(sql)
            rows = self.cursor.fetchall()
            self.connection.commit()
            return rows
        except (psycopg2.Error,), foutmelding:
            log("*** FOUT *** Kan SQL-statement '%s' niet uitvoeren:\n %s" %(sql, foutmelding))
            return []
    
    def controleerOfMaakLog(self):
        try:
            self.cursor.execute("SELECT * FROM BAGextractpluslog")
        except:
            sql  = "CREATE TABLE BAGextractpluslog"
            sql += "(datum   DATE"
            sql += ",actie   VARCHAR(1000)"
            sql += ",bestand VARCHAR(1000)"
            sql += ",logfile VARCHAR(1000))"
            self.maakTabel("BAGextractpluslog", sql)
            
    def log(self, actie, bestand, logfile):
        self.controleerOfMaakLog()
        dt = datetime.datetime.now()
        sql  = "INSERT INTO BAGextractpluslog (datum, actie, bestand, logfile) VALUES (%s, %s, %s, %s);"
        parameters = (dt.date(), str(actie), str(bestand), str(logfile))
        self.execute(sql, parameters)
        
    def getLog(self):
        self.controleerOfMaakLog()
        sql = "SELECT * FROM BAGextractpluslog ORDER BY datum, logfile"
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        self.connection.commit()
        return rows

    def controleerTabel(self, tabel):
        schema = 'public'
        sql = "select exists(select * from information_schema.tables where table_schema=%s AND table_name=%s)"
        parameters = (tabel,schema)
        self.cursor.execute(sql, parameters)
        if cur.fetchone()[0]:
            return True
        else:
            return False

