class Gemeentewoonplaats():
    """
    Klasse Gemeente
    """

    def __init__(self,record, configuratie):
        self.config = configuratie
        mydb = self.config.get_database()
        # TODO: De csv is niet volledig gevuld, controleer of een record wel het minimaal aantal objecten bevat.
        # Woonplaats;Woonplaats code;Ingangsdatum WPL;Einddatum WPL;Gemeente;Gemeente code;
        # Ingangsdatum nieuwe gemeente;Aansluitdatum;Bijzonderheden;Nieuwe code Gemeente;
        # Gemeente beeindigd per;Behandeld;        Laatste WPL code:;3513

        # Dirty! Dit kan vast makkelijker, mijn python tekortkoming blijkt hier ;-)
        emptylist = [None,None,None,None,None,None,None,None,None,None,None,None]
        record.extend(emptylist)
        # Stel de lengte van het record object in op 12
        if record[0]:
            #print record
            self.tag = "gem_LVC:GemeenteWoonplaats"
            self.naam = "gemeente_woonplaats"
            self.type = 'G_W'
            self.woonplaatsnaam = record[0]
            self.woonplaatscode = record[1]
            self.ingangsdatum_woonplaats = mydb.getDate(record[2])
            self.einddatum_woonplaats = mydb.getDate(record[3])
            self.gemeentenaam = record[4]
            self.gemeentecode = record[5]
            self.ingangsdatum_gemeente = mydb.getDate(record[6])
            self.einddatum_gemeente = mydb.getDate(record[7])

    def __repr__(self):
       return "<GemeenteWoonplaats('%s','%s', '%s')>" % (self.naam, self.gemeentecode, self.woonplaatscode)

    def insert(self):
        _sql = "INSERT INTO " + self.config.schema + ".gemeente_woonplaats ("
        self.sql = _sql + """
            woonplaatsnaam,
            woonplaatscode,
            ingangsdatum_woonplaats,
            einddatum_woonplaats,
            gemeentenaam,
            gemeentecode,
            ingangsdatum_gemeente,
            einddatum_gemeente)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
        self.valuelist = (self.woonplaatsnaam, self.woonplaatscode, self.ingangsdatum_woonplaats, \
            self.einddatum_woonplaats,self.gemeentenaam, self.gemeentecode, self.ingangsdatum_gemeente, \
            self.einddatum_gemeente)
            
    drop = "DROP TABLE IF EXISTS gemeente_woonplaats;"
    
    create = """CREATE TABLE gemeente_woonplaats (
                  gid serial,
                  woonplaatsnaam character varying(80),
                  woonplaatscode numeric(4),
                  ingangsdatum_woonplaats date,
                  einddatum_woonplaats date,
                  gemeentenaam character varying(80),
                  gemeentecode numeric(4),
                  ingangsdatum_gemeente date,
                  einddatum_gemeente date,
                  PRIMARY KEY (gid)
                );"""
