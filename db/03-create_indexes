DROP INDEX IF EXISTS sa.sidx_trail_geom;
CREATE INDEX IF NOT EXISTS sidx_trail_geom
    ON sa.trail USING gist
    (geom)
    TABLESPACE pg_default;