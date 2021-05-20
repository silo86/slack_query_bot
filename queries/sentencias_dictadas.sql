SELECT current_database() AS base,j.dscr as "unidad",fn_devuelvenumexptecompleto(i.procid) as "expediente",fn_tproc(i.procid)as proceso
--, h.tiesid as "id de hijo"
, h.dscr as hijo_escrito,
--h.tiesidp as "id de padre", 
h.padre as padre_escrito,p.fini as fecha_inicio, i.fefi as "fecha_firma", e.dscr as "estado",
p.aux1,p.aux2,p.aux3,p.aux4,p.aux5
from (select x.tiesid, x.dscr, x.padr, x.tgesid, x.tireid, x.fidi, x.casi, x.padre_2, case when padre_2 is null then dscr else padre_2 end as padre, case when tiesidp is null then tiesid else tiesidp end as tiesidp from (SELECT h.tiesid, h.dscr, h.padr, h.tgesid, h.tireid, h.fidi, h.casi, p.dscr as padre_2, p.tiesid as tiesidp FROM public."TIES" as h left join public."TIES" as p on h.padr = p.tiesid) as x) as h 
left join public."HIST" as i on i.tiesid = h.tiesid left join public."JUZG" as j on j.juzgid = i.juzgid left join public."ESTA" as e on e.estaid = i.estaid left join public."PROC" as p on p.procid = i.procid 
where (h.padre ilike '%sentenc%' or h.padre ilike 'autos%') 
and i.fefi >= '{0}'and i.fefi <= '{1}'  order by i.fefi