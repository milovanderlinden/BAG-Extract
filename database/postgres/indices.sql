-- Maak geometrie indexen
CREATE INDEX ligplaats_geom_idx ON ligplaats USING gist (geovlak);
CREATE INDEX pand_geom_idx ON pand USING gist (geovlak);
CREATE INDEX standplaats_geom_idx ON standplaats USING gist (geovlak);
CREATE INDEX verblijfsobject_punt_idx ON verblijfsobject USING gist (geopunt);
CREATE INDEX verblijfsobject_vlak_idx ON verblijfsobject USING gist (geovlak);
CREATE INDEX woonplaats_vlak_idx ON woonplaats USING gist (geovlak);

-- Unieke key indexen
CREATE INDEX ligplaats_key ON ligplaats USING btree (identificatie,aanduidingrecordinactief,aanduidingrecordcorrectie,begindatumtijdvakgeldigheid);
CREATE INDEX standplaats_key ON standplaats USING btree (identificatie,aanduidingrecordinactief,aanduidingrecordcorrectie,begindatumtijdvakgeldigheid);
CREATE INDEX verblijfsobject_key ON verblijfsobject USING btree (identificatie,aanduidingrecordinactief,aanduidingrecordcorrectie,begindatumtijdvakgeldigheid);
CREATE INDEX pand_key ON pand USING btree (identificatie,aanduidingrecordinactief,aanduidingrecordcorrectie,begindatumtijdvakgeldigheid);
-- met nummeraanduiding lijkt een probleem als unieke index  (in de gaten houden)
CREATE INDEX nummeraanduiding_key ON nummeraanduiding USING btree (identificatie,aanduidingrecordinactief,aanduidingrecordcorrectie,begindatumtijdvakgeldigheid);
CREATE INDEX openbareruimte_key ON openbareruimte USING btree (identificatie,aanduidingrecordinactief,aanduidingrecordcorrectie,begindatumtijdvakgeldigheid);
CREATE INDEX woonplaats_key ON woonplaats USING btree (identificatie,aanduidingrecordinactief,aanduidingrecordcorrectie,begindatumtijdvakgeldigheid);

-- Overige indexen
CREATE INDEX nummeraanduiding_postcode ON nummeraanduiding USING btree (postcode);
CREATE INDEX openbareruimte_naam ON openbareruimte USING btree (openbareruimtenaam);
CREATE INDEX woonplaats_naam ON woonplaats USING btree (woonplaatsnaam);

-- Indexen relatie tabellen
CREATE INDEX verblijfsobjectpandkey ON verblijfsobjectpand USING btree (identificatie, aanduidingrecordinactief, aanduidingrecordcorrectie, begindatumtijdvakgeldigheid, gerelateerdpand);
CREATE INDEX verblijfsobjectgebruiksdoelkey ON verblijfsobjectgebruiksdoel USING btree (identificatie, aanduidingrecordinactief, aanduidingrecordcorrectie, begindatumtijdvakgeldigheid, gebruiksdoelverblijfsobject);
CREATE INDEX
        adresseerbaarobjectnevenadreskey ON adresseerbaarobjectnevenadres USING btree (identificatie, aanduidingrecordinactief, aanduidingrecordcorrectie, begindatumtijdvakgeldigheid, nevenadres);

