import requests
import geopandas as gpd
import psycopg2
from psycopg2.extras import RealDictCursor

def savefootway_to_db():
    """ Save footway attributes to the sa.footway table in the database
    Args:
        None
    Returns:
        None
    """
    DB_CONFIG = {
        "database": "running-trails",
        "user": "postgres",
        "password": "postgres",
        "host": "localhost",
        "port": "5432",
        "encoding": "unicode"}

    def get_db_connection():
        """ Function to connect ro database
        Args:
            None
        Returns:
            None
        """
        return psycopg2.connect(
            database=DB_CONFIG["database"],
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"],
            host=DB_CONFIG["host"],
            port=DB_CONFIG["port"],
            cursor_factory=RealDictCursor
        )

    def get_geoms(df):
        """ Extracts and formats geometries from a DataFrame into a list of SQL ST_MAKEPOINT() expressions.
        Args:
            df (pandas.DataFrame): A DataFrame containing a "geometry" column with coordinate dictionaries.
        Returns:
            list: A list of strings, where each string is a concatenated series of ST_MAKEPOINT(lat, lon) expressions.
        """
        result = []
        for i in range(df.size):
            geom = df["geometry"][i]
            result.append(", ".join([f"ST_MAKEPOINT({g["lat"]},{g["lon"]})" for g in geom]))
        
        return result

    # Get footway data from osm overpass api
    url = "https://overpass-api.de/api/interpreter?data=[out:json] [timeout:2500];%0A area(3605400890) -%3E .area_0;%0A(%0A node[%22footway%22](area.area_0);%0A way[%22footway%22](area.area_0);%0A relation[%22footway%22](area.area_0);%0A);%0A(._;%3E;);%0Aout geom;&info=QgisQuickOSMPlugin"

    headers = {"Content-Type":"application/json"}
    response = requests.get(url, headers=headers)

    footways = response.json()["elements"]
    footways = [x for x in footways if x['type'] == 'way']
    gdf = gpd.GeoDataFrame(footways)
    gdf = gdf[["geometry"]]
    gdf.dropna(inplace=True)


    conn = get_db_connection()
    cursor = conn.cursor()

    geoms = get_geoms(gdf)
    for i, geom in enumerate(geoms):

        query = f"""
        INSERT INTO sa.footway
        VALUES (
            {i}, 
            ST_TRANSFORM(
                ST_SetSRID(
                    ST_MAKELINE(
                        ARRAY[{geom}]
                    ), 
                4326), 
            3763)
        );"""
        cursor.execute(query, (i))
        rides = conn.commit()

    cursor.close()
    conn.close()