from flask import Flask, jsonify, request
from flask_cors import CORS
import psycopg2
from psycopg2.extras import RealDictCursor
import requests


DB_CONFIG = {
    "database": "running-trails",
    "user": "postgres",
    "password": "postgres",
    "host": "localhost",
    "port": "5432",
    "encoding": "unicode"}


app = Flask(__name__)

# Enable CORS to send API requests
CORS(app, resources={r"/*": {"origins": "*"}})

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


# GET all trail from sa.trail
@app.route('/trails', methods=['GET'])
def get_rides():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM sa.trail""")
    rides = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(rides)

# GET all data for a scepcific trail
@app.route('/trail/<int:id>', methods=['GET'])
def get_trail_data(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(f"""SELECT * FROM sa.trail WHERE id_0 = {id}""")
    rides = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(rides)

# GET comments for a specific trail
@app.route('/trail/<int:id_trail>/comments', methods=['GET'])
def get_comments(id_trail):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(f"""SELECT * FROM sa.comment WHERE id_trail = {id_trail}""")
    comments = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(comments)

# Get best 3 trails
@app.route('/best_trails', methods=['GET'])
def get_best_trails():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            id_trail, 
            name, 
            CAST(AVG(score) AS numeric(10,2)) AS score,
            ST_AsGeoJSON(ST_Transform(t.geom, 4326)) AS geometry
        FROM sa.comment
        JOIN sa.trail t ON id_trail = id_0
        GROUP BY id_trail, t.name, geom
        ORDER BY score DESC, id_trail ASC
        LIMIT 3;
    """)
    rides = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(rides)

# Get trails by difficulty
@app.route('/ntrails/difficulty/<string:difficulty>', methods=['GET'])
def get_difficulty_trails(difficulty):
    conn = get_db_connection()
    cursor = conn.cursor()
    if difficulty == "easy":
        cursor.execute(f"""select count(*)
                from sa.trail t
                where t.slope_max between 0 and 2;""")
    elif difficulty == "medium":
        cursor.execute(f"""select count(*)
                from sa.trail t
                where t.slope_max between 3 and 4""")
    elif difficulty == "hard":
        cursor.execute(f"""select count(*)
                from sa.trail t
                where t.slope_max between 5 and 8;""")
    rides = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(rides)


# Get trails by location
@app.route('/trails/location', methods=['GET'])
def get_location_trails():

    long = request.args.get('long')
    lat = request.args.get('lat')
    epsg = request.args.get('epsg')

    # Validate arguments
    if not long or not lat or not epsg:
        return jsonify({"error": "Missing arguments"})
    if epsg not in ["4326", "3763"]:
        return jsonify({"error": "Invalid EPSG"})
    

    point = ""
    if epsg == "4326":
        point = f"ST_TRANSFORM(ST_GEOMFROMTEXT('POINT({long} {lat})', 4326), 3763"
    elif epsg == "3763":
        point = f"ST_GEOMFROMTEXT('POINT({long} {lat})', 3763)"


    """

    # Get desired location coords with https://nominatim.openstreetmap.org/search?q=valencia&format=json&countrycodes=pt
    loc = requests.get(f"https://nominatim.openstreetmap.org/search?q={location}&format=json&countrycodes=pt")
    print(loc.content)

    loc = loc.content.json()[0]

    lon = loc["lon"] #"-9.1646135"
    lat = loc["lat"] #"38.727895"
    """
    # select st_x(st_transform(ST_GEOMFROMTEXT('POINT(38.72 -9.16)', 4326), 3763))

    """select st_x(st_centroid(st_transform(geom, 3763))), st_y(st_centroid(st_transform(geom, 3763)))
    from sa.trail"""

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(f"""
    select id_0, name, 
    cast(st_distance({point}, st_centroid(st_transform(geom, 3763))) as numeric(10,2)) as dist
    from sa.trail
    order by dist asc
    """)
    rides = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(rides)


if __name__ == '__main__':
    app.run(debug=True)