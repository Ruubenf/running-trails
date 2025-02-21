import psycopg2
import os

# Database connection details
DB_CONFIG = {
    "dbname": "running-trails",
    "user": "postgres",
    "password": "postgres",
    "host": "localhost",  # Change if your DB is on another server
    "port": "5432",  # Default PostgreSQL port
    "options": "-c client_encoding=UTF8"
}

# Directory containing the SQL files
SQL_DIR = "db/"  # Update with your folder path
SQL_FILES = ["02-create_tables.sql", "03-create_indexes.sql", "04-create_triggers.sql", "data.sql"]

def execute_sql_file(cursor, file_path):
    """Executes an SQL file.
    Args:
        None
    Returns:
        None
    """
    with open(file_path, "r", encoding="utf-8") as file:
        sql_content = file.read()
        cursor.execute(sql_content)

def create_db():
    """Executes the sql files in the SQL_FILES list order
    Args:
        None
    Returns:
        None
    """
    try:
        # Connect to the PostgreSQL database
        conn = psycopg2.connect(**DB_CONFIG)

        cursor = conn.cursor()
        
        # Loop through SQL files and execute them
        for sql_file in SQL_FILES:  # Ensures order if needed
            sql_path = os.path.join(SQL_DIR, sql_file)
            print(f"📄 Executing {sql_file}...")
            execute_sql_file(cursor, sql_path)
        
        # Commit changes and close connection
        conn.commit()
        print("✅ All SQL files executed successfully!")

    except Exception as e:
        conn.rollback()
        print(f"❌ Error: {e}")

    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    create_db()