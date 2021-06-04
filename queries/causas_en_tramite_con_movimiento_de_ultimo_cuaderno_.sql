/* Causas en tramite con movimiento de ultimo cuaderno --firmado */	
SELECT 	
* 	
FROM	
	(SELECT 	
	 current_database() as base, 	
	 j.dscr as unidad,	
	 case when t.tcuaid = 1 then 'PRINCIPAL' else 'OTROS'end as cuaderno,	
	 procid,	
	 fn_devuelvenumexptecompleto(procid) as expte,	
	 split_part(fn_devuelvenumexptecompleto(procid),'-', 1) as raiz,	
	 replace(fn_tproc(procid),'.','') as proceso,	
	 fini as fecha_de_inicio	
	 FROM public."PROC" as p 	
	 left join public."JUZG" as j on p.juzgid = j.juzgid	
	 left join public."TCUA" as t on p.tcuaid = t.tcuaid	
	 where	
	 acum = false	
	 and p.eproid = 1)ingresadas	
	 	
LEFT JOIN	
(	
/*ultimo mov por exp*/	
 select distinct on (procid) 	
 procid,	
 fech as ultimo_movimiento	
 from (	
 select * from public."HIST" 	
    order by procid,histid desc	
	 )a 	
 /* END ultimo mov por exp */	
)ultimo_movimiento on ultimo_movimiento.procid = ingresadas.procid	
LEFT JOIN	
(	
/* cuaderno con movimiento mas reciente */	
select 	
distinct on (raiz)	
* 	
from(	
	/* ultimo movimiento por expte*/	
	SELECT DISTINCT ON (procid)	
	procid as procid_con_movimiento_mas_reciente,	
	fn_devuelvenumexptecompleto(procid) as cuaderno_con_movimiento_mas_reciente,	
	split_part(fn_devuelvenumexptecompleto(procid),'-', 1) as raiz,	
	fech as fecha_de_movimiento_mas_reciente,		
	febo,	
	fefi	
	from public."HIST"	
	where 	
	split_part(fn_devuelvenumexptecompleto(procid),'-', 1)	
	in	
		(		
			/* expte raiz*/	
			select  	
			distinct on (procid)	
			split_part(fn_devuelvenumexptecompleto(procid),'-', 1) as raiz	
			from public."HIST" 	
			/*END expte raiz*/	
		)	
		and fefi is not null --quitar esto para tomar ultimo mov por fech	
			order by procid,histid desc	
		/* END ultimo movimiento por expte*/		
)ultimo_movimiento_por_expte	
ORDER BY  raiz,fecha_de_movimiento_mas_reciente	DESC	
/* END cuaderno con movimiento mas reciente */	
)cuaderno_con_movimiento_mas_reciente on cuaderno_con_movimiento_mas_reciente.raiz = ingresadas.raiz	
/* END causas en tramite con movimiento de ultimo cuaderno*/