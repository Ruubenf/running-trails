-- Calculate green area distance on the newly added trail
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

-- Calculate the type of terrain in the newly added trail
CREATE OR REPLACE FUNCTION tg_add_pav()
RETURNS TRIGGER 
LANGUAGE PLPGSQL
AS $$

DECLARE 
	pav_ratio VARCHAR(155);
BEGIN
    
	SELECT 
		CASE
			WHEN SUM(ST_LENGTH(ST_INTERSECTION(NEW.geom, bga.geom))) / NEW.distance_m < 0.3 THEN 'Dirt/Gravel/Unknown'
			ELSE 'Pavimented'
		END INTO pav_ratio
	FROM (
		SELECT ST_UNION(ST_BUFFER(ST_TRANSFORM(pav.geom, 3763), 20)) AS geom 
		FROM sa.footway AS pav 
		WHERE ST_INTERSECTS(NEW.geom, ST_BUFFER(ST_TRANSFORM(pav.geom, 3763), 20))
	) AS bga;
	
	NEW.type_terra := pav_ratio;

	RETURN NEW;
END;
$$;

CREATE OR REPLACE TRIGGER trigger_add_pav
BEFORE INSERT 
ON sa.trail
FOR EACH ROW
EXECUTE PROCEDURE tg_add_pav();