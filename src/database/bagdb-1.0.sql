-- Systeem tabellen
DROP TABLE IF EXISTS bagextractpluslog;
CREATE TABLE bagextractpluslog (
    datum date,
    actie character varying(1000),
    bestand character varying(1000),
    logfile character varying(1000)
);

DROP TABLE IF EXISTS bagextractplus;
CREATE TABLE bagextractplus (
    id serial,
    sleutel character varying (25),
    waarde character varying (100)
);
INSERT INTO bagextractplus (sleutel,waarde) VALUES ('versie', '1.0.2');

-- BAG tabellen
DROP TABLE IF EXISTS adresseerbaarobjectnevenadres;
CREATE TABLE adresseerbaarobjectnevenadres (
    identificatie character varying(16),
    aanduidingrecordinactief character varying(1),
    aanduidingrecordcorrectie character varying(5),
    begindatumtijdvakgeldigheid character varying(16),
    nevenadres character varying(16)
);

DROP VIEW IF EXISTS ligplaatsactueelbestaand;
DROP VIEW IF EXISTS ligplaatsactueel;

DROP TABLE IF EXISTS ligplaats;
CREATE TABLE ligplaats (
    identificatie character varying(16),
    aanduidingrecordinactief character varying(1),
    aanduidingrecordcorrectie character varying(5),
    officieel character varying(1),
    inonderzoek character varying(1),
    begindatumtijdvakgeldigheid character varying(16),
    einddatumtijdvakgeldigheid character varying(16),
    documentnummer character varying(20),
    documentdatum character varying(8),
    hoofdadres character varying(16),
    ligplaatsstatus character varying(80),
    ligplaatsgeometrie character varying(1000000),
    begindatum date,
    einddatum date,
    geometrie geometry,
    CONSTRAINT enforce_dims_geometrie CHECK ((st_ndims(geometrie) = 3)),
    CONSTRAINT enforce_geotype_geometrie CHECK (((geometrytype(geometrie) = 'POLYGON'::text) OR (geometrie IS NULL))),
    CONSTRAINT enforce_srid_geometrie CHECK ((st_srid(geometrie) = 28992))
) WITH ( OIDS=TRUE );

CREATE VIEW ligplaatsactueel AS
    SELECT (ligplaats.oid)::character varying AS oid, ligplaats.identificatie, ligplaats.aanduidingrecordinactief, ligplaats.aanduidingrecordcorrectie, ligplaats.officieel, ligplaats.inonderzoek, ligplaats.begindatumtijdvakgeldigheid, ligplaats.einddatumtijdvakgeldigheid, ligplaats.documentnummer, ligplaats.documentdatum, ligplaats.hoofdadres, ligplaats.ligplaatsstatus, ligplaats.ligplaatsgeometrie, ligplaats.begindatum, ligplaats.einddatum, ligplaats.geometrie FROM ligplaats WHERE (((ligplaats.begindatum <= ('now'::text)::date) AND (ligplaats.einddatum >= ('now'::text)::date)) AND ((ligplaats.aanduidingrecordinactief)::text = 'N'::text));

CREATE VIEW ligplaatsactueelbestaand AS
    SELECT (ligplaats.oid)::character varying AS oid, ligplaats.identificatie, ligplaats.aanduidingrecordinactief, ligplaats.aanduidingrecordcorrectie, ligplaats.officieel, ligplaats.inonderzoek, ligplaats.begindatumtijdvakgeldigheid, ligplaats.einddatumtijdvakgeldigheid, ligplaats.documentnummer, ligplaats.documentdatum, ligplaats.hoofdadres, ligplaats.ligplaatsstatus, ligplaats.ligplaatsgeometrie, ligplaats.begindatum, ligplaats.einddatum, ligplaats.geometrie FROM ligplaats WHERE ((((ligplaats.begindatum <= ('now'::text)::date) AND (ligplaats.einddatum >= ('now'::text)::date)) AND ((ligplaats.aanduidingrecordinactief)::text = 'N'::text)) AND ((ligplaats.ligplaatsstatus)::text <> 'Plaats ingetrokken'::text));

DROP VIEW IF EXISTS nummeraanduidingactueel;
DROP VIEW IF EXISTS nummeraanduidingactueelbestaand;

DROP TABLE IF EXISTS nummeraanduiding;
CREATE TABLE nummeraanduiding (
    identificatie character varying(16),
    aanduidingrecordinactief character varying(1),
    aanduidingrecordcorrectie character varying(5),
    officieel character varying(1),
    inonderzoek character varying(1),
    begindatumtijdvakgeldigheid character varying(16),
    einddatumtijdvakgeldigheid character varying(16),
    documentnummer character varying(20),
    documentdatum character varying(8),
    huisnummer character varying(5),
    huisletter character varying(5),
    huisnummertoevoeging character varying(4),
    postcode character varying(6),
    nummeraanduidingstatus character varying(80),
    typeadresseerbaarobject character varying(20),
    gerelateerdeopenbareruimte character varying(16),
    gerelateerdewoonplaats character varying(16),
    begindatum date,
    einddatum date
);

CREATE VIEW nummeraanduidingactueel AS
    SELECT nummeraanduiding.identificatie, nummeraanduiding.aanduidingrecordinactief, nummeraanduiding.aanduidingrecordcorrectie, nummeraanduiding.officieel, nummeraanduiding.inonderzoek, nummeraanduiding.begindatumtijdvakgeldigheid, nummeraanduiding.einddatumtijdvakgeldigheid, nummeraanduiding.documentnummer, nummeraanduiding.documentdatum, nummeraanduiding.huisnummer, nummeraanduiding.huisletter, nummeraanduiding.huisnummertoevoeging, nummeraanduiding.postcode, nummeraanduiding.nummeraanduidingstatus, nummeraanduiding.typeadresseerbaarobject, nummeraanduiding.gerelateerdeopenbareruimte, nummeraanduiding.gerelateerdewoonplaats, nummeraanduiding.begindatum, nummeraanduiding.einddatum FROM nummeraanduiding WHERE (((nummeraanduiding.begindatum <= ('now'::text)::date) AND (nummeraanduiding.einddatum >= ('now'::text)::date)) AND ((nummeraanduiding.aanduidingrecordinactief)::text = 'N'::text));

CREATE VIEW nummeraanduidingactueelbestaand AS
    SELECT nummeraanduiding.identificatie, nummeraanduiding.aanduidingrecordinactief, nummeraanduiding.aanduidingrecordcorrectie, nummeraanduiding.officieel, nummeraanduiding.inonderzoek, nummeraanduiding.begindatumtijdvakgeldigheid, nummeraanduiding.einddatumtijdvakgeldigheid, nummeraanduiding.documentnummer, nummeraanduiding.documentdatum, nummeraanduiding.huisnummer, nummeraanduiding.huisletter, nummeraanduiding.huisnummertoevoeging, nummeraanduiding.postcode, nummeraanduiding.nummeraanduidingstatus, nummeraanduiding.typeadresseerbaarobject, nummeraanduiding.gerelateerdeopenbareruimte, nummeraanduiding.gerelateerdewoonplaats, nummeraanduiding.begindatum, nummeraanduiding.einddatum FROM nummeraanduiding WHERE ((((nummeraanduiding.begindatum <= ('now'::text)::date) AND (nummeraanduiding.einddatum >= ('now'::text)::date)) AND ((nummeraanduiding.aanduidingrecordinactief)::text = 'N'::text)) AND ((nummeraanduiding.nummeraanduidingstatus)::text <> 'Naamgeving ingetrokken'::text));

DROP VIEW IF EXISTS openbareruimteactueel;
DROP VIEW IF EXISTS openbareruimteactueelbestaand;

DROP TABLE openbareruimte;
CREATE TABLE openbareruimte (
    identificatie character varying(16),
    aanduidingrecordinactief character varying(1),
    aanduidingrecordcorrectie character varying(5),
    officieel character varying(1),
    inonderzoek character varying(1),
    begindatumtijdvakgeldigheid character varying(16),
    einddatumtijdvakgeldigheid character varying(16),
    documentnummer character varying(20),
    documentdatum character varying(8),
    openbareruimtenaam character varying(80),
    openbareruimtestatus character varying(80),
    openbareruimtetype character varying(40),
    gerelateerdewoonplaats character varying(16),
    verkorteopenbareruimtenaam character varying(80),
    begindatum date,
    einddatum date
);

CREATE VIEW openbareruimteactueel AS
    SELECT openbareruimte.identificatie, openbareruimte.aanduidingrecordinactief, openbareruimte.aanduidingrecordcorrectie, openbareruimte.officieel, openbareruimte.inonderzoek, openbareruimte.begindatumtijdvakgeldigheid, openbareruimte.einddatumtijdvakgeldigheid, openbareruimte.documentnummer, openbareruimte.documentdatum, openbareruimte.openbareruimtenaam, openbareruimte.openbareruimtestatus, openbareruimte.openbareruimtetype, openbareruimte.gerelateerdewoonplaats, openbareruimte.verkorteopenbareruimtenaam, openbareruimte.begindatum, openbareruimte.einddatum FROM openbareruimte WHERE (((openbareruimte.begindatum <= ('now'::text)::date) AND (openbareruimte.einddatum >= ('now'::text)::date)) AND ((openbareruimte.aanduidingrecordinactief)::text = 'N'::text));

CREATE VIEW openbareruimteactueelbestaand AS
    SELECT openbareruimte.identificatie, openbareruimte.aanduidingrecordinactief, openbareruimte.aanduidingrecordcorrectie, openbareruimte.officieel, openbareruimte.inonderzoek, openbareruimte.begindatumtijdvakgeldigheid, openbareruimte.einddatumtijdvakgeldigheid, openbareruimte.documentnummer, openbareruimte.documentdatum, openbareruimte.openbareruimtenaam, openbareruimte.openbareruimtestatus, openbareruimte.openbareruimtetype, openbareruimte.gerelateerdewoonplaats, openbareruimte.verkorteopenbareruimtenaam, openbareruimte.begindatum, openbareruimte.einddatum FROM openbareruimte WHERE ((((openbareruimte.begindatum <= ('now'::text)::date) AND (openbareruimte.einddatum >= ('now'::text)::date)) AND ((openbareruimte.aanduidingrecordinactief)::text = 'N'::text)) AND ((openbareruimte.openbareruimtestatus)::text <> 'Naamgeving ingetrokken'::text));

DROP VIEW IF EXISTS pandactueel;
DROP VIEW IF EXISTS pandactueelbestaand;

DROP TABLE IF EXISTS pand;
CREATE TABLE pand (
    identificatie character varying(16),
    aanduidingrecordinactief character varying(1),
    aanduidingrecordcorrectie character varying(5),
    officieel character varying(1),
    inonderzoek character varying(1),
    begindatumtijdvakgeldigheid character varying(16),
    einddatumtijdvakgeldigheid character varying(16),
    documentnummer character varying(20),
    documentdatum character varying(8),
    pandstatus character varying(80),
    bouwjaar character varying(6),
    pandgeometrie character varying(1000000),
    begindatum date,
    einddatum date,
    geometrie geometry,
    CONSTRAINT enforce_dims_geometrie CHECK ((st_ndims(geometrie) = 3)),
    CONSTRAINT enforce_geotype_geometrie CHECK (((geometrytype(geometrie) = 'POLYGON'::text) OR (geometrie IS NULL))),
    CONSTRAINT enforce_srid_geometrie CHECK ((st_srid(geometrie) = 28992))
) WITH ( OIDS=TRUE );

CREATE VIEW pandactueel AS
    SELECT (pand.oid)::character varying AS oid, pand.identificatie, pand.aanduidingrecordinactief, pand.aanduidingrecordcorrectie, pand.officieel, pand.inonderzoek, pand.begindatumtijdvakgeldigheid, pand.einddatumtijdvakgeldigheid, pand.documentnummer, pand.documentdatum, pand.pandstatus, pand.bouwjaar, pand.pandgeometrie, pand.begindatum, pand.einddatum, pand.geometrie FROM pand WHERE (((pand.begindatum <= ('now'::text)::date) AND (pand.einddatum >= ('now'::text)::date)) AND ((pand.aanduidingrecordinactief)::text = 'N'::text));

CREATE VIEW pandactueelbestaand AS
    SELECT (pand.oid)::character varying AS oid, pand.identificatie, pand.aanduidingrecordinactief, pand.aanduidingrecordcorrectie, pand.officieel, pand.inonderzoek, pand.begindatumtijdvakgeldigheid, pand.einddatumtijdvakgeldigheid, pand.documentnummer, pand.documentdatum, pand.pandstatus, pand.bouwjaar, pand.pandgeometrie, pand.begindatum, pand.einddatum, pand.geometrie FROM pand WHERE (((((pand.begindatum <= ('now'::text)::date) AND (pand.einddatum >= ('now'::text)::date)) AND ((pand.aanduidingrecordinactief)::text = 'N'::text)) AND ((pand.pandstatus)::text <> 'Niet gerealiseerd pand'::text)) AND ((pand.pandstatus)::text <> 'Pand gesloopt'::text));

DROP VIEW IF EXISTS standplaatsactueel;
DROP VIEW IF EXISTS standplaatsactueelbestaand;

DROP TABLE IF EXISTS standplaats;
CREATE TABLE standplaats (
    identificatie character varying(16),
    aanduidingrecordinactief character varying(1),
    aanduidingrecordcorrectie character varying(5),
    officieel character varying(1),
    inonderzoek character varying(1),
    begindatumtijdvakgeldigheid character varying(16),
    einddatumtijdvakgeldigheid character varying(16),
    documentnummer character varying(20),
    documentdatum character varying(8),
    hoofdadres character varying(16),
    standplaatsstatus character varying(80),
    standplaatsgeometrie character varying(1000000),
    begindatum date,
    einddatum date,
    geometrie geometry,
    CONSTRAINT enforce_dims_geometrie CHECK ((st_ndims(geometrie) = 3)),
    CONSTRAINT enforce_geotype_geometrie CHECK (((geometrytype(geometrie) = 'POLYGON'::text) OR (geometrie IS NULL))),
    CONSTRAINT enforce_srid_geometrie CHECK ((st_srid(geometrie) = 28992))
) WITH ( OIDS=TRUE );

CREATE VIEW standplaatsactueel AS
    SELECT (standplaats.oid)::character varying AS oid, standplaats.identificatie, standplaats.aanduidingrecordinactief, standplaats.aanduidingrecordcorrectie, standplaats.officieel, standplaats.inonderzoek, standplaats.begindatumtijdvakgeldigheid, standplaats.einddatumtijdvakgeldigheid, standplaats.documentnummer, standplaats.documentdatum, standplaats.hoofdadres, standplaats.standplaatsstatus, standplaats.standplaatsgeometrie, standplaats.begindatum, standplaats.einddatum, standplaats.geometrie FROM standplaats WHERE (((standplaats.begindatum <= ('now'::text)::date) AND (standplaats.einddatum >= ('now'::text)::date)) AND ((standplaats.aanduidingrecordinactief)::text = 'N'::text));

CREATE VIEW standplaatsactueelbestaand AS
    SELECT (standplaats.oid)::character varying AS oid, standplaats.identificatie, standplaats.aanduidingrecordinactief, standplaats.aanduidingrecordcorrectie, standplaats.officieel, standplaats.inonderzoek, standplaats.begindatumtijdvakgeldigheid, standplaats.einddatumtijdvakgeldigheid, standplaats.documentnummer, standplaats.documentdatum, standplaats.hoofdadres, standplaats.standplaatsstatus, standplaats.standplaatsgeometrie, standplaats.begindatum, standplaats.einddatum, standplaats.geometrie FROM standplaats WHERE ((((standplaats.begindatum <= ('now'::text)::date) AND (standplaats.einddatum >= ('now'::text)::date)) AND ((standplaats.aanduidingrecordinactief)::text = 'N'::text)) AND ((standplaats.standplaatsstatus)::text <> 'Plaats ingetrokken'::text));

DROP VIEW IF EXISTS verblijfsobjectactueel;
DROP VIEW IF EXISTS verblijfsobjectactueelbestaand;

DROP TABLE IF EXISTS verblijfsobject;
CREATE TABLE verblijfsobject (
    identificatie character varying(16),
    aanduidingrecordinactief character varying(1),
    aanduidingrecordcorrectie character varying(5),
    officieel character varying(1),
    inonderzoek character varying(1),
    begindatumtijdvakgeldigheid character varying(16),
    einddatumtijdvakgeldigheid character varying(16),
    documentnummer character varying(20),
    documentdatum character varying(8),
    hoofdadres character varying(16),
    verblijfsobjectstatus character varying(80),
    oppervlakteverblijfsobject character varying(6),
    verblijfsobjectgeometrie character varying(100),
    begindatum date,
    einddatum date,
    geometrie geometry,
    CONSTRAINT enforce_dims_geometrie CHECK ((st_ndims(geometrie) = 3)),
    CONSTRAINT enforce_geotype_geometrie CHECK (((geometrytype(geometrie) = 'POINT'::text) OR (geometrie IS NULL))),
    CONSTRAINT enforce_srid_geometrie CHECK ((st_srid(geometrie) = 28992))
) WITH ( OIDS=TRUE );

CREATE VIEW verblijfsobjectactueel AS
    SELECT (verblijfsobject.oid)::character varying AS oid, verblijfsobject.identificatie, verblijfsobject.aanduidingrecordinactief, verblijfsobject.aanduidingrecordcorrectie, verblijfsobject.officieel, verblijfsobject.inonderzoek, verblijfsobject.begindatumtijdvakgeldigheid, verblijfsobject.einddatumtijdvakgeldigheid, verblijfsobject.documentnummer, verblijfsobject.documentdatum, verblijfsobject.hoofdadres, verblijfsobject.verblijfsobjectstatus, verblijfsobject.oppervlakteverblijfsobject, verblijfsobject.verblijfsobjectgeometrie, verblijfsobject.begindatum, verblijfsobject.einddatum, verblijfsobject.geometrie FROM verblijfsobject WHERE (((verblijfsobject.begindatum <= ('now'::text)::date) AND (verblijfsobject.einddatum >= ('now'::text)::date)) AND ((verblijfsobject.aanduidingrecordinactief)::text = 'N'::text));

CREATE VIEW verblijfsobjectactueelbestaand AS
    SELECT (verblijfsobject.oid)::character varying AS oid, verblijfsobject.identificatie, verblijfsobject.aanduidingrecordinactief, verblijfsobject.aanduidingrecordcorrectie, verblijfsobject.officieel, verblijfsobject.inonderzoek, verblijfsobject.begindatumtijdvakgeldigheid, verblijfsobject.einddatumtijdvakgeldigheid, verblijfsobject.documentnummer, verblijfsobject.documentdatum, verblijfsobject.hoofdadres, verblijfsobject.verblijfsobjectstatus, verblijfsobject.oppervlakteverblijfsobject, verblijfsobject.verblijfsobjectgeometrie, verblijfsobject.begindatum, verblijfsobject.einddatum, verblijfsobject.geometrie FROM verblijfsobject WHERE (((((verblijfsobject.begindatum <= ('now'::text)::date) AND (verblijfsobject.einddatum >= ('now'::text)::date)) AND ((verblijfsobject.aanduidingrecordinactief)::text = 'N'::text)) AND ((verblijfsobject.verblijfsobjectstatus)::text <> 'Niet gerealiseerd verblijfsobject'::text)) AND ((verblijfsobject.verblijfsobjectstatus)::text <> 'Verblijfsobject ingetrokken'::text));

DROP TABLE IF EXISTS verblijfsobjectgebruiksdoel;
CREATE TABLE verblijfsobjectgebruiksdoel (
    identificatie character varying(16),
    aanduidingrecordinactief character varying(1),
    aanduidingrecordcorrectie character varying(5),
    begindatumtijdvakgeldigheid character varying(16),
    gebruiksdoelverblijfsobject character varying(50)
);

DROP TABLE IF EXISTS verblijfsobjectpand;
CREATE TABLE verblijfsobjectpand (
    identificatie character varying(16),
    aanduidingrecordinactief character varying(1),
    aanduidingrecordcorrectie character varying(5),
    begindatumtijdvakgeldigheid character varying(16),
    gerelateerdpand character varying(16)
);

DROP TABLE IF EXISTS woonplaats;
CREATE TABLE woonplaats (
    identificatie character varying(16),
    aanduidingrecordinactief character varying(1),
    aanduidingrecordcorrectie character varying(5),
    officieel character varying(1),
    inonderzoek character varying(1),
    begindatumtijdvakgeldigheid character varying(16),
    einddatumtijdvakgeldigheid character varying(16),
    documentnummer character varying(20),
    documentdatum character varying(8),
    woonplaatsnaam character varying(80),
    woonplaatsstatus character varying(80),
    woonplaatsgeometrie character varying(1000000),
    begindatum date,
    einddatum date,
    geometrie geometry,
    CONSTRAINT enforce_dims_geometrie CHECK ((st_ndims(geometrie) = 2)),
    CONSTRAINT enforce_geotype_geometrie CHECK (((geometrytype(geometrie) = 'MULTIPOLYGON'::text) OR (geometrie IS NULL))),
    CONSTRAINT enforce_srid_geometrie CHECK ((st_srid(geometrie) = 28992))
);

CREATE INDEX adresseerbaarobjectnevenadreskey ON adresseerbaarobjectnevenadres USING btree (identificatie, aanduidingrecordinactief, aanduidingrecordcorrectie, begindatumtijdvakgeldigheid, nevenadres);
CREATE INDEX ligplaatsgist ON ligplaats USING gist (geometrie);
CREATE UNIQUE INDEX ligplaatskey ON ligplaats USING btree (identificatie, aanduidingrecordinactief, aanduidingrecordcorrectie, begindatumtijdvakgeldigheid);
CREATE UNIQUE INDEX ligplaatsoid ON ligplaats USING btree (oid);
CREATE UNIQUE INDEX nummeraanduidingkey ON nummeraanduiding USING btree (identificatie, aanduidingrecordinactief, aanduidingrecordcorrectie, begindatumtijdvakgeldigheid);
CREATE INDEX nummeraanduidingpostcode ON nummeraanduiding USING btree (postcode);
CREATE UNIQUE INDEX openbareruimtekey ON openbareruimte USING btree (identificatie, aanduidingrecordinactief, aanduidingrecordcorrectie, begindatumtijdvakgeldigheid);
CREATE INDEX openbareruimtenaam ON openbareruimte USING btree (openbareruimtenaam);
CREATE INDEX pandgist ON pand USING gist (geometrie);
CREATE UNIQUE INDEX pandkey ON pand USING btree (identificatie, aanduidingrecordinactief, aanduidingrecordcorrectie, begindatumtijdvakgeldigheid);
CREATE UNIQUE INDEX pandoid ON pand USING btree (oid);
CREATE INDEX standplaatsgist ON standplaats USING gist (geometrie);
CREATE UNIQUE INDEX standplaatskey ON standplaats USING btree (identificatie, aanduidingrecordinactief, aanduidingrecordcorrectie, begindatumtijdvakgeldigheid);
CREATE UNIQUE INDEX standplaatsoid ON standplaats USING btree (oid);
CREATE INDEX verblijfsobjectgebruiksdoelkey ON verblijfsobjectgebruiksdoel USING btree (identificatie, aanduidingrecordinactief, aanduidingrecordcorrectie, begindatumtijdvakgeldigheid, gebruiksdoelverblijfsobject);
CREATE INDEX verblijfsobjectgist ON verblijfsobject USING gist (geometrie);
CREATE UNIQUE INDEX verblijfsobjectkey ON verblijfsobject USING btree (identificatie, aanduidingrecordinactief, aanduidingrecordcorrectie, begindatumtijdvakgeldigheid);
CREATE UNIQUE INDEX verblijfsobjectoid ON verblijfsobject USING btree (oid);
CREATE INDEX verblijfsobjectpandkey ON verblijfsobjectpand USING btree (identificatie, aanduidingrecordinactief, aanduidingrecordcorrectie, begindatumtijdvakgeldigheid, gerelateerdpand);

