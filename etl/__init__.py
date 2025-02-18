from logs import init_logger
from kml_to_shp import init_converter
from modify_shp import modify_columns
from shp_to_db import save_to_db, del_folders

init_logger()

init_converter()

modify_columns()

save_to_db()

del_folders()