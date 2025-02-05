from os.path import join, dirname, abspath, splitext, basename
from os import listdir, makedirs
import geopandas as gpd
import pandas as pd
import fiona  # To list layers into the KML file

PATH = join(dirname(abspath(__file__)), "data")  # Get the path of the current file

def convert_kml_to_shp(input_folder, output_folder):
    
    # Create the output file
    makedirs(join(output_folder), exist_ok=True)

    # Get the KML files
    kml_files = [f for f in listdir(input_folder) if f.endswith(".kml")]
    
    # Convert each KML file
    for file in kml_files:
        kml_path = join(input_folder, file)
        print(f"Reading KML file: {kml_path}")
        shp_output = join(output_folder, file.replace(".kml", ".shp"))

        try:
            # List layers into each KML file
            layers = fiona.listlayers(kml_path)
            for layer in layers:
                gdf = gpd.read_file(kml_path, driver='KML', layer=layer)
                
            # Filter only polylines
            gdf = gdf[gdf.geometry.type == "LineString"]

            # Save as shapefiles
            gdf.to_file(shp_output, driver='ESRI Shapefile')
        except Exception as e:
            print(e)




def merge_shapefiles(input_folder, output_folder, output_shp, target_epsg):
    shapefiles = [f for f in listdir(input_folder) if f.endswith(".shp")]
    gdfs = []
    for file in shapefiles:
        shp_path = join(input_folder, file)
        print(f"Reading shapefile: {shp_path}")
        gdf = gpd.read_file(shp_path)

        # Add the name of the file in the attribute 'Name'
        file_name = splitext(basename(file))[0]
        gdf["Name"] = file_name  
        gdfs.append(gdf)

    # Join the shapefiles in one
    merged_gdf = gpd.GeoDataFrame(pd.concat(gdfs, ignore_index=True), crs=gdfs[0].crs)

    #Project the coordinate system to EPSG:3763-ETRS89/Portugal TM06
    merged_gdf= merged_gdf.to_crs(epsg=target_epsg)

    # Create a folder
    makedirs(output_folder, exist_ok=True)
    output_shp_path = join(output_folder, output_shp)

    print(f"Saving the final shapefile at: {output_shp_path}")

    # Save the final shapefile
    merged_gdf.to_file(output_shp_path, driver="ESRI Shapefile")
    print(f"Merged and projected shapefile saved at: {output_shp_path}")


def init_converter():
    original = join(PATH, "original")
    preprocessed = join(PATH, "preprocessed")
    processed = join(PATH, "processed")

    # Execute convertion
    convert_kml_to_shp(original, preprocessed)

    # Ejecutar la función
    merge_shapefiles(preprocessed, processed, "lisbon_trails.shp", 3763)