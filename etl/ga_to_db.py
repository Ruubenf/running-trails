import requests
import psycopg2
from psycopg2.extras import RealDictCursor
import osm2geojson
import json
import os

def save_ga_to_db():
    DB_CONFIG = {
        "database": "running-trails",
        "user": "postgres",
        "password": "postgres",
        "host": "localhost",
        "port": "5432",
        "encoding": "unicode"}

    # Database connection function
    def get_db_connection():
        return psycopg2.connect(
            database=DB_CONFIG["database"],
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"],
            host=DB_CONFIG["host"],
            port=DB_CONFIG["port"],
            cursor_factory=RealDictCursor
        )

    def get_osm_ga_query():
        """
        Returns osm_query in the style of:
            way["landuse"="grass"];
            way["landuse"="paddy"];

            way["leisure"="park"](area.searchArea);
            way["leisure"="natural_reserve"](area.searchArea);

            way["natural"](area.searchArea);

            for each node, way and relation
        """

        osm_ga_elems = {
            "landuse":["grass", "paddy", "flowerbed", "allotments", "vineyard", "cemetery", "famland", "forest", "logging", "meadow", "orchad", "plant_nursery", "basin", "salt_pond"],
            "leisure":["park", "natural_reserve"],
            "natural": None,
            "water": None
        }

        objs = ("node", "way", "relation")

        osm_ga_query = ""
        for key, value in osm_ga_elems.items():
            if value is None:
                for obj in objs:
                    osm_ga_query += f'{obj}["{key}"](area.searchArea);\n'
            else:
                for elem in value:
                    for obj in objs:
                        osm_ga_query += f'{obj}["{key}" = "{elem}"](area.searchArea);\n'

        return osm_ga_query

    # Do the query and also remove the whole iberian peninsula (id:3870917)
    overpass_query = f"""
    [out:xml][timeout:2500];
    area(id:3605400890)->.searchArea;
    (
    {get_osm_ga_query()}
    ) ->.green_areas;

    /* Exclude the whole iberian peninsula with ID 3870917 */
    (
    node(id:3870917);
    way(id:3870917);
    relation(id:3870917);
    ) ->.excluded;

    (.green_areas; - .excluded;);

    out geom;
    >;
    out skel qt;
    """

    # 🔹 2. Hacer la petición a Overpass API
    url = "http://overpass-api.de/api/interpreter"
    response = requests.get(url, params={"data": overpass_query})

    if response.status_code != 200:
        print("Error on request: " + str(response.status_code))
        exit()

    xml = response.text
    geojson = osm2geojson.xml2geojson(xml, filter_used_refs=False)

    """ Uncomment it if you want to save the ga geojson file
    ga_osm_path = os.path.join("etl", "data", "green_areas.geojson")
    with open(ga_osm_path, "w", encoding="utf-8") as f:
        json.dump(geojson, f, indent=4, ensure_ascii=False)


    ga_osm_path = os.path.join("data", "green_areas.geojson")
    with open(ga_osm_path, "r") as f:
        geojson = json.load(f)
    """

    conn = get_db_connection()
    cursor = conn.cursor()


    for id, feature in enumerate(geojson["features"]):
        if feature["geometry"]["type"] == "MultiPolygon" or feature["geometry"]["type"] == "Polygon":
            geometry = json.dumps(feature["geometry"])
            query = f"""INSERT INTO sa.green_area VALUES ({id}, ST_MULTI(ST_TRANSFORM(ST_SetSRID(ST_GeomFromGeoJSON('{geometry}'), 4326), 3763)));"""
            cursor.execute(query)
            rides = conn.commit()

    cursor.close()
    conn.close()