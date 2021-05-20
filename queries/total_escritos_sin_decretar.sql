select 
current_database() as base,
dscr as unidad,
count(*) as total 
from (
SELECT histid, fn_devuelvenumexptecompleto(procid) as expte, procid, h.tiesid, t.dscr as hijo, h.dscr as observacion, j.dscr, 
fech, febo, fepf, fefi, hora,
diashabiles(h.fech, to_char(current_date-1,'YYYYMMDD'),h.juzgid) as "dias habiles", 
current_date-1 - to_date(h.fech,'YYYYMMDD') as "dias corridos"
FROM public."HIST" as h
left join public."JUZG" AS j
on h.juzgid = j.juzgid
left join public."TIES" as t
on h.tiesid = t.tiesid
where t.dscr ilike '%escritos%ingre%ados%' 
and estaid <> 3
) as detalle group by dscr  