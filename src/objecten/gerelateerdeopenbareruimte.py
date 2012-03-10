class Gerelateerdeopenbareruimte():
    """
    BAG sub-klasse.
    """
    def __init__(self, xmlnode, configuratie):
        self.config = configuratie
        self.tag = "bag_LVC:gerelateerdeOpenbareRuimte"
        self.naam = "gerelateerdeOpenbareRuimte"
        self.type = ''
        mydb = self.config.get_database()
        for node in xmlnode.childNodes:
            if node.localName == 'identificatie':
                self.identificatie = mydb.getText(node.childNodes)
    def __repr__(self):
       return "<Gerelateerdeopenbareruimte('%s')>" % (self.identificatie,)
