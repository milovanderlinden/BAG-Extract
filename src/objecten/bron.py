class Bron():
    """
    BAG sub-klasse Bron. Deze wordt platgeslagen vanwege het ontbreken van sleutels.
    """
    def __init__(self, xmlnode, configuratie):
        self.config = configuratie
        self.tag = "bag_LVC:bron"
        self.naam = "bron"
        self.type = ''
        mydb = self.config.get_database()
        for node in xmlnode.childNodes:
            if node.localName == 'documentdatum':
                self.documentdatum = mydb.getDate(node)
            if node.localName == 'documentnummer':
                self.documentnummer = mydb.getText(node.childNodes)
    def __repr__(self):
       return "<Bron('%s','%s')>" % (self.documentdatum, self.documentnummer)
