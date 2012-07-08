class Gemeentewoonplaats():
    """
    Klasse Gemeente
    """

    def __init__(self,record, configuratie):
        self.config = configuratie
        mydb = self.config.get_database()
        # TODO: de woonplaats_gemeente tabel ophalen met curl of wget
        if record[0]:
            self.woonplaatsnaam = record[0]
            self.woonplaatscode = record[1]
            self.begindatum_woonplaats = mydb.getDate(record[2])
            self.einddatum_woonplaats = mydb.getDate(record[3])
            self.gemeentenaam = record[4]
            self.gemeentecode = record[5]
            self.begindatum_gemeente = mydb.getDate(record[6])
            self.einddatum_gemeente = mydb.getDate(record[7])

    def __repr__(self):
       return "<GemeenteWoonplaats('%s','%s', '%s')>" % (self.woonplaatsnaam, self.gemeentecode, self.woonplaatscode)

    def insert(self):
        _sql = "INSERT INTO " + self.config.schema + ".gemeente_woonplaats ("
        self.sql = _sql + """
            woonplaatsnaam,
            woonplaatscode,
            begindatum_woonplaats,
            einddatum_woonplaats,
            gemeentenaam,
            gemeentecode,
            begindatum_gemeente,
            einddatum_gemeente)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
        self.valuelist = (self.woonplaatsnaam, self.woonplaatscode, self.begindatum_woonplaats, \
            self.einddatum_woonplaats,self.gemeentenaam, self.gemeentecode, self.begindatum_gemeente, \
            self.einddatum_gemeente)

    @staticmethod      
    def drop(schema):
        return "DROP TABLE IF EXISTS " + schema + ".gemeente_woonplaats;"

    @staticmethod    
    def create(schema):
        return """CREATE TABLE """ + schema + """.gemeente_woonplaats (
                  gid serial,
                  woonplaatsnaam character varying(80),
                  woonplaatscode numeric(4),
                  begindatum_woonplaats date,
                  einddatum_woonplaats date,
                  gemeentenaam character varying(80),
                  gemeentecode numeric(4),
                  begindatum_gemeente date,
                  einddatum_gemeente date,
                  PRIMARY KEY (gid)
                );"""
