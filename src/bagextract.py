"""
 Naam: bagextract.py (voorheen: BAG.py)
 Omschrijving: Universe commandline starter voor de BAG extract applicatie
 Auteur(s): Stefan de Konink, Milo van der Linden, Just van den Broecke
"""

import sys
import os
import logging
from time import gmtime, strftime

try:
    import argparse #apt-get install python-argparse
except:
    formatter = logging.Formatter('%(levelname)s - %(message)s')
    logging.critical("Python argparse is vereist")
    sys.exit()   

class ArgParser(argparse.ArgumentParser):
     def error(self, message):
        self.print_help()
        sys.exit()


def main():

    """
    Voorbeelden: 
    1. Initialiseer een database:
    python bagextract.py -H localhost -d bag -U postgres -W postgres -c

    2. Importeer een extract in de database:
    python bagextract.py -H localhost -d bag -U postgres -W postgres -e 9999STA01052011-000002.xml

    of

    python bagextract.py -H localhost -d bag -U postgres -W postgres -e 9999STA01052011.zip

    Importeer gemeente_woonplaats informatie van het kadaster http://www.kadaster.nl/bag/docs/BAG_Overzicht_aangesloten_gemeenten.zip

    python bagextract.py -H localhost -d bag -U postgres -W postgres -e BAG_Overzicht_aangesloten_gemeenten.zip

    Theoretisch is het mogelijk de hele bag in te lezen vanuit de "hoofd" zip, maar dit is nog niet getest op
    geheugen-problemen.
    """

    parser = ArgParser(description='bag-extract, commandline tool voor het extraheren en inlezen van BAG bestanden',
        epilog="Configureer de database in extract.conf of geef eigen versie van extract.conf via -f of geef parameters via commando regel expliciet op")
    parser.add_argument('-c', '--dbinit', action='store_true', help='verwijdert alle BAG tabellen en maakt deze opnieuw aan')
    parser.add_argument('-d', '--database', metavar='<naam>', help='geef naam van de database')
    parser.add_argument('-s', '--schema', metavar='<naam>', help='geef naam van het database schema')
    parser.add_argument('-f', '--config', metavar='<bestand>', help='gebruik dit configuratiebestand i.p.v. extract.conf')
    parser.add_argument('-q', '--query', metavar='<bestand>', help='voer database bewerkingen uit met opgegeven SQL bestand')
    parser.add_argument('-e', '--extract', metavar='<naam>', help='importeert of muteert de database met gegeven BAG-bestand of -directory')
    parser.add_argument('-H', '--host', metavar='<hostnaam of -adres>', help='verbind met de database op deze host')
    parser.add_argument('-U', '--username', metavar='<naam>', help='verbind met database met deze gebruikersnaam')
    parser.add_argument('-p', '--port', metavar='<poort>', help='verbind met database naar deze poort')
    parser.add_argument('-W', '--password', metavar='<paswoord>', help='gebruikt dit wachtwoord voor database gebruiker')
    parser.add_argument('-w', '--no-password', action='store_true', help='gebruik geen wachtwoord voor de database verbinding')
    parser.add_argument('-v', '--verbose', action='store_true', help='toon uitgebreide informatie tijdens het verwerken')

    # Initialiseer
    args = parser.parse_args()

    # Init globale configuratie
    from bagconfig import BAGConfig
    myconfig = BAGConfig(args)
    
    if args.verbose:
        myconfig.logger.setLevel(logging.DEBUG)
    else:
        myconfig.logger.setLevel(logging.INFO)
        
    if args.dbinit:
        mydb = myconfig.get_database()
        mydb.maak_database()
        
    elif args.extract:
        from bagfilereader import BAGFilereader
        myreader = BAGFilereader(myconfig)
        myreader.process()
        
    elif args.query:
        #TODO geen args gebruiken maar BAGConfig.
        # Op deze manier gaan beide configuraties uit de pas lopen met kans op fouten
        # Voer willekeurig SQL script uit uit
        mydb = myconfig.get_database()
        mydb.file_uitvoeren(myconfig.query)
        
    else:
        myconfig.logger.critical("Kan de opdracht niet verwerken. Type -h of --help voor een overzicht van parameters")

    myconfig.logger.info("bagextract.py beeindigd")
    sys.exit()
    
if __name__ == "__main__":
    main()
