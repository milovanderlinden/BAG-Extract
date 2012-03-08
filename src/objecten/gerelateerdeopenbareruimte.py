class GerelateerdeOpenbareRuimte():
    """
    BAG sub-klasse.
    """
    def __init__(self,xmlnode):
        self.tag = "bag_LVC:gerelateerdeOpenbareRuimte"
        self.naam = "gerelateerdeOpenbareRuimte"
        self.type = ''
        for node in xmlnode.childNodes:
            if node.localName == 'identificatie':
                self.identificatie = getText(node.childNodes)
    def __repr__(self):
       return "<GerelateerdeOpenbareRuimte('%s')>" % (self.identificatie,)
