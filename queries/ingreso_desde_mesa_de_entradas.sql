select * from (
	select distinct on (procid) * from(
		select 
		current_database() as base,
		r.procid,
		fn_devuelvenumexptecompleto(r.procid) as expediente,
		fn_tproc(r.procid) as proceso,
		feca as "fecha de cargo",
		i.dscr as "juzgado de origen",
		j.dscr as "juzgado de destino",
		k.dscr as "juzgado actual"
		from public."RADI" as r
		left join public."PROC" as p on p.procid = r.procid
		left join public."JUZG" as j on j.juzgid = r.juzgid
		left join public."JUZG" as i on i.juzgid = r.juorid
		left join public."JUZG" as k on k.juzgid = p.juzgid
		where r.juorid in (/* id de unidad mesa de entrada */select juzgid from public."JUZG" where dscr ilike '%mesa%entra%' and acti = true and csae = true)
		and feca >= '{0}'
		and feca <= '{1}'
		and acum = false
		and anul = false
		and feca is not null
		order by r.procid,r.radiid) as expedientes_radicados_desde_ME
			) as nested_query  order by "juzgado de destino"
