select 
base,
sala,
tipo,
count(*)
from(
select
distinct on (sala,expte) *
from(
select
current_database() as base,
 j.dscr as sala,
case when p.tcuaid = 1 then 'PRINCIPAL' else 'OTROS' end as tipo,
fn_devuelvenumexptecompleto(s.procid) as expte,
t.dscr,
* 
from public."SALI" as s
left join public."TSAL" as t on t.tsalid = s.tsalid
left join public."JUZG" as j on s.juzgid = j.juzgid
left join public."PROC" as p on s.procid = p.procid
where  t.dscr ilike 'ingreso%sal%'
and j.dscr not ilike '%juzg%'
and fsal >= '{0}'
and fsal <= '{1}'
order by s.procid, s.saliid) as q
) as subquery group by 1,2,3