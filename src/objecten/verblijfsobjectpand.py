class Verblijfsobjectpand():
    drop = "DROP TABLE IF EXISTS verblijfsobjectpand CASCADE;"

    create = """CREATE TABLE verblijfsobjectpand (
                  gid serial,
                  identificatie numeric(16,0),
                  aanduidingrecordinactief boolean,
                  aanduidingrecordcorrectie integer,
                  begindatumtijdvakgeldigheid timestamp without time zone,
                  einddatumtijdvakgeldigheid timestamp without time zone,
                  gerelateerdpand numeric(16,0),
                  PRIMARY KEY (gid)
                );"""

