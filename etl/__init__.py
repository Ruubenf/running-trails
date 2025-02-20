from logs import init_logger
from get_trails import get_trails
from kml_to_shp import init_converter
from modify_shp import modify_columns
from shp_to_db import saveshp_to_db, del_folders
from footway_to_db import savefootway_to_db
from ga_to_db import save_ga_to_db

init_logger()

get_trails()

init_converter()

modify_columns()

savefootway_to_db()

save_ga_to_db()

saveshp_to_db()

del_folders()