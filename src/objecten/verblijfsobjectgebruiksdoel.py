class Verblijfsobjectgebruiksdoel():

    @staticmethod      
    def drop(schema):
        return "DROP TABLE IF EXISTS " + schema + ".verblijfsobjectgebruiksdoel CASCADE;"
    
    @staticmethod      
    def create(schema):
        return """CREATE TABLE """ + schema + """.verblijfsobjectgebruiksdoel (
                  gid serial,
                  identificatie numeric(16,0),
                  aanduidingrecordinactief boolean,
                  aanduidingrecordcorrectie integer,
                  begindatumtijdvakgeldigheid timestamp without time zone,
                  einddatumtijdvakgeldigheid timestamp without time zone,
                  gebruiksdoelverblijfsobject character varying(50),
                  PRIMARY KEY (gid)
                );"""

