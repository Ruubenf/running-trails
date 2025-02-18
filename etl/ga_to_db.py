import requests
import geopandas as gpd
import psycopg2
from psycopg2.extras import RealDictCursor
import osm2geojson
import json
import os
from osgeo import ogr

DB_CONFIG = {
    "database": "running-trails",
    "user": "postgres",
    "password": "postgres",
    "host": "localhost",
    "port": "5432",
    "encoding": "unicode"}

# Database connection function
def get_db_connection():
    db_name =  "running-trails"
    db_user = "postgres"
    db_password = "postgres"
    db_host = "localhost"
    db_port =  "5432"

    return f"PG:dbname={db_name} user={db_user} password={db_password} host={db_host} port={db_port}"


def get_osm_ga_query():
    """
    Returns osm_query in the style of:
        way["landuse"="grass"](area.searchArea)(if:count_distinct_members() + 1 == count_members());
        way["landuse"="paddy"](area.searchArea)(if:count_distinct_members() + 1 == count_members());

        way["leisure"="park"](area.searchArea)(if:count_distinct_members() + 1 == count_members());
        way["leisure"="natural_reserve"](area.searchArea)(if:count_distinct_members() + 1 == count_members());

        way["natural"](area.searchArea)(if:count_distinct_members() + 1 == count_members());

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

ga_osm_path = os.path.join("etl", "data", "green_areas.osm")
with open(ga_osm_path, "w", encoding="utf-8") as f:
    json.dump(geojson, f, indent=4, ensure_ascii=False)

os.system("osm2pgsql-bin/osm2pgsql.exe -a -d running-trails -U postgres -H localhost --password=postgres --schema sa --proj 3763 --prefix ga etl/data/green_areas.osm")

ga_src = ogr.Open(ga_osm_path)

# Get first layer
source_layer = ga_src.GetLayer()

# Create db connection 
ga_target = ogr.Open(get_db_connection(), 1) # 1 is write mode

ogr.Layer.CopyLayer(source_layer, ga_target, "sa.ga")

