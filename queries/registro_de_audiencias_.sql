
/*Registro de Audiencias Capital y Monteros*/
SELECT
current_database() as base,
j.juzgid as id,
j.dscr as unidad,
fn_devuelvenumexptecompleto(procid) as expediente,
fn_tproc(procid) as proceso,
t.dscr as tipo_registro,
CASE WHEN TRIM(UPPER(r.txt1)) = 'R' then 'REMOTA' WHEN TRIM(UPPER(r.txt1)) = 'P' THEN 'PRESENCIAL' ELSE 'S/C' END AS MODALIDAD,
CASE 
WHEN TRIM(UPPER(r.num1)) = 'SI' or TRIM(UPPER(r.num1)) in ('1','01') then 'CONCILIACION'
WHEN TRIM(UPPER(r.num1)) in ('2','02') then 'TESTIMONIAL'
WHEN TRIM(UPPER(r.num1)) in ('3','03') then 'ABSOLUCION DE POSICIONES'
WHEN TRIM(UPPER(r.num1)) in ('4','04') then 'RECONOCIMIENTO'
WHEN TRIM(UPPER(r.num1)) in ('5','05') then 'CUERPO DE ESCRITURA'
WHEN TRIM(UPPER(r.num1)) in ('6','06') then 'JUICIO SUMARISIMO'
WHEN TRIM(UPPER(r.num1)) in ('7','07') then 'CONCILIACION-TRANSACCION ART 41'
WHEN TRIM(UPPER(r.num1)) in ('8','08') then 'CONCILIACION-TRANSACCION ART 42'
WHEN TRIM(UPPER(r.num1)) in ('9','09') then 'DESISTIMIENTO DE DERECHO'
WHEN TRIM(UPPER(r.num1)) in ('10') then 'OTRAS AUDIENCIAS' else 'S/C' END AS TIPO,
CASE
WHEN TRIM(UPPER(r.num1)) = 'SI' or TRIM(UPPER(r.num1)) in ('1','01') AND (TRIM(UPPER(r.num2)) = 'SI' or TRIM(UPPER(r.num2)) in ('1','01')) THEN 'CONCILIADA'
WHEN TRIM(UPPER(r.num1)) = 'SI' or TRIM(UPPER(r.num1)) in ('1','01') AND (TRIM(UPPER(r.num2)) = 'NO' or TRIM(UPPER(r.num2)) in ('0','00')) THEN 'NO CONCILIADA' ELSE 'S/C' END AS CONCILIADA,
r.fec1,
r.fec2,
r.feen,
r.fesa,
r.txt1,
r.txt2,
r.num1,
r.num2
from public."REGI" as r
left join public."JUZG" as j on j.juzgid = r.juzgid
left join public."TIRE" as t on r.tireid = t.tireid 
where  t.dscr ilike '%audiencia%'
order by procid,r.fec1