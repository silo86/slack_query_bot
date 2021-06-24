/* Ingreso a corte */
select * from (
	select distinct on (procid) * from(
		select 
		current_database() as base,
		r.procid,
		p.tcuaid,
		CASE 
			WHEN p.tcuaid = 1
			THEN 'PRINCIPAL'
			ELSE 'OTRO'
		END AS tipo_de_cuaderno,
		t.dscr as descripcion_cuaderno,
		fn_devuelvenumexptecompleto(r.procid) as expediente,
		fn_tproc(r.procid) as proceso,
		feca as fecha_de_cargo,
		i.dscr as juzgado_de_origen,
		j.dscr as juzgado_de_destino,
		k.dscr as juzgado_actual
		from public."RADI" as r
		left join public."PROC" as p on p.procid = r.procid
		left join public."TCUA" as t on t.tcuaid = p.tcuaid
		left join public."JUZG" as j on j.juzgid = r.juzgid
		left join public."JUZG" as i on i.juzgid = r.juorid
		left join public."JUZG" as k on k.juzgid = p.juzgid
		where /*r.juorid in (/* id de unidad mesa de entrada */select juzgid from public."JUZG" where dscr ilike '%mesa%entra%' and acti = true and csae = true)
		and*/ feca >= '{0}'
		and feca <= '{1}'
		and acum = false
		and anul = false
		and j.dscr ilike '%corte%'
		and feca is not null
		order by r.procid,r.feca) as expedientes_por_primera_radicacion
			) as ingreso_a_corte  order by juzgado_de_destino