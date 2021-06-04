/*Causas ingresadas ME listado*/
SELECT 
current_database() AS db,
j.juzgid,
procid,
fn_devuelvenumexptecompleto(procid) as expte,
fn_tproc(procid) proceso,
fini as fecha_de_inicio,
p.tcuaid,
t.dscr as tipo_de_cuaderno,
j.dscr as juzgado_actual,
j.coju as juzgado_actual_corto
FROM public."PROC" as p
left join public."JUZG" as j on j.juzgid = p.juzgid
left join public."TCUA" as t on t.tcuaid = p.tcuaid
where acum is false
and fini >= '{0}'
and fini <= '{1}'