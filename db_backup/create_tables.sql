-- Table: sa.trail

-- DROP TABLE IF EXISTS sa.trail;

CREATE TABLE IF NOT EXISTS sa.trail
(
    id_0 integer NOT NULL DEFAULT nextval('sa.trail_id_0_seq'::regclass),
    geom geometry(MultiLineString,3763),
    id bigint,
    name character varying(20) COLLATE pg_catalog."default",
    descript character varying(50) COLLATE pg_catalog."default",
    location character varying(25) COLLATE pg_catalog."default",
    pt_start_x double precision,
    pt_start_y double precision,
    pt_end_x double precision,
    pt_end_y double precision,
    type_terra character varying(15) COLLATE pg_catalog."default",
    slope_mean bigint,
    slope_max bigint,
    distance_m double precision,
    CONSTRAINT trail_pkey PRIMARY KEY (id_0)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS sa.trail
    OWNER to postgres;
-- Index: sidx_trail_geom

-- DROP INDEX IF EXISTS sa.sidx_trail_geom;

CREATE INDEX IF NOT EXISTS sidx_trail_geom
    ON sa.trail USING gist
    (geom)
    TABLESPACE pg_default;