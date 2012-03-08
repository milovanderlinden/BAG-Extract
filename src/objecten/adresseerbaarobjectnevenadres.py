class Adresseerbaarobjectnevenadres():

    drop = "DROP TABLE IF EXISTS adresseerbaarobjectnevenadres CASCADE;"

    create = """CREATE TABLE adresseerbaarobjectnevenadres (
                  gid serial,
                  identificatie numeric(16,0),
                  aanduidingrecordinactief boolean,
                  aanduidingrecordcorrectie integer,
                  begindatumtijdvakgeldigheid timestamp without time zone,
                  nevenadres numeric(16,0),
                  PRIMARY KEY (gid)
                );"""

