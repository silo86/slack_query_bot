SELECT 
current_database() as base,
unidad,
count(*) as total
FROM(
		SELECT 
		distinct on (juzgid,procid) histid,
		h.procid,fn_devuelvenumexptecompleto(h.procid) as expte,
		h.codb, estaid,
		tiesid, h.dscr,
		foja, fech,
		febo, fepf,
		fefi, hora,
		copa, firm,
		certid, h.juzgid,
		j.dscr as unidad, usua,
		usfi, usfd,
		h.rese, adju,
		agre, feag,
		esinid, cafi,
		hode, eiweid
		FROM public."HIST" as h
		left join public."JUZG" as j on h.juzgid = j.juzgid
		left join public."PROC" as p on h.procid = p.procid
		where febo >= '{0}'
        and febo <= '{1}'
		and p.acum = false
		order by juzgid,procid,histid desc)a 
		group by unidad