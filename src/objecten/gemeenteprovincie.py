class Gemeenteprovincie():
    drop = "DROP TABLE IF EXISTS gemeente_provincie;"
    create = """CREATE TABLE gemeente_provincie (
                  gid serial,
                  gemeentecode numeric(4),
                  gemeentenaam character varying(80),
                  provinciecode numeric(4),
                  provincienaam character varying(80),
                  PRIMARY KEY (gid)
                );"""

