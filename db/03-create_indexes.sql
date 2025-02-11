DROP INDEX IF EXISTS sa.sidx_trail_geom;
CREATE INDEX IF NOT EXISTS sidx_trail_geom
    ON sa.trail USING gist
    (geom)
    TABLESPACE pg_default;

DROP INDEX IF EXISTS sa.sidx_green_area_geom;
CREATE INDEX IF NOT EXISTS sidx_green_area_geom
    ON sa.green_area USING gist
    (geom)
    TABLESPACE pg_default;

-- Create index for trail name
DROP INDEX IF EXISTS sa.sidx_trail_name;
CREATE INDEX IF NOT EXISTS sidx_trail_name
    ON sa.trail
    USING btree
    (name COLLATE pg_catalog."default" ASC NULLS LAST)
    TABLESPACE pg_default;