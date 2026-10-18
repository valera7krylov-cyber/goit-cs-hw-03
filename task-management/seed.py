import random
import os
from dotenv import load_dotenv
import psycopg2
from faker import Faker

load_dotenv()

conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD")
)

fake = Faker("en_US")

def seed_users(conn, num_users):
    cursor = None

    try:
        cursor = conn.cursor()

        for _ in range(num_users):
            fullname = fake.name()
            email = fake.email()

            cursor.execute(
                """
                INSERT INTO users (fullname, email)
                VALUES (%s, %s)
                """,
                (fullname, email)
            )

        conn.commit()
        print("Users seeded successfully!")

    except psycopg2.Error as e:
        conn.rollback()
        print(f"Database error: {e}")
        raise

    finally:
        if cursor is not None:
            cursor.close()

def seed_statuses(conn):
    cursor = None

    try:
        cursor = conn.cursor()

        cursor.executemany(
            """
            INSERT INTO status (name)
            VALUES (%s)
            ON CONFLICT (name) DO NOTHING
            """,
            [("new",), ("in progress",), ("completed",)]
        )
        conn.commit()
        print("Statuses seeded successfully!")

    except psycopg2.Error as e:
        conn.rollback()
        print(f"Database error: {e}")
        raise
    finally:
        if cursor is not None:
            cursor.close()

def seed_tasks(conn, num_tasks):
    cursor = None

    try:
        cursor = conn.cursor()

        cursor.execute("SELECT id FROM users")
        user_ids = [row[0] for row in cursor.fetchall()]

        cursor.execute("SELECT id FROM status")
        status_ids = [row[0] for row in cursor.fetchall()]

        if not user_ids or not status_ids:
            raise ValueError("Users and statuses must exist before seeding tasks.")

        for _ in range(num_tasks):

            user_id = random.choice(user_ids)
            status_id = random.choice(status_ids)

            title = fake.sentence(nb_words=4)
            description = fake.text()

            cursor.execute(
                """
                INSERT INTO tasks (title, description, status_id, user_id)
                VALUES (%s, %s, %s, %s)
                """,
                (title, description, status_id, user_id)
            )

        conn.commit()
        print(f"{num_tasks} tasks seeded successfully!")

    except psycopg2.Error as e:
        conn.rollback()
        print(f"Database error: {e}")
        raise

    finally:
        if cursor is not None:
            cursor.close()

try:
    seed_users(conn, 20)
    seed_statuses(conn)
    seed_tasks(conn, 30)
finally:
    conn.close()