class GerelateerdeAdressen():
    """
    BAG sub-klasse.
    Collectie van gerelateerde adressen
    """
    def __init__(self,xmlnode):
        self.tag = "bag_LVC:gerelateerdeAdressen"
        self.naam = "gerelateerdeAdressen"
        self.type = ''
        for node in xmlnode.childNodes:
            if node.localName == 'hoofdadres':
                for adresElement in node.childNodes:
                    if adresElement.localName == 'identificatie':
                        self.hoofdadres = getText(adresElement.childNodes)
    def __repr__(self):
       return "<GerelateerdeAdressen('%s')>" % (self.hoofdadres,)

