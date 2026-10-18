import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def create_table(conn, create_table_sql):
    cursor = None

    try:
        cursor = conn.cursor()
        cursor.execute(create_table_sql)
        conn.commit()
        print("Table created successfully!")

    except psycopg2.Error as e:
        conn.rollback()
        print(f"Database error: {e}")

    finally:
        if cursor is not None:
            cursor.close()

sql_create_users_table = """
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    fullname VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE
);
"""

sql_create_status_table = """
CREATE TABLE IF NOT EXISTS status (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE
);
"""
sql_create_tasks_table = """
CREATE TABLE IF NOT EXISTS tasks (
    id SERIAL PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    description TEXT,
    status_id INTEGER REFERENCES status(id),
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE
);
"""

conn = None

try:
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )

    create_table(conn, sql_create_users_table)
    create_table(conn, sql_create_status_table)
    create_table(conn, sql_create_tasks_table)

finally:
    if conn is not None:
        conn.close()
