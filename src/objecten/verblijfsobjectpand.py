class Verblijfsobjectpand():
    @staticmethod      
    def drop(schema):
        return "DROP TABLE IF EXISTS " + schema + ".verblijfsobjectpand CASCADE;"

    @staticmethod      
    def create(schema):
        return """CREATE TABLE """ + schema + """.verblijfsobjectpand (
                  gid serial,
                  identificatie numeric(16,0),
                  aanduidingrecordinactief boolean,
                  aanduidingrecordcorrectie integer,
                  begindatumtijdvakgeldigheid timestamp without time zone,
                  einddatumtijdvakgeldigheid timestamp without time zone,
                  gerelateerdpand numeric(16,0),
                  PRIMARY KEY (gid)
                );"""

