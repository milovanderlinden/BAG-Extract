class Tijdvakgeldigheid():
    """
    BAG sub-klasse.
    """
    def __init__(self,xmlnode):
        self.tag = "bag_LVC:tijdvakgeldigheid"
        self.naam = "tijdvakgeldigheid"
        self.type = ''
        self.einddatum = None
        self.begindatum = None
        for node in xmlnode.childNodes:
            if node.localName == 'begindatumTijdvakGeldigheid':
                self.begindatum = getDate(node)
            if node.localName == 'einddatumTijdvakGeldigheid':
                self.einddatum = getDate(node)
    def __repr__(self):
       return "<Tijdvakgeldigheid('%s','%s')>" % (self.begindatum, self.einddatum)

