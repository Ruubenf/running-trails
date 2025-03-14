-- Table: sa.trail
DROP TABLE IF EXISTS sa.trail;
CREATE TABLE IF NOT EXISTS sa.trail
(
    id_0 SERIAL PRIMARY KEY,
    name character varying(255),
    descript character varying(255),
    location character varying(255),
    type_terra character varying(255),
    slope_mean double precision,
    slope_max double precision,
    distance_m double precision,
    green_areas_50m double precision,
    geom geometry(LineStringZ,3763)
);

-- Table: sa.user
DROP TABLE IF EXISTS sa.runner;
create table sa.runner(
	username varchar(255) NOT NULL PRIMARY KEY
);


-- Table: sa.comment
DROP TABLE IF EXISTS sa.comment;
CREATE TABLE IF NOT EXISTS sa.comment
(
    id_trail integer NOT NULL,
    score smallint NOT NULL,
    text text COLLATE pg_catalog."default",
    runner varchar(255) NOT NULL REFERENCES sa.runner(username),
    id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    CONSTRAINT comment_pkey PRIMARY KEY (id),
    CONSTRAINT ck_comment_score CHECK (score >= 1 AND score <= 5)
);

-- Table: sa.green_area
DROP TABLE IF EXISTS sa.green_area;
CREATE TABLE IF NOT EXISTS sa.green_area
(
	id INTEGER PRIMARY KEY,
	geom GEOMETRY(MULTIPOLYGON, 3763)
);

-- Table: sa.footway
DROP TABLE IF EXISTS sa.footway;
CREATE TABLE IF NOT EXISTS sa.footway
(
    fid SERIAL NOT NULL,
    geom geometry(LineString,3763),
    CONSTRAINT footway_lines_pkey PRIMARY KEY (fid)
);