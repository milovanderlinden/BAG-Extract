class Adresseerbaarobjectnevenadres():

    @staticmethod
    def drop(schema):
        return "DROP TABLE IF EXISTS " + schema + ".adresseerbaarobjectnevenadres CASCADE;"

    @staticmethod
    def create(schema):
        return """CREATE TABLE """ + schema + """.adresseerbaarobjectnevenadres (
                  gid serial,
                  identificatie numeric(16,0),
                  aanduidingrecordinactief boolean,
                  aanduidingrecordcorrectie integer,
                  begindatumtijdvakgeldigheid timestamp without time zone,
                  einddatumtijdvakgeldigheid timestamp without time zone,
                  nevenadres numeric(16,0),
                  PRIMARY KEY (gid)
                );"""

