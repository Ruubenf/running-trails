# RunLisboa
**_Helping runners discover scenic, safe, and highly recommended routes in Lisbon_**

## 📌 Overview
This project is aimed at helping runners of all levels in Lisbon find scenic and safe routes based on spatial analytics and user feedback. Geospatial data and runner insights are integrated to give trail recommentdations that promote green and enjoyable running experiences.

#### 🔑 Key Features:
 - Suggests running trails based on green and difficulty factors.  
 - Displays spatial analytics (e.g., elevation, distance, green areas).  
 - Collects runner feedback to refine recommendations.  
 - Supports geospatial queries (e.g., finding nearby trails).  
 - Allows creating new running trails.

## 🚀 Setup & Execution
1. **Database Setup.** In the _'db'_ folder, run the sql files in the following order:
   - `00-create_db.sql`
   - `01-create_schemas.sql`
   - `02-create_tables.sql` (lines 1-53)
   - `03-create_indexes.sql`
   - `04-create_triggers.sql`
   - `data.sql` (lines 1-35)
2. **Environment Initialization.** Install the packages inside _`requirements.txt`_ and, in the same environment, do a pip install of osm2geojson.
3. **ETL Execution.** In the _`etl`_ folder, run _`scrape.py`_ followed by `__init__.py`_.
4. **Open Route Service Key Initialization.** Open _`key.py`_ and update the api key as instructed in the file.
5. **API Activation.** In the _`api`_ folder, run _`api.py`_.
6. **Web Navigation.** In the _`web`_ folder, open _`index.html`_.

## 🗄 Database
PostgreSQL and PostGIS are used for spatial data storage and analysis.

| 📊 Tables | Description |
|-------|-------------|
| sa.trail | Stores trail information (name, description, terrain type, average slope, maximum slope, distance, green areas traversed, geometry). |
| sa.green_area | Stores geometries of green areas. |
| sa.footway | Stores footway data. |
| sa.user | Maintains runner details (for tracking feedback). |
| sa.comment | Collects feedback on trails (ratings, text reviews). |

#### ❓ Example Queries:
 - Find the trails near a user’s location:
```sql
WITH user_point AS (
    SELECT ST_SetSRID(ST_MakePoint(-23794, -176132), 3763) AS geom
)
SELECT 
    t.id_0, 
    t.name, 
    t.location, 
    t.distance_m, 
    ST_Distance(ST_Centroid(t.geom), u.geom) AS distance_to_user
FROM sa.trail t, user_point u
ORDER BY distance_to_user ASC
LIMIT 1;
```
 - Get the most reviewed trails:
```sql
SELECT 
    t.name AS trail_name, 
    c.id_trail, 
    COUNT(*) AS review_count
FROM sa.comment c
JOIN sa.trail t ON c.id_trail = t.id_0
GROUP BY c.id_trail, t.name
ORDER BY review_count DESC;
```

## 🔄 ETL (Extract, Transform, Load) Process

| 📝 Python scripts | Description |
|------|-------------|
| init.py | Initializes the ETL module. |
| db.py | Manages database connections. |
| scrape.py | Scrapes trail data (route IDs) from Plotaroute.com and downloads KML files using Selenium. |
| logs.py | Handles logging of ETL script execution and errors. |
| get_trails.py | ... |
| kml_to_shp.py | Collates KML files into a single shapefile. |
| modify_shp.py | Adopts database field naming to shapefiles and adds attributes. |
| footway_to_db.py | Extracts footway data and processes it for database integration. |
| ga_to_db.py | Extracts data on green areas and processes it for database integration. |
| shp_to_db.py | Loads the final processed shapefile into the PostgreSQL/PostGIS database. |


### 📥 Extract
**Data Sources:**
 - Plotaroute.com – Provides running trail data in KML format with attributes such as distance and slope.
 - OpenStreetMap (OSM) – Supplies the spatial analytics, including traversed green areas and dominant terrain type extracted from polygon geometries.

_Data extraction is uses the sites' APIs._

### ⚙ Transform
**Data Processing**
 - The extracted OSM attributes (terrain type, green areas) are merged with the KML trail data.
 - All data is standardized to EPSG:3763 (Portuguese official projected CRS).
 - A single shapefile consolidates all the processed trails and spatial attributes.

_No filtering and cleaning of trails was applied._

### 🛢 Load
**Database Integration**
 - The processed trail data is loaded into PostgreSQL/PostGIS, in the sa.trail table.
 - The sa.comment table stores runner reviews and ratings.
 - The frontend allows users to create new trails and submit reviews, which automatically updates the database.
 - The frontend also dynamically updates displayed information whenever the database changes.

### 🛠 Implementation

**Backend Tools**
- Python
- PostgreSQL/PostGIS

**Libraries**
- flask, flask-cors
- psycopg2, psycopg2.extras,
- michaelsjp::openrouteservice
 
 _No scheduled ETL updates are planned - updates happen in real-time via the frontend._

## 🌍 API
This project exposes an API for accessing trail data, performing spatial queries, and submitting reviews.

| 📡 Endpoints | Description |
|-----------------|-------------|
| GET /trails | Retrieve all running trails with optional filters (distance, terrain type). |
| GET /trail/<int:id> | Get details of a specific trail by ID.
| GET /trail/<int:id_trail>/comments | ⓘ Get all comments/reviews for a specific trail. |
| GET /best_trails | Retrieve the top 3 highest-rated trails based on user reviews. |
| GET /trails/location?lat=<lat>&lon=<lon>&epsg=<epsg> | Get trails sorted by proximity to a given location (EPSG 4326 or 3763). |
| GET /trails/search?name=<name> | Search for trails by name. |
| GET /trail/create?starting=<lat,lon>&ending=<lat,lon>&green_priority=<0-1> | Generate a new trail between two points with a green area priority setting. |
| POST /submit_review | Submit a review for a specific trail (requires trail ID, runner name, score, and text).|

#### 📚 Libraries and Packages
   - pandas, geopandas, sqlalchemy, geoalchemy2
   - requests, selenium, bs4 (for web scraping)
   - shapely, fiona, osm2geojson, json (for spatial data handling)
   - flask, flask-cors, michaelsjp::openrouteservice, shutil

| 📌 Features | Documentation |
|-------------|---------------|
| ❶ **Interactive home page** with a retractable sidebar and dynamic basemap. |  ![Feature_01](assets/feature_01.gif) |
| ❷ **Search trails by name** to view details and user reviews. | ![Feature_02](assets/feature_02.gif) |
| ❸ **Filter trails** by distance and terrain type for personalized suggestions. | ![Feature_03](assets/feature_03.gif) |
| ❹ **Explore top-rated trails**, displaying the three highest-reviewed routes. | ![Feature_04](assets/feature_04.gif) |
| ❺ **Find the nearest trails**, showing the three closest to the user. | ![Feature_05](assets/feature_05.gif) |
| ❻ **Submit reviews and ratings**, storing user feedback in the database. | ![Feature_06](assets/feature_06.gif) |
| ❼ **Create new trails** dynamically using OpenRouteService. | ... |
| ❽ **Learn More section** providing project insights and background. | ![Feature_08](assets/feature_08.gif) |
| ❾ **Quick access to developers** via LinkedIn, GitHub, and email. | ![Feature_09](assets/feature_09.gif) |
| ❿ **Toggle light/dark mode** for a customizable sidebar experience. | ![Feature_10](assets/feature_10.gif) |

## ✨ Future Work
1. Enhance User Experience & Accessibility
   - Improve UI/UX for mobile users.
   - Implement a voice reader feature.
   - Allow offline access to saved trails.
2. Personalized Trail Recommendations
   - Suggest trails based on users' past reviews, preferences, and running history.
   - Improve trail filtering by terrain type, difficulty, and user ratings.
3. Automated Data Updates & Expansion
   - Automate a scheduled ETL pipeline to update trail data from Plotaroute.com and OpenStreetMap (OSM).
   - Expand the database to include more terrain types for better trail categorization.
4. More Interactive User Engagement
   - Enable photo uploads with reviews.
   - Introduce a social leaderboard to encourage user participation.
   - Allow users to report obstacles or hazards on trails for safety updates.
5. User Authentication & Security
   - Implement a user login and authentication system for personalized experiences.

## 👨‍👩‍👧‍👦 Group members
 - Rubén Femenía Carrascosa
 - Melanie Annabela Menoscal
 - Margaux Elijah Neri