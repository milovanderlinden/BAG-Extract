class Verblijfsobjectgebruiksdoel():

    drop = "DROP TABLE IF EXISTS verblijfsobjectgebruiksdoel CASCADE;"
    
    create = """CREATE TABLE verblijfsobjectgebruiksdoel (
                  gid serial,
                  identificatie numeric(16,0),
                  aanduidingrecordinactief boolean,
                  aanduidingrecordcorrectie integer,
                  begindatumtijdvakgeldigheid timestamp without time zone,
                  gebruiksdoelverblijfsobject character varying(50),
                  PRIMARY KEY (gid)
                );"""

