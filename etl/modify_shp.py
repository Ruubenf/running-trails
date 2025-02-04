import geopandas as gpd
import pandas as pd
import numpy as np
from sqlalchemy import create_engine

# Load the shapefile
shapefile_path = "etl\data\processed\lisbon_trails.shp"
gdf = gpd.read_file(shapefile_path)

# List of columns to drop if they exist
columns_to_drop = ["id", "descriptio", "timestamp", "begin", "end", 
                   "altitudeMo", "tessellate", "extrude", "visibility", 
                   "drawOrder", "icon"]

# Drop only the columns that exist in the GeoDataFrame
gdf = gdf.drop(columns=columns_to_drop, errors="ignore")

# Rename column 'Name' to match 'name' in the database
gdf = gdf.rename(columns={"Name":"name"})

# Define the required columns and their default values
missing_columns = {
    "descript": "No description",  # Default text
    "location": "Lisbon",
    "type_terra": "Unknown",
    "slope_mean": np.nan,  # Default numeric value
    "slope_max": np.nan,
    "distance_m": np.nan
}

# Add missing columns
for col, default in missing_columns.items():
    if col not in gdf.columns:
        gdf[col] = default

print("Updated Columns:", gdf.columns)

# Define custom textvalues for the 'descript' and 'type_terra columns
descriptions = [
    "Park loop with greenery",
    "Popular running route",
    "Beginner-friendly trail that runs along a lake",
    "Challenging hilly trail for experienced runners",
    "Flat running trail perfect to practice for marathons",
    "Shaded path with trees",
    "Coastal trail with ocean breeze"
]

terrain = [
    "asphalt",
    "dirtroad",
    "grass",
    "cobblestone",
    "boardwalk",
    "concrete",
    "rubberized tracks"
]

# Assign random descriptions to the 'descript' and 'type_terra" columns
gdf["descript"] = np.random.choice(descriptions, size = len(gdf))
gdf["type_terra"] = np.random.choice(terrain, size = len(gdf))

# Ensure correct Coordinate Reference System (CRS) - Convert to EPSG:3763 if needed
target_crs = 3763
if gdf.crs is None or gdf.crs.to_epsg() != target_crs:
    print(f"Converting CRS to EPSG:{target_crs}...")
    gdf = gdf.to_crs(epsg=target_crs)

# Compute the length of each trail in meters
gdf["distance_m"] = gdf.length

# Assign random values to columns
gdf["descript"] = np.random.choice(descriptions, size = len(gdf))
gdf["type_terra"] = np.random.choice(terrain, size = len(gdf))
gdf["slope_mean"] = 4.56
gdf["slope_max"] = 8.00

print("Final Data Preview:\n", gdf[["name", "descript", "type_terra", "distance_m"]].head())

# Save the cleaned shapefile
output_shapefile = "etl/data/processed/lisbon_trails_appended1.shp"
gdf.to_file(output_shapefile)
print(f"Appended shapefile saved to: {output_shapefile}")

# Upload to PostgreSQL (PostGIS)
# db_connection = "postgresql://postgres:postgres@localhost:5432/running-trails"
# engine = create_engine(db_connection)

# gdf.to_postgis(name="trail", con=engine, schema="sa", if_exists="append", index=False)
# print("Data successfully uploaded to PostgreSQL!")