class GerelateerdeWoonplaats():
    """
    BAG sub-klasse.
    """
    def __init__(self,xmlnode=None):
        self.tag = "bag_LVC:gerelateerdeWoonplaats"
        self.naam = "gerelateerdeWoonplaats"
        self.type = ''
        if xmlnode:
            for node in xmlnode.childNodes:
                if node.localName == 'identificatie':
                    self.identificatie = getText(node.childNodes)
        else:
            self.identificatie = None

    def __repr__(self):
        return "<GerelateerdeWoonplaats('%s')>" % (self.identificatie,)
