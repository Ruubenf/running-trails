-- Table: sa.trail
DROP TABLE IF EXISTS sa.trail;
CREATE TABLE IF NOT EXISTS sa.trail
(
    id_0 integer NOT NULL DEFAULT nextval('sa.trail_id_0_seq'::regclass),
    geom geometry(MultiLineString,3763),
    id bigint,
    name character varying(20) COLLATE pg_catalog."default",
    descript character varying(50) COLLATE pg_catalog."default",
    location character varying(25) COLLATE pg_catalog."default",
    type_terra character varying(15) COLLATE pg_catalog."default",
    slope_mean bigint,
    slope_max bigint,
    distance_m double precision,
    CONSTRAINT trail_pkey PRIMARY KEY (id_0)
)

-- Table: sa.user
DROP TALBE IF EXISTS sa.user;
create table sa.user(
	username varchar(63) NOT NULL PRIMARY KEY
);


-- Table: sa.comment
DROP TABLE IF EXISTS sa.comment;
CREATE TABLE IF NOT EXISTS sa.comment
(
    id_trail integer NOT NULL,
    score smallint NOT NULL,
    text text COLLATE pg_catalog."default",
    user varchar(63) NOT NULL REFERENCES sa.user(username),
    id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    CONSTRAINT comment_pkey PRIMARY KEY (id),
    CONSTRAINT ck_comment_score CHECK (score >= 1 AND score <= 5)
)