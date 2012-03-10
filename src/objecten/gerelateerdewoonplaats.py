class Gerelateerdewoonplaats():
    """
    BAG sub-klasse.
    """
    def __init__(self,xmlnode, configuratie):
        self.config = configuratie
        self.tag = "bag_LVC:gerelateerdeWoonplaats"
        self.naam = "gerelateerdeWoonplaats"
        self.type = ''
        mydb = self.config.get_database()
        if xmlnode:
            for node in xmlnode.childNodes:
                if node.localName == 'identificatie':
                    self.identificatie = mydb.getText(node.childNodes)
        else:
            self.identificatie = None

    def __repr__(self):
        return "<Gerelateerdewoonplaats('%s')>" % (self.identificatie,)
