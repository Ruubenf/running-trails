from flask import Flask, jsonify, request
from flask_cors import CORS
import psycopg2
from psycopg2.extras import RealDictCursor
import openrouteservice as ors
from key import KEY

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
            t.descript,
            CAST(AVG(score) AS numeric(10,2)) AS score,
            ST_AsGeoJSON(ST_Transform(t.geom, 4326)) AS geometry
        FROM sa.comment
        JOIN sa.trail t ON id_trail = id_0
        GROUP BY id_trail, t.name, geom, t.descript
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
        cursor.execute(f"""
            SELECT count(*)
            FROM sa.trail t
            WHERE t.slope_max BETWEEN 0 and 2;
            """)
    elif difficulty == "medium":
        cursor.execute(f"""
            SELECT count(*)
            FROM sa.trail t
            WHERE t.slope_max BETWEEN 3 and 4;
            """)
    elif difficulty == "hard":
        cursor.execute(f"""
            SELECT count(*)
            FROM sa.trail t
            WHERE t.slope_max BETWEEN 5 and 8;
            """)
    rides = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(rides)


# Get trails by location
@app.route('/trails/location', methods=['GET'])
def get_location_trails():

    long = request.args.get('lon')
    lat = request.args.get('lat')
    epsg = request.args.get('epsg')

    # Validate arguments
    if not long or not lat or not epsg:
        return jsonify({"error": "Missing arguments"})
    if epsg not in ["4326", "3763"]:
        return jsonify({"error": "Invalid EPSG"})
    

    point = ""
    if epsg == "4326":
        point = f"ST_TRANSFORM(ST_GEOMFROMTEXT('POINT({long} {lat})', 4326), 3763)"
    elif epsg == "3763":
        point = f"ST_GEOMFROMTEXT('POINT({long} {lat})', 3763)"

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(f"""
        SELECT id_0, name, 
        CAST(ST_DISTANCE({point}, ST_CENTROID(ST_TRANSFORM(geom, 3763))) AS numeric(10,2)) AS dist,
        ST_AsGeoJSON(ST_Transform(geom, 4326)) AS geometry
        FROM sa.trail
        ORDER BY dist ASC;
    """)
    rides = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(rides)

# Search by name
@app.route('/trails/search', methods=['GET'])
def search_trails():
    name = request.args.get('name')
    if not name:
        return jsonify({"error": "Missing arguments"})
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(f"""
        SELECT id_0, name, descript, 
        ST_AsGeoJSON(ST_Transform(geom, 4326)) AS geometry
        FROM sa.trail
        WHERE name ILIKE '%{name}%';
    """)
    rides = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(rides)

# Create trail with 2 given points
@app.route('/trail/create', methods=['GET'])
def create_trail():
    starting = request.args.get('starting')
    ending = request.args.get('ending')
    green_priority = request.args.get('green_priority')

    if not starting or not ending or not green_priority:
        return jsonify({"error": f"Missing arguments {starting}, {ending}, {green_priority}"})

    #coords = [list(starting), list(ending)]

    starting_pt = [float(c) for c in starting.split(", ")]
    ending_pt = [float(c) for c in ending.split(", ")]

    coords = (starting_pt, ending_pt)

    print(coords)

    client = ors.Client(key=KEY)
    groute_req = {
    "coordinates": [list(reversed(point)) for point in coords],
    "format": "geojson",
    "profile": "foot-walking",
    "options":{"profile_params":{"weightings":{"green":green_priority}}},
    "language": "en",
    }

    directions = client.directions(**groute_req)["features"][0]

    #directions = [list(reversed(coord)) for coord in directions['features'][0]['geometry']['coordinates']]
    #directions = [list(reversed(coord)) for coord in directions['features'][0]['geometry']['coordinates']]
    
    print(directions)
    return jsonify(directions)

if __name__ == '__main__':
    app.run(debug=True)