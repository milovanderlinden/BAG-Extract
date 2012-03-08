class Bron():
    """
    BAG sub-klasse.
    """
    def __init__(self,xmlnode):
        self.tag = "bag_LVC:bron"
        self.naam = "bron"
        self.type = ''
        for node in xmlnode.childNodes:
            if node.localName == 'documentdatum':
                self.documentdatum = getDate(node)
            if node.localName == 'documentnummer':
                self.documentnummer = getText(node.childNodes)
    def __repr__(self):
       return "<Bron('%s','%s')>" % (self.documentdatum, self.documentnummer)
