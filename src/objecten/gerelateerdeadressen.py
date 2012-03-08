class Gerelateerdeadressen():
    """
    BAG sub-klasse.
    Collectie van gerelateerde adressen
    """
    def __init__(self, xmlnode, configuratie):
        self.config = configuratie
        self.tag = "bag_LVC:gerelateerdeAdressen"
        self.naam = "gerelateerdeAdressen"
        self.type = ''
        
        mydb = self.config.get_database()
        
        for node in xmlnode.childNodes:
            if node.localName == 'hoofdadres':
                for adresElement in node.childNodes:
                    if adresElement.localName == 'identificatie':
                        self.hoofdadres = mydb.getText(adresElement.childNodes)
    def __repr__(self):
       return "<GerelateerdeAdressen('%s')>" % (self.hoofdadres,)

