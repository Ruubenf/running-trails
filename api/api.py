from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api, reqparse, fields, marshal_with, abort
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

"""
COMMENTS SAVED FOR FUTURE WORK

app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"
db = SQLAlchemy(app)
api = Api(app)
class TrailModel(db.Model):
    __tablename__ = 'trail'
    __table_args__ = {"schema": "sa"}
    id_0 = db.Column(db.Integer, primary_key=True, auto_increment=True)
    geom = db.Column(db.String)
    name = db.Column(db.String(255))
    descript = db.Column(db.String(255))
    location = db.Column(db.String(255))
    type_terra = db.Column(db.String(255))
    slope_mean = db.Column(db.BigInteger)
    slope_max = db.Column(db.BigInteger)
    distance_m = db.Column(db.Double)

    def __repr__(self):
        return f'<Trail {self.name}, id: {self.id_0}>'




trail_args = reqparse.RequestParser()
trail_args.add_argument('name', type=str, help='Name of the trail')
trail_args.add_argument('geom', type=str, help='Geometry of the trail')
trail_args.add_argument('descript', type=str, help='Description of the trail')
trail_args.add_argument('location', type=str, help='Location of the trail')
trail_args.add_argument('type_terra', type=str, help='Type of terrain')
trail_args.add_argument('slope_mean', type=int, help='Mean slope of the trail')
trail_args.add_argument('slope_max', type=int, help='Max slope of the trail')
trail_args.add_argument('distance_m', type=float, help='Distance of the trail')

trailFields = {
    'id_0': fields.Integer,
    'geom': fields.String,
    'name': fields.String,
    'descript': fields.String,
    'location': fields.String,
    'type_terra': fields.String,
    'slope_mean': fields.Integer,
    'slope_max': fields.Integer,
    'distance_m': fields.Float
}

class Trail(Resource):
    def get(self):
        trails = TrailModel.query.all()
        return trails

@app.route('/')
def home():
    return 'Hello, World!'

"""


# GET all rides from pa.rides_geojson
@app.route('/trails', methods=['GET'])
def get_rides():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM sa.trail""")
    rides = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(rides)



if __name__ == '__main__':
    app.run(debug=True)