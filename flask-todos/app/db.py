import os
import psycopg2

def get_db(config):
    dsn = config.get("DATABASE_URL") or os.environ.get("DATABASE_URL")
    return psycopg2.connect(dsn)

def init_db(conn):
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS todos(
            id SERIAL PRIMARY KEY,
            title TEXT NOT NULL
        );
    """)
    conn.commit()
