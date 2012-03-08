class Tijdvakgeldigheid():
    """
    BAG sub-klasse.
    """

    def __init__(self, xmlnode, configuratie):
        self.config = configuratie
        self.tag = "bag_LVC:tijdvakgeldigheid"
        self.naam = "tijdvakgeldigheid"
        self.type = ''
        self.einddatum = None
        self.begindatum = None
        mydb = self.config.get_database()
        for node in xmlnode.childNodes:
            if node.localName == 'begindatumTijdvakGeldigheid':
                self.begindatum = mydb.getDate(node)
            if node.localName == 'einddatumTijdvakGeldigheid':
                self.einddatum = mydb.getDate(node)

    def __repr__(self):
       return "<Tijdvakgeldigheid('%s','%s')>" % (self.begindatum, self.einddatum)

