import mysql.connector
from mysql.connector import Error

# Path to your SQL file
sql_file_path = r"00_CREATE.sql"

conn = None
cursor = None

try:
    # Connect to MySQL
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="finances_db"
    )

    if conn.is_connected():
        print("Connected to MySQL server")

        cursor = conn.cursor()

        # Read SQL script
        with open(sql_file_path, 'r', encoding='utf-8') as f:
            sql_script = f.read()

        # Split statements by ';' and execute
        for statement in sql_script.split(';'):
            stmt = statement.strip()
            if stmt:
                cursor.execute(stmt)

        conn.commit()
        print("Database initialized successfully")

except Error as e:
    print("Error:", e)

finally:
    if cursor:
        cursor.close()
    if conn and conn.is_connected():
        conn.close()
        print("MySQL connection closed")
