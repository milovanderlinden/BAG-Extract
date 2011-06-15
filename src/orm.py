__author__="Milo van der Linden"
__date__ ="$Jun 14, 2011 11:11:01 AM$"

import Objecten
import postgresdb

class Orm:
    def __init__(self, args):
        self.args = args
        self.database = postgresdb.Database(args)
    def getDocument(self, node):
        #print node.localName
        self.ligplaatsen = []
        self.woonplaatsen = []
        self.verblijfsobjecten = []
        self.openbareRuimten = []
        self.nummeraanduidingen = []
        self.standplaatsen = []
        self.panden = []

        if node.localName == 'BAG-Extract-Deelbestand-LVC':
            #firstchild moet zijn 'antwoord'
            if node.firstChild.localName == 'antwoord':
                # Antwoord bevat twee childs: vraag en producten
                antwoord = node.firstChild
                for child in antwoord.childNodes:
                    if child.localName == "vraag":
                        vraag = child
                        #print 'vraag'
                    elif child.localName == "producten":
                        producten = child
                        for productnode in producten.childNodes:
                            if productnode.localName == 'LVC-product':
                                for bagnode in productnode.childNodes:
                                    if bagnode.localName == 'Ligplaats':
                                        self.ligplaatsen.append(Objecten.Ligplaats(bagnode))
                                    if bagnode.localName == 'Woonplaats':
                                        self.woonplaatsen.append(Objecten.Woonplaats(bagnode))
                                    if bagnode.localName == 'Verblijfsobject':
                                        self.verblijfsobjecten.append(Objecten.Verblijfsobject(bagnode))
                                    if bagnode.localName == 'OpenbareRuimte':
                                        self.openbareRuimten.append(Objecten.OpenbareRuimte(bagnode))
                                    if bagnode.localName == 'Nummeraanduiding':
                                        self.nummeraanduidingen.append(Objecten.Nummeraanduiding(bagnode))
                                    if bagnode.localName == 'Standplaats':
                                        self.standplaatsen.append(Objecten.Standplaats(bagnode))
                                    if bagnode.localName == 'Pand':
                                        self.panden.append(Objecten.Pand(bagnode))
                                    #elif bagnode.localName == 'productcode':
                                        #print gettext(bagnode.childNodes)
                                    #    print 'productcode'
                                    #else:
                                    #    print bagnode.localName
            #self.database.verbind()
            # Raymonds commit loop nodig!
            #for ligplaats in self.ligplaatsen:
            #    ligplaats.insert()
            #    self.database.uitvoeren(ligplaats.sql,ligplaats.valuelist)
            print self.ligplaatsen
            print self.woonplaatsen
            print self.verblijfsobjecten
            print self.openbareRuimten
            print self.nummeraanduidingen
            print self.standplaatsen
            print self.panden
            return self

        # Leveringsinformatie
        if node.localName == 'BAG-Extract-Levering':
            return 'levering'
        # Mutatie
        if node.localName == '':
            return 'mutatie'