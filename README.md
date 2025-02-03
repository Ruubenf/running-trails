RunLisboa
Helping runners discover scenic, safe, and highly recommended routes in Lisbon

📌 Overview
This project is aimed at helping runners of all levels in Lisbon find scenic and safe routes based on spatial analytics and user feedback. Geospatial data and runner insights are integrated to give trail recommentdations that promote green and enjoyable running experiences.

    🌿 Key Features:
        ✔ Suggests running trails based on green and difficulty factors.
        ✔ Displays spatial analytics (e.g., elevation, distance, popularity).
        ✔ Collects runner feedback to refine recommendations.
        ✔ Supports geospatial queries (e.g., finding nearby and circular trails).

🗄 Database
The project uses PostgreSQL with PostGIS for spatial data storage and analysis.

    Main Tables:
    > sa.trail – Stores trail information (geometry, name, distance, terrain type).
    > sa.user – Maintains runner details (for tracking feedback).
    > sa.comment – Collects feedback on trails (ratings, text reviews).

    Example Queries:
    ✔ Find all trails near a user’s location:
```sql
        SELECT * FROM sa.trail 
        WHERE ST_DWithin(geom, ST_SetSRID(ST_Point(-9.139, 38.722), 3763), 5000);
```
    ✔ Get the most reviewed trails:
```sql
        SELECT trail_id, COUNT(*) AS review_count 
        FROM sa.comment GROUP BY trail_id ORDER BY review_count DESC;
```

🔄 ETL (Extract, Transform, Load) Process
    📥 Data Sources:
        > Plotaroute.com – Provides trail data.
        > OpenStreetMap (OSM) – Supplies additional geospatial details (roads, parks, landmarks).
    📊 Planned Transformations:
        > Convert raw GPX or JSON data to a format compatible with PostGIS.
        > Extract key attributes (distance, terrain type, start/end points).
        > Validate and filter trails based on quality and safety factors.
        > Load processed data into the PostgreSQL database.
        > ETL Implementation is yet to be finalized.

🌍 API
The project will expose an API for accessing trail data and submitting feedback.

    📡 Endpoints:
        Method  Endpoint	Description
        GET	    /trails	    Retrieve a list of running trails.
        POST	/feedback	Submit user feedback on a trail.
    📌 Features:
        > Supports finding nearby trails.
        > Allows filtering by circular vs. non-circular routes.
        > API framework is yet to be determined.

🚀 Next Steps
    ✔ Finalize the ETL process.
    ✔ Choose the API framework.
    ✔ Develop trail recommendation logic.
    ✔ Implement user feedback analysis.