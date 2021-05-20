SELECT  
current_database() as base,
j.dscr as unidad,
t.dscr as tramite,
 count(*) as total
FROM public."SALI" as s left join public."TSAL" as t on s.tsalid = t.tsalid
LEFT JOIN PUBLIC."JUZG" AS j ON j.juzgid = s.juzgid
WHERE (t.dscr ILIKE'PARA%HACER%CEDULA%' OR t.dscr ILIKE'PARA%HACER%MANDAMIENTO%' OR t.dscr ILIKE'PARA%HACER%OFICIO%')
AND freg IS null
group by j.dscr,t.dscr