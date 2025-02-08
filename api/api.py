from flask import Flask, jsonify, request
import psycopg2
from psycopg2.extras import RealDictCursor
from flask_cors import CORS

# Database configuration
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

# Get best 3 trails (based on average score given on the comment table)
@app.route('/best_trails', methods=['GET'])
def get_best_trails():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""select id_trail, t.name, cast(avg(score) as numeric(10,2)) as score from sa.comment
                        join sa.trail t on id_trail = id_0
                        group by id_trail, t.name
                        order by score desc, id_trail asc limit 3""")
    rides = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(rides)

# Get trails by difficulty (actually, all the trails have a max slope of 8)
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


# Get trails by location (location is given by the web browser in the get request by frontend js)
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
    
    # Project if needed
    point = ""
    if epsg == "4326":
        point = f"ST_TRANSFORM(ST_GEOMFROMTEXT('POINT({long} {lat})', 4326), 3763"
    elif epsg == "3763":
        point = f"ST_GEOMFROMTEXT('POINT({long} {lat})', 3763)"

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