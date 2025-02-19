from logs import init_logger
from kml_to_shp import init_converter
from modify_shp import modify_columns
from shp_to_db import saveshp_to_db, del_folders
from footway_to_db import savefootway_to_db
from ga_to_db import savega_to_db

init_logger()

init_converter()

modify_columns()

saveshp_to_db()

savefootway_to_db()

savega_to_db()

del_folders()