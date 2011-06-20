__author__="Milo van der Linden"
__date__ ="$Jun 14, 2011 11:11:01 AM$"

import Objecten
import postgresdb

class Orm:
    # TODO:
    # Ben tot hier gekomen met etree. node.localName kent alleen een representatief
    # in de vorm van element.tag
    # Maar hier zitten de namespaces in:
    #
    # print xml.getroot().tag
    #   {http://www.kadaster.nl/schemas/bag-verstrekkingen/extract-deelbestand-lvc/v20090901}BAG-Extract-Deelbestand-LVC
    #
    # Deze moeten of gestript worden, of de functie die dit automatisch doet moet worden gevonden.

    def __init__(self, args):
        self.args = args
        self.database = postgresdb.Database(args)

    def getCSV(self, csvreader):
        self.gemeentewoonplaatsen = []
        # TODO: Controleer of de eerste regel de verwachte headers bevat
        cols = csvreader.next()
        if (cols[0] == 'Woonplaats') and (cols[4] == 'Gemeente'):
            for record in csvreader:
                if record[0]:
                    obj = Objecten.GemeenteWoonplaats(record)
                    self.gemeentewoonplaatsen.append(obj)
                    print obj
                
        #self.database.verbind()
        #for gemeentewoonplaats in self.gemeentewoonplaatsen:
        #    gemeentewoonplaats.insert()
        #    self.database.uitvoeren(gemeentewoonplaats.sql, gemeentewoonplaats.valuelist)

    def getDocument(self, node):
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
                        # TODO: Is het een idee om vraag als object ook af te
                        # handelen en op te slaan
                        vraag = child
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

            self.database.verbind()
            for ligplaats in self.ligplaatsen:
                ligplaats.insert()
                self.database.uitvoeren(ligplaats.sql, ligplaats.valuelist)
            for woonplaats in self.woonplaatsen:
                woonplaats.insert()
                self.database.uitvoeren(woonplaats.sql, woonplaats.valuelist)
            for verblijfsobject in self.verblijfsobjecten:
                verblijfsobject.insert()
                self.database.uitvoeren(verblijfsobject.sql, verblijfsobject.valuelist)
            for openbareruimte in self.openbareRuimten:
                openbareruimte.insert()
                self.database.uitvoeren(openbareruimte.sql, openbareruimte.valuelist)
            for nummeraanduiding in self.nummeraanduidingen:
                nummeraanduiding.insert()
                self.database.uitvoeren(nummeraanduiding.sql, nummeraanduiding.valuelist)
            for standplaats in self.standplaatsen:
                standplaats.insert()
                self.database.uitvoeren(standplaats.sql, standplaats.valuelist)
            for pand in self.panden:
                pand.insert()
                self.database.uitvoeren(pand.sql, pand.valuelist)
            self.database.connection.commit()
        # Leveringsinformatie
        if node.localName == 'BAG-Extract-Levering':
            return 'levering'
        # Mutatie
        if node.localName == '':
            return 'mutatie'