from flask import Flask, jsonify
from flask_cors import CORS
import psycopg2
from psycopg2.extras import RealDictCursor
from api import get_db_connection

app = Flask(__name__)

# Enable CORS to send API requests
CORS(app, resources={r"/*": {"origins": "*"}})

# Get top 3 best trails (!! distances are used as placeholders for now)
@app.route('/top_trails', methods=['GET'])
def get_top_trails():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            name,
            distance_m,
            ST_AsGeoJSON(ST_Transform(geom,4326)) AS geometry
        FROM sa.trail 
        ORDER BY distance_m 
        LIMIT 3;
    """)
    top_trails = cursor.fetchall()
    print("DB Query Result:", top_trails)  # Print results in the terminal
    cursor.close()
    conn.close()
    
    return jsonify(top_trails)  # Returns a list of top 3 trails

if __name__ == '__main__':
    app.run(debug=True)