__author__ = "Stefan de Konink"
__date__ = "$Jun 11, 2011 3:46:27 PM$"

#------------------------------------------------------------------------------
# Naam:         BAG.py
# Omschrijving: Universe starter voor de applicatie, console als grafisch
# Auteur:       Stefan de Konink
#------------------------------------------------------------------------------

import argparse
import sys
import postgresdb
import logger
import BAGFileReader

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
    parser = BAGParser(description='BAG Extract, commandline tool voor het verwerken van BAG bestanden',
        epilog="LET OP: configureer de database in BAG.conf")
    parser.add_argument('-c', '--dbinit', action='store_true', help='wist oude tabellen en maakt nieuw tabellen')
    parser.add_argument('-d', '--database', metavar='BAG', help='database naam')
    parser.add_argument('-e', '--extract', metavar='bestand', help='neemt een pad naar een extract en laadt deze')
    parser.add_argument('-H', '--host', metavar='localhost', help='database host')
    #parser.add_argument('-m', '--mutatie', metavar='bestand', help='neemt een pad naar een mutatie en laadt deze')
    parser.add_argument('-U', '--username', metavar='postgres', help='database gebruiker')
    parser.add_argument('-p', '--port', metavar='5432', help='database poort')
    parser.add_argument('-W', '--password', metavar='postgres', help='wachtwoord voor postgres')
    parser.add_argument('-w', '--no-password', action='store_true', help='gebruik geen wachtwoord voor de database verbinding')
    parser.add_argument('-v', '--verbose', action='store_true', help='toon uitgebreide informatie tijdens het verwerken')

    # Initialiseer
    args = parser.parse_args()
    database = postgresdb.Database(args)
    log = logger.LogHandler(args)
    
    #bagObjecten = []
    #bagObjecten.append(libBAG.Woonplaats())
    #bagObjecten.append(libBAG.OpenbareRuimte())
    #bagObjecten.append(libBAG.Nummeraanduiding())
    #bagObjecten.append(libBAG.Ligplaats())
    #bagObjecten.append(libBAG.Standplaats())
    #bagObjecten.append(libBAG.Verblijfsobject())
    #bagObjecten.append(libBAG.Pand())

    if args.dbinit:
        database.initialiseer('database/bagdb-1.0.sql')
        sys.exit()
    elif args.extract:
        #Verwerkt levering, extract en mutatie
        myreader = BAGFileReader.BAGFileReader(args.extract, args)
        myreader.process()
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
    main()
