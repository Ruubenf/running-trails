from flask import Flask, jsonify
from flask_cors import CORS
import psycopg2
from psycopg2.extras import RealDictCursor
from api import get_db_connection

app = Flask(__name__)

# Explicitly Allow CORS for All Domains
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/max_distance', methods=['GET'])
def get_max_distance():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(distance_m) AS max_distance FROM sa.trail;")
    max_distance = cursor.fetchone()

    print("Database Query Result:", max_distance)  # Debugging output

    cursor.close()
    conn.close()
    return jsonify(max_distance)

if __name__ == '__main__':
    app.run(debug=True)