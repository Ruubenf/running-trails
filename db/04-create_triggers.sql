CREATE OR REPLACE FUNCTION tg_add_trail()
RETURNS TRIGGER 
LANGUAGE PLPGSQL
AS $$

DECLARE 
	green_distance DOUBLE PRECISION;
BEGIN
    
	SELECT SUM(ST_LENGTH(ST_INTERSECTION(NEW.geom, bga.geom))) INTO green_distance
	FROM (
		SELECT ST_UNION(ST_BUFFER(ga.geom, 50)) AS geom 
		FROM sa.green_area AS ga 
		WHERE ST_INTERSECTS(NEW.geom, geom)
	) AS bga;
	
	NEW.green_areas_50m := green_distance;

	RETURN NEW;
END;
$$;

CREATE OR REPLACE TRIGGER trigger_add_trail
BEFORE INSERT 
ON sa.trail
FOR EACH ROW
EXECUTE PROCEDURE tg_add_trail();