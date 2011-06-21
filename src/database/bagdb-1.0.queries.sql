drop table if exists gemeente;
create table gemeente as select gemeentecode,gemeentenaam,ST_Multi(ST_Union(woonplaats.geometrie)) as geometrie
from gemeente_woonplaats, woonplaats where woonplaatscode = woonplaats.identificatie group by gemeentecode,gemeentenaam;
alter table gemeente add column id bigserial;
select probe_geometry_columns();

drop table if exists adres;
create table adres as
select
v.identificatie as verblijfsobject,
v.punt,
n.identificatie as nummeraanduiding,
n.huisnummer,
n.huisletter,
n.huisnummertoevoeging,
o.openbareruimtenaam,
w.woonplaatsnaam,
g.gemeentenaam
from
(select identificatie, punt, hoofdadres from verblijfsobject where einddatum is null) v,
(select identificatie, huisnummer, huisletter, huisnummertoevoeging, gerelateerdeopenbareruimte from nummeraanduiding where einddatum is null) n,
(select identificatie, openbareruimtenaam, gerelateerdewoonplaats from openbareruimte where einddatum is null) o,
(select identificatie, woonplaatsnaam from woonplaats where einddatum is null) w,
(select woonplaatscode,gemeentenaam from gemeente_woonplaats where einddatum_gemeente is null) g
where
v.hoofdadres = n.identificatie
and n.gerelateerdeopenbareruimte = o.identificatie
and o.gerelateerdewoonplaats = w.identificatie
and w.identificatie = g.woonplaatscode