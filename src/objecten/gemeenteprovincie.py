class Gemeenteprovincie():
    
    @staticmethod
    def drop(schema):
        return "DROP TABLE IF EXISTS  " + schema + ".gemeente_provincie;"
    
    @staticmethod
    def create(schema):
        return"""CREATE TABLE """ + schema + """.gemeente_provincie (
                  gid serial,
                  gemeentecode numeric(4),
                  gemeentenaam character varying(80),
                  provinciecode numeric(4),
                  provincienaam character varying(80),
                  PRIMARY KEY (gid)
                );"""

