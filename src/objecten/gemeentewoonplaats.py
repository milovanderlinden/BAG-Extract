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
            self.begindatum_woonplaats = mydb.getDate(record[2])
            self.einddatum_woonplaats = mydb.getDate(record[3])
            self.gemeentenaam = record[4]
            self.gemeentecode = record[5]
            self.begindatum_gemeente = mydb.getDate(record[6])
            self.aansluitdatum_gemeente = mydb.getDate(record[7])
            self.bijzonderheden = record[8]
            self.gemeentecode_nieuw = record[9]
            self.einddatum_gemeente = mydb.getDate(record[10])
            self.behandeld = record[11]

    def __repr__(self):
       return "<GemeenteWoonplaats('%s','%s', '%s')>" % (self.naam, self.gemeentecode, self.woonplaatscode)

    def insert(self):
        self.sql = """INSERT INTO gemeente_woonplaats (
            woonplaatsnaam,
            woonplaatscode,
            begindatum_woonplaats,
            einddatum_woonplaats,
            gemeentenaam,
            gemeentecode,
            begindatum_gemeente,
            aansluitdatum_gemeente,
            bijzonderheden,
            gemeentecode_nieuw,
            einddatum_gemeente,
            behandeld)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        self.valuelist = (self.woonplaatsnaam, self.woonplaatscode, self.begindatum_woonplaats, \
            self.einddatum_woonplaats,self.gemeentenaam, self.gemeentecode, self.begindatum_gemeente, \
            self.aansluitdatum_gemeente, self.bijzonderheden, self.gemeentecode_nieuw, self.einddatum_gemeente, \
            self.behandeld)
            
    drop = "DROP TABLE IF EXISTS gemeente_woonplaats;"
    
    create = """CREATE TABLE gemeente_woonplaats (
                  gid serial,
                  woonplaatsnaam character varying(80),
                  woonplaatscode numeric(4),
                  begindatum_woonplaats date,
                  einddatum_woonplaats date,
                  gemeentenaam character varying(80),
                  gemeentecode numeric(4),
                  begindatum_gemeente date,
                  aansluitdatum_gemeente date,
                  bijzonderheden text,
                  gemeentecode_nieuw numeric(4),
                  einddatum_gemeente date,
                  behandeld character varying(1),
                  PRIMARY KEY (gid)
                );"""
