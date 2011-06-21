__author__ = "Stefan de Konink"
__date__ = "$Jun 11, 2011 3:46:27 PM$"

"""
 Naam:         BAG.py
 Omschrijving: Universe starter voor de applicatie, console als grafisch
 Auteur:       Stefan de Konink
"""

import argparse #apt-get install python-argparse
import sys
import postgresdb
import logger
import BAGFileReader
from time import gmtime, strftime

nogui = False
try:
    import wx
except:
    nogui = True

class BAGParser(argparse.ArgumentParser):
     def error(self, message):
        if nogui:
            print "\nLet op: De wx bibliotheek is niet geinstalleerd, alleen de commandline versie is beschikbaar.\n"
        self.print_help()
        sys.exit(2)

def main():
    """
    Voorbeelden: 
        1. Initialiseer een database:
            python BAG.py -H localhost -d bag -U postgres -W postgres -c

        2. Importeer een extract in de database:
            python BAG.py -H localhost -d bag -U postgres -W postgres -e 9999STA01052011-000002.xml

            of

            python BAG.py -H localhost -d bag -U postgres -W postgres -e 9999STA01052011.zip

            Importeer gemeente_woonplaats informatie van het kadaster http://www.kadaster.nl/bag/docs/BAG_Overzicht_aangesloten_gemeenten.zip

            python BAG.py -H localhost -d bag -U postgres -W postgres -e BAG_Overzicht_aangesloten_gemeenten.zip

        Theoretisch is het mogelijk de hele bag in te lezen vanuit de "hoofd" zip, maar dit is nog niet getest op
        geheugen-problemen.

    """

    parser = BAGParser(description='BAG Extract, commandline tool voor het verwerken van BAG bestanden',
        epilog="Configureer de database in BAG.conf of geef de database parameters op")
    parser.add_argument('-c', '--dbinit', action='store_true', help='wist oude tabellen en maakt nieuw tabellen')
    parser.add_argument('-d', '--database', metavar='BAG', help='database naam')
    parser.add_argument('-e', '--extract', metavar='bestand', help='neemt een pad naar een bestand en importeert deze in de database')
    parser.add_argument('-H', '--host', metavar='localhost', help='database host')
    parser.add_argument('-U', '--username', metavar='postgres', help='database gebruiker')
    parser.add_argument('-p', '--port', metavar='5432', help='database poort')
    parser.add_argument('-W', '--password', metavar='postgres', help='wachtwoord voor postgres')
    parser.add_argument('-w', '--no-password', action='store_true', help='gebruik geen wachtwoord voor de database verbinding')
    parser.add_argument('-v', '--verbose', action='store_true', help='toon uitgebreide informatie tijdens het verwerken')

    # Initialiseer
    args = parser.parse_args()
    database = postgresdb.Database(args)
    log = logger.LogHandler(args)

    if args.dbinit:
        database.initialiseer('database/bagdb-1.0.sql')
        sys.exit()
    elif args.extract:
        myreader = BAGFileReader.BAGFileReader(args.extract, args)
        myreader.process()
        print strftime("%Y-%m-%d %H:%M:%S", gmtime())
        sys.exit()
    else:
        if nogui:
            log.log("\nLet op: De wx bibliotheek is niet geinstalleerd, alleen de commandline versie is beschikbaar.\n")
            self.print_help()
            sys.exit(2)
        else:
            import BAGextractplus
            app = wx.App(0)
            BAGextractplus.BAGExtractPlus(app, bagObjecten)
            app.MainLoop()

if __name__ == "__main__":
    print strftime("%Y-%m-%d %H:%M:%S", gmtime())
    main()
