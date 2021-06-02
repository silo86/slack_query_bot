SELECT
To_char(CURRENT_DATE, 'YYYYMMDD') as fecha_de_extraccion,
current_database() as base,
j.juzgid,
Initcap(J.dscr)  AS unidad,
j.coju as unidad_corto,
p.procid,
Fn_devuelvenumexptecompleto(p.procid) AS expte,
--p.eproid,
--p.suep,
coalesce(a.eproid,p.eproid) as eproid,
s.dscr as estado,
case
   when a.procid is not null
      then a.suep
   else p.suep
   end as
suep,
e.dscr as subestado,
replace(fn_tproc(p.procid),'.','') as proceso,
case
   when t.tcuaid = 1
      then 'PRINCIPAL'
   else 'OTROS'end as
cuaderno,
acto,
dema,
p.obse,
fini
FROM public."PROC" as p
left join public."JUZG" as j on p.juzgid = j.juzgid
left join public."TCUA" as t on p.tcuaid = t.tcuaid
left join (
select distinct on (procid) procid,
   eproid,suep,hast
   from public."PREP"
   where hast >= '{1}'
   order by procid, prepid
)a on p.procid = a.procid
left join public."EPRO" as e
on case when p.suep is null or p.suep = 0 then p.eproid = e.eproid  else p.suep = e.eproid end
left join public."EPRO" as s on case when a.eproid is null then p.eproid = s.eproid else a.eproid = s.eproid end
where
acum = false
and fini <= '{1}'
and s.dscr = 'TRAMITE'