from flask import Flask, jsonify
import psycopg2
from psycopg2.extras import RealDictCursor


DB_CONFIG = {
    "database": "running-trails",
    "user": "postgres",
    "password": "postgres",
    "host": "localhost",
    "port": "5432",
    "encoding": "unicode"}


app = Flask(__name__)


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
    cursor.execute("""select id_trail, t.name, cast(avg(score) as numeric(10,2)) as score from sa.comment
                        join sa.trail t on id_trail = id_0
                        group by id_trail, t.name
                        order by score desc, id_trail asc limit 3""")
    rides = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(rides)

# Get difficult trails
@app.route('/trails/difficulty/<string:difficulty>', methods=['GET'])
def get_difficulty_trails(difficulty):
    conn = get_db_connection()
    cursor = conn.cursor()
    if difficulty == "easy":
        cursor.execute(f"""select t.id_0, t.name, t.slope_max, t.slope_mean
                from sa.trail t
                where t.slope_max between 0 and 2
                order by t.slope_max asc, id_0 asc;""")
    elif difficulty == "medium":
        cursor.execute(f"""select t.id_0, t.name, t.slope_max, t.slope_mean
                from sa.trail t
                where t.slope_max between 3 and 4
                order by t.slope_max asc, id_0 asc;""")
    elif difficulty == "hard":
        cursor.execute(f"""select t.id_0, t.name, t.slope_max, t.slope_mean
                from sa.trail t
                where t.slope_max between 5 and 8
                order by t.slope_max desc, id_0 asc;""")
    rides = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(rides)



if __name__ == '__main__':
    app.run(debug=True)