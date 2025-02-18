import geopandas
from sqlalchemy import create_engine, Column, Integer, String, Double, BigInteger
from sqlalchemy.orm import sessionmaker, declarative_base
from geoalchemy2 import Geometry
import os
import shutil

def save_to_db():
    """ Save shapefile contents into the sa.trail table in the database
    Args:
        None
    Returns:
        None
    """
    USERNAME = 'postgres'
    PASSWORD = 'postgres'
    HOST = 'localhost'
    PORT = '5432'
    DATABASE = 'running-trails'

    # Create db connection
    engine = create_engine(f"postgresql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}", echo=True)

    # Create session
    Session = sessionmaker(bind=engine)
    session = Session()

    # Create representation of the Trail table
    Base = declarative_base()
    class Trail(Base):
        __tablename__ = 'trail'
        __table_args__ = {"schema": "sa"}
        id_0 = Column(Integer, primary_key=True, auto_increment=True)
        geom = Column(Geometry(geometry_type='LineStringZ', srid='3763'))
        name = Column(String(255))
        descript = Column(String(255))
        location = Column(String(255))
        type_terra = Column(String(255))
        slope_mean = Column(Double)
        slope_max = Column(Double)
        distance_m = Column(Double)
        

    # Read the shapefile with the Trails data
    filename = os.path.join("etl","data","appended","lisbon_trails_appended.shp")
    df = geopandas.read_file(filename)

    # Iterate over the dataframe to add objects to the db
    for row in df.itertuples():
        trail = Trail(
            geom=row.geometry.wkt,
            name=row.name.split(".shp")[0], # Remove .shp from the name
            descript=row.descript,
            location = row.location,
            type_terra=row.type_terra,
            slope_mean=row.slope_mean,
            slope_max=row.slope_max,
            distance_m=row.distance_m
        )
        session.add(trail)

    # Send all the inserted values to the db
    session.commit()

def del_folders():
    """ Deletes 'preprocessed', 'processed', and 'appended' folders if they exist to clear out unnecessary files.
    Args:
        None
    Returns:
        None
    """
    from os.path import join, dirname, abspath

    PATH = join(dirname(abspath(__file__)), "data")  # Get the base data directory
    folders_to_delete = ["preprocessed", "processed", "appended"]  # List of folders to remove

    for folder in folders_to_delete:
        folder_path = join(PATH, folder)
        if os.path.exists(folder_path):
            shutil.rmtree(folder_path)
            print(f"✅ Deleted folder: {folder_path}")
        else:
            print(f"⚠️ Folder not found: {folder_path}")