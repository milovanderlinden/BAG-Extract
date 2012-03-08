class GerelateerdPand():
    """
    BAG sub-klasse.
    """
    def __init__(self,xmlnode):
        self.tag = "bag_LVC:gerelateerdPand"
        self.naam = "gerelateerdPand"
        self.type = ''
        for node in xmlnode.childNodes:
            if node.localName == 'identificatie':
                self.identificatie = getText(node.childNodes)
    def __repr__(self):
       return "<GerelateerdPand('%s')>" % (self.identificatie,)
