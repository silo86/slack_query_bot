SELECT current_database() as base, 
j.dscr as unidad,
case when t.tcuaid = 1 then 'PRINCIPAL' else 'OTROS'end as cuaderno,
fn_devuelvenumexptecompleto(procid) as expte,
replace(fn_tproc(procid),'.','') as proceso 
FROM public."PROC" as p 
left join public."JUZG" as j on p.juzgid = j.juzgid
left join public."TCUA" as t on p.tcuaid = t.tcuaid
where --p.tcuaid = 1 and
--j.dscr ilike '%juzg%'and 
acum = false
and p.eproid = 1