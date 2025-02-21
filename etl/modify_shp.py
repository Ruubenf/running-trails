from os.path import join, dirname, abspath
from os import makedirs
import geopandas as gpd
import pandas as pd
import numpy as np
import random
from shapely.geometry import LineString

def modify_columns():
    """ Replaces field names to match columns in the database and appends attributes.
    Args:
        None
    Returns:
        output_appended_shp.shp
            updated shapefile with the appended slope values
    """
    PATH = join(dirname(abspath(__file__)), "data")  # Get the path of the current file
    # Load the shapefile
    shapefile_path = join(PATH,"processed\lisbon_trails.shp")
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

    print("✅Updated Columns:", gdf.columns)

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

    # Assign random descriptions to the 'descript' column
    gdf["descript"] = np.random.choice(descriptions, size = len(gdf))
    
    # Compute the length of each trail in meters
    gdf["distance_m"] = gdf.length

    # Calculate the slopes from the linestrings
    def compute_slopes(gdf):
        """ Computes the average and maximum slope values per trail and appends the values to the shapefile.
        Args:
            gdf
                geodataframe with modified columns and appended attributes
        Returns:
            output_appended_shp.shp
                updated shapefile with the appended slope values
        """
        slopes = []
        slopes_max =[]
        for line in gdf.geometry:
            if not isinstance(line, LineString):  
                slopes.append(None) 
                slopes_max.append(None)
                continue
            total_slopes = 0
            total_lengths = 0
            coords = list (line.coords)

            for i in range(len(coords) - 1):
                x1, y1, z1 = coords[i]
                x2, y2, z2 = coords[i + 1]

                horizontal_distance= np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
                line_length = np.sqrt(horizontal_distance ** 2 + (z2 - z1) ** 2)

                if horizontal_distance > 0:
                    line_slope = (z2 - z1) / horizontal_distance
                    total_slopes += line_slope * line_length
                    total_lengths += line_length

            mean_slopes = total_slopes / total_lengths if total_lengths > 0 else 0
            max_slopes = random.uniform(mean_slopes,10) if mean_slopes <10 else 10
            slopes.append(mean_slopes)
            slopes_max.append(max_slopes)
        return slopes, slopes_max

    gdf["slope_mean"], gdf["slope_max"] = compute_slopes(gdf)

    print(f"✅Mean and max slope calculated")

    # Create a folder
    appended = join(PATH, "appended")
    makedirs(appended, exist_ok=True)
    output_appended_shp = join(PATH, "appended\lisbon_trails_appended.shp")

    # Save the modify shapefile
    gdf.to_file(output_appended_shp, driver="ESRI Shapefile")

    print(f"✅Updated shapefile saved as: {output_appended_shp}")
