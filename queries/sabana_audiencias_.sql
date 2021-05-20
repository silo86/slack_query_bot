select current_database() as db,
       a.id AS audienciaid,
	   CASE
           WHEN k.juezid IS NOT NULL THEN concat(a.id, '-', k.juezid)
       END AS juezaudienciaid,
	   CASE
           WHEN m.resultadoid IS NOT NULL THEN concat(m.audienciaid, '-', m.resultadoid)
       END AS resultadoaudienciaid,
	   CASE
           WHEN s.audiencia_tipoid IS NOT NULL THEN concat(s.audienciaid, '-', s.audiencia_tipoid)
       END AS tipoaudienciaid,
	   s.audiencia_tipoid,
       a.estadoid,
       a.orden,
       CASE
           WHEN a.estadoid IN (1,
                               2,
                               10) THEN 10
           WHEN a.estadoid IN (3) THEN 21
           WHEN a.estadoid IN (4,
                               5,
                               6,
							   7,
                               8) THEN 22
           WHEN a.estadoid IN (9) THEN 23
       END AS orden_grupo,
       CASE
           WHEN a.estadoid IN (1,
                               2,
                               10) THEN 'Preagendamiento'
           WHEN a.estadoid IN (3) THEN 'Agendadas'
           WHEN a.estadoid IN (4,
                               5,
                               6,
							   7,
                               8) THEN 'Realizadas'
           WHEN a.estadoid IN (9) THEN 'Canceladas'
       END AS descripcion_grupo,
	   CASE
           WHEN a.estadoid IN (1,
                               2,
                               10) THEN 'Preagendamiento'
           WHEN a.estadoid IN (3) THEN 'Agendadas'
           WHEN a.estadoid IN (4,
                               5,
                               6,
							   7,
                               8) THEN 'Realizadas'
           WHEN a.estadoid IN (9) THEN 'Canceladas'
       END AS descripcion_ultimo_grupo,
       a.salaid,
       a.motivoid,
       a.usuarioid,
       a.requirenteid,
       a.expedienteid,
       a.unidadid,
       a.prioridadid,
       a.operadorid,
	   UPPER(concat(w.apellido, ', ', w.nombre)) AS nombre_operador,
       a.invenietid,
       a.fiscaliaid,
       a.fecha_inicio,
	   t.descripcion AS tipo_audiencia,
       ult_estado,
	   ue.descripcion AS descripcion_ult_estado,
       e.descripcion AS descripcion_estado,
       fecha_mov,
       to_char(a.fecha_mov, 'YYYYMM') AS aniomes_mov,
       date(a.fecha_mov) - date(a.fecha_inicio) AS dias_inicio,
       inicio_planificado,
       fin_planificado,
       extract(EPOCH
               FROM fin_planificado - inicio_planificado)/60 AS tiempo_audiencia_planificado,
	   case when inicio_real::date = '0001-01-01' then null
	   else inicio_real end as inicio_real,
	   case when fin_real::date = '0001-01-01' then null
	   else fin_real end as fin_real,
       extract(EPOCH
               FROM fin_real - inicio_real)/60 AS tiempo_audiencia_real,
       UPPER(concat(u.apellido, ', ', u.nombre)) AS nombre_usuario,
       p.descripcion AS perfil_usuario,
       UPPER(v.descripcion) AS nombre_req,
       UPPER(v.descripcion) AS perfil_req,
	   k.tipo_jurado,
	   CASE
                    WHEN v.descripcion ilike '%defen%' THEN 'MPD'
                    WHEN v.descripcion ilike '%fisc%' THEN 'MPF'
                    WHEN v.descripcion LIKE '%OGA%' THEN 'OGA'
                    ELSE 'Otros'
          END AS requirente,
	   CASE
           WHEN k IS NOT NULL THEN UPPER(concat(k.apellido, ', ', k.nombre))
       END AS nombre_juez,
	   r.descripcion AS descripcion_resultado,
       a.menor,
       a.confirmada,
       a.cuenta,
	   case when k.juezid in (15,23,10,9,32,17,13,24,12,6,2,14,8,28) then 'Colegio de Jueces'
	   		when k.juezid in (4) then 'Ejecución'
			when k.juezid in (30,25,5,31) then 'Impugnación' end as grupo_juez,
	   ex.numero as expediente,
	   ex.caratula,
	   ex.created_at as fecha_inicio_expediente,
	   trim(REGEXP_REPLACE(REGEXP_REPLACE(split_part(split_part(upper(caratula),'S/',2),'VICT',1),'[^a-zA-Z0-9ÁÉÍÓÚ ]+','','g'),' {2,}', ' ')) AS delito,
	   case when a.estadoid in (1,2,10,11) then a.fecha_inicio
	   		else a.inicio_planificado
	   end as fecha_filtro,
	   mo.descripcion as descripcion_motivo
	   from
(
        (SELECT DISTINCT on(id, excl_1) h.audienciaid AS id,
                         h.estadoid_new AS estadoid,
                         a.salaid,
                         h.motivoid,
                         h.usuarioid,
                         a.unidadid AS requirenteid,
                         coalesce(h.created_at, h.updated_at) AS fecha_mov,
                         a.created_at AS fecha_inicio,
                         a.inicio AS inicio_planificado,
                         a.fin AS fin_planificado,
                         a.inicio_real,
                         a.fin_real,
                         a.expedienteid,
                         a.unidadid,
                         a.menor,
                         a.prioridadid,
                         a.confirmada,
                         a.operadorid,
                         a.invenietid,
                         a.fiscaliaid,
                         a.estadoid AS ult_estado,
                         CASE
                             WHEN h.estadoid_new IN (1,
                                                     11) THEN '1'
                             WHEN h.estadoid_new IN (2,
                                                     10) THEN '2'
                             WHEN h.estadoid_new IN (3) THEN '3'
                             WHEN h.estadoid_new IN (7) THEN '4'
                             WHEN h.estadoid_new IN (8,
                                                     9) THEN '5'
                             WHEN h.estadoid_new IN (6) THEN '6'
                             WHEN h.estadoid_new IN (4,
                                                     5) THEN '7'
                         END AS orden,
                         CASE
                             WHEN h.estadoid_new IN (4,
                                                     5,
                                                     8,
                                                     9) THEN 'A'
                             WHEN h.estadoid_new IN (2,
                                                     10) THEN 'B'
                             ELSE h.estadoid_new::text
                         END AS excl_1,
                         1 AS cuenta
      	 FROM public.audiencia_historias AS h
         LEFT JOIN audiencias AS a ON h.audienciaid = a.id
		 WHERE a.estadoid <> '11'
         AND h.estadoid_new IS NOT NULL
	and h.estadoid_new not in (1) -- para que no traiga estados 1
         ORDER BY id,
                  excl_1,
                  fecha_mov DESC)
      UNION ALL
        (SELECT DISTINCT on(id, excl_1) id,
                         '1' AS estadoid,
                         salaid,
                         motivoid,
                         usuarioid,
                         unidadid AS requirenteid,
                         created_at AS fecha_mov,
                         created_at AS fecha_inicio,
                         inicio AS inicio_planificado,
                         fin AS fin_planificado,
                         inicio_real,
                         fin_real,
                         expedienteid,
                         unidadid,
                         menor,
                         prioridadid,
                         confirmada,
                         operadorid,
                         invenietid,
                         fiscaliaid,
                         estadoid AS ult_estado,
                         '1' AS orden,
                         'C' AS excl_1,
                         1 AS cuenta
         FROM public.audiencias
         ORDER BY id,
                  excl_1,
                  fecha_mov DESC)
      UNION ALL
        (SELECT DISTINCT on(id, excl_1) id,
                         estadoid,
                         salaid,
                         motivoid,
                         usuarioid,
                         unidadid AS requirenteid,
                         created_at AS fecha_mov,
                         created_at AS fecha_inicio,
                         inicio AS inicio_planificado,
                         fin AS fin_planificado,
                         inicio_real,
                         fin_real,
                         expedienteid,
                         unidadid,
                         menor,
                         prioridadid,
                         confirmada,
                         operadorid,
                         invenietid,
                         fiscaliaid,
                         estadoid AS ult_estado,
                         CASE
                             WHEN estadoid IN (1,
                                                     11) THEN '1'
                             WHEN estadoid IN (2,
                                                     10) THEN '2'
                             WHEN estadoid IN (3) THEN '3'
                             WHEN estadoid IN (7) THEN '4'
                             WHEN estadoid IN (8,
                                                     9) THEN '5'
                             WHEN estadoid IN (6) THEN '6'
                             WHEN estadoid IN (4,
                                                     5) THEN '7'
                         END AS orden,
                         CASE
                             WHEN estadoid IN (4,
                                                     5,
                                                     8,
                                                     9) THEN 'A'
                             WHEN estadoid IN (2,
                                                     10) THEN 'B'
                             ELSE estadoid::text
                         END AS excl_1,
                         1 AS cuenta
         FROM public.audiencias
         WHERE id IN
             (SELECT id
              FROM public.audiencias
              EXCEPT SELECT audienciaid
              FROM public.audiencia_historias
              WHERE estadoid_new IS NOT NULL)
		 	  or estadoid = 11
         	  ORDER BY id,
              excl_1,
              fecha_mov DESC)) as a
              LEFT JOIN public.estados AS e ON a.estadoid = e.id
              LEFT JOIN public.usuarios AS u ON a.usuarioid = u.id
              LEFT JOIN public.perfiles AS p ON u.perfilid = p.id
              LEFT JOIN public.unidades AS v ON a.unidadid = v.id
			  LEFT JOIN
			  (SELECT audienciaid,
					  k.id,
					  k.nombre,
					  k.apellido,
					  juezid,
					  CASE
						  WHEN count(*) OVER (PARTITION BY audienciaid) = 1 THEN 'Unipersonal'
						  ELSE 'Colegiado'
					  END AS tipo_jurado
			   FROM public.audiencia_jueces AS j
			   LEFT JOIN public.jueces AS k ON j.juezid = k.id
			   WHERE j.anulado = 0) AS k ON a.id = k.audienciaid
			  LEFT JOIN public.estados AS ue ON a.ult_estado = ue.id
			  LEFT JOIN public.audiencia_resultados AS m ON a.id = m.audienciaid
			  LEFT JOIN public.resultados AS r ON m.resultadoid = r.id
			  LEFT JOIN public.audiencia_tipo_audiencias AS s ON a.id = s.audienciaid
			  LEFT JOIN public.audiencia_tipos AS t ON s.audiencia_tipoid = t.id
			  LEFT JOIN public.usuarios AS w ON a.operadorid = w.id
			  LEFT JOIN public.expedientes as ex on a.expedienteid = ex.id
			  LEFT JOIN public.motivos as mo on a.motivoid = mo.id
			  where fecha_inicio::date >= '20200901'