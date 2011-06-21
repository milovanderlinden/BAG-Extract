drop table gemeente;
create table gemeente as select gemeentecode,gemeentenaam,ST_Multi(ST_Union(woonplaats.geometrie)) as geometrie
from gemeente_woonplaats, woonplaats where woonplaatscode = woonplaats.identificatie group by gemeentecode,gemeentenaam;
alter table gemeente add column id bigserial;
select probe_geometry_columns();