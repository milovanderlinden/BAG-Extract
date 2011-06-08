#------------------------------------------------------------------------------
# Naam:         BAG.py
# Omschrijving: Universe starter voor de applicatie, console als grafisch
# Auteur:       Stefan de Konink
#------------------------------------------------------------------------------


import getopt
import sys
from libLog import *
from libDatabase import *
from libBAG import *
from libUnzip import *
from libLijm import *

try:
    import wx
except:
    nogui = True

def gebruik():
    print "%s		--dbinit        - wist oude tabellen en maakt nieuw tabellen\n" \
          "		--dbindex       - herindexeert de database\n" \
          "		--extract=<pad> - neemt een pad naar een extract en laadt deze\n" \
          "		--mutatie=<pad> - neemt een pad naar een mutatie en laadt deze\n" \
          "\n" \
          "De connectie naar de database wordt geconfigureerd in: BAG.conf" % sys.argv[0]

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "ho:v", ["help", "dbinit", "dbindex", "extract=", "mutatie="])
    except getopt.GetoptError, err:
        print str(err) # will print something like "option -a not recognized"
        gebruik()
        sys.exit(2)

    bagObjecten = []
    bagObjecten.append(Woonplaats())
    bagObjecten.append(OpenbareRuimte())
    bagObjecten.append(Nummeraanduiding())
    bagObjecten.append(Ligplaats())
    bagObjecten.append(Standplaats())
    bagObjecten.append(Verblijfsobject())
    bagObjecten.append(Pand())
    # TODO verbose wordt nog niet gebruikt
    verbose = False
    for o, a in opts:
        if o == "-v":
            verbose = True
        elif o in ("-h", "--help"):
            gebruik()
            sys.exit()
        elif o in ("--dbinit"):
            dbInit(bagObjecten)
            sys.exit()
        elif o in ("--dbindex"):
            dbMaakIndex(bagObjecten)
            sys.exit()
        elif o in ("--extract="):
            bestandVerwerkExtractPad(log, a, bagObjecten)
            sys.exit()
        elif o in ("--mutatie="):
            bestandVerwerkMutatiePad(log, a)
            sys.exit()
        else:
            assert False, "unhandled option"


    if nogui:
        print "\nLet op: De wx bibliotheek is niet geinstalleerd, alleen de commandline versie is beschikbaar.\n"
        gebruik()
        sys.exit()
    else:
        app = wx.App(0)
        BAGExtractPlus(app, bagObjecten)
        app.MainLoop()

if __name__ == "__main__":
    main()
